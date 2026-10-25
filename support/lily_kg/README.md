# Lily KG experiment

The first Lily experiment uses a small symbolic world to generate a pretraining corpus, then trains the original TinyStories model architecture for ten epochs from random initialization.

- [Dataset on Hugging Face](https://huggingface.co/datasets/chewiesays/lily-kg-mini-v1)
- [Runpod notebook](https://rovm0pofzpp6n9-8888.proxy.runpod.net/lab/tree/workspace/lily-kg/Lily_KG.ipynb)
- [Dataset card and split definitions](DATASET_CARD.md)
- [Completed run, predictions and interpretation](../results/lily-kg-v1/README.md)

## Where a coding agent should start

1. `world.json` defines 22 typed entities, 35 seed facts, world assumptions and held-out query pairs.
2. `logic.py` implements the positive/negative closure, Unknown semantics, and text rendering.
3. `generate.py` builds independent scenes with counterbalanced answers and contrast groups.
4. `validate.py` checks logical corner cases, every label/proof, split separation, question-only shortcuts, and context fit.
5. `publish.py` publishes an allowlisted folder to HF, fetches the committed snapshot and verifies file hashes.
6. `model.py` contains the same model classes as the TinyStories notebook. `train.py` trains and evaluates the experiment.

The dataset is not a single global story in which every fact remains simultaneously true. Each record is a new scene, so colors, locations and relative weights can vary. The declared toy reach rule is not a general physical model and does not imply grasping. There is no identity, action-selection or curriculum objective in this baseline.

## Size and training budget

24,000 training records contain 3,823,235 ASCII character tokens. Each complete record fits within the 256-character context; right padding is ignored. Predicting every within-record target once gives 3,799,235 targets per epoch and 37,992,350 over ten epochs, with 375 optimizer updates per epoch.

Model: six layers, six heads, width 384, context 256, batch 64, dropout 0.2, learning rate 3e-4, AdamW defaults, seed 1337. The declared 96-character alphabet gives 10,812,768 parameters. Training uses full-record next-character loss, not answer-only masking. Keeping complete scenes together changes packing from the original TinyStories packed-stream run; the architecture and optimizer settings are preserved.

## Validation and tests

- `validation`: 1,200 fresh semantic cases in the training wording. Select the best checkpoint using full-scene loss.
- `test_composition`: 600 reach/order cases with reserved query endpoint combinations. Familiar words and relation meanings are retained.
- `test_paraphrase`: 1,200 deliberate re-renderings of validation graphs using different wording. This paired design holds semantics fixed; it is not an independent world sample.

The paraphrase templates introduce eleven word forms absent from training, so this measures vocabulary and wording transfer together. The composition test includes only reach/order tasks; compare it with those same tasks in validation, rather than the four-task aggregate.

Tests are first evaluated after ten epochs and checkpoint selection. Unknown is explicitly supervised. All splits balance Yes, No and Unknown, including for each exact query, so a question-only predictor cannot exceed one-third accuracy.

Report full-scene loss, per-task answer accuracy, Unknown precision/recall, closed-label Y/N/U first-character accuracy, and unconstrained greedy exact-answer accuracy. Closed-label accuracy and generated-answer accuracy are distinct measurements.

The notebook also records the original TinyStories-style estimate: 20 random batches of 64 x 256 windows per split. These windows can begin mid-scene or cross scene boundaries; they do not match the scene-aligned training distribution. Keep that diagnostic separate from the primary complete-scene validation loss. Raw loss numbers on different corpora do not establish a capability ranking.

## Run on the pod

The existing project is `/workspace/lily-kg`, with its Python environment at `/root/venvs/lily-kg`. The notebook uses the `lily-kg` kernel. Credentials are loaded from the standard HF cache and a private root-owned training credential file, not notebook cells.

```sh
python generate.py --out generated
python validate.py generated
python build_notebook.py
python execute_notebook.py
```

Install a GPU-capable PyTorch 2.8 environment plus `huggingface_hub`, `wandb`, `matplotlib`, `nbformat`, `nbclient` and `ipykernel`. The helper notebook and executor assume the original pod layout. The notebook publishes to `chewiesays/lily-kg-mini-v1`; review that destination before reusing the helpers for another account or world version.

Generated data and runtime checkpoints are excluded from Git. HF contains the dataset, generation sources and hashes. Local checkpoints retain both best and final models, optimizer state, vocabulary, configuration and the pinned HF revision. W&B receives the actual training curves, final evaluations, and the best inference checkpoint.

Future curriculum experiments should compare against this static baseline at matched training exposure and keep these validation/test policies explicit. Changing the ontology or templates should produce a new dataset version.
