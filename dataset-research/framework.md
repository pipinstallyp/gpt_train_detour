# Describe a dataset beyond its task list

The Nous catalogue helps answer **which operation a task asks for**. A dataset description also needs to explain the content, the supervision, its trustworthiness, and whether that content is usable by the intended model.

## The sixteen dimensions

| Dimension | Questions to answer | Evidence to collect |
| --- | --- | --- |
| 1. Purpose | What capability is the dataset intended to support? At which training stage? | Stated objective; target model and evaluation |
| 2. Source and unit | Is a record a page, story, dialogue, question, proof, or trajectory? How was it selected? | Source/version, generation and filtering pipeline, unit boundaries |
| 3. Topics and knowledge | Which subjects, entities, facts, and prerequisites appear? How broad is the long tail? | Multi-label topic annotations; examples; mass by topic |
| 4. Reasoning operations | Does an answer require deduction, causality, state tracking, analogy, planning, or another operation? | A specific input/output relationship and an evidence span |
| 5. Supervision and solution structure | Does the text mention, demonstrate, or elicit a skill? Is there a valid answer or merely a plausible explanation? | Input, target, rationale, verifier, answer multiplicity, partial-credit rule |
| 6. Language and communication | Which languages, registers, speech acts, sentence structures, and interaction patterns appear? | Dialogue, explanation, persuasion, instruction and narration distributions |
| 7. Quality | Are grammar, word meanings, entities, causes and conclusions internally sound? Is factual grounding available? | Separate evidence-backed quality labels, not one overall score |
| 8. Difficulty and prerequisites | What knowledge and number of steps does the task require for this model? | Controlled probes, calibrated difficulty and failure examples |
| 9. Dependency and context | How far apart are relevant facts? Does packing or truncation remove them? | Dependency distance, context units, boundaries and tokenizer |
| 10. Diversity and redundancy | Are examples distinct problems, paraphrases, templates, or renamed copies? | Exact/fuzzy/semantic families with reviewed matches |
| 11. Balance and exposure | Which slices dominate the actual training stream? | Story/document and character/token weights; tails and intersections |
| 12. Annotation trust | Who supplied the labels? How were disagreement and uncertainty handled? | Teacher/model version, human review, agreement, calibration |
| 13. Leakage and generalization | What overlaps across splits, sources, problem families, or evaluation sets? | Split methodology, contamination checks and fresh holdouts |
| 14. Model compatibility | Can this tokenizer represent the text? Does the model have sufficient context and usable target formats? | Encoding checks, target budget, packing and format constraints |
| 15. Empirical utility | Does this data change improve the intended behavior under controlled training? | Matched-budget ablations, repeated seeds, per-skill and generation tests |
| 16. Access and reproducibility | Can someone recover the same records and reproduce the analysis? | Version/hash, access, licensing metadata, code and artifact lineage |

## Describe the learning signal, not only the subject

Consider two texts about a lost toy. Both have the topic `family/toys`. One states where the toy is; another tracks who last saw it and who missed a move. The second may support belief/state tracking, but a successful completion must actually depend on that information before we call it a reasoning test.

For each example, distinguish:

1. **Mentioned:** reasoning vocabulary appears.
2. **Implicit signal:** a relation is present in a narrative.
3. **Demonstrated:** the text works through a relation or solution.
4. **Elicited:** the prompt requires the operation to answer correctly.
5. **Validated:** the answer or solution was checked with a specified method.

Then test **learned ability** separately on held-out prompts. A dataset tag cannot establish it. A long explanation is not automatically a valid reasoning trace, and a benchmark's title does not certify every example inside it.

## Quality is a vector

Assess linguistic well-formedness, semantic correctness, entity/state consistency, causal sufficiency, factual grounding when applicable, instruction/answer alignment, repetition, and formatting separately. Difficulty, fantasy, emotional tone, and moral content are descriptors; they are not automatic quality penalties.

For a pilot, use `supported`, `mixed`, `clear_issue`, `not_applicable`, or `unknown`, with an exact supporting span and a short explanation. These are proposed annotation conventions, not a validated scoring scale. A genuinely difficult example may be useful even if the model assigns it high loss.

## Quantify only after validating the labels

Keep uniform samples for prevalence separate from targeted samples for finding failures. Use independent review of a subset, record disagreements, and report denominators and uncertainty. Distinguish record-weighted and training-exposure-weighted percentages. Characters in our mini corpus and GPT-2 subword tokens in FineWeb experiments are different units.

The 17 study families in the Nous inventory are our provisional navigation aid. They are neither a validated cognitive ontology nor mutually exclusive abilities. Keep the original task IDs, allow multiple example labels, and inspect overlaps such as motive inference versus emotional inference.

## Minimum useful next experiment

Choose one claim, such as: repairing weak goal/action links improves held-out narrative consistency. Calibrate that label, preserve a fresh evaluation set, and compare original and revised data at the same target budget and model settings over several seeds. Change context or tokenizer in a separate ablation. The description should lead to this experiment rather than indefinitely expanding a taxonomy.
