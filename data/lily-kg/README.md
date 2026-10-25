# Lily KG mini v1

The raw dataset lives on [Hugging Face](https://huggingface.co/datasets/chewiesays/lily-kg-mini-v1). The training run used revision `dfbe3515218955f3b737e7cbb3a894be96ffddf1`, also tagged `v1`. These receipts preserve the exact split sizes, hashes, validation checks and downloaded source revision without duplicating the corpus in Git.

| Split | Records | Purpose |
| --- | ---: | --- |
| train | 24,000 | Four equally represented tasks, balanced Yes/No/Unknown |
| validation | 1,200 | Fresh scenes with familiar wording; checkpoint selection |
| test_composition | 600 | Reach/order questions with reserved endpoint pairs |
| test_paraphrase | 1,200 | Validation graphs rendered using different wording |

The training text contains 3,823,235 character tokens. Training predicts 3,799,235 within-record targets per epoch, excluding each supplied first character and ignored padding. Ten epochs expose 37,992,350 targets.

See the [world and generation source](../../support/lily_kg/README.md), [dataset card](../../support/lily_kg/DATASET_CARD.md), and [completed results](../../support/results/lily-kg-v1/README.md). The paraphrase split shares validation semantics intentionally and introduces eleven word forms absent from training; it measures combined wording and vocabulary transfer.
