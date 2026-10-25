# Supporting material

The main experiments are [Shakespeare](../notebooks/Shakespeare.ipynb), [TinyStories](../notebooks/TinyStories.ipynb), and [Lily's world](../notebooks/Lily_KG.ipynb). This directory holds the material behind them.

| Material | Location |
| --- | --- |
| Lily world, dataset generator, rule checker, and training code | [lily_kg/](lily_kg/) |
| Lily's ten-epoch results, predictions, and interpretation | [results/lily-kg-v1/](results/lily-kg-v1/) |
| TinyStories dataset analysis notebook | [TinyStories_DataAnalysis.ipynb](notebooks/TinyStories_DataAnalysis.ipynb) |
| Additional 5,000-step recipe, without a completed run | [TinyStories_5000Steps.ipynb](notebooks/TinyStories_5000Steps.ipynb) |
| Original loss histories, generated sample, and dataset analysis | [results/](results/) |
| Recorded training recipes | [configs/baselines.json](configs/baselines.json) |
| Preparation, analysis, verification, and W&B scripts | [scripts/](scripts/) |
| Original file hashes and release-asset verification | [provenance/](provenance/) |
| Comparison rules and next experiments | [experiment-tracking.md](docs/experiment-tracking.md) |
| Original notebook builders and v1 layout/importer | [archive/](archive/) |

Run the commands below **from the repository root**. Historical files in `archive/`, saved outputs, and the preserved dataset metadata describe the original v1 paths; use the current commands here for this layout.

## Restore checkpoints

```sh
gh release download v1 --repo pipinstallyp/gpt_train_detour --dir .release
python support/scripts/restore_checkpoints.py
python support/scripts/verify_data.py
```

Verified weights are placed in `support/checkpoints/`, which is excluded from Git. Both saved models were loaded strictly and produced finite logits in an inference check. Only final checkpoints survive; TinyStories' final checkpoint is also its best evaluated checkpoint. The best evaluated Shakespeare checkpoint was not saved.

## Prepare or analyze data

The exact corpora remain under `data/`. The TinyStories split contains 18,000 training and 2,000 held-out stories with zero exact cross-split overlap. It is a filtered subset of the upstream training corpus, rather than the official upstream validation split.

```sh
python support/scripts/prepare_tinystories.py
python support/scripts/analyze_tinystories.py
```

Preparation regenerates the data files; the checked-in snapshot is the authoritative v1 corpus. Analysis is exploratory. Its nearest-neighbor similarities and inferred topics are not semantic duplication or quality labels.

## W&B publication and verification

The [W&B project](https://wandb.ai/peepaclan/gpt_train_detour) contains two historical training runs, one dataset-publication run, and [Lily's actual ten-epoch training run](https://forge.coreweave.com/wandb/peepaclan/gpt_train_detour/runs/stg4wug8). It includes input dataset lineage, model artifacts, loss histories, analysis, and the saved TinyStories sample. Training-machine telemetry was not recorded for the historical imports; Lily was logged during training.

```sh
python support/scripts/publish_wandb.py --entity peepaclan --project gpt_train_detour --release v1
python support/scripts/verify_publication.py
```

Supply `WANDB_API_KEY` through the environment or `--env-file` when publishing. In the local `lasg` checkout, the default env-file is `../.credentials/.env`. No credentials are stored in the repository.

The W&B release alias is `release-v1`, distinct from its native `v0` artifact version. Completed publication IDs are deterministic, so repeating a release skips its finished imports. New experiments need separately preserved configs and results and a new release name.

The original v1 GitHub tag preserves the layout used when the results were first published. [archive/README-v1.md](archive/README-v1.md) retains its original guide. Current verification receipts are under `support/results/`.
