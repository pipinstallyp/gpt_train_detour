"""Publish only generated data and public source files, then fetch a pinned copy."""
from pathlib import Path
import hashlib
import json
import shutil


def publish_dataset(root):
    from huggingface_hub import HfApi, snapshot_download

    root=Path(root); generated=root/'generated'
    manifest=json.loads((generated/'manifest.json').read_text())
    for name in ['logic.py','generate.py','validate.py']:
        target=generated/'generation'/name;target.parent.mkdir(exist_ok=True)
        shutil.copyfile(root/name,target)
    shutil.copyfile(root/'world.json',generated/'generation/world.json')
    shutil.copyfile(root/'DATASET_CARD.md',generated/'README.md')
    shutil.copyfile(root/'LICENSE',generated/'LICENSE')
    api=HfApi();username=api.whoami()['name']
    assert username=='chewiesays',f'Unexpected HF account: {username}'
    repo_id=username+'/lily-kg-mini-v1'
    api.create_repo(repo_id=repo_id,repo_type='dataset',private=False,exist_ok=True)
    commit=api.upload_folder(repo_id=repo_id,repo_type='dataset',folder_path=generated,
                             allow_patterns=['*.jsonl','manifest.json','validation_report.json','world.json','README.md','LICENSE','generation/*'],
                             commit_message='Publish Lily KG v1: grounded counterbalanced scenes and held-out tests')
    revision=commit.oid
    api.create_tag(repo_id=repo_id,repo_type='dataset',tag='v1',revision=revision,exist_ok=True)
    snapshot=Path(snapshot_download(repo_id=repo_id,repo_type='dataset',revision=revision,
                      allow_patterns=['*.jsonl','manifest.json','validation_report.json','world.json','README.md','LICENSE']))
    (root/'dataset').mkdir(exist_ok=True)
    for path in snapshot.iterdir():
        if path.is_file():shutil.copyfile(path,root/'dataset'/path.name)
    for split,info in manifest['splits'].items():
        assert hashlib.sha256((root/'dataset'/(split+'.jsonl')).read_bytes()).hexdigest()==info['sha256']
    result={'repo_id':repo_id,'revision':revision,'url':f'https://huggingface.co/datasets/{repo_id}',
            'manifest_sha256':hashlib.sha256((root/'dataset/manifest.json').read_bytes()).hexdigest()}
    (root/'hf_source.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    return result
