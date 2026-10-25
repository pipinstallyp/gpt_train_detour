# What matters for these experiments

The question is: **does a recipe change improve held-out next-character prediction and the generated text at a comparable training budget?**

| Publish | Why it matters | v1 evidence |
| --- | --- | --- |
| Train and validation cross-entropy, best validation and its step, final gap | Distinguish learning from memorization | Both saved histories |
| Corpus identity, hashes, filters, split rules, vocabulary, context length | A loss is meaningful only with its data and evaluation definition | Exact datasets and manifests |
| Architecture, parameter count, optimizer, learning rate, batch, dropout, seed | Explain what changed between runs | Configs and notebooks |
| Updates and character targets seen; runtime where recorded | Compare recipes at comparable work or cost | Both budgets; runtime only for TinyStories |
| Final checkpoint hash and selection rule | Make each result recoverable | Both final checkpoints |
| Fixed-prompt samples, ideally a prompt suite and fixed sampling seeds | Check coherence, repetition, spelling, and long-range structure | One original TinyStories sample only |
| Dataset analysis and train/validation overlap | Understand easy templates, coverage, and possible contamination | TinyStories exact overlap and exploratory lexical analysis |
| Git commit and original source hashes | Tie data, code, weights, and curves together | Provenance manifest and run config |

W&B stores time series with `run.log`, scalar comparison fields with `run.summary`, generated samples with Tables, and data/model files with Artifacts. Dataset artifacts are explicitly linked as inputs to the historical model runs. See the official [logging documentation](https://docs.wandb.ai/guides/track/log/) and [artifact documentation](https://docs.wandb.ai/guides/artifacts/).

## Read v1 correctly

- Shakespeare's training loss keeps improving while validation worsens after its best recorded step 3,000. That is evidence consistent with overfitting. The saved final checkpoint is not the best evaluated model.
- TinyStories completes one pass over all 16,046,877 next-character training targets in shuffled, non-overlapping chunks. It packs stories with blank lines and has no special EOS token. Its 256-character window does not span most complete stories. Its sample has locally plausible wording and clear grammatical/narrative failures; lower character loss alone is not enough to claim story quality.
- TinyStories uses 18,000 training and 2,000 held-out stories from the first 20,000 eligible, exact-deduplicated stories in the upstream **training** file. The held-out split is not the upstream official validation corpus. Filtering and sequential subset selection change coverage.
- Cross-entropy is in natural-log units. `exp(loss)` is character perplexity; do not compare it to word/subword perplexity or treat the Shakespeare/TinyStories difference as a controlled experiment.
- Saved evaluations sample random batches. No confidence intervals, complete validation pass, GPU-utilization trace, memory peak, or historical dollar cost were recorded. Importing cannot recover those measurements.
- The TinyStories 5,000-step notebook has no saved executed run. Do not publish it as a completed result.

## Next useful experiments

1. Fix a TinyStories dataset version and a fixed held-out evaluation set. Repeat the baseline across three seeds, logging full validation or identical fixed batches.
2. Compare the existing random-window and packed-epoch recipes at the same number of character targets. Change one factor at a time.
3. Save best-validation and final checkpoints separately. Add a learning-rate schedule and test dropout changes against a stable baseline.
4. Use the same prompt suite and sampling seed/temperature for every checkpoint. Score repetition, coherence, completion, and context-dependent consistency; retain the raw samples.
5. Record training time separately from evaluation/checkpoint time, measured tokens/s, peak GPU memory, and GPU model in the training process. Add cost only when the actual price and measured billed duration are available.

Weight/gradient histograms on every step are not a priority for v1. Start with trustworthy comparisons and recoverable artifacts; add diagnostic traces when investigating a specific training failure.
