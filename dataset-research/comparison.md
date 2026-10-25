# Initial comparison and what it means

| Aspect | FineWeb / FineWeb-Edu | Our TinyStories mini | Open Reasoning Tasks |
| --- | --- | --- | --- |
| Role | Web pretraining corpus; Edu is a filtered subset | Exact 20,000-story experimental subset | Task reference with illustrative examples |
| Content | Broad web knowledge; Edu has an educational selection objective | Simplified narratives; family, play, animals, food and other themes in reviewed examples | Named operations across logic, social reasoning, mathematics, language, planning and other areas |
| Reasoning signal | Published aggregate evaluation; per-task prevalence unmeasured here | Implicit narrative signals observed; explicit task coverage unmeasured | Definitions and examples say which operation is intended |
| Quality evidence | Documented curation and classifier evaluation | Full validation computation plus a 32-story diagnostic review | Reference examples require their own answer-quality review |
| Context fit | Must inspect selected documents and intended tokenizer/model | Median training story spans about three current contexts | Some tasks may need states or instructions over several turns |
| Learning evidence | Authors' controlled comparisons, within their research setting | One baseline; no controlled mix intervention yet | An inventory alone provides no trained-model result |
| Main next action | Sample a pinned slice and annotate with the common framework | Validate semantic labels, then test a controlled data change | Select relevant task definitions and build checkable held-out probes |

See the source-specific evidence in [FineWeb](fineweb/description.json), [mini](tinystories-mini/description.json), and the [reference inventory](open-reasoning-tasks/task-inventory.json). The comparisons above have different evidence strengths; they are not numerical dataset rankings.

## What this tells us already

- The same topic can exercise different operations. A family story can teach a preference, a causal consequence, a location update, or only a stock phrase.
- Fluent prose can contain incorrect word meanings or a missing causal bridge. Conversely, an unusual or fantastical story can still be consistent.
- FineWeb's educational selection objective and our narrative-coherence objective need different quality rubrics. We should borrow the discipline of validating curation through learning experiments.
- The Nous collection helps design probes, but its categories overlap and its examples are not a universal answer oracle. The pinned snapshot has 95 Markdown tasks and 91 JSON counterparts; this is a count of definitions, not training diversity.
- We cannot yet responsibly state dataset-wide percentages for these reasoning operations or recommend mixture weights from them.

## Which gaps deserve attention first?

For the current character model, prioritize local semantic correctness, goal/action/consequence links, entity/state continuity, and context availability. Use the existing mini pilot to define examples and failure criteria. Broad mathematical, legal, and counterfactual task families can remain in the inventory until the training objective and model justify evaluating them.

Keep the original data as the baseline. Test semantic repair/filtering and diversity-preserving sampling as separate interventions, with an unchanged held-out set and equal character-target budgets. The result we want is a measured capability change with attributable causes.
