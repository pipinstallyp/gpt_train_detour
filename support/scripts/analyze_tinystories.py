import os
os.environ['OMP_NUM_THREADS']='4'
os.environ['OPENBLAS_NUM_THREADS']='4'
import json,re,collections,csv
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer,ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF
from sklearn.neighbors import NearestNeighbors
root=Path(__file__).resolve().parents[2]
out=root/'support/results/tinystories-data-analysis'; out.mkdir(parents=True,exist_ok=True)
train=[json.loads(l)['text'] for l in (root/'data/tinystories/train.jsonl').read_text().splitlines()]
val=[json.loads(l)['text'] for l in (root/'data/tinystories/val.jsonl').read_text().splitlines()]
texts=train+val
tokens=[re.findall(r"[a-z]+",s.lower()) for s in texts]
words=collections.Counter(w for ts in tokens for w in ts)
lengths=np.array([len(t) for t in texts])
wl=np.array([len(ts) for ts in tokens])
phrases=collections.Counter()
for ts in tokens:
    phrases.update(set(' '.join(ts[i:i+4]) for i in range(len(ts)-3)))
stop=sorted(set(ENGLISH_STOP_WORDS)|set('said little day time once upon went saw wanted like just really very one two three lily tim tom lucy ben sam jane jack anna amy'.split()))
vec=TfidfVectorizer(max_features=12000,min_df=10,max_df=.65,ngram_range=(1,2),stop_words=stop)
# Fit topics on training only, then assign held-out stories.
X=vec.fit_transform(train)
V=vec.transform(val)
nmf=NMF(n_components=12,random_state=1337,init='nndsvda',max_iter=200)
W=nmf.fit_transform(X); WV=nmf.transform(V)
terms=vec.get_feature_names_out()
labels=np.r_[W.argmax(1),WV.argmax(1)]
topics=[]
for k,h in enumerate(nmf.components_):
    ranked=np.argsort(h)[-12:][::-1]
    best=np.argsort(W[:,k])[-3:][::-1]
    topics.append(dict(topic=k,keywords=terms[ranked].tolist(),train_stories=int((labels[:18000]==k).sum()),val_stories=int((labels[18000:]==k).sum()),examples=[dict(train_id=int(i),text=train[i]) for i in best]))
# Approximate lexical overlap, not a duplicate verdict. Batch query limits memory.
nn=NearestNeighbors(n_neighbors=1,metric='cosine',algorithm='brute',n_jobs=2).fit(X)
dist,idx=nn.kneighbors(V)
sim=1-dist[:,0]
pairs=np.argsort(sim)[-20:][::-1]
near=[dict(val_id=int(i),train_id=int(idx[i,0]),cosine=float(sim[i]),validation=val[i],training=train[idx[i,0]]) for i in pairs]
summary=dict(stories=len(texts),train=len(train),validation=len(val),unique_word_types=len(words),
characters=dict(zip(['min','p10','median','p90','p99','max'],np.quantile(lengths,[0,.1,.5,.9,.99,1]).tolist())),
words=dict(zip(['min','p10','median','p90','p99','max'],np.quantile(wl,[0,.1,.5,.9,.99,1]).tolist())),
fraction_longer_than_context=float((lengths>256).mean()),
exact_cross_split_overlap=len(set(train)&set(val)),
validation_nearest_train_cosine=dict(median=float(np.median(sim)),p95=float(np.quantile(sim,.95)),above_090=int((sim>=.9).sum())),
top_words=words.most_common(40),repeated_4grams=phrases.most_common(25),
caveats=['Sequential source subset, not a uniform full-corpus sample.','ASCII/length filtering changes coverage.','Topic count 12 is exploratory, not validated truth.','Each story assigned its strongest topic for counts; stories can have several themes.','Lexical similarity can reflect common templates, not duplication.'])
(out/'summary.json').write_text(json.dumps(summary,indent=2))
(out/'topics.json').write_text(json.dumps(topics,indent=2))
(out/'similar_pairs.json').write_text(json.dumps(near,indent=2))
with (out/'story_metrics.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['id','split','characters','words','unique_word_ratio','dominant_topic'])
    for i,ts in enumerate(tokens): w.writerow([i,'train' if i<18000 else 'val',int(lengths[i]),len(ts),len(set(ts))/len(ts),int(labels[i])])
report=['# TinyStories subset: exploratory profile',json.dumps(summary,indent=2),'## Exploratory topics']
for t in topics:
    report.append(str(t['topic'])+': '+', '.join(t['keywords'])+' | train='+str(t['train_stories'])+' val='+str(t['val_stories']))
report+=['## Next analyses','Validate topic names using exemplars and 100-200 stratified manual labels. Compare 8/12/20 topics and seeds. Add semantic embeddings to detect paraphrases missed by TF-IDF. Audit protagonist/setting/goal/conflict/resolution; pronouns and stereotyped roles; narrative contradictions and abrupt endings. Use confidence intervals and multi-label categories. Compare per-topic held-out loss and generation after training. Evaluate changes with controlled filtering/reweighting ablations, not a single quality score.']
(out/'report.md').write_text('\n\n'.join(report))
print(json.dumps(summary,indent=2))
for t in topics: print('TOPIC',t['topic'],t['train_stories'],t['val_stories'],', '.join(t['keywords'][:8]))
print('ANALYSIS COMPLETE')
