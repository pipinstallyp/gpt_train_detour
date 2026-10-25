"""Three-valued toy-world logic. Missing facts are not negative facts."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
WORLD = json.loads((ROOT / 'world.json').read_text())
ENTITIES = {entity['id']: entity for entity in WORLD['entities']}
POOLS = {kind: [key for key, value in ENTITIES.items() if value['type'] == kind] for kind in ['agent', 'object', 'place', 'color']}
ANSWERS = ['Yes', 'No', 'Unknown']


def fact(head, relation, tail, positive=True):
    return {'head': head, 'relation': relation, 'tail': tail, 'positive': positive}


def key(value):
    return value['head'], value['relation'], value['tail']


def solve(facts, query):
    positive, negative = {}, {}
    for item in facts:
        types = WORLD['relation_types'][item['relation']]
        assert ENTITIES[item['head']]['type'] == types[0]
        assert ENTITIES[item['tail']]['type'] == types[1]
        target = positive if item['positive'] else negative
        target[key(item)] = [item]
    for relation, alternatives in [('color', POOLS['color']), ('on', POOLS['place'])]:
        known = {}
        for (head, rel, tail), proof in list(positive.items()):
            if rel != relation:
                continue
            assert head not in known or known[head] == tail, 'Conflicting single-valued property'
            known[head] = tail
            for alternative in alternatives:
                if alternative != tail:
                    negative[(head, relation, alternative)] = proof
    changed = True
    while changed:
        changed = False
        weights = [(a, b, proof) for (a, rel, b), proof in positive.items() if rel == 'heavier']
        for a, b, proof_a in weights:
            assert a != b, 'Cyclic strict order'
            for b2, c, proof_b in weights:
                if b == b2 and (a, 'heavier', c) not in positive:
                    positive[(a, 'heavier', c)] = proof_a + proof_b
                    changed = True
    for (a, rel, b), proof in list(positive.items()):
        if rel == 'heavier':
            assert a != b, 'Cyclic strict order'
            negative[(b, rel, a)] = proof
    locations = [(obj, place, proof) for (obj, rel, place), proof in positive.items() if rel == 'on']
    for obj, place, on_proof in locations:
        for agent in POOLS['agent']:
            if (agent, 'reach', place) in positive:
                positive[(agent, 'reachable', obj)] = positive[(agent, 'reach', place)] + on_proof
            if (agent, 'reach', place) in negative:
                negative[(agent, 'reachable', obj)] = negative[(agent, 'reach', place)] + on_proof
    assert not positive.keys() & negative.keys(), 'Contradictory graph'
    target = key(query)
    if target in positive:
        return 'Yes', positive[target]
    if target in negative:
        return 'No', negative[target]
    return 'Unknown', []


def label(entity):
    return ENTITIES[entity]['label']


def sentence(item, style='base'):
    a, rel, b, sign = item['head'], item['relation'], item['tail'], item['positive']
    if rel == 'color':
        return f'The {label(a)} is {label(b)}.' if style == 'base' else f'{label(b).capitalize()} is the color of the {label(a)}.'
    if rel == 'on':
        return f'The {label(a)} is on the {label(b)}.' if style == 'base' else f'On the {label(b)} sits the {label(a)}.'
    if rel == 'reach':
        if style == 'base':
            return f'{label(a)} {"can" if sign else "cannot"} reach the {label(b)}.'
        return f'The {label(b)} is {"within" if sign else "out of"} reach for {label(a)}.'
    if rel == 'heavier':
        assert sign
        return f'The {label(a)} is heavier than the {label(b)}.' if style == 'base' else f'Compared to the {label(b)}, the {label(a)} is heavier.'
    raise ValueError(rel)


def question(query, style='base'):
    a, rel, b = query['head'], query['relation'], query['tail']
    if rel == 'color':
        return f'Is the {label(a)} {label(b)}?' if style == 'base' else f'Does the {label(a)} have the color {label(b)}?'
    if rel == 'on':
        return f'Is the {label(a)} on the {label(b)}?' if style == 'base' else f'Is the {label(b)} where the {label(a)} is?'
    if rel == 'reachable':
        return f'Can {label(a)} reach the {label(b)}?' if style == 'base' else f'Is the {label(b)} within reach for {label(a)}?'
    if rel == 'heavier':
        return f'Is the {label(a)} heavier than the {label(b)}?' if style == 'base' else f'Compared to the {label(b)}, is the {label(a)} heavier?'
    raise ValueError(rel)


def render(facts, query, answer, style='base'):
    prompt = 'Facts: ' + ' '.join(sentence(item, style) for item in facts) + '\nQuestion: ' + question(query, style) + '\nAnswer: '
    return prompt, prompt + answer + '.\n'
