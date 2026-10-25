# Open Reasoning Tasks: reference, template, and inventory

[Nous Research's collection](https://github.com/NousResearch/Open-Reasoning-Tasks) describes tasks and gives illustrative inputs/outputs. We use it to name candidate operations and design probes. Corpus prevalence, answer validity, and learned model ability still need separate evidence.

Pinned commit: [`35df7000b8f636178e303add868415b30f92cad0`](https://github.com/NousResearch/Open-Reasoning-Tasks/tree/35df7000b8f636178e303add868415b30f92cad0). Retrieved 2026-10-25.

- [Original task template](task-template.upstream.md): Description, Modality, optional Diagram/Citations, Examples, and Tags. Copied unchanged.
- [Full inventory](task-inventory.json): all **95 Markdown task definitions**, linked to pinned source files and grouped into **17 provisional study families**.
- [Inventory summary](inventory-summary.json): family counts, original JSON-tag counts, and the four Markdown-only tasks.
- [Source record](source.json): commit and copied-file hashes.

There are **91 JSON task records** at this snapshot. Curry's Paradox, Multiturn LaTeX Generation, Stack Based Reasoning, and Towers of Hanoi have Markdown definitions without JSON counterparts. The inventory includes them, so reading only `tasks-json/` would miss four definitions.

The family grouping is our navigation aid. Original tags and task names are retained; overlapping task definitions have not been treated as independent dimensions of intelligence. Task-count and tag-count statistics describe this reference repository, not FineWeb or TinyStories exposure.

The inventory deliberately leaves task-level coverage in both training corpora unmeasured. [Mini pilot annotations](../tinystories-mini/pilot-annotations.json) record selected narrative signals with exact spans. Seeing an emotion in a story does not by itself certify the explicit task of inferring an unstated emotional state, and it does not establish false-belief reasoning.

## Attribution

Upstream: Nous Research, Open Reasoning Tasks / LLM Reasoning Task Collection. The unmodified upstream template is distributed under [Apache-2.0](LICENSE.upstream); its license is included. Inventory grouping, coverage fields, and dataset-description extensions are our additions, not upstream claims. Upstream examples were inspected, but are linked rather than vendored as a training dataset.
