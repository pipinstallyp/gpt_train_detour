---
language:
- en
license: mit
task_categories:
- text-generation
tags:
- synthetic
- knowledge-graph
- reasoning
pretty_name: Lily KG Mini v1
configs:
- config_name: default
  data_files:
  - split: train
    path: train.jsonl
  - split: validation
    path: validation.jsonl
  - split: test_composition
    path: test_composition.jsonl
  - split: test_paraphrase
    path: test_paraphrase.jsonl
---

# Lily KG Mini v1

A small, fully templated pretraining corpus generated from independent scenes in Lily's typed toy world. A symbolic solver checks every answer. There are no LLM-generated facts or borrowed story texts.

## Contents

22 entities (four agents, eight objects, six places and four colors), 35 illustrative seed facts, and explicit rules for single-valued colors/locations, reachability composition and strict transitive weight order. The generator recombines entity bindings and facts into independent scenes; the seed is a schema example, not fixed global truth.

| Split | Records | Character tokens | Purpose |
| --- | ---: | ---: | --- |
| train | 24,000 | 3,823,235 | Four tasks, balanced Yes/No/Unknown |
| validation | 1,200 | 191,105 | Fresh semantic cases in familiar wording |
| test_composition | 600 | 104,444 | Held-out reach/weight query endpoint pairs |
| test_paraphrase | 1,200 | 239,555 | Reworded versions of the validation graphs |

All records fit within 256 characters; the longest paraphrase is 243 characters. Character counts include whitespace and punctuation. Record-aligned training predicts all characters except the first in each record: 3,799,235 targets per epoch, 37,992,350 across ten epochs. These are not subword-token or word counts.

The four tasks are color binding, location binding, reachability composition, and two-edge heavier-than chains. All use a common Facts / Question / Answer text format. Whole-record next-character prediction trains on the facts and the answer; no answer-only mask is required.

## Logic and uncertainty

Every object has at most one color and current location in a scene. A known different value disproves a queried value. Reachability uses an explicitly simplified rule: if an item is on a place an agent can/cannot reach, that agent can/cannot reach the item. Weight order is transitive and asymmetric.

**Unknown means that neither the query nor its negation follows from the observed facts and these rules. Missing information is not automatically No.** These rules are toy-world assumptions, not a complete model of physical affordances. There are no grasping conclusions from reachability alone.

Each contrast group contains Yes, No and Unknown variants. Color, location and reach Yes/No variants change one relevant fact; weight-chain variants reverse the two-edge chain. The same question has balanced labels, preventing a question-only predictor from beating one-third accuracy. Facts include distractors and their order is shuffled.

## Splits and limitations

The generator partitions entire contrast groups, rejects repeated semantic cases across training/validation/composition, and excludes reserved query endpoint pairs from training. Familiar entities and relation meanings remain available. The composition split therefore tests new endpoint combinations, not an unseen reasoning algorithm.

The paraphrase split intentionally shares semantic graphs with validation to measure a paired wording change; neither split is trained on. It is not an independent sample of worlds. The natural-language templates are deliberately narrow. Success does not establish general reasoning, narrative ability, identity, curiosity, spontaneous abstention or consciousness. Unknown examples are explicitly supervised.

This first experiment uses a static shuffled mixture for ten epochs. Curriculum learning and active graph exploration are future controlled comparisons. Model scores should be reported separately for familiar scenes, new combinations, and new wording, with per-task accuracy and Unknown precision/recall alongside language-model loss.

## Reproduce and load

Source rules and generation/validation scripts are included under `generation/`. The manifest provides per-split hashes. `validation_report.json` records logic and leakage checks.

```python
from datasets import load_dataset
data = load_dataset('chewiesays/lily-kg-mini-v1', revision='v1')
print(data['train'][0]['text'])
```

Use only the `text` field as language-model input. Graph facts, query, proofs and split metadata are provided for auditing and evaluation; they are not additional hidden model inputs. Evaluation prompts end immediately before the answer.

Synthetic data and generator code: MIT. The separate experimental model is derived from Andrej Karpathy's GPT lecture; its training is maintained in the author's experiment repository.
