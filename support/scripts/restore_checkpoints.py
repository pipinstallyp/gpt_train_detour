"""Restore and hash-check checkpoint assets downloaded with gh release download."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = {
    'shakespeare-baseline-checkpoint.pt': 'shakespeare-baseline',
    'tinystories-one-epoch-checkpoint.pt': 'tinystories-one-epoch',
}
manifest = json.loads((ROOT / 'support/provenance/runpod-files.json').read_text())['files']
for filename, name in ASSETS.items():
    asset = ROOT / '.release' / filename
    source = '/workspace/shakespeare-gpt/out/checkpoint.pt' if name == 'shakespeare-baseline' else '/workspace/tinystories-gpt/out_one_epoch/checkpoint.pt'
    expected = next(row['sha256'] for row in manifest if row['source'] == source)
    with asset.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if actual != expected:
        raise ValueError(f'Checkpoint hash mismatch: {filename}')
    target = ROOT / 'support/checkpoints' / name / 'checkpoint.pt'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(asset, target)
    print(f'Restored {name}; SHA-256 verified.')
