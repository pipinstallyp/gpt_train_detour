# TinyStories selection

Source: https://huggingface.co/datasets/roneneldan/TinyStories

Run `python data_filtering/prepare.py` from the project folder. Streams source until 20,000 unique eligible stories are found. This is a sequential subset, not a uniform sample of the full dataset. Normalizes punctuation/whitespace; accepts printable ASCII and 300-10,000 characters; exact deduplication. Seed 1337 shuffles the accepted subset, then splits 18,000/2,000 by whole story. train.jsonl and val.jsonl preserve records. manifest.json records source, counts, filters and input hash. Root input.txt is combined; train.txt and val.txt are used by the notebook.
