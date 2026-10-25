"""Read-only checkpoint evaluation and exposure audit; writes derived audit files."""
import collections
import csv
import hashlib
import json
import math
import random
import re
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

ROOT = Path('/workspace/tinystories-gpt')
OUT = ROOT / 'data_analysis/deep_audit'
OUT.mkdir(parents=True, exist_ok=True)
torch.set_num_threads(4)


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


splits = {split: [json.loads(line)['text'] for line in (ROOT / f'data_filtering/{split}.jsonl').read_text().splitlines()] for split in ['train', 'val']}
metrics = list(csv.DictReader((ROOT / 'data_analysis/name_masked/story_metrics.csv').open()))
topics = json.loads((ROOT / 'data_analysis/name_masked/topics.json').read_text())
topic_by_id = {int(row['id']): int(row['dominant_topic']) for row in metrics}
exposure = []
for topic in range(12):
    ids = [i for i in range(len(splits['train'])) if topic_by_id[i] == topic]
    exposure.append({'factor': topic, 'keywords': topics[topic]['keywords'][:8], 'stories': len(ids),
                     'story_share': len(ids) / len(splits['train']),
                     'characters': sum(len(splits['train'][i]) for i in ids),
                     'character_share': sum(len(splits['train'][i]) for i in ids) / sum(map(len, splits['train']))})
train_lengths = np.array(list(map(len, splits['train'])))
offset = 0
boundary_chunks = set()
for story in splits['train'][:-1]:
    offset += len(story) + 2
    boundary_chunks.add(offset // 256)
packed_targets = len((ROOT / 'train.txt').read_text()) - 1
summary = {'data_sha256': hashlib.sha256((ROOT / 'input.txt').read_bytes()).hexdigest(),
           'training_stories': len(splits['train']), 'validation_stories': len(splits['val']),
           'longest_20pct_training_stories_character_share': float(np.sort(train_lengths)[-3600:].sum() / train_lengths.sum()),
           'median_story_context_lengths': float(np.median(train_lengths) / 256),
           'packed_training_chunks': math.ceil(packed_targets / 256),
           'chunks_containing_a_next_story_start': len(boundary_chunks),
           'next_story_start_chunk_fraction': len(boundary_chunks) / math.ceil(packed_targets / 256),
           'lexical_factors_not_validated_semantic_topics': exposure}
save('exposure.json', summary)

# A fixed uniform sample for close reading, rather than hand-picked topic exemplars.
rng = random.Random(20261025)
review = []
for split in ['train', 'val']:
    for sid in sorted(rng.sample(range(len(splits[split])), 16)):
        review.append({'split': split, 'story_id': sid, 'factor': topic_by_id[sid + (18000 if split == 'val' else 0)], 'text': splits[split][sid]})
save('review_sample.json', {'method': '16 uniformly sampled train and 16 uniformly sampled val stories; seed 20261025; one assistant close-reading pass, not human-validated annotations', 'stories': review})

checkpoint = torch.load(ROOT / 'out_one_epoch/checkpoint.pt', map_location='cpu', weights_only=True)
nb = json.loads((ROOT / 'TinyStories_OneEpoch.ipynb').read_text())
source = next(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code' and ''.join(c['source']).startswith('class Head'))
device = 'cuda' if torch.cuda.is_available() else 'cpu'
scope = dict(torch=torch, nn=nn, F=F, device=device, vocab_size=len(checkpoint['chars']), **checkpoint['config'])
exec(compile(source, 'original_model_definition', 'exec'), scope)
model = scope['GPTLanguageModel']().to(device)
model.load_state_dict(checkpoint['model'], strict=True)
model.eval()
alphabet = {char: i for i, char in enumerate(checkpoint['chars'])}


def evaluate(stories, stride, label):
    sequences = [torch.tensor([alphabet[c] for c in text], dtype=torch.long) for text in stories]
    jobs = []
    for sid, text in enumerate(stories):
        for target_start in range(1, len(text), stride):
            target_end = min(len(text), target_start + stride)
            left = max(0, target_end - 1 - 256)
            jobs.append((sid, left, target_end, target_start))
    totals = np.zeros(len(stories), dtype=np.float64)
    counts = np.zeros(len(stories), dtype=np.int64)
    started = time.time()
    with torch.inference_mode():
        for batch_start in range(0, len(jobs), 64):
            batch = jobs[batch_start:batch_start + 64]
            width = max(end - 1 - left for sid, left, end, first in batch)
            x = torch.zeros((len(batch), width), dtype=torch.long)
            y = torch.full_like(x, -100)
            for row, (sid, left, end, first) in enumerate(batch):
                width_i = end - 1 - left
                x[row, :width_i] = sequences[sid][left:end - 1]
                begin = first - left - 1
                y[row, begin:width_i] = sequences[sid][first:end]
            logits, _ = model(x.to(device))
            target = y.to(device)
            loss = F.cross_entropy(logits.reshape(-1, len(alphabet)), target.reshape(-1), reduction='none').reshape(target.shape)
            sums = loss.sum(dim=1).cpu().numpy()
            ns = (y != -100).sum(dim=1).numpy()
            for row, (sid, left, end, first) in enumerate(batch):
                totals[sid] += sums[row]
                counts[sid] += ns[row]
            if batch_start % 6400 == 0:
                print(label, batch_start, '/', len(jobs), flush=True)
    assert np.array_equal(counts, np.array([len(text) - 1 for text in stories]))
    print(label, 'complete', float(totals.sum() / counts.sum()), 'seconds', time.time() - started, flush=True)
    return totals, counts


packed_totals, packed_counts = evaluate([(ROOT / 'val.txt').read_text()], 256, 'full_packed_validation')
short_totals, counts = evaluate(splits['val'], 256, 'story_reset_256')
long_totals, counts_long = evaluate(splits['val'], 64, 'story_stride64_more_context')
assert np.array_equal(counts, counts_long)
rows = []
for sid, story in enumerate(splits['val']):
    rows.append({'story_id': sid, 'factor': topic_by_id[18000 + sid], 'characters': len(story), 'targets': int(counts[sid]),
                 'starts_once_upon_a_time': int(story.lower().startswith('once upon a time')),
                 'dialogue_quote_marker': int('"' in story),
                 'explicit_lesson_marker': int(bool(re.search(r'\b(moral|lesson|learned|learnt)\b', story.lower()))),
                 'loss_reset256': float(short_totals[sid] / counts[sid]),
                 'loss_more_context_stride64': float(long_totals[sid] / counts[sid])})
with (OUT / 'validation_per_story.csv').open('w', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)


def aggregate(indices):
    return {'stories': len(indices), 'targets': int(counts[indices].sum()),
            'loss_reset256': float(short_totals[indices].sum() / counts[indices].sum()),
            'loss_more_context_stride64': float(long_totals[indices].sum() / counts[indices].sum())}


evaluation = {'checkpoint_sha256': hashlib.sha256((ROOT / 'out_one_epoch/checkpoint.pt').read_bytes()).hexdigest(),
              'device': device, 'full_packed_validation': {'targets': int(packed_counts.sum()), 'loss': float(packed_totals.sum() / packed_counts.sum())},
              'all_story_internal_targets': aggregate(list(range(len(rows)))), 'slices': {},
              'protocol': 'Float32 eval mode, no weight changes. Packed protocol scores every val.txt next-character target once. Story protocols reset at each story, omit its first character and separators, and score each remaining target once. stride256 uses non-overlapping blocks; stride64 overlaps inputs so later targets usually see 193-256 preceding characters. Slice labels are lexical factors or explicit string markers, not semantic quality labels. Differences between slices are observational, not causal.'}
for factor in range(12):
    evaluation['slices']['factor_' + str(factor)] = aggregate([i for i, row in enumerate(rows) if row['factor'] == factor])
for feature in ['starts_once_upon_a_time', 'dialogue_quote_marker', 'explicit_lesson_marker']:
    for value in [0, 1]:
        evaluation['slices'][feature + '_' + str(value)] = aggregate([i for i, row in enumerate(rows) if row[feature] == value])
for label, lo, hi in [('short', 0, 600), ('medium', 600, 1000), ('long', 1000, 100000)]:
    evaluation['slices']['length_' + label] = aggregate([i for i, row in enumerate(rows) if lo <= row['characters'] < hi])
save('evaluation.json', evaluation)
hardest = sorted(range(len(rows)), key=lambda i: rows[i]['loss_more_context_stride64'], reverse=True)[:10]
save('high_loss_examples.json', [{'metrics': rows[i], 'text': splits['val'][i]} for i in hardest])
print(json.dumps(evaluation, indent=2), flush=True)
