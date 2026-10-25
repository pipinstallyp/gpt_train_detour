# TinyStories mini: our exact experimental subset

This entry concerns the **20,000 filtered stories actually used here**. Claims about the full TinyStories research do not automatically apply to this subset or our model.

## Entry points

- [Filled description](description.json): the sixteen dimensions, with evidence and uncertainty.
- [Audit notebook](DeepAudit.ipynb): explanation and an inspectable results-loading cell.
- [Audit report](evidence/report.txt): measured findings and close-reading notes.
- [Evaluation](evidence/evaluation.json) and [exposure](evidence/exposure.json): full validation and the character-weighted mix.
- [Per-story losses](evidence/validation_per_story.csv): both story evaluation protocols.
- [Review sample](evidence/review_sample.json) and [pilot annotations](pilot-annotations.json): exact records and selected reasoning/quality observations.

The full packed validation pass covers 1,777,321 targets at loss 1.029617. The longest 20% of training stories supply 34.01% of story characters. The close-reading sample has 16 training and 16 validation stories; its semantic observations are one assistant review, not independently validated prevalence estimates.

The original corpus is under [data/tinystories](../../data/tinystories/). Its initial lexical analysis is under [support/results](../../support/results/tinystories-data-analysis/). The original training notebook remains under [notebooks](../../notebooks/TinyStories.ipynb).

`evidence/audit.py` reproduces the computation on the original Runpod layout and installed PyTorch environment. Its fixed root is `/workspace/tinystories-gpt`; it reads the existing notebook model definition and checkpoint and writes derived audit files. It does not train or modify the checkpoint. The new notebook can read the copied results from this research folder or from that pod layout.

## Data attribution

TinyStories data providers: Ronen Eldan and Yuanzhi Li. Source: [TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories). The subset has been normalized, filtered, deduplicated and rearranged; source details are in the original [manifest](../../data/tinystories/manifest.json).

The full story texts in the review/high-loss evidence and their excerpts retain **CDLA-Sharing-1.0**, separately from code licensing. See the included [data license](DATA_LICENSE.txt) and [original modification notices](../../data/tinystories/README.md). New pilot annotations are assistant analysis of these records, not upstream labels.
