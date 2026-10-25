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
    "median": 0.4825085968322434,
    "p95": 0.7105849783936892,
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

0: mom, asked mom, asked, did, toys, room, mom smiled, clean, cake, mom mom, girl named, told | train=2414 val=259

1: bird, flew, tree, fly, bird flew, bird bird, sky, flew away, bird happy, nest, help bird, help | train=999 val=95

2: mommy, daddy, mommy daddy, girl, girl named, named, mommy smiled, loved, named loved, asked mommy, asked, mommy mommy | train=1252 val=137

3: dog, big dog, tail, owner, dog dog, park, scared, ran, away, big, pet, barked | train=600 val=65

4: girl, friends, play, boy, happy, big, started, felt, decided, friend, tree, fun | train=7246 val=854

5: says, say, sees, want, play, does, sorry, slide, asks, likes, blocks, wants | train=1050 val=100

6: car, toy, toy car, toys, play, cars, boy, truck, doll, box, played, drove | train=798 val=100

7: man, old man, old, man smiled, boat, smiled, girl, thanked, help, walking, man happy, asked | train=787 val=80

8: bear, teddy, teddy bear, rabbit, forest, fox, bear bear, big, bear happy, cave, big bear, bunny | train=632 val=68

9: dad, mom dad, boat, mum, fish, water, mum dad, did, asked dad, big, family, beach | train=1220 val=125

10: ball, play, red ball, play ball, red, played, boy, park, fun, catch, kick, friends | train=459 val=50

11: cat, mittens, cat cat, mouse, tree, fluffy, kitty, cat happy, cat named, house, box, big | train=543 val=67

## Next analyses

Validate topic names using exemplars and 100-200 stratified manual labels. Compare 8/12/20 topics and seeds. Add semantic embeddings to detect paraphrases missed by TF-IDF. Audit protagonist/setting/goal/conflict/resolution; pronouns and stereotyped roles; narrative contradictions and abrupt endings. Use confidence intervals and multi-label categories. Compare per-topic held-out loss and generation after training. Evaluate changes with controlled filtering/reweighting ablations, not a single quality score.