from pathlib import Path
import urllib.request, json, random, hashlib, unicodedata, collections
ROOT=Path(__file__).resolve().parents[2]/'data/tinystories'
ROOT.mkdir(parents=True, exist_ok=True)
OUT=ROOT
URL='https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStories-train.txt'
stories=[]; seen=set(); rejected=collections.Counter(); buffer=[]
translation=str.maketrans({'‘':"'",'’':"'",'“':'"','”':'"','–':'-','—':'-'})
with urllib.request.urlopen(URL,timeout=120) as response:
    for raw in response:
        line=raw.decode('utf-8')
        if '<|endoftext|>' not in line:
            buffer.append(line); continue
        buffer.append(line.split('<|endoftext|>')[0])
        text=unicodedata.normalize('NFKC',''.join(buffer)).translate(translation)
        text=' '.join(text.split()); buffer=[]
        if not 300<=len(text)<=10000:
            rejected['length']+=1; continue
        if not all(32<=ord(c)<127 for c in text):
            rejected['non_ascii']+=1; continue
        key=hashlib.sha256(text.encode()).hexdigest()
        if key in seen:
            rejected['duplicate']+=1; continue
        seen.add(key); stories.append(text)
        if len(stories)%5000==0: print('Selected',len(stories),flush=True)
        if len(stories)==20000: break
assert len(stories)==20000, len(stories)
random.Random(1337).shuffle(stories)
train=stories[:18000]; val=stories[18000:]
for name,items in [('train',train),('val',val)]:
    (OUT/(name+'.jsonl')).write_text(''.join(json.dumps({'text':t})+'\n' for t in items), encoding='utf-8', newline='\n')
    (ROOT/(name+'.txt')).write_text('\n\n'.join(items)+'\n', encoding='utf-8', newline='\n')
(ROOT/'input.txt').write_text('\n\n'.join(stories)+'\n', encoding='utf-8', newline='\n')
assert not set(train)&set(val)
summary=dict(source=URL, selection='first 20000 unique eligible stories, then seeded shuffle',seed=1337,total=20000,train=18000,val=2000,filters='NFKC; smart punctuation to ASCII; collapse whitespace; 300-10000 chars; printable ASCII; exact deduplication',rejected=dict(rejected),input_characters=len((ROOT/'input.txt').read_text()),vocab_size=len(set((ROOT/'input.txt').read_text())),sha256=hashlib.sha256((ROOT/'input.txt').read_bytes()).hexdigest())
(OUT/'manifest.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
