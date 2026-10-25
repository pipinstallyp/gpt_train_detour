from pathlib import Path
import json
root=Path('/workspace/tinystories-gpt')
root.mkdir(exist_ok=True)
(root/'data_filtering').mkdir(exist_ok=True)
script="""from pathlib import Path
import urllib.request, json, random, hashlib, unicodedata, collections
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data_filtering'
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
    (OUT/(name+'.jsonl')).write_text(''.join(json.dumps({'text':t})+'\\n' for t in items))
    (ROOT/(name+'.txt')).write_text('\\n\\n'.join(items)+'\\n')
(ROOT/'input.txt').write_text('\\n\\n'.join(stories)+'\\n')
assert not set(train)&set(val)
summary=dict(source=URL, selection='first 20000 unique eligible stories, then seeded shuffle',seed=1337,total=20000,train=18000,val=2000,filters='NFKC; smart punctuation to ASCII; collapse whitespace; 300-10000 chars; printable ASCII; exact deduplication',rejected=dict(rejected),input_characters=len((ROOT/'input.txt').read_text()),vocab_size=len(set((ROOT/'input.txt').read_text())),sha256=hashlib.sha256((ROOT/'input.txt').read_bytes()).hexdigest())
(OUT/'manifest.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
"""
(root/'data_filtering/prepare.py').write_text(script)
nb=json.loads(Path('/workspace/shakespeare-gpt/Shakespeare_GPT.ipynb').read_text())
for c in nb['cells']:
    c['source']=''.join(c['source'])
    if c['cell_type']=='code': c['outputs']=[]; c['execution_count']=None
    c['source']=c['source'].replace('/workspace/shakespeare-gpt','/workspace/tinystories-gpt').replace('Shakespeare GPT on Runpod','TinyStories GPT on Runpod').replace("prompt='ROMEO:'","prompt='Once upon a time'")
data=nb['cells'][3]['source']
data=data.replace("n = int(0.9*len(data)) # first 90% will be train, rest val\ntrain_data = data[:n]\nval_data = data[n:]", "from pathlib import Path\ntrain_data = torch.tensor(encode(Path('train.txt').read_text()), dtype=torch.long)\nval_data = torch.tensor(encode(Path('val.txt').read_text()), dtype=torch.long)")
nb['cells'][3]['source']=data
nb['cells'][2]['source']='## 1. TinyStories data and tokenizer\n20,000 unique filtered stories: 18,000 train / 2,000 validation. Split by whole story before encoding. input.txt contains all selected stories; training uses train.txt and val.txt. Character-level model with 256-character context.'
nb['cells'][0]['source']='# TinyStories GPT on Runpod\nKarpathy architecture, trained from scratch on 20,000 filtered TinyStories. Filtering code and manifest: data_filtering/. Original model dimensions preserved. Run top to bottom.'
nb['cells'][4]['source']="print(len(text), 'characters;', vocab_size, 'symbols')\nprint('Train chars:', len(train_data), 'Validation chars:', len(val_data))\nprint(text[:300])"
nb['cells'][8]['source']=nb['cells'][8]['source'].replace("print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')", "print(f'{sum(p.numel() for p in m.parameters()):,} trainable parameters')").replace("'step':max_iters}", "'step':max_iters,'config':dict(n_embd=n_embd,n_head=n_head,n_layer=n_layer,block_size=block_size,dropout=dropout),'optimizer':optimizer.state_dict()}")
nb['cells'][10]['source']="from IPython.display import SVG, display\nxs=[r['step'] for r in history]\nlines=[]\nfor key,color in [('train','steelblue'),('val','darkorange')]:\n    points=' '.join(f'{40+520*x/max(xs):.1f},{250-200*r[key]/max(v[k] for v in history for k in [\"train\",\"val\"]):.1f}' for x,r in zip(xs,history))\n    lines.append(f'<polyline points=\"{points}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"2\"/>')\ndisplay(SVG('<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"620\" height=\"290\"><rect width=\"620\" height=\"290\" fill=\"white\"/><text x=\"40\" y=\"20\">Cross entropy: train (blue), validation (orange)</text>'+''.join(lines)+'<text x=\"220\" y=\"280\">Training step: 0 to 5000</text></svg>'))"
(root/'TinyStories_GPT.ipynb').write_text(json.dumps(nb))
print('TinyStories notebook and filtering pipeline created')
