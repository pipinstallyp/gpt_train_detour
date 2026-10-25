"""Execute and persist the Lily notebook with a separate kernel."""
from pathlib import Path
import traceback
import nbformat
from nbclient import NotebookClient

root=Path(__file__).resolve().parent
for name in ['notebook_error.txt','notebook_complete.txt']:
    (root/name).unlink(missing_ok=True)
path=root/'Lily_KG.ipynb'
nb=nbformat.read(path,as_version=4)
def save(*args,**kwargs):
    nbformat.write(nb,path)
client=NotebookClient(nb,timeout=None,kernel_name='lily-kg',resources={'metadata':{'path':str(root)}},on_cell_executed=save)
try:
    client.execute()
    (root/'notebook_complete.txt').write_text('All notebook cells completed successfully.\n')
except BaseException:
    (root/'notebook_error.txt').write_text(traceback.format_exc())
    raise
finally:
    save()
