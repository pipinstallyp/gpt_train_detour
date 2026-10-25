# GPT training detour

My notebook for tweaking training recipes, starting from [Andrej Karpathy's GPT lecture](https://github.com/karpathy/ng-video-lecture).

**v1 is the preserved baseline**, copied from Runpod on 2026-10-25. It contains the datasets, runnable notebooks, saved evaluation curves, dataset analysis, and two completed model checkpoints. It does not claim a new training result.

| Completed experiment | Updates | Final logged train loss | Final logged validation loss | Best recorded validation |
| --- | ---: | ---: | ---: | --- |
| Shakespeare, random windows | 5,000 | 0.8577 | 1.5653 | 1.4837 at logged step 3,000 |
| TinyStories, one packed epoch | 980 | 1.0339 | 1.0312 | 1.0312 at update 980 |

These are next-character cross-entropy losses on **different corpora and vocabularies**, so they are not a ranking of training recipes. The Shakespeare final evaluation occurs before the last optimizer update. Only final checkpoints survive; the best Shakespeare checkpoint was not saved. TinyStories evaluation averages 20 random batches per split, rather than the entire validation corpus.

## Files

```text
data/            Exact corpus bytes, story splits, source/license notes, hashes
notebooks/       Shakespeare, TinyStories, one-epoch training, dataset analysis
scripts/         Original lecture scripts, data preparation, analysis, W&B import
configs/         Recorded baseline recipes
results/         Original loss histories, TinyStories sample and analysis
provenance/      Hashes of all 38 original Runpod files
checkpoints/     Local weights, downloaded from release assets; excluded from Git
archive/runpod/  Original notebook generators for reference
```

The unused `TinyStories_GPT.ipynb` is a 5,000-step recipe, **not a completed experiment**. The one-epoch notebook is the completed TinyStories run.

## Run locally or on a GPU pod

Use Python 3.10–3.13. Training was performed with PyTorch 2.8.0+cu128. Install the appropriate PyTorch wheel for the GPU environment, then install `requirements.txt` and start JupyterLab from the repository root:

```sh
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open a notebook in `notebooks/` and run from the top. CPU execution is supported by the original code but much slower. Rerunning training replaces its local output files; preserve a new experiment separately before comparing recipes. The original Shakespeare plotting cell recorded a missing-matplotlib error; matplotlib is now listed as a dependency. Old cell outputs remain historical evidence.

Download [v1 release assets](https://github.com/pipinstallyp/gpt_train_detour/releases/tag/v1) to reload the existing weights:

```sh
gh release download v1 --repo pipinstallyp/gpt_train_detour --dir .release
python scripts/restore_checkpoints.py
python scripts/verify_data.py
```

Run the notebook data/model definitions and the optional reload cell instead of its training cell. Full-corpus inputs and per-story JSONL are both retained under `data/` to preserve provenance.

## W&B

Project: [peepaclan/gpt_train_detour](https://wandb.ai/peepaclan/gpt_train_detour). The publication includes two historical training runs plus one dataset-publication run, versioned dataset artifacts, final model checkpoints, loss histories, analysis, and the saved TinyStories generation.

```sh
# Supply WANDB_API_KEY through the environment or a local --env-file.
python scripts/publish_wandb.py --entity peepaclan --project gpt_train_detour --release v1
```

The local default env-file is `../.credentials/.env` when this repo is inside `lasg`. No credentials are included in this repository. Completed publication IDs are deterministic; repeating the same release skips finished imports. Use a new release name for a genuinely new experiment, after preserving its config and outputs.

See [what to track](docs/experiment-tracking.md) for the comparison rules and next experiments. W&B upload time and upload-machine telemetry are not training measurements; system statistics are disabled during imports.

## Attribution and data rights

Lecture code is derived from Andrej Karpathy's `ng-video-lecture`, whose README identifies MIT licensing. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). TinyStories is separately distributed under CDLA-Sharing-1.0; its source, transformations, and per-file notices are in `data/tinystories/`. Dataset licensing is not replaced by the code license.
