# Qwen-Image-2.1 (7B, Wan2GP) batch for doc-chine, based on Emilio's kernel emiliomoreau/qwen-image-2-1-7b-on-t4-x2 (loading code untouched)
import json, sys, os
sys.path.insert(0, '.')
import kq
from build_img_prompts import shots_with_prompts
nb = json.load(open('qi21_orig.ipynb'))
src = lambda i: nb['cells'][i]['source'] if isinstance(nb['cells'][i]['source'], str) else ''.join(nb['cells'][i]['source'])
c_env, c_inst, c_w, c_script = src(2), src(4), src(6), src(8)
c_w = c_w.replace('WEIGHTS = "/kaggle/working/weights"', 'WEIGHTS = "/kaggle/tmp/weights"')  # keep the 18.7 GB out of the 20 GB output disk
c_w = c_w.replace('st = os.statvfs("/kaggle/working")', 'os.makedirs("/kaggle/tmp", exist_ok=True); st = os.statvfs("/kaggle/tmp")')
assert 'if SMOKE:' in c_script
old_cast = """        for p in comp.parameters():
            if p.is_floating_point() and p.data.dtype != target:
                p.data = p.data.to(target)
                n_cast += 1"""
new_cast = """        n_q = 0
        for p in comp.parameters():
            if type(p.data) is not torch.Tensor:   # INT8 convrot / quanto weights: never cast (their dtype is locked)
                n_q += 1
                continue
            if p.is_floating_point() and p.data.dtype != target:
                p.data = p.data.to(target)
                n_cast += 1
        log(f"  {name}: {n_q} poids quantifies laisses tels quels")"""
assert old_cast in c_script, 'cast block not found'
c_script = c_script.replace(old_cast, new_cast)
old_prof = """except Exception:
    log("mmgp profile skipped:")
    traceback.print_exc()"""
new_prof = """except Exception:
    log("mmgp profile skipped:")
    traceback.print_exc()
    # a defaut : tout l'encodeur texte (embeddings compris) sur le meme device que les index
    try:
        components["text_encoder"].to("cuda:0"); log("text_encoder -> cuda:0 (fallback)")
    except Exception:
        traceback.print_exc()"""
assert old_prof in c_script, 'profile block not found'
c_script = c_script.replace(old_prof, new_prof)

batch = r'''
if "--batch" in sys.argv:
    import json as _json
    SHOTS = _json.load(open("/kaggle/working/shots21.json"))
    IMG = "/kaggle/working/img"; os.makedirs(IMG, exist_ok=True)
    ok = 0; tb = time.time()
    for i, s in enumerate(SHOTS):
        try:
            with torch.inference_mode():
                im = run_one(s["prompt"], steps=20, width=s["w"], height=s["h"], seed=s["seed"], guide=4.0,
                             negative="text, letters, words, numbers, logo, watermark, signature, blurry, low quality")
            im.convert("RGB").save(f"{IMG}/{s['name']}.png"); ok += 1
            log(f"IMG {i+1}/{len(SHOTS)} {s['name']} {s['w']}x{s['h']} total={time.time()-tb:.0f}s")
        except Exception:
            log("FAILED", s["name"]); traceback.print_exc()
            gc.collect(); torch.cuda.empty_cache()
    log("BATCH DONE", ok, "of", len(SHOTS))
    sys.exit(0)

'''
c_script = c_script.replace('if SMOKE:', batch + 'if SMOKE:', 1)
shots = shots_with_prompts()
# [Video-hark] ajouts facultatifs (comportement par défaut inchangé) : sous-ensemble de plans en arguments,
# nom/titre du notebook par variables d'environnement -> permet de couper un gros lot en 2 notebooks (limite Kaggle 12 h).
only = sys.argv[1:]
if only: shots = [s for s in shots if s['name'] in only]
SLUG = os.environ.get('IMG_SLUG', 'doc-chine-qwen-image-2-1-prive'); TITLE = os.environ.get('IMG_TITLE', 'doc-chine Qwen-Image-2.1 (prive)')
c_shots = "import json\njson.dump(json.loads(%r), open('/kaggle/working/shots21.json', 'w'), ensure_ascii=False)\nprint('shots', %d)" % (json.dumps(shots, ensure_ascii=False), len(shots))
c_run = "!python -u run_qwen_image.py --batch\nimport os; print('images:', len(os.listdir('/kaggle/working/img')) if os.path.isdir('/kaggle/working/img') else 0)"
print(kq.push(SLUG, TITLE, [c_env, c_inst, c_w, c_shots, c_script, c_run]))
