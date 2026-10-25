"""Generate independent graph scenes and counterbalanced QA from a typed world."""
import argparse
import collections
import hashlib
import json
import random
from pathlib import Path

from logic import WORLD, POOLS, ANSWERS, fact, solve, render, key

TASKS = ['color', 'on', 'reachable', 'heavier']
HELD_REACH = {tuple(x) for x in WORLD['held_out_reach_queries']}
HELD_WEIGHT = {frozenset(x) for x in WORLD['held_out_weight_queries']}


def signature(facts, query):
    return json.dumps([sorted((x['head'], x['relation'], x['tail'], x['positive']) for x in facts), key(query)], separators=(',', ':'))


def group(rng, task, composition=False):
    agents, objects, places, colors = [POOLS[x] for x in ['agent', 'object', 'place', 'color']]
    a = rng.choice(agents)
    o, other, mid, end, spare, spare2 = rng.sample(objects, 6)
    place, elsewhere, noise_place = rng.sample(places, 3)
    color, other_color = rng.sample(colors, 2)
    noise_agent = rng.choice([x for x in agents if x != a])
    noise_reach = fact(noise_agent, 'reach', noise_place, rng.choice([True, False]))
    if task == 'reachable' and ((a, o) in HELD_REACH) != composition:
        return None
    if task == 'heavier' and (frozenset([o, end]) in HELD_WEIGHT) != composition:
        return None
    if task == 'color':
        query = fact(o, 'color', color)
        cases = [
            [fact(o, 'color', color), fact(o, 'on', place), noise_reach, fact(other, 'color', other_color)],
            [fact(o, 'color', other_color), fact(o, 'on', place), noise_reach, fact(other, 'color', other_color)],
            [fact(spare, 'color', color), fact(o, 'on', place), noise_reach, fact(other, 'color', other_color)],
        ]
    elif task == 'on':
        query = fact(o, 'on', place)
        cases = [
            [fact(o, 'on', place), fact(o, 'color', color), noise_reach, fact(other, 'on', elsewhere)],
            [fact(o, 'on', elsewhere), fact(o, 'color', color), noise_reach, fact(other, 'on', elsewhere)],
            [fact(spare, 'on', place), fact(o, 'color', color), noise_reach, fact(other, 'on', elsewhere)],
        ]
    elif task == 'reachable':
        query = fact(a, 'reachable', o)
        cases = [
            [fact(a, 'reach', place), fact(o, 'on', place), noise_reach, fact(other, 'on', noise_place)],
            [fact(a, 'reach', place, False), fact(o, 'on', place), noise_reach, fact(other, 'on', noise_place)],
            [fact(a, 'reach', elsewhere), fact(o, 'on', place), noise_reach, fact(other, 'on', noise_place)],
        ]
    else:
        query = fact(o, 'heavier', end)
        cases = [
            [fact(o, 'heavier', mid), fact(mid, 'heavier', end), fact(spare, 'heavier', spare2), fact(end, 'color', color)],
            [fact(end, 'heavier', mid), fact(mid, 'heavier', o), fact(spare, 'heavier', spare2), fact(end, 'color', color)],
            [fact(o, 'heavier', mid), fact(mid, 'heavier', other), fact(spare, 'heavier', spare2), fact(end, 'color', color)],
        ]
    order = list(range(4)); rng.shuffle(order)
    return [([items[i] for i in order], query, intended) for items, intended in zip(cases, ANSWERS)]


def build_split(rng, split, groups_per_task, seen, tasks=TASKS, composition=False):
    records = []
    for task in tasks:
        count = 0
        while count < groups_per_task:
            variants = group(rng, task, composition)
            if variants is None:
                continue
            signatures = [signature(facts, query) for facts, query, intended in variants]
            if any(s in seen for s in signatures):
                continue
            rendered = [render(facts, query, intended) for facts, query, intended in variants]
            if any(len(text) > 256 for prompt, text in rendered):
                continue
            seen.update(signatures)
            group_id = f'{split}-{task}-{count:05d}'
            for (facts, query, intended), (prompt, text) in zip(variants, rendered):
                answer, proof = solve(facts, query)
                assert answer == intended, (split, task, facts, query, answer, intended)
                records.append({'id': group_id + '-' + intended.lower(), 'group_id': group_id, 'task': task,
                                'facts': facts, 'query': query, 'answer': answer, 'proof_facts': proof,
                                'surface_style': 'base', 'prompt': prompt, 'text': text,
                                'semantic_sha256': hashlib.sha256(signature(facts, query).encode()).hexdigest()})
            count += 1
    rng.shuffle(records)
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent / 'dataset')
    args = parser.parse_args()
    out = args.out; out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(1337)
    seen = set()
    splits = {'train': build_split(rng, 'train', 2000, seen), 'validation': build_split(rng, 'validation', 100, seen),
              'test_composition': build_split(rng, 'test_composition', 100, seen, ['reachable', 'heavier'], True)}
    paraphrases = []
    for row in splits['validation']:
        prompt, text = render(row['facts'], row['query'], row['answer'], 'paraphrase')
        assert len(text) <= 256
        paraphrases.append({**row, 'id': row['id'] + '-paraphrase', 'surface_style': 'paraphrase', 'prompt': prompt, 'text': text})
    splits['test_paraphrase'] = paraphrases
    summaries = {}
    for split, records in splits.items():
        path = out / (split + '.jsonl')
        with path.open('w', encoding='utf-8', newline='\n') as stream:
            for row in records:
                stream.write(json.dumps(row, separators=(',', ':')) + '\n')
        summaries[split] = {'records': len(records), 'characters': sum(len(row['text']) for row in records),
                            'record_targets': sum(len(row['text']) - 1 for row in records),
                            'max_record_characters': max(len(row['text']) for row in records),
                            'labels': dict(collections.Counter(row['answer'] for row in records)),
                            'tasks': dict(collections.Counter(row['task'] for row in records)),
                            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    manifest = {'version': 'v1', 'seed': 1337, 'unit': 'character tokens, including punctuation and whitespace',
                'training_objective': 'full-record next-character cross entropy; first character supplied as context',
                'training_epochs': 10, 'splits': summaries,
                'split_policy': 'Contrast groups stay in one split. Train/validation/composition semantic cases are disjoint. Paraphrase deliberately re-renders the held-out validation graphs with unseen wording. Composition holds out query endpoint pairs, not new relation meanings.',
                'world_sha256': hashlib.sha256((Path(__file__).resolve().parent / 'world.json').read_bytes()).hexdigest()}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (out / 'world.json').write_text(json.dumps(WORLD, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
