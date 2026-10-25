"""Create the runnable Lily notebook in the original Runpod workspace."""
from pathlib import Path
import json


def build(root):
    root=Path(root);cells=[]
    def md(text):
        cells.append({'id':f'cell-{len(cells)}','cell_type':'markdown','metadata':{},'source':text.splitlines(keepends=True)})
    def code(text):
        cells.append({'id':f'cell-{len(cells)}','cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':text.splitlines(keepends=True)})
    md('# Lily KG: grounded pretraining, ten epochs\n\nA reproducible first experiment in Lily\'s toy world. We generate short scenes from explicit rules, verify the answers, publish the data to Hugging Face, download its pinned version, and train the TinyStories architecture from fresh random weights.\n\nThis is a fixed shuffled baseline. It does not test curriculum learning or identity.\n')
    code("from pathlib import Path\nimport sys, json, subprocess\nROOT = Path('/workspace/lily-kg')\nif str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))\nimport torch\nprint('PyTorch:', torch.__version__)\nprint('GPU:', torch.cuda.get_device_name(0))\n")
    md('## 1. Define the world\n\nObjects have at most one color and location in each independent scene. Reachability composes through a location. Heavier-than is transitive and asymmetric. Missing evidence produces **Unknown**, unless a declared rule supplies a negative conclusion. Reachability is not grasping.\n')
    code("world=json.loads((ROOT/'world.json').read_text())\nprint('Entities:', len(world['entities']), 'Seed facts:', len(world['seed_scene']))\nprint(json.dumps(world['entities'], indent=2))\nfor rule in world['rules']: print(rule['id']+': '+rule['rule'])\nprint('Seed facts:',json.dumps(world['seed_scene'][:8],indent=2))\n")
    md('## 2. Generate and validate\n\n24,000 training scenes; 1,200 validation scenes; 600 composition tests; 1,200 paired paraphrases. Every question is counterbalanced across Yes/No/Unknown. Composition holds out entity endpoint combinations while keeping their meanings familiar. All text fits within 256 characters.\n')
    code("result=subprocess.run([sys.executable,str(ROOT/'generate.py'),'--out',str(ROOT/'generated')],capture_output=True,text=True,check=True)\nprint(result.stdout)\nresult=subprocess.run([sys.executable,str(ROOT/'validate.py'),str(ROOT/'generated')],capture_output=True,text=True,check=True)\nprint(result.stdout)\nexamples=[json.loads(line) for line in (ROOT/'generated/validation.jsonl').read_text().splitlines()]\nfor example in examples[:6]: print(example['task']+'\\n'+example['text'])\n")
    md('## 3. Publish to Hugging Face and pin the training input\n\nCredentials come from the standard HF cache configured on the pod. No credential is stored in the notebook. We verify hashes after downloading the committed dataset. Re-running this cell republishes the deterministic source and data under the same repository.\n')
    code("from publish import publish_dataset\nhf_source=publish_dataset(ROOT)\n")
    md('## 4. Train from scratch for ten epochs\n\nSame six layers, six heads, width 384, context 256, batch 64, dropout 0.2, AdamW learning rate 3e-4, and seed 1337 as the TinyStories baseline. A declared 96-character ASCII alphabet covers unseen wording. Each full scene stays together; right padding has ignored loss.\n\nPrimary validation loss scores every held-out scene target. We also report the TinyStories-style estimate: 20 random batches of 64 x 256 character windows per split. Different corpora have different loss scales. Answer accuracy and Unknown recall are evaluated separately. Test sets are first inspected after epoch 10 and checkpoint selection.\n')
    code("from train import train\nsummary=train(ROOT)\n")
    md('## 5. Inspect the learning curve and final tests\n\nThe best checkpoint is selected using validation record loss. Final tests include closed-label accuracy using Y/N/U first-character scores and unconstrained greedy exact-answer accuracy. Chance is one-third. Unknown is explicitly taught; success is not evidence of spontaneous abstention.\n')
    code("import matplotlib.pyplot as plt\nhistory=json.loads((ROOT/'out/history.json').read_text())\nfig,axes=plt.subplots(1,2,figsize=(11,4))\naxes[0].plot([r['epoch'] for r in history],[r['tiny_style_train_loss'] for r in history],label='train: random windows')\naxes[0].plot([r['epoch'] for r in history],[r['tiny_style_validation_loss'] for r in history],label='validation: random windows')\naxes[0].plot([r['epoch'] for r in history],[r['validation_record_loss'] for r in history],label='validation: complete scenes')\naxes[0].set(xlabel='Epoch',ylabel='Cross entropy (nats/character)');axes[0].legend()\naxes[1].plot([r['epoch'] for r in history],[r['validation_label_accuracy'] for r in history],label='validation label accuracy')\naxes[1].axhline(1/3,color='gray',linestyle='--',label='chance')\naxes[1].set(xlabel='Epoch',ylabel='Accuracy',ylim=(0,1));axes[1].legend()\nfig.tight_layout();fig.savefig(ROOT/'out/learning_curves.png',dpi=160);plt.show()\nprint(json.dumps(summary['last'],indent=2))\nprint('W&B:',summary['wandb_url'])\n")
    code("predictions=json.loads((ROOT/'out/test_composition_predictions.json').read_text())\nfor example in predictions[:12]:\n    print(example['prompt']+example['greedy_answer'])\n    print('Expected:',example['truth'],'| Task:',example['task'],'\\n')\n")
    md('## Interpretation limits\n\nCompare composition accuracy with the reach/order subset of validation: the overall validation set includes two easier lookup tasks. The paraphrase templates introduce eleven unseen word forms, so this is a joint vocabulary and wording shift. Low full-text loss can be dominated by predictable templates; generated answer accuracy is the stronger capability check. A single fixed-mixture seed does not test curriculum benefits or identity.\n')
    nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'name':'lily-kg','language':'python','display_name':'Lily-KG'}},'cells':cells}
    path=root/'Lily_KG.ipynb';path.write_text(json.dumps(nb,indent=2)+'\n');print(path)


if __name__=='__main__':
    build(Path(__file__).resolve().parent)
