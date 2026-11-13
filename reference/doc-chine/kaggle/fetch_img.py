import os, sys, json, pathlib
# [Video-hark] KGW_KAGGLE_AUTH=none seulement derrière le proxy Hark ; ailleurs : KAGGLE_USERNAME + KAGGLE_KEY ou ~/.kaggle/kaggle.json
os.environ.setdefault("KAGGLE_USERNAME", "emiliomoreau")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # [Video-hark] client kgw/kaggle_api.py copié ici (original : /workspace/work/kaggle-gateway)
from kgw.kaggle_api import KaggleAPI
api = KaggleAPI(os.environ["KAGGLE_USERNAME"])
slug=sys.argv[1] if len(sys.argv) > 1 else "doc-chine-qwen-image-2-1-prive"
dest=pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "out_img21"); tok=None; imgs=[]; pages=0
while True:
    p={"userName":api.username,"kernelSlug":slug,"pageSize":500}
    if tok: p["pageToken"]=tok
    d=api._req("GET","/kernels/output",params=p); pages+=1
    fs=d.get("files") or []
    for f in fs:
        n=f.get("fileName","")
        if n.startswith("img/") or "/img/" in n: imgs.append(f)
    tok=d.get("nextPageToken")
    print("page",pages,len(fs),"imgs so far",len(imgs),"next",bool(tok), flush=True)
    if not tok or pages>40: break
for f in imgs:
    n=f["fileName"]; out=dest/n[n.index("img/"):]
    if out.exists() and out.stat().st_size>0: continue
    api.download(f["url"], out); print("dl",n,flush=True)
