"""Check graph truth, counterbalances, leakage, and context fit before training."""
import argparse
import collections
import hashlib
import json
from pathlib import Path

from logic import fact, solve, render, WORLD
from generate import HELD_REACH, HELD_WEIGHT


def check_logic():
    assert solve([fact('ball','on','mat')],fact('lily','reachable','ball'))[0]=='Unknown'
    assert solve([fact('ball','on','mat'),fact('milo','reach','mat')],fact('lily','reachable','ball'))[0]=='Unknown'
    assert solve([fact('ball','on','mat'),fact('lily','reach','mat',False)],fact('lily','reachable','ball'))[0]=='No'
    assert solve([fact('ball','on','mat'),fact('lily','reach','table',False)],fact('lily','reachable','ball'))[0]=='Unknown'
    assert solve([fact('stone','heavier','cup'),fact('cup','heavier','ball')],fact('ball','heavier','stone'))[0]=='No'
    assert solve([fact('stone','heavier','cup')],fact('stone','heavier','ball'))[0]=='Unknown'
    assert solve([fact('ball','color','blue')],fact('ball','color','red'))[0]=='No'
    assert solve([],fact('ball','color','red'))[0]=='Unknown'
    try:
        solve([fact('ball','heavier','cup'),fact('cup','heavier','ball')],fact('ball','heavier','cup'))
    except AssertionError:
        pass
    else:
        raise AssertionError('Cyclic order accepted')


def validate(folder):
    check_logic()
    manifest=json.loads((folder/'manifest.json').read_text())
    fingerprints={};queries={};splits={}
    for split,summary in manifest['splits'].items():
        p=folder/(split+'.jsonl')
        assert hashlib.sha256(p.read_bytes()).hexdigest()==summary['sha256']
        rows=[json.loads(line) for line in p.read_text().splitlines()]
        splits[split]=rows
        fingerprints[split]={r['semantic_sha256'] for r in rows}
        assert len(rows)==len(fingerprints[split])==summary['records']
        assert sum(len(r['text'])-1 for r in rows)==summary['record_targets']
        by_question=collections.defaultdict(collections.Counter)
        for row in rows:
            answer,proof=solve(row['facts'],row['query'])
            assert answer==row['answer'] and proof==row['proof_facts']
            assert render(row['facts'],row['query'],answer,row['surface_style'])==(row['prompt'],row['text'])
            assert len(row['text'])<=256 and row['text'].isascii()
            by_question[json.dumps(row['query'],sort_keys=True)][answer]+=1
            if row['task']=='reachable':
                held=(row['query']['head'],row['query']['tail']) in HELD_REACH
                assert held==(split=='test_composition')
            if row['task']=='heavier':
                held=frozenset([row['query']['head'],row['query']['tail']]) in HELD_WEIGHT
                assert held==(split=='test_composition')
        assert all(len(c)==3 and len(set(c.values()))==1 for c in by_question.values()),'Question-only label shortcut'
    for a,b in [('train','validation'),('train','test_composition'),('validation','test_composition')]:
        assert not fingerprints[a]&fingerprints[b],(a,b)
    assert fingerprints['validation']==fingerprints['test_paraphrase']
    result={'logic_corner_cases_passed':9,'records_checked':sum(len(x) for x in splits.values()),
            'all_labels_match_symbolic_oracle':True,'train_validation_composition_overlap':0,
            'counterbalanced_question_only_accuracy':1/3,'all_records_fit_256_characters':True,
            'paraphrase_policy':'Deliberate paired re-rendering of validation graphs; never trained.'}
    (folder/'validation_report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);args=parser.parse_args()
    print(json.dumps(validate(args.folder),indent=2))
