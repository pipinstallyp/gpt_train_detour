"""Check corpus identity, train/validation separation, and text/JSONL agreement."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
checksums = json.loads((ROOT / 'data/checksums.json').read_text())
for name, expected in checksums.items():
    with (ROOT / name).open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    assert actual == expected, f'Hash mismatch: {name}'
folder = ROOT / 'data/tinystories'
splits = {}
for split, count in [('train', 18000), ('val', 2000)]:
    stories = [json.loads(line)['text'] for line in (folder / f'{split}.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(stories) == count
    assert len(set(stories)) == count
    assert (folder / f'{split}.txt').read_text(encoding='utf-8') == '\n\n'.join(stories) + '\n'
    splits[split] = stories
assert not set(splits['train']) & set(splits['val']), 'Exact train/validation overlap'
assert (folder / 'input.txt').read_text(encoding='utf-8') == '\n\n'.join(splits['train'] + splits['val']) + '\n'
assert len((folder / 'train.txt').read_text()) - 1 == 16046877
print(f'Verified {len(checksums)} hashes, 20,000 unique stories, exact split reconstruction, and zero exact cross-split overlap.')
