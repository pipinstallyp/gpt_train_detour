"""Organize a local /workspace copy. Does not connect to or modify the pod."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '.runpod-import'


def copy(source, destination):
    destination = ROOT / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE / source, destination)


def write_json(path, value):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def main():
    for relative in ['data/shakespeare', 'data/tinystories', 'notebooks', 'results', 'checkpoints', 'archive/runpod', 'configs']:
        (ROOT / relative).mkdir(parents=True, exist_ok=True)
    copy('shakespeare-gpt/input.txt', 'data/shakespeare/input.txt')
    for name in ['input.txt', 'train.txt', 'val.txt']:
        copy(f'tinystories-gpt/{name}', f'data/tinystories/{name}')
    for name in ['train.jsonl', 'val.jsonl', 'manifest.json']:
        copy(f'tinystories-gpt/data_filtering/{name}', f'data/tinystories/{name}')
    for original, name in [('shakespeare-gpt/out', 'shakespeare-baseline'), ('tinystories-gpt/out_one_epoch', 'tinystories-one-epoch')]:
        for p in (SOURCE / original).iterdir():
            target = f'checkpoints/{name}/{p.name}' if p.suffix == '.pt' else f'results/{name}/{p.name}'
            copy(str(p.relative_to(SOURCE)), target)
    shutil.copytree(SOURCE / 'tinystories-gpt/data_analysis', ROOT / 'results/tinystories-data-analysis', dirs_exist_ok=True)
    # Preserve the original builders exactly as provenance; current notebooks live in notebooks/.
    for src in ['setup_epoch.py', 'setup_tiny.py', 'shakespeare-gpt/make_notebook.py', 'shakespeare-gpt/README.md', 'tinystories-gpt/data_filtering/README.md']:
        copy(src, 'archive/runpod/' + src)
    for src, dest in [('shakespeare-gpt/gpt.py', 'scripts/shakespeare_gpt.py'), ('shakespeare-gpt/bigram.py', 'scripts/shakespeare_bigram.py')]:
        text = (SOURCE / src).read_text(encoding='utf-8')
        text = 'from pathlib import Path\nROOT = Path(__file__).resolve().parents[1]\n' + text
        text = text.replace("open('input.txt',", "open(ROOT / 'data/shakespeare/input.txt',")
        (ROOT / dest).write_text(text, encoding='utf-8')
    prep = (SOURCE / 'tinystories-gpt/data_filtering/prepare.py').read_text(encoding='utf-8')
    prep = prep.replace("ROOT=Path(__file__).resolve().parents[1]", "ROOT=Path(__file__).resolve().parents[1]/'data/tinystories'\nROOT.mkdir(parents=True, exist_ok=True)")
    prep = prep.replace("OUT=ROOT/'data_filtering'", 'OUT=ROOT')
    # Explicit encoding/newlines reproduce the Linux corpus bytes on Windows.
    prep = prep.replace(".write_text(''.join(json.dumps({'text':t})+'\\n' for t in items))", ".write_text(''.join(json.dumps({'text':t})+'\\n' for t in items), encoding='utf-8', newline='\\n')")
    prep = prep.replace(".write_text('\\n\\n'.join(items)+'\\n')", ".write_text('\\n\\n'.join(items)+'\\n', encoding='utf-8', newline='\\n')")
    prep = prep.replace(".write_text('\\n\\n'.join(stories)+'\\n')", ".write_text('\\n\\n'.join(stories)+'\\n', encoding='utf-8', newline='\\n')")
    (ROOT / 'scripts/prepare_tinystories.py').write_text(prep, encoding='utf-8')
    analysis = (SOURCE / 'tinystories-gpt/data_analysis/analyze.py').read_text(encoding='utf-8')
    analysis = analysis.replace("root=Path('/workspace/tinystories-gpt')", 'root=Path(__file__).resolve().parents[1]')
    analysis = analysis.replace("out=root/'data_analysis'; out.mkdir(exist_ok=True)", "out=root/'results/tinystories-data-analysis'; out.mkdir(parents=True,exist_ok=True)")
    analysis = analysis.replace('data_filtering/', 'data/tinystories/')
    (ROOT / 'scripts/analyze_tinystories.py').write_text(analysis, encoding='utf-8')
    notebook_specs = [
        ('shakespeare-gpt/Shakespeare_GPT.ipynb', 'Shakespeare_GPT.ipynb', 'shakespeare', 'shakespeare-baseline'),
        ('tinystories-gpt/TinyStories_GPT.ipynb', 'TinyStories_GPT.ipynb', 'tinystories', 'tinystories-5000-step'),
        ('tinystories-gpt/TinyStories_OneEpoch.ipynb', 'TinyStories_OneEpoch.ipynb', 'tinystories', 'tinystories-one-epoch'),
    ]
    for src, filename, dataset, experiment in notebook_specs:
        nb = json.loads((SOURCE / src).read_text(encoding='utf-8'))
        bootstrap = ("from pathlib import Path\n"
                     "ROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p/'data').is_dir() and (p/'notebooks').is_dir())\n"
                     f"DATA_DIR = ROOT/'data/{dataset}'\nOUT_DIR = ROOT/'results/{experiment}'\nCHECKPOINT_DIR = ROOT/'checkpoints/{experiment}'\n"
                     "OUT_DIR.mkdir(parents=True, exist_ok=True)\nCHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)\n")
        nb['cells'][0]['source'] = ''.join(nb['cells'][0]['source']) + '\n\nImported v1 snapshot. Saved outputs describe the original Runpod run; paths below were adapted for this repository. Rerunning training replaces the local result files. Checkpoints are GitHub release assets and W&B model artifacts.\n'
        for cell in nb['cells']:
            s = ''.join(cell.get('source', []))
            if cell['cell_type'] == 'code':
                if s.startswith('%cd '):
                    s = bootstrap + '\n'.join(s.splitlines()[1:])
                s = s.replace("open('input.txt',", "open(DATA_DIR/'input.txt',")
                for name in ['train.txt', 'val.txt']:
                    s = s.replace(f"Path('{name}').read_text()", f"(DATA_DIR/'{name}').read_text(encoding='utf-8')")
                s = s.replace("'out/checkpoint.pt'", "CHECKPOINT_DIR/'checkpoint.pt'")
                s = s.replace("'out_one_epoch/checkpoint.pt'", "CHECKPOINT_DIR/'checkpoint.pt'")
                s = s.replace("out/'checkpoint.pt'", "CHECKPOINT_DIR/'checkpoint.pt'")
                for name in ['loss.json', 'sample.txt']:
                    s = s.replace(f"Path('out/{name}')", f"(OUT_DIR/'{name}')")
                s = s.replace("Path('out_one_epoch')", 'OUT_DIR').replace("Path('out')", 'OUT_DIR')
            s = s.replace('data_filtering/', '../data/tinystories/').replace('out_one_epoch/', '../results/tinystories-one-epoch/')
            s = s.replace('python ../data/tinystories/prepare.py` in this folder', 'python scripts/prepare_tinystories.py` from the repository root')
            cell['source'] = s.splitlines(keepends=True)
        write_json('notebooks/' + filename, nb)
    nb = json.loads((SOURCE / 'tinystories-gpt/TinyStories_DataAnalysis.ipynb').read_text(encoding='utf-8'))
    bootstrap = ("from pathlib import Path\nROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p/'data').is_dir() and (p/'notebooks').is_dir())\n")
    first = True
    for cell in nb['cells']:
        s = ''.join(cell.get('source', []))
        if cell['cell_type'] == 'code':
            if first:
                s = bootstrap + s
                first = False
            s = s.replace("Path('/workspace/tinystories-gpt/data_analysis/analyze.py')", "(ROOT/'scripts/analyze_tinystories.py')")
            s = s.replace("Path('/workspace/tinystories-gpt/data_analysis/", "(ROOT/'results/tinystories-data-analysis/")
            s = s.replace("out=root/'data_analysis'", "out=root/'results/tinystories-data-analysis'")
            s = s.replace("out=root/'data_analysis/name_masked'", "out=root/'results/tinystories-data-analysis/name_masked'")
            s = s.replace("exec(compile(source, 'name_masked_analysis', 'exec'))", "exec(compile(source, 'name_masked_analysis', 'exec'), {'__file__': str(ROOT/'scripts/analyze_tinystories.py')})")
        cell['source'] = s.splitlines(keepends=True)
    write_json('notebooks/TinyStories_DataAnalysis.ipynb', nb)
    entries = []
    for p in sorted(SOURCE.rglob('*')):
        if p.is_file() and '.ipynb_checkpoints' not in p.parts:
            entries.append({'source': '/workspace/' + p.relative_to(SOURCE).as_posix(), 'bytes': p.stat().st_size, 'sha256': hashlib.file_digest(p.open('rb'), 'sha256').hexdigest()})
    write_json('provenance/runpod-files.json', {'pod_id': 'rovm0pofzpp6n9', 'copied_on': '2026-10-25', 'files': entries})
    print(f'Organized {len(entries)} original files; source copy retained in .runpod-import/.')


if __name__ == '__main__':
    main()
