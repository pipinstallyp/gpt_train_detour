# TinyStories: what is actually in our 20,000-story subset

## Measured profile

| Measure | Result |
|---|---|
| Stories | 18,000 training + 2,000 validation |
| Median length | 154 word tokens / 780 characters |
| 90th percentile length | 278 word tokens / 1,368 characters |
| Observed alphabetic word types | 10,798; contractions split by the simple regex |
| Stories containing once upon a time | 12,058 / 20,000 = 60.29% |
| Exact cross-split matches | 0 |
| Validation nearest-train TF-IDF cosine >= 0.90 | 0 / 2,000; this does not rule out paraphrases |
| Stories longer than 256-character context | 100%; partly guaranteed by our minimum-length filter |

## Exploratory themes after suppressing frequent names

Labels below are analyst interpretations of keywords, not manually validated annotations. Counts assign each story its strongest NMF factor; these are not multi-label theme prevalence estimates.

| Factor interpretation | Stories | Share | Keywords |
|---|---:|---:|---|
| Mother / home / chores | 2,673 | 13.4% | mom, asked mom, asked, did, toys |
| Birds / flying | 1,094 | 5.5% | bird, flew, tree, fly, bird flew |
| Parents / family | 1,389 | 6.9% | mommy, daddy, mommy daddy, girl, girl named |
| Dogs | 665 | 3.3% | dog, big dog, tail, owner, dog dog |
| General friendship / play | 8,100 | 40.5% | girl, friends, play, boy, happy |
| Present-tense dialogue style | 1,150 | 5.8% | says, say, sees, want, play |
| Toy vehicles | 898 | 4.5% | car, toy, toy car, toys, play |
| Older people / helping | 867 | 4.3% | man, old man, old, man smiled, boat |
| Bears / woodland animals | 700 | 3.5% | bear, teddy, teddy bear, rabbit, forest |
| Dad / boating / fishing | 1,345 | 6.7% | dad, mom dad, boat, mum, fish |
| Ball games | 509 | 2.5% | ball, play, red ball, play ball, red |
| Cats | 610 | 3.0% | cat, mittens, cat cat, mouse, tree |

## Interpretation

This subset mixes content themes (pets, family, toys, nature) with stylistic factors (dialogue tense). A large general-play factor means 12 lexical factors do not yield a clean topic taxonomy. The first pass clustered names; the second pass helps but is not a validated semantic analysis.

This is the first 20,000 eligible stories, shuffled afterward. It is not a uniform sample from all TinyStories. ASCII and 300-10,000-character filters change coverage.

## Further analysis needed

| Question | Method | Evidence to collect |
|---|---|---|
| Which themes really occur? | Annotate 100-200 stratified exemplars with multiple labels; compare 8/12/20 factors and seeds | Label agreement, per-theme examples and uncertainty |
| Are stories repetitive beyond exact copies? | Character shingles / MinHash plus semantic embeddings; manually check closest pairs | Within- and cross-split duplicate families; template frequency |
| What narrative abilities are represented? | Tag setting, protagonist, goal, conflict, causal link and resolution | Coverage matrix; missing combinations; contradictory or unfinished stories |
| What linguistic range exists? | Sentence lengths, dialogue fraction, lexical frequency, POS and dependency patterns | Distributions by theme and story length; rare construction examples |
| What stereotypes or skew exist? | Character-role and pronoun/occupation associations with manual context review | Counts and effect sizes, not demographic guesses from names |
| What helps our model learn? | Compare held-out loss by theme/length; fixed-prompt generation rubric; controlled filtering and reweighting ablations | Generalization and memorization changes at matched token budget |

## Training implications

All stories exceed the current context. This run is a useful local-language baseline; whole-story coherence needs longer context or a subword tokenizer. Do not silently change the tokenizer mid-run. Quality, diversity and difficulty should be separate axes rather than one educational-quality score.

## Representative texts for review

### Mother / home / chores

Once upon a time, there was a little girl named Sasha. She loved her mom very much and always did what she asked. One day, Sasha asked mom for a special gift. Sasha's mom replied, "Honey, I don't have the money to buy you a gift." Sasha insisted. "Please, mom. It's very important to me!" Mom smiled. She knew that Sasha was not asking for just anything, so she decided to do something special. The next day, Sasha's mom took her to a special shop. There, Sasha saw the most amazing gift ever. "This is for you, Sasha," said mom. "I hope it will make you happy." Sasha was so excited. "Thank you, mom! I love it!" Sasha's mom was happy. She couldn't have asked for a better reaction.

### Birds / flying

Once upon a time, there was a kind girl named Lily. She had a big heart and always wanted to help others. She lived in a small house with her mom, dad, and her dog, Spot. One day, Lily saw a little bird with a hurt wing. She wanted to help the bird. Lily picked up the bird very gently and took it home. Her mom and dad said she could keep the bird in her room. Lily took care of the bird every day. She gave it food and water. She was very kind to the bird. Soon, the bird's wing was all better. The bird wanted to fly again. Lily knew it was time to let the bird go. She took the bird outside and opened her hands. The bird flew up into the sky. Lily was sad to see the bird go, but her heart was happy because she had been kind and helped the bird get better.

### Parents / family

Once upon a time, there was a little boy named Timmy. Timmy loved his mommy's cooking, especially when she made cookies in the kitchen. One day, Timmy's mommy got very sick and had to go to the hospital. Timmy was sad because he missed his mommy. One day, Timmy went to the hospital to visit his mommy. He saw her lying in a bed and she looked very pale. Timmy asked, "Mommy, are you going to be okay?" His mommy replied, "I hope so, but the doctors don't know if they can heal me." Timmy was very worried and sad. He went back home and waited for his mommy to come back. But one day, his daddy came home and told him that his mommy was dead. Timmy was heartbroken and didn't know what to do without his mommy's cookies in the kitchen.

### Dogs

Lily and Ben were friends. They liked to play in the park. One day, they saw a big dog. The dog had a red collar and a long tail. The dog looked friendly. "Hello, dog!" Lily said. "Do you want to play with us?" The dog wagged its tail and barked. It came closer to Lily and Ben. Ben was scared of the dog. He hid behind a tree. "Lily, be careful!" Ben said. "We don't know the dog. It might bite us." Lily did not listen to Ben. She trusted the dog. She thought the dog was nice. She gave the dog a snack. She had a cookie in her pocket. The dog ate the cookie and licked Lily's hand. "See, Ben? The dog is helpful. It likes us. It is our friend." Lily said. Ben shook his head. He did not trust the dog. He thought the dog was greedy. He wanted to go home. Lily and the dog played for a while. They ran and jumped and rolled on the grass. Ben watched them from the tree. He felt lonely and sad. Then, something bad happened. The dog saw a squirrel. The dog wanted to catch the squirrel. The dog ran after the squirrel. The dog forgot about Lily. The dog pulled Lily with its collar. Lily fell down. She hurt her knee. She cried. "Help! Help!" Lily shouted. "The dog is hurting me!" Ben heard Lily. He ran to help her. He tried to pull the dog away. But the dog was too strong. The dog bit Ben's arm. Ben cried too. A man came to the park. He saw Lily and Ben and the dog. He was angry. He was the dog's owner. He shouted at the dog. He took the dog away. He said sorry to Lily and Ben. He said they should not play with strange dogs. He said they should be careful. Lily and Ben were hurt. They were scared. They were sorry. They learned a lesson. They learned to not trust strange dogs. They learned to listen to their friends. They learned to be careful.

### General friendship / play

Once upon a time, there was a little girl named Lily. She loved to play outside with her friends. One day, Lily and her friends decided to play hide and seek. They ran around and hid behind trees and bushes. After a while, it started to get dark outside. Lily's mom called out to her to come inside, but Lily wanted to keep playing. She didn't want to stop having fun. Lily's friend, Sarah, tried to talk her into going home, but Lily didn't listen. She wanted to keep playing. As they played, they kept score of who was winning. Suddenly, Lily tripped and fell. She hurt her knee and started to cry. Her friends tried to help her, but it was too dark to see anything. They didn't know what to do. The moral of the story is that it's important to listen to your parents and friends when they tell you to come inside. Playing outside is fun, but it's not worth getting hurt.

### Present-tense dialogue style

Tom is a boy who likes to play with cars. He has many cars of different colors and sizes. He likes to make them go fast and make loud noises. One day, he goes to the park with his mom and dad. He brings his favorite car, a red one with big wheels. At the park, he sees a girl who is playing with a doll. She has long hair and a pink dress. She smiles at Tom and says hello. Tom says hello back and shows her his car. She says it is nice and asks if she can touch it. Tom says yes and gives her his car. She makes it go fast and makes loud noises too. Tom laughs and thinks she is fun. They play together for a while, and then they decide to go on the slide. They take turns going down the slide and then run back up. Tom goes first and then the girl follows. But when she reaches the bottom, she bumps her head on Tom's car, which he left on the ground. She cries and holds her head. Tom feels bad and says sorry. He picks up his car and gives it to her. He says it is hers now and he hopes she feels better. The girl stops crying and smiles. She says thank you and hugs Tom. She says he is nice and she likes him. She asks him what his name is. He says he is Tom and asks her what her name is. She says she is Lily and says they are friends now. Tom agrees and says they are friends. They hug again and then go to their moms and dads. They tell them they met a new friend and show them their toys. Their moms and dads are happy and say they are proud of them. They say they can play together again next time. Tom and Lily are happy and say goodbye. They wave and smile as they leave the park.

### Toy vehicles

One day, a boy named Tim had a big, heavy toy car. He loved to play with it and make it zoom all around his room. Tim liked to use his toy car to race with his other toys. His toy car was the fastest of them all. One day, Tim met a girl named Sue. Sue had a toy car too, but it was not heavy like Tim's. It was light and small. Sue said, "My car can zoom faster than yours!" Tim said, "No way! My car is the best!" So, Tim and Sue had a race with their toy cars. They both used their hands to make the cars go zoom. The heavy car and the light car raced and raced. In the end, Tim's heavy car won the race. Tim was happy and said, "See, I told you my car is the best!" Sue smiled and said, "Your car is very fast, but I still love my car too." They both played together and had lots of fun with their toy cars.

### Older people / helping

Once upon a time, there lived a young boy called Jack. He had a mild heart and was always very kind to others. One day, Jack decided to take a walk in the park, as he enjoyed feeling the gentle sunshine and fresh air. On his way through the park, he saw an old man who was crying and seemed to be in pain. Jack went over and asked the man what was wrong. Through his tears, the old man told Jack that he was suffering from a broken heart. The old man went on to explain that a close friend of his had passed away recently, and he was so sad that his heart felt like it was breaking. Jack's mild heart ached for the old man and he wanted to help. Jack told the man: "I want to help make your heart feel better. Do you like to play?" The old man nodded, and so Jack spent the rest of the afternoon with the old man, playing games, laughing and having fun. When they were done, the old man smiled, and his heart felt a little less heavy. Jack bid the old man farewell, and they both went on their way. From that day onwards, whenever Jack passed by the park, the old man and Jack exchanged smiles, and their hearts were filled with warmth and mildness.

### Bears / woodland animals

Once upon a time there was a girl who had a pet bear. The bear was so loud that it could be heard for miles. The girl always included the bear in her playtime. One day, the girl and the bear decided to go for a walk in the woods. As they explored, the bear stopped to wait for something. The bear was very quiet and seemed to sense something. The girl asked the bear what was wrong. The bear replied, "I hear something loud coming." Suddenly, the trees started shaking and a large elephant emerged from the forest. The girl was so scared she ran back home. The bear stayed put. When the elephant came close, the bear started making loud noises. The elephant backed away and ran away. The girl was so amazed and thanked the bear for protecting her. She included the bear in everything she did, but this time the bear included her too.

### Dad / boating / fishing

Jack and his dad went for a ride in the park. In their car, dad gave Jack a good lecture about why it's important to be safe. They drove past a big lake, and Jack wanted to go for a ride in a boat. Dad said no, so they looked at the lake instead. Then they rode to the park. They saw a playground with swings and slides. Jack wanted to go play, but Dad said it was time for a picnic. Dad set up a blanket and Jack ate a good lunch. After lunch, Jack saw a tire swing. He asked dad if he could give it a ride. Dad said yes, and Jack had so much fun swinging around. He asked for another ride and Dad said it was time to go home. Jack was sad, but Dad said they would come back again soon. On their way home, Jack thought of all the good times he had with his Dad.

### Ball games

Once upon a time, there was a little girl named Lily. She had a new red ball. One day, Lily went outside to play with her ball. She saw a big bush near her house. Lily loved to throw her ball and watch it bounce. Lily threw her ball high in the air. But, oh no! The ball went into the bush. Lily tried to get her ball, but it was stuck. She asked her friend, Tom, for help. "Tom, can you help me get my ball?" she said. Tom tried to reach the ball, but he couldn't. Then, Tom had an idea. He found a long stick. Tom used the stick to poke the ball. The ball began to slip out of the bush. With one more poke, the ball was free. Lily and Tom were so happy. They played with the new red ball all day long. From that day on, they were always careful not to let the ball go near the big bush again.

### Cats

Tim has a pet cat. He likes to play with his cat and give her food. His cat is soft and nice. She purrs when Tim pets her. One day, Tim hears a loud noise outside. He goes to the window and sees a big dog. The dog is fierce and angry. He barks and growls at the cat. The cat is scared and runs away. Tim is sad and worried. He wants to find his cat and make her safe. He puts on his shoes and coat and goes outside. He listens for his cat. He hears a meow from under a car. He sees his cat hiding there. Tim calls his cat and reaches for her. The cat comes out and jumps into his arms. Tim hugs his cat and takes her inside. He gives her some milk and a toy. The cat is happy and calm. She purrs again when Tim pets her. Tim is glad he found his cat. He loves his pet and wants to protect her. He tells his cat not to go outside when there is a fierce dog. He tells his cat he will always listen to her. The cat and Tim are good friends.