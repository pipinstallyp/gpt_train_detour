# GPT training detour

A learning log for understanding how GPT training recipes affect learning and generated text, starting from [Andrej Karpathy's lecture](https://github.com/karpathy/ng-video-lecture). The notebooks follow the data, model, training loop, and results; future experiments will change one part of the recipe at a time and compare what happens.

## Start here

**Begin with Shakespeare to understand the baseline, then explore TinyStories to follow a full pass through a different dataset.** v1 preserves these two original runs as the starting point for later experiments.

| Start here | What's inside |
| --- | --- |
| **[1. Shakespeare](notebooks/Shakespeare.ipynb)** | A character GPT trained on Shakespeare for 5,000 updates. Follow the model and training loop, then see where validation loss begins to worsen. |
| **[2. TinyStories](notebooks/TinyStories.ipynb)** | The same model family trained for one packed epoch on 20,000 filtered stories. Inspect the data split, learning curve, and generated story. |

Both notebooks contain the original saved outputs. **[View the runs in W&B](https://wandb.ai/peepaclan/gpt_train_detour)** or **[download the v1 checkpoints](https://github.com/pipinstallyp/gpt_train_detour/releases/tag/v1)**.

## Run a notebook

Use Python 3.11–3.13 and install a PyTorch build suitable for your machine. The original runs used PyTorch 2.8.0+cu128.

```sh
python -m pip install -r requirements.txt
python -m jupyterlab
```

Launch from the repository root and open either notebook above. Run the data/model definitions and the optional reload cell to use a downloaded checkpoint, or run the training cell to train from scratch.

## Repository layout

```text
notebooks/   The two main experiments — start with the links above
data/        Datasets, exact splits, and source/license notes
support/     Results, analysis, scripts, configs, and provenance
```

[Supporting material](support/README.md) covers checkpoint setup, dataset analysis, verification, and W&B publishing. The additional TinyStories analysis notebook and unexecuted 5,000-step recipe live there too.

## What the baselines show

Shakespeare's best recorded validation loss was **1.4837 at step 3,000**, rising to **1.5653** at the final logged evaluation. TinyStories finished its one epoch at **1.0312** validation loss. These use different corpora and vocabularies, so the numbers are not a controlled comparison of recipes.

Future experiments should compare held-out loss and generated samples at the same training budget. See [what to track](support/docs/experiment-tracking.md).

Code: [MIT](LICENSE), derived from Karpathy's lecture. Dataset terms and attribution are separate; see [source notices](support/THIRD_PARTY_NOTICES.md).
