# FineWeb and FineWeb-Edu dossier

This is a source-based review of the original 2024 FineWeb/FineWeb-Edu research. FineWeb is the parent web corpus; Edu adds an educational-value selection objective. We have not independently sampled the current full corpus or measured its coverage of the 95 Nous tasks.

Read the filled [sixteen-dimension description](description.json) alongside the [common framework](../framework.md). Each dimension states its evidence level, sources, and uncertainty.

The strongest evidence here concerns the authors' curation and training experiments. Fine-grained operation prevalence, narrative correctness rates, and usefulness to our 10.8M character model remain open. Educational relevance is also distinct from correctness, diversity, or suitability for our specific training objective.

In the authors' topic analysis, Edu shifts the parent mix toward education and history/culture/politics, reducing several business, entertainment and travel clusters. Those are topic-distribution observations, not direct counts of reasoning skills. [Paper, topic analysis](https://arxiv.org/html/2406.17557v2#S4.SS1)

## Sources

- [Versioned paper](https://arxiv.org/html/2406.17557v2): pipeline and controlled experiments; topic/domain analyses.
- [Technical report](https://huggingfacefw-blogpost-fineweb-v1.static.hf.space/index.html): design choices and threshold tradeoffs.
- [FineWeb-Edu dataset card](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu): release documentation and metadata.
- [Educational classifier card](https://huggingface.co/HuggingFaceFW/fineweb-edu-classifier): rubric, held-out metrics and limitations.

The living cards may describe later revisions. Numeric release-scale claims in this dossier refer to the original research, not every subsequent update. The published materials use different approximate annotation counts; we do not silently merge them into a single exact total.
