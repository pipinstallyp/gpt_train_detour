"""Verify finished W&B histories and uploaded checkpoint/data manifests."""
import base64
import hashlib
import json
import os
from pathlib import Path

from publish_wandb import ROOT, load_env


def md5(path):
    with path.open('rb') as stream:
        return base64.b64encode(hashlib.file_digest(stream, 'md5').digest()).decode()


def main():
    load_env(ROOT.parent / '.credentials/.env')
    os.environ.setdefault('WANDB_BASE_URL', 'https://api.wandb.ai')
    import wandb

    api = wandb.Api(timeout=30)
    publication = json.loads((ROOT / 'results/wandb-publication.json').read_text())
    project = publication['entity'] + '/' + publication['project']
    verified = []
    for record in publication['runs']:
        run = api.run(project + '/' + record['id'])
        assert run.state == 'finished', f'{run.name} is {run.state}'
        if record['name'] != 'datasets':
            original = json.loads((ROOT / 'results' / record['name'] / 'loss.json').read_text())
            imported = list(run.scan_history(keys=['train/updates', 'loss/train', 'loss/validation']))
            assert len(imported) == len(original), f'History length mismatch: {run.name}'
            for expected, actual in zip(original, imported):
                assert actual['train/updates'] == expected['step']
                assert abs(actual['loss/train'] - expected['train']) < 1e-7
                assert abs(actual['loss/validation'] - expected['val']) < 1e-7
            model = next(a for a in run.logged_artifacts() if a.type == 'model')
            checkpoint = ROOT / 'checkpoints' / record['name'] / 'checkpoint.pt'
            assert model.manifest.entries['checkpoint.pt'].digest == md5(checkpoint)
            assert any(a.type == 'dataset' for a in run.used_artifacts()), 'Missing dataset lineage'
            verified.append({'run': record['name'], 'history_rows': len(imported), 'checkpoint_manifest_matches': True, 'dataset_lineage_present': True})
    for dataset, name in [('shakespeare', 'shakespeare-char'), ('tinystories', 'tinystories-20k-char')]:
        artifact = api.artifact(project + '/' + name + ':release-' + publication['release'])
        files = [p for p in (ROOT / 'data' / dataset).rglob('*') if p.is_file()]
        assert len(artifact.manifest.entries) == len(files)
        for path in files:
            relative = path.relative_to(ROOT / 'data' / dataset).as_posix()
            assert artifact.manifest.entries[relative].digest == md5(path), relative
        verified.append({'dataset': dataset, 'uploaded_file_manifests_match': len(files)})
    result = {'project': project, 'checks': verified}
    (ROOT / 'results/wandb-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
