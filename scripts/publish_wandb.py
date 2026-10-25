"""Publish saved Runpod baselines; this script does not train a model."""
import argparse
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_env(path):
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        key, sep, value = line.strip().partition('=')
        if sep and key in {'WANDB_API_KEY', 'WANDB_BASE_URL', 'WANDB_ENTITY', 'WANDB_PROJECT'}:
            os.environ.setdefault(key, value.strip().strip('\"\x27'))


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entity', default='peepaclan')
    parser.add_argument('--project', default='gpt_train_detour')
    parser.add_argument('--release', default='v1')
    parser.add_argument('--env-file', type=Path, default=ROOT.parent / '.credentials/.env')
    args = parser.parse_args()
    load_env(args.env_file)
    os.environ.setdefault('WANDB_BASE_URL', 'https://api.wandb.ai')
    if not os.environ.get('WANDB_API_KEY'):
        parser.error('Set WANDB_API_KEY or provide a local --env-file.')
    import wandb

    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    configs = read_json('configs/baselines.json')
    release_alias = 'release-' + args.release
    api = wandb.Api(timeout=30)
    settings = wandb.Settings(x_disable_stats=True, x_disable_machine_info=True, disable_git=True, console='off')
    publication = {'entity': args.entity, 'project': args.project, 'release': args.release, 'code_commit': commit, 'runs': []}

    def run_id(name):
        return hashlib.sha256(f'{args.project}/{args.release}/{name}'.encode()).hexdigest()[:12]

    def completed(name):
        try:
            previous = api.run(f'{args.entity}/{args.project}/{run_id(name)}')
        except wandb.errors.CommError as exc:
            # Only a missing project/run is safe to treat as a fresh publication.
            if 'not find' not in str(exc).lower() and 'not found' not in str(exc).lower():
                raise
            return False
        if previous.state == 'finished':
            # W&B reserves v0/v1/... for native artifact versions, so release
            # labels must have their own prefix. Repair old publication aliases.
            for artifact in previous.logged_artifacts():
                if release_alias not in artifact.aliases:
                    artifact.aliases.append(release_alias)
                    artifact.save()
            publication['runs'].append({'name': name, 'id': previous.id, 'url': previous.url})
            return True
        if not previous.summary.get('source_history_rows') and not list(previous.logged_artifacts()) and not any(key.startswith('loss/') for key in previous.summary.keys()):
            return False  # Empty failed setup can be resumed without duplicating history.
        raise RuntimeError(f'Prior publication {previous.url} is {previous.state}; inspect it before retrying.')

    def initialize(name, job_type, config):
        return wandb.init(entity=args.entity, project=args.project, id=run_id(name), resume='allow', name=f'{args.release}-{name}',
                          job_type=job_type, group=args.release, tags=[args.release, 'historical-import', 'runpod'],
                          config={**config, 'release': args.release, 'source_code_commit': commit,
                                  'code_url': f'https://github.com/pipinstallyp/gpt_train_detour/tree/{commit}',
                                  'historical_import': True, 'training_date': '2026-10-25',
                                  'system_metrics_available': False}, settings=settings, save_code=False,
                          notes='Imported from saved Runpod files. The import machine and upload time do not describe the training hardware or training runtime.')

    if not completed('datasets'):
        with initialize('datasets', 'dataset-publication', {'source': 'Runpod /workspace snapshot'}) as run:
            for dataset, artifact_name in [('shakespeare', 'shakespeare-char'), ('tinystories', 'tinystories-20k-char')]:
                artifact = wandb.Artifact(artifact_name, type='dataset', metadata=read_json(f'data/{dataset}/manifest.json'))
                artifact.add_dir(str(ROOT / 'data' / dataset))
                run.log_artifact(artifact, aliases=[release_alias]).wait()
            analysis = wandb.Artifact('tinystories-data-analysis', type='analysis', metadata={'exploratory': True})
            analysis.add_dir(str(ROOT / 'results/tinystories-data-analysis'))
            run.log_artifact(analysis, aliases=[release_alias]).wait()
            publication['runs'].append({'name': 'datasets', 'id': run.id, 'url': run.url})
    for name, config in configs.items():
        if completed(name):
            continue
        history = read_json(f'results/{name}/loss.json')
        checkpoint = ROOT / f'checkpoints/{name}/checkpoint.pt'
        if not checkpoint.exists():
            raise FileNotFoundError(f'{checkpoint}: download the v1 GitHub release assets first.')
        with initialize(name, 'historical-training', config) as run:
            dataset_name = 'shakespeare-char' if config['dataset'] == 'shakespeare' else 'tinystories-20k-char'
            run.use_artifact(f'{args.entity}/{args.project}/{dataset_name}:{release_alias}', type='dataset')
            run.define_metric('train/updates')
            run.define_metric('loss/*', step_metric='train/updates')
            run.define_metric('validation/character_perplexity', step_metric='train/updates')
            for row in history:
                values = {'train/updates': row['step'], 'loss/train': row['train'], 'loss/validation': row['val'],
                          'loss/generalization_gap': row['val'] - row['train'],
                          'validation/character_perplexity': math.exp(row['val'])}
                if 'seconds' in row:
                    values['time/elapsed_seconds'] = row['seconds']
                run.log(values)
            best = min(history, key=lambda row: row['val'])
            last = history[-1]
            run.summary.update({'best_validation_loss': best['val'], 'best_validation_logged_step': best['step'],
                                'final_logged_validation_loss': last['val'], 'final_logged_train_loss': last['train'],
                                'final_logged_generalization_gap': last['val'] - last['train'],
                                'final_logged_character_perplexity': math.exp(last['val']),
                                'checkpoint_sha256': digest(checkpoint), 'checkpoint_selection': 'final',
                                'best_checkpoint_available': False, 'source_history_rows': len(history)})
            summary_path = ROOT / f'results/{name}/summary.json'
            if config['dataset'] == 'tinystories' and summary_path.exists():
                summary = json.loads(summary_path.read_text())
                run.summary.update({'training_seconds_including_eval_and_saves': summary['seconds'],
                                    'training_targets_seen': summary['targets_seen'],
                                    'effective_targets_per_second': summary['targets_seen'] / summary['seconds'],
                                    'completed_epochs': summary['epoch']})
            model = wandb.Artifact(name + '-checkpoint', type='model', metadata={'selection': 'final', 'sha256': digest(checkpoint), **config})
            model.add_file(str(checkpoint), name='checkpoint.pt')
            run.log_artifact(model, aliases=[release_alias, 'final']).wait()
            result = wandb.Artifact(name + '-results', type='evaluation')
            result.add_dir(str(ROOT / 'results' / name))
            run.log_artifact(result, aliases=[release_alias]).wait()
            sample = ROOT / f'results/{name}/sample.txt'
            if sample.exists():
                table = wandb.Table(columns=['prompt', 'completion', 'source'])
                table.add_data(config['sample_prompt'], sample.read_text(encoding='utf-8'), 'Original saved sample; sampling seed not separately recorded')
                run.log({'generation/saved_sample': table})
            publication['runs'].append({'name': name, 'id': run.id, 'url': run.url})
    target = ROOT / 'results/wandb-publication.json'
    target.write_text(json.dumps(publication, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(publication, indent=2))


if __name__ == '__main__':
    main()
