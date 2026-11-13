# 07 — Générer les 34 images : Qwen-Image 2.1 (7B) via Wan2GP sur Kaggle T4×2

Scripts d'origine : `reference/doc-chine/kaggle/build_img21.py` (construit et pousse le notebook), `build_img_prompts.py` (assemble les prompts),
`qi21_orig.ipynb` (le notebook Kaggle d'Emilio « Qwen-Image-2.1 7B on T4 x2 », repris **tel quel**), `fetch_img.py` (récupère les images), `kq.py` (statut/log).
Journaux réels : `reference/doc-chine/kaggle/logs/`.

> Licence : Qwen-Image 2.1 est sous licence **qwen-research** (voir `LICENSE-NOTES.md`). L'utilisateur du film l'a choisie en connaissance de cause.
> Pour un nouveau projet, **DEMANDER** une fois à l'utilisateur s'il garde ce modèle ; ne jamais maquiller l'origine des images.

## Entrées
- `kaggle/shots.json` validé (étape 06), token Kaggle, quota GPU Kaggle suffisant (~11 h pour 34 images).

## Ce que fait le notebook (6 cellules)

| # | Cellule | Contenu |
|---|---|---|
| 1 | environnement | RAM, `nvidia-smi` (doit montrer **2 × Tesla T4, 15360 MiB**), variables `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` |
| 2 | installation | `git clone --depth 1 https://github.com/DeepBeepMeep/Wan2GP.git` + `pip install -r Wan2GP/requirements.txt` + `mmgp gradio huggingface_hub` |
| 3 | poids (~18,7 Go) | `DeepBeepMeep/Qwen_image_2` : `qwen_image_21_7B_int8_convrot.safetensors`, VAE et configs ; `DeepBeepMeep/Ideogram4` : encodeur texte `Qwen3-VL-8B-Instruct` INT8 + vision bf16 + tokenizer. **Modifié** : poids dans `/kaggle/tmp/weights` (et pas `/kaggle/working`, sinon ils remplissent les 20 Go de sortie du notebook). |
| 4 | `shots21.json` | les prompts finaux écrits dans `/kaggle/working/shots21.json` |
| 5 | `run_qwen_image.py` | le script d'Emilio (chargement Wan2GP, correctifs T4, profil mémoire mmgp, pré-test) + **2 corrections** + le mode `--batch` |
| 6 | lancement | `!python -u run_qwen_image.py --batch` puis affiche `images: N` |

Mode `--batch` : pour chaque plan, `run_one(prompt, steps=20, width, height, seed, guide=4.0, negative="text, letters, words, numbers, logo, watermark, signature, blurry, low quality")`,
sauve `/kaggle/working/img/<name>.png`, écrit `IMG i/N name WxH total=…s` ; une erreur sur un plan n'arrête pas les suivants ; à la fin `BATCH DONE ok of N`.

**Les 2 seules corrections apportées au notebook d'Emilio** (dans `build_img21.py`, par remplacement de texte vérifié par `assert`) :
1. Dans `_fix_dtypes_for_t4` : ne **jamais** convertir un poids quantifié — `if type(p.data) is not torch.Tensor: continue` (les poids INT8 « convrot » refusent tout changement de type).
2. Si le profil mmgp échoue quand même : `components["text_encoder"].to("cuda:0")` (l'encodeur ne doit pas rester sur CPU).

## Temps de calcul réels (T4×2, 20 étapes) — À LIRE AVANT DE LANCER

| Taille | Secondes par image | | Taille | Secondes par image |
|---|---|---|---|---|
| 1664×928 (décor) | ~1 360 | | 1024×1024 | ~810 |
| 1664×832 | ~1 190 | | 832×1248 | ~875 |
| 1472×832 | ~1 030 | | 1664×640 | ~880 |

Pré-test (1 image 1024×1024) : ~806 s. Chargement du modèle : ~48 s. **34 images du film : 37 081 s = 10 h 18 min** de lot.
**Kaggle coupe une session GPU à 12 h.** Calcule ton lot avant de lancer :

```bash
cd kaggle && python3 -c "
import json; T={(1664,928):1360,(1664,832):1190,(1472,832):1030,(1024,1024):810,(832,1248):875,(1664,640):880}
s=json.load(open('shots.json')); t=sum(T.get((x['w'],x['h']),1400) for x in s)+806+1800
print(len(s),'images, estimation', round(t/3600,1),'h  ->', 'OK' if t<11*3600 else 'TROP LONG : couper en 2 notebooks')"
```
Couper en 2 : `IMG_SLUG=<slug>-img-a IMG_TITLE="<slug> img a" python3 build_img21.py <noms des plans du lot A…>` puis pareil pour le lot B
(les deux notebooks tournent l'un après l'autre ou en parallèle si ton quota le permet).

## Actions

```bash
cd films/<slug>/kaggle
export KAGGLE_USERNAME=<ton_nom_kaggle>                 # + KAGGLE_KEY ou ~/.kaggle/kaggle.json
IMG_SLUG=<slug>-qwen-image-2-1-prive IMG_TITLE="<slug> Qwen-Image-2.1 (prive)" python3 build_img21.py
```
Le nom réel du notebook = la version « slug » du titre : `<slug>-qwen-image-2-1-prive` (choisis titre et slug cohérents, voir étape 04).

**Surveiller** (toutes les 30 à 60 min, pas plus ; c'est long) :
```bash
python3 kq.py status <slug>-qwen-image-2-1-prive          # ('queued'|'running'|'complete'|'error', message)
```
Pendant `running`, l'API ne montre **ni log ni fichier** : c'est normal. N'en conclus rien avant la fin.

**Quand c'est `complete`** :
```bash
python3 kq.py fetch <slug>-qwen-image-2-1-prive ../out_img __rien__   # ne télécharge que kernel.log (le motif ne correspond à aucun fichier)
grep -a -E "PRE-FLIGHT|mmgp profile|IMG [0-9]+/|BATCH DONE|FAILED|Traceback" ../out_img/kernel.log | tail -50
python3 fetch_img.py <slug>-qwen-image-2-1-prive ../out_img         # pagination : parcourt TOUTES les pages de la sortie
mkdir -p ../images && cp ../out_img/img/*.png ../images/ && ls ../images | wc -l
```
`fetch_img.py` affiche `page 1 500 imgs so far 0 next True` … film : les images étaient en **page 7 sur 7**.

**Regarde chaque image** (règle 2) : ouvre les 34 PNG une par une et note dans `PROGRESS.md` pour chacune : OK / défaut (lequel).
Planche contact pour aller plus vite (puis zoome sur chaque image douteuse) :
```bash
python3 - <<'EOF'
from PIL import Image; import glob, math
f=sorted(glob.glob('../images/*.png')); W=6; th=[Image.open(p).convert('RGB') for p in f]
for t in th: t.thumbnail((320,320))
sheet=Image.new('RGB',(W*330, math.ceil(len(f)/W)*330),(40,40,40))
for i,t in enumerate(th): sheet.paste(t,((i%W)*330+5,(i//W)*330+5))
sheet.save('/tmp/planche.jpg', quality=85); print(len(f),'images -> /tmp/planche.jpg')
EOF
```

## Sorties
`images/<name>.png` × 34 (mêmes noms que `shots.json`), `out_img/kernel.log`.

## Contrôles
- STOP si le log ne contient pas `mmgp profile applied` et `PRE-FLIGHT OK`.
- STOP si `BATCH DONE n of N` avec n < N : regarde `FAILED <name>` dans le log, régénère seulement ces plans (2e notebook avec leurs noms en arguments).
- STOP si une **découpe** n'a pas un fond vert uni (le détourage échouera) ; si un **décor** a du texte, une marque, une tache vert vif, un visage déformé au premier plan.
- Décision par image défectueuse : (a) défaut petit ou caché par les découpes → garder ; (b) taches vertes dans un décor → `tools/inpaint_green.py` (étape 09) ; (c) sinon → régénérer avec seed + 100 (au plus 2 fois, règle 7).

## Problèmes rencontrés et solutions (dans l'ordre où ils sont arrivés)

### Avec Qwen-Image 20B (premier choix, abandonné) — `kaggle/build_img.py`
| Version | Erreur exacte | Cause | Correction |
|---|---|---|---|
| v1 | `AttributeError: 'NoneType' object has no attribute 'cpu'` (`EMB[...] = (pe.float().cpu(), pm.cpu())`) | `encode_prompt` renvoie un masque `None` | `None if pm is None else pm.cpu()` |
| v2 | import de diffusers impossible (`FqnToConfig` de `torchao`) | `torchao` préinstallé sur Kaggle incompatible | `pip uninstall -y torchao` |
| v3 | `pip` coupé (read timeout), `bitsandbytes` absent | réseau Kaggle | boucle de 4 essais `--timeout 120 --retries 8` + `assert` des modules |
| v4 | resté en file d'attente | — | remplacé par une v5 « vide » sur CPU quand on a changé de modèle |

### Avec Qwen-Image 2.1 (Wan2GP) — `kaggle/build_img21.py`
| Tentative | Erreur exacte (voir `logs/qwen-image-2-1-v1_kernel.log`) | Cause | Correction |
|---|---|---|---|
| 1 | `ValueError: The dtype of a weights Tensor cannot be changed` (dans `_fix_dtypes_for_t4`), puis `AssertionError` (`assert model_dtype == dtype`, mmgp `_configure`) → `mmgp profile skipped`, puis `RuntimeError: Expected all tensors to be on the same device, but got index is on cuda:0, different from other tensors on cpu (… index_select)` → `PRE-FLIGHT FAILED` | la conversion fp16 essayait aussi de convertir les poids INT8 ; conversion partielle → le profil mémoire refuse de s'appliquer → l'encodeur texte reste sur CPU | ignorer les poids quantifiés dans la conversion + repli `text_encoder.to("cuda:0")` |
| 2 | aucune : `mmgp profile applied`, `PRE-FLIGHT OK`, `BATCH DONE 34 of 34` | — | — |

### Récupération des sorties
| Symptôme | Cause | Solution |
|---|---|---|
| `complete` + « images: 34 » dans le log, mais aucun `img/*.png` dans la liste des fichiers | l'API liste les sorties par pages de **500** ; le dossier `Wan2GP/` cloné dans `/kaggle/working` remplit les pages 1 à 6 | `fetch_img.py` suit `nextPageToken` jusqu'à la dernière page |
| `ModuleNotFoundError: httpx` | dépendance du client | `pip install httpx` |
| Le statut reste `running` pendant des heures sans rien montrer | normal : rien n'est visible avant la fin | attendre ; ne pas relancer (un 2e notebook consommerait le quota en double) |
| Disque de sortie plein | 18,7 Go de poids dans `/kaggle/working` (limite 20 Go) | poids dans `/kaggle/tmp` |

Note : la vérification d'espace disque du notebook affiche `poids requis : 0.0 Go` (la taille n'est pas lue sur Hugging Face) ; elle ne protège donc de rien. Ce n'est pas bloquant.

**Règle de boucle** : après 2 tentatives ratées sur la même erreur, tu t'arrêtes et tu rapportes (erreur, 2 corrections tentées, fin du log). C'est ce qui a été fait pour le film (« si la tentative 2 échoue → rapport, pas de 3e essai »).
