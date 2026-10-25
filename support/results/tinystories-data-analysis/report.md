# TinyStories subset: exploratory profile

{
  "stories": 20000,
  "train": 18000,
  "validation": 2000,
  "unique_word_types": 10798,
  "characters": {
    "min": 301.0,
    "p10": 578.0,
    "median": 780.0,
    "p90": 1368.0,
    "p99": 2422.0099999999984,
    "max": 4524.0
  },
  "words": {
    "min": 59.0,
    "p10": 115.0,
    "median": 154.0,
    "p90": 278.0,
    "p99": 492.0099999999984,
    "max": 882.0
  },
  "fraction_longer_than_context": 1.0,
  "exact_cross_split_overlap": 0,
  "validation_nearest_train_cosine": {
    "median": 0.4935637059503526,
    "p95": 0.7069591860872103,
    "above_090": 0
  },
  "top_words": [
    [
      "the",
      189569
    ],
    [
      "and",
      171268
    ],
    [
      "to",
      119150
    ],
    [
      "a",
      108974
    ],
    [
      "was",
      87570
    ],
    [
      "he",
      74164
    ],
    [
      "she",
      73248
    ],
    [
      "it",
      66799
    ],
    [
      "they",
      64115
    ],
    [
      "her",
      47506
    ],
    [
      "said",
      33752
    ],
    [
      "you",
      31661
    ],
    [
      "lily",
      31138
    ],
    [
      "in",
      30391
    ],
    [
      "his",
      30273
    ],
    [
      "with",
      30141
    ],
    [
      "that",
      27745
    ],
    [
      "day",
      25640
    ],
    [
      "so",
      25091
    ],
    [
      "of",
      24724
    ],
    [
      "but",
      24028
    ],
    [
      "had",
      22292
    ],
    [
      "mom",
      22244
    ],
    [
      "on",
      22173
    ],
    [
      "s",
      21525
    ],
    [
      "i",
      20354
    ],
    [
      "one",
      19509
    ],
    [
      "for",
      18704
    ],
    [
      "there",
      17910
    ],
    [
      "very",
      17600
    ],
    [
      "little",
      17318
    ],
    [
      "time",
      17095
    ],
    [
      "happy",
      16695
    ],
    [
      "is",
      16587
    ],
    [
      "big",
      15998
    ],
    [
      "saw",
      15703
    ],
    [
      "not",
      15671
    ],
    [
      "t",
      14724
    ],
    [
      "play",
      14239
    ],
    [
      "once",
      13882
    ]
  ],
  "repeated_4grams": [
    [
      "once upon a time",
      12058
    ],
    [
      "upon a time there",
      11411
    ],
    [
      "a time there was",
      10703
    ],
    [
      "time there was a",
      10422
    ],
    [
      "there was a little",
      5898
    ],
    [
      "was a little girl",
      3924
    ],
    [
      "a little girl named",
      3576
    ],
    [
      "little girl named lily",
      2687
    ],
    [
      "girl named lily she",
      2137
    ],
    [
      "from that day on",
      2125
    ],
    [
      "named lily she loved",
      1552
    ],
    [
      "once there was a",
      1370
    ],
    [
      "was a little boy",
      1330
    ],
    [
      "lily she loved to",
      1317
    ],
    [
      "a little boy named",
      1294
    ],
    [
      "was so happy and",
      940
    ],
    [
      "went to the park",
      907
    ],
    [
      "she loved to play",
      905
    ],
    [
      "to play in the",
      903
    ],
    [
      "loved to play with",
      890
    ],
    [
      "do you want to",
      830
    ],
    [
      "boy named timmy timmy",
      813
    ],
    [
      "to play with her",
      782
    ],
    [
      "little boy named timmy",
      729
    ],
    [
      "they like to play",
      717
    ]
  ],
  "caveats": [
    "Sequential source subset, not a uniform full-corpus sample.",
    "ASCII/length filtering changes coverage.",
    "Topic count 12 is exploratory, not validated truth.",
    "Each story assigned its strongest topic for counts; stories can have several themes.",
    "Lexical similarity can reflect common templates, not duplication."
  ]
}

## Exploratory topics

0: girl, friends, boy, john, big, happy, looked, started, felt, smiled, fun, decided | train=6818 val=805

1: timmy, named timmy, timmy timmy, timmy loved, boy named, boy, timmy mom, billy, play, timmy happy, named, toy | train=1158 val=121

2: max, named max, max max, named, dog named, max loved, owner, max happy, play, max felt, play max, max owner | train=522 val=56

3: bird, flew, tree, fly, bird flew, sky, bird bird, flew away, bird happy, nest, help, help bird | train=938 val=88

4: says, sara, car, sees, say, play, want, sorry, does, likes, box, asks | train=1065 val=118

5: mom, dad, did, asked, toys, asked mom, mom dad, room, cake, mom smiled, clean, girl named | train=3041 val=319

6: mommy, daddy, mommy daddy, girl, girl named, named loved, named, mommy smiled, loved, asked mommy, asked, mommy mommy | train=1130 val=133

7: man, old man, old, man smiled, smiled, thanked, girl, help, man happy, boat, asked, lady | train=757 val=77

8: dog, ball, spot, cat, play, sue, park, tail, big dog, big, ran, dog dog | train=1059 val=106

9: bear, benny, teddy, rabbit, teddy bear, forest, bunny, fox, big, big bear, bear happy, cave | train=810 val=92

10: mia, mia says, named mia, boat, mia happy, mia mia, mia mom, mia friends, says, slide, mia playing, play | train=379 val=42

11: bob, sue, bob bob, named bob, friends, bob happy, bob smiled, called bob, joe, bob loved, help, named | train=323 val=43

## Next analyses

Validate topic names using exemplars and 100-200 stratified manual labels. Compare 8/12/20 topics and seeds. Add semantic embeddings to detect paraphrases missed by TF-IDF. Audit protagonist/setting/goal/conflict/resolution; pronouns and stereotyped roles; narrative contradictions and abrupt endings. Use confidence intervals and multi-label categories. Compare per-topic held-out loss and generation after training. Evaluate changes with controlled filtering/reweighting ablations, not a single quality score.