# TinyStories subset ? modification and attribution notice

Data providers: Ronen Eldan and Yuanzhi Li. Source: https://huggingface.co/datasets/roneneldan/TinyStories . Paper: https://arxiv.org/abs/2305.07759 .

License: CDLA-Sharing-1.0. The complete unmodified agreement is in LICENSE.txt and at https://cdla.dev/sharing-1-0/ . This data license applies to input.txt, train.txt, val.txt, train.jsonl, val.jsonl, and story excerpts in the dataset analysis. It is separate from the repository code license. Adjacent .license files identify the changed data files without changing the training bytes.

MODIFIED DATA: these files are a normalized, filtered, deduplicated and rearranged subset of the original TinyStories-train.txt, not the complete upstream dataset. The first 20,000 eligible unique stories were selected, NFKC-normalized, punctuation mapped to ASCII, whitespace collapsed, restricted to printable ASCII and 300?10,000 characters, then shuffled with seed 1337. The 18,000/2,000 split is by complete story. It is not the upstream official validation split. Source selection is sequential, not a uniform full-corpus sample. The original processing manifest is retained as manifest.json; reproduce with python scripts/prepare_tinystories.py.

input.txt concatenates train followed by validation; train.txt and val.txt are the actual model inputs for their respective splits. Blank lines separate stories; no special EOS token is inserted. JSONL preserves per-story records for analysis.
