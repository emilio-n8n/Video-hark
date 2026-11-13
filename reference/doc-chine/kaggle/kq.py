# tiny helper: push/poll/download Kaggle kernels via the kaggle-gateway client (proxy-managed auth)
import os, sys, json, time, pathlib
# [Video-hark] KGW_KAGGLE_AUTH=none seulement derrière le proxy Hark ; ailleurs : KAGGLE_USERNAME + KAGGLE_KEY ou ~/.kaggle/kaggle.json
os.environ.setdefault("KAGGLE_USERNAME", "emiliomoreau")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # [Video-hark] client kgw/kaggle_api.py copié ici (original : /workspace/work/kaggle-gateway)
from kgw.kaggle_api import KaggleAPI
api = KaggleAPI(os.environ["KAGGLE_USERNAME"])
def nb(cells, title):
    return {"cells": [{"cell_type": "markdown", "metadata": {}, "source": f"# {title}"}] +
            [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": c} for c in cells],
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"},
                         "kaggle": {"accelerator": "nvidiaTeslaT4", "isInternetEnabled": True, "isGpuEnabled": True}},
            "nbformat": 4, "nbformat_minor": 4}
def push(slug, title, cells): return api.push_kernel(slug, title, nb(cells, title), gpu=True, internet=True)
def status(slug): return api.kernel_status(slug.split("/")[-1])
def fetch(slug, dest, pattern=None):
    log, files = api.kernel_output(slug)
    d = pathlib.Path(dest); d.mkdir(parents=True, exist_ok=True)
    (d / "kernel.log").write_text(log)
    for f in files:
        n = f.get("fileName")
        if pattern and not any(p in n for p in pattern): continue
        api.download(f["url"], d / n)
    return log, [f.get("fileName") for f in files]
if __name__ == "__main__":
    cmd, slug = sys.argv[1], sys.argv[2]
    if cmd == "status": print(status(slug))
    elif cmd == "fetch":
        log, files = fetch(slug, sys.argv[3], sys.argv[4:] or None); print(log[-4000:]); print(files)
