from pathlib import Path
import json
s=Path('gpt.py').read_text()
a,b=s.split('class Head',1)
b,c=('class Head'+b).split('model = GPTLanguageModel()',1)
c='model = GPTLanguageModel()'+c.split('# generate from the model')[0]
c=c.replace('for iter in range(max_iters):','history=[]\nfor iter in range(max_iters):').replace('        losses = estimate_loss()', "        losses = estimate_loss()\n        history.append({k:float(v) for k,v in losses.items()} | {'step':iter})")
c+="\nfrom pathlib import Path\nimport json\nPath('out').mkdir(exist_ok=True)\ntorch.save({'model':model.state_dict(),'chars':chars,'step':max_iters},'out/checkpoint.pt')\nPath('out/loss.json').write_text(json.dumps(history))\nprint('Training complete; checkpoint saved.')\n"
def md(t): return dict(cell_type='markdown',metadata={},source=t)
def code(t): return dict(cell_type='code',metadata={},source=t,outputs=[],execution_count=None)
cells=[md('# Shakespeare GPT on Runpod\nOriginal Karpathy lecture architecture and hyperparameters. Run cells with Shift+Enter. Training runs inside this notebook. Source: https://github.com/karpathy/ng-video-lecture'),
code("%cd /workspace/shakespeare-gpt\nimport torch\nprint(torch.__version__, torch.cuda.is_available())\nprint(torch.cuda.get_device_name(0))"),
md('## 1. Data and tokenizer\n90% training / 10% validation. Character-level tokens; context length 256.'),
code(a),code("print(len(text), 'characters;', vocab_size, 'symbols')\nprint(text[:300])"),
md('## 2. Model\n6 transformer layers, 6 attention heads, 384 embedding dimensions.'),
code(b),md('## 3. Train\n5,000 steps, batch size 64. Leave the pod and kernel running. Reports loss every 500 steps. Saves checkpoint after training. Exact results vary by hardware.'),
code(c),md('## 4. Learning curves'),
code("import matplotlib.pyplot as plt\nfor k in ['train','val']:\n    plt.plot([r['step'] for r in history],[r[k] for r in history],label=k)\nplt.xlabel('Step'); plt.ylabel('Cross entropy'); plt.legend(); plt.show()"),
md('## 5. Generate\nChange the prompt and rerun. This is a text completion model, not a chat assistant.'),
code("prompt='ROMEO:'\nmodel.eval()\nwith torch.no_grad():\n    context=torch.tensor([encode(prompt)],dtype=torch.long,device=device)\n    sample=decode(model.generate(context,max_new_tokens=1000)[0].tolist())\nprint(sample)\nPath('out/sample.txt').write_text(sample)"),
md('## Reload after a kernel restart\nRun data and model definitions first, then use the following optional cell instead of training. Workspace retention depends on Runpod volume settings.'),
code("# ckpt=torch.load('out/checkpoint.pt',map_location=device,weights_only=False)\n# model=GPTLanguageModel().to(device)\n# model.load_state_dict(ckpt['model'])\n# model.eval()")]
Path('Shakespeare_GPT.ipynb').write_text(json.dumps(dict(cells=cells,metadata={'kernelspec':{'display_name':'Python 3 (ipykernel)','language':'python','name':'python3'}},nbformat=4,nbformat_minor=5)))
print('Notebook created')

