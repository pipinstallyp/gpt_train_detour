# Dataset research: what does the data actually offer?

Use this workspace to describe datasets, identify gaps, and choose training experiments. **Keep this folder until the owner explicitly asks to remove it.** Its files are isolated from the training code.

## Start here

1. [The description framework](framework.md): 16 dimensions beyond a list of reasoning tasks.
2. [The current comparison](comparison.md): what we know, what we infer, and what remains unmeasured.
3. [FineWeb / FineWeb-Edu](fineweb/README.md) and [TinyStories mini](tinystories-mini/README.md): filled descriptions and evidence.
4. [Open Reasoning Tasks](open-reasoning-tasks/README.md): the pinned task reference and a complete inventory.

| Folder | Role |
| --- | --- |
| `fineweb/` | Literature-based description of the original FineWeb and Edu releases |
| `tinystories-mini/` | Description of our exact 20,000-story subset, audit notebook, and measured evidence |
| `open-reasoning-tasks/` | Nous task definitions as a reference, with 95 tasks indexed |
| `templates/` | A reusable dataset dossier and an example-level annotation template |

## Is this activity useful?

Yes, when it helps us choose a measurable intervention: which examples to add or repair, which diversity to retain, which context or tokenizer the task needs, and which evaluation would reveal a gain. It also exposes assumptions, such as treating topic frequency as reasoning coverage or a low language-model loss as semantic correctness.

The output should be a **coverage hypothesis with evidence and a next test**. A long task list or a universal quality ranking would provide much less value. Start with a few capabilities relevant to the model and expand when a decision needs more detail.

## Read the evidence labels

- `measured_local`: a specified computation on the exact mini subset or checkpoint.
- `pilot_review`: an assistant's review of identified examples; no validated population rate.
- `author_reported`: evidence from a linked source; not independently replicated here.
- `inference`: an interpretation or compatibility consequence, with its assumptions stated.
- `unknown`: not measured or not recoverable from the current records.

Topic presence, a reasoning signal in the text, an explicit reasoning exercise, a valid solution, and an ability learned by a model are separate claims. Unknown coverage stays unknown. Frequency denominators are explicit: stories, characters, subword tokens, or task definitions.

This is an initial comparative dossier. We have not sampled the full FineWeb corpus or annotated every reasoning task in the mini subset. FineWeb's section documents the original 2024 research scope; it is not an audit of every later dataset revision.

The dataset and model descriptions are in `*/description.json`. The 95-task inventory keeps task-level corpus coverage unmeasured while separate pilot annotations record the narrative signals actually inspected. All new research material is contained here for review and continued development.
