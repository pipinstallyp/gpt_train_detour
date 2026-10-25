"""Ten fresh epochs of the TinyStories architecture on pinned Lily graph data."""
import collections
import hashlib
import json
import math
import os
from pathlib import Path
import random
import string
import time

import numpy as np
import torch
from torch.nn import functional as F

from logic import ANSWERS
from model import build_model


def train(root):
    root=Path(root);out=root/'out';out.mkdir(exist_ok=True)
    credentials=Path('/root/.config/lily-kg/credentials.json')
    if credentials.exists():
        values=json.loads(credentials.read_text())
        if values.get('WANDB_API_KEY'):os.environ['WANDB_API_KEY']=values['WANDB_API_KEY']
    os.environ['WANDB_BASE_URL']='https://api.wandb.ai'
    os.environ['WANDB_DIR']=str(root)
    import wandb

    torch.set_num_threads(4);torch.manual_seed(1337);random.seed(1337);np.random.seed(1337)
    device='cuda' if torch.cuda.is_available() else 'cpu'
    assert device=='cuda','This experiment expects the existing GPU pod.'
    chars='\n'+string.ascii_lowercase+string.ascii_uppercase+string.digits+string.punctuation+' '
    assert len(chars)==len(set(chars))==96
    stoi={c:i for i,c in enumerate(chars)}
    encode=lambda text:torch.tensor([stoi[c] for c in text],dtype=torch.long)
    manifest=json.loads((root/'dataset/manifest.json').read_text())
    source=json.loads((root/'hf_source.json').read_text())
    rows={name:[json.loads(line) for line in (root/'dataset'/(name+'.jsonl')).read_text().splitlines()] for name in manifest['splits']}
    tensors={name:[encode(row['text']) for row in records] for name,records in rows.items()}
    flat={name:torch.cat(tensors[name]) for name in ['train','validation']}
    model=build_model(len(chars),device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=3e-4)
    config={'epochs':10,'batch_size':64,'block_size':256,'n_layer':6,'n_head':6,'n_embd':384,'dropout':.2,
            'learning_rate':3e-4,'optimizer':'AdamW defaults','seed':1337,'vocab_size':len(chars),
            'parameters':sum(p.numel() for p in model.parameters()),'token_unit':'character',
            'targets_per_epoch':manifest['splits']['train']['record_targets'],'packing':'one complete scene per sequence, ignored right padding',
            'objective':'next-character cross entropy over the entire record; not answer-only loss',
            'curriculum':'fixed shuffled mixture; no curriculum or identity objective',**source}
    (out/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    run=wandb.init(entity='peepaclan',project='gpt_train_detour',name='lily-kg-v1-10epochs',job_type='train',
                   tags=['lily-kg','v1','10-epochs','from-scratch'],config=config,
                   settings=wandb.Settings(disable_git=True),save_code=False)
    run.define_metric('epoch');run.define_metric('loss/*',step_metric='epoch');run.define_metric('validation/*',step_metric='epoch')
    history=[];began=time.time();updates=0;best_loss=float('inf');best_epoch=0

    def batch(sequences,indices):
        width=max(len(sequences[i])-1 for i in indices)
        x=torch.zeros((len(indices),width),dtype=torch.long)
        y=torch.full_like(x,-100)
        for row,i in enumerate(indices):
            sequence=sequences[i];n=len(sequence)-1
            x[row,:n]=sequence[:-1];y[row,:n]=sequence[1:]
        return x.to(device),y.to(device)

    @torch.inference_mode()
    def record_loss(name):
        total=0.;count=0
        for start in range(0,len(tensors[name]),64):
            x,y=batch(tensors[name],list(range(start,min(start+64,len(tensors[name])))))
            logits,_=model(x)
            total+=F.cross_entropy(logits.reshape(-1,len(chars)),y.reshape(-1),reduction='sum').item()
            count+=(y!=-100).sum().item()
        assert count==manifest['splits'][name]['record_targets']
        return total/count

    @torch.inference_mode()
    def tiny_style_loss(name):
        # The original TinyStories protocol: 20 random batches of 64 x 256.
        data=flat[name];generator=torch.Generator().manual_seed(9001)
        losses=[]
        for _ in range(20):
            ix=torch.randint(len(data)-256,(64,),generator=generator)
            x=torch.stack([data[i:i+256] for i in ix]).to(device)
            y=torch.stack([data[i+1:i+257] for i in ix]).to(device)
            _,loss=model(x,y);losses.append(loss.item())
        return sum(losses)/len(losses)

    @torch.inference_mode()
    def answer_metrics(name,greedy=False):
        records=rows[name];predictions=[];free_predictions=[]
        initials=torch.tensor([stoi[a[0]] for a in ANSWERS],device=device)
        for start in range(0,len(records),64):
            part=records[start:start+64];seqs=[encode(r['prompt']) for r in part]
            width=max(map(len,seqs));x=torch.zeros((len(seqs),width),dtype=torch.long)
            for i,s in enumerate(seqs):x[i,:len(s)]=s
            logits,_=model(x.to(device));last=logits[torch.arange(len(seqs),device=device),torch.tensor([len(s)-1 for s in seqs],device=device)]
            choices=last[:,initials].argmax(dim=-1).tolist()
            predictions.extend(ANSWERS[i] for i in choices)
            if greedy:
                generated=['']*len(seqs);done=[False]*len(seqs)
                for step in range(16):
                    trimmed=[s[-256:] for s in seqs];width=max(map(len,trimmed))
                    x=torch.zeros((len(seqs),width),dtype=torch.long)
                    for i,s in enumerate(trimmed):x[i,:len(s)]=s
                    logits,_=model(x.to(device))
                    next_ids=logits[torch.arange(len(seqs),device=device),torch.tensor([len(s)-1 for s in trimmed],device=device)].argmax(dim=-1).tolist()
                    for i,nxt in enumerate(next_ids):
                        if done[i]:continue
                        char=chars[nxt]
                        if char in '.\n':done[i]=True
                        else:generated[i]+=char
                        seqs[i]=torch.cat([seqs[i],torch.tensor([nxt])])
                    if all(done):break
                free_predictions.extend(s.strip() for s in generated)
        gold=[r['answer'] for r in records]
        correct=sum(a==b for a,b in zip(gold,predictions));unknown_tp=sum(a==b=='Unknown' for a,b in zip(gold,predictions))
        per_task={}
        for task in sorted({r['task'] for r in records}):
            ids=[i for i,r in enumerate(records) if r['task']==task]
            per_task[task]=sum(gold[i]==predictions[i] for i in ids)/len(ids)
        result={'records':len(records),'label_accuracy':correct/len(records),'unknown_recall':unknown_tp/gold.count('Unknown'),
                'unknown_precision':unknown_tp/max(1,predictions.count('Unknown')),'per_task':per_task,
                'confusion':{a:{b:sum(g==a and p==b for g,p in zip(gold,predictions)) for b in ANSWERS} for a in ANSWERS}}
        if greedy:
            result['greedy_exact_answer_accuracy']=sum(g==p for g,p in zip(gold,free_predictions))/len(gold)
            (out/(name+'_predictions.json')).write_text(json.dumps([{'id':r['id'],'task':r['task'],'truth':g,'closed_label_prediction':p,'greedy_answer':f,'prompt':r['prompt']} for r,g,p,f in zip(records,gold,predictions,free_predictions)],indent=2)+'\n')
        return result

    def evaluate(epoch,training_mean=None):
        model.eval()
        vl=record_loss('validation');metric=answer_metrics('validation')
        row={'epoch':epoch,'updates':updates,'targets_seen':epoch*config['targets_per_epoch'],'seconds':time.time()-began,
             'train_record_loss':training_mean,'validation_record_loss':vl,
             'tiny_style_train_loss':tiny_style_loss('train'),'tiny_style_validation_loss':tiny_style_loss('validation'),
             'validation_label_accuracy':metric['label_accuracy'],'validation_unknown_recall':metric['unknown_recall'],
             'validation_per_task':metric['per_task']}
        history.append(row);(out/'history.json').write_text(json.dumps(history,indent=2)+'\n')
        run.log({'epoch':epoch,'updates':updates,'targets_seen':row['targets_seen'],'loss/validation_record':vl,
                 'loss/tiny_style_train':row['tiny_style_train_loss'],'loss/tiny_style_validation':row['tiny_style_validation_loss'],
                 'validation/label_accuracy':metric['label_accuracy'],'validation/unknown_recall':metric['unknown_recall'],
                 **{f'validation/task_{k}':v for k,v in metric['per_task'].items()}})
        print(json.dumps(row),flush=True)
        return vl

    def checkpoint(epoch,path):
        torch.save({'model':model.state_dict(),'optimizer':optimizer.state_dict(),'chars':chars,'config':config,
                    'epoch':epoch,'updates':updates,'source':source},path)

    try:
        evaluate(0)
        for epoch in range(1,11):
            model.train();order=torch.randperm(len(rows['train'])).tolist();covered=0;total=0.;count=0
            for start in range(0,len(order),64):
                x,y=batch(tensors['train'],order[start:start+64])
                _,loss=model(x,y)
                assert torch.isfinite(loss),'Nonfinite training loss'
                optimizer.zero_grad(set_to_none=True);loss.backward();optimizer.step()
                n=(y!=-100).sum().item();covered+=n;count+=n;total+=loss.item()*n;updates+=1
            assert covered==config['targets_per_epoch']
            vl=evaluate(epoch,total/count)
            checkpoint(epoch,out/'last.pt')
            if vl<best_loss:
                best_loss=vl;best_epoch=epoch;checkpoint(epoch,out/'best.pt')
        # Tests are first inspected after training and selection by validation loss.
        model.eval()
        last_metrics={name:answer_metrics(name,greedy=True) for name in ['validation','test_composition','test_paraphrase']}
        best=torch.load(out/'best.pt',map_location=device,weights_only=True)
        model.load_state_dict(best['model']);model.eval()
        best_metrics={name:answer_metrics(name,greedy=False) for name in ['validation','test_composition','test_paraphrase']}
        torch.save({'model':model.state_dict(),'chars':chars,'config':config,'epoch':best_epoch,'source':source},out/'best_weights.pt')
        summary={'completed_epochs':10,'updates':updates,'training_targets_seen':10*config['targets_per_epoch'],
                 'best_epoch_by_validation_loss':best_epoch,'best_validation_record_loss':best_loss,
                 'last':last_metrics,'best_by_validation_loss':best_metrics,'seconds':time.time()-began,
                 'wandb_url':run.url,'hf_dataset':source,'config':config,
                 'caveats':['Single seed; no curriculum comparison.','Unknown is explicitly supervised, not spontaneous abstention.',
                            'Composition test holds out endpoint pairs, not unseen algorithms.','Paraphrase test intentionally shares held-out validation graphs.',
                            'Closed-label accuracy uses equal-length first-character verbalizers Y/N/U; greedy exact accuracy is separate.',
                            'Losses on Lily and TinyStories are not directly comparable across corpora.']}
        (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        run.summary.update({'completed_epochs':10,'best_epoch':best_epoch,'best_validation_record_loss':best_loss,
                            **{f'last/{name}/label_accuracy':m['label_accuracy'] for name,m in last_metrics.items()},
                            **{f'last/{name}/greedy_exact_accuracy':m['greedy_exact_answer_accuracy'] for name,m in last_metrics.items()}})
        artifact=wandb.Artifact('lily-kg-v1-best-checkpoint',type='model',metadata={'selection':'best_validation_record_loss','epoch':best_epoch,**source})
        artifact.add_file(str(out/'best_weights.pt'));run.log_artifact(artifact,aliases=['release-v1','best'])
        result=wandb.Artifact('lily-kg-v1-evaluation',type='evaluation')
        for path in out.glob('*.json'):result.add_file(str(path))
        run.log_artifact(result,aliases=['release-v1'])
        run.finish()
        print(json.dumps(summary,indent=2),flush=True)
        return summary
    except BaseException:
        run.finish(exit_code=1)
        raise
