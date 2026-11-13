# 12 — Dépannage : tous les problèmes rencontrés (symptôme → cause → solution)

Règle : **2 essais de correction maximum par problème**, puis rapport à l'utilisateur (erreur exacte, essais faits, 20 dernières lignes du log, proposition).

## Environnement / machine

| Symptôme | Cause | Solution |
|---|---|---|
| `chrome-headless-shell: error while loading shared libraries: libatk-1.0.so.0` à l'installation du moteur `short-editing` | bibliothèques système absentes, pas de droits root | télécharger les `.deb` manquants, les extraire (`dpkg -x x.deb libs/root`) et `export LD_LIBRARY_PATH=$PWD/libs/root/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH` (voir `reference/doc-chine/env.sh.original`). Inutile pour ce pipeline : le rendu n'utilise pas Chrome. |
| Une commande est coupée au bout de 120 s | limite du bac à sable Hark | découper : `render_plan.py` (rendu par lots), `assemble.sh enc` (encodage par segments), `assemble.sh preview` (en 2 moitiés, reprend où il s'est arrêté) |
| `Unable to re-open … for shifting data` à la fin d'un ffmpeg avec `-movflags +faststart` | le système de fichiers `/workspace` (JuiceFS) ne permet pas la réécriture en place | écrire dans `/tmp/…mp4`, puis `cp` |
| Une commande de surveillance renvoie exactement la même sortie qu'avant | sortie en cache | modifier légèrement la commande (`; date`, autre ordre d'options) |
| `ModuleNotFoundError: numpy / soundfile / cv2 / fontTools / httpx` | dépendances Python | `pip install numpy pillow soundfile opencv-python-headless fonttools httpx` |

## Kaggle

| Symptôme | Cause | Solution |
|---|---|---|
| `Kaggle refuse l'authentification (401/403)` | token absent ou faux | `KAGGLE_USERNAME` + `KAGGLE_KEY`, ou `~/.kaggle/kaggle.json` ; `KGW_KAGGLE_AUTH=none` **seulement** derrière le proxy Hark |
| `status` → introuvable alors que `push` a réussi | Kaggle dérive l'identifiant du **titre** (`doc-chine TTS Qwen3 (prive)` → `doc-chine-tts-qwen3-prive`) | utiliser l'identifiant dérivé du titre ; `kq.py` envoie le slug nu (sans `user/`) |
| Statut `error` sans message | — | `python3 kq.py fetch <slug> <dossier> __rien__` puis lire `kernel.log` (chercher `Traceback`) |
| `running` pendant des heures, aucune sortie visible | normal : log et fichiers ne sont lisibles qu'à la fin | attendre ; vérifier toutes les 30-60 min ; ne pas relancer |
| La session s'arrête à 12 h | limite Kaggle | estimer la durée (étape 07) ; couper en 2 notebooks au-delà de ~11 h |
| `complete` mais les fichiers attendus ne sont pas dans la liste | liste paginée par 500 ; dossier cloné (`Wan2GP/`) en tête | `fetch_img.py` (suit `nextPageToken`) ; film : images en page 7/7 |
| Disque de sortie plein (20 Go) | gros poids téléchargés dans `/kaggle/working` | télécharger les poids dans `/kaggle/tmp` |
| `pip` coupé (read timeout), module absent ensuite | réseau | boucle d'essais `--timeout 120 --retries 8` + `assert importlib.util.find_spec(...)` |
| Import diffusers cassé (`FqnToConfig`) | `torchao` préinstallé incompatible | `pip uninstall -y torchao` |
| `AttributeError: 'NoneType' object has no attribute 'cpu'` (Qwen-Image 20B) | masque de prompt `None` | tester `None` avant `.cpu()` |
| `ValueError: The dtype of a weights Tensor cannot be changed` (Wan2GP, INT8 convrot) | conversion fp16 appliquée aux poids quantifiés | ignorer les poids dont `type(p.data) is not torch.Tensor` |
| `AssertionError` dans `mmgp … _configure` (`assert model_dtype == dtype`) → `mmgp profile skipped` | conséquence de la conversion partielle ci-dessus | même correction ; repli `text_encoder.to("cuda:0")` |
| `RuntimeError: Expected all tensors to be on the same device … index_select` | encodeur texte resté sur CPU (profil non appliqué) | idem ; vérifier `mmgp profile applied` dans le log |
| Image noire / uniforme (Qwen-Image 20B, fp16) | débordement fp16 | le script 20B repasse en fp32 si moyenne < 4 ou écart-type < 2 |

## Voix

| Symptôme | Cause | Solution |
|---|---|---|
| Beaucoup de phrases « bad » dans `qa.json` | Whisper écrit les nombres en chiffres | faux positifs : transcrire en local et lire (étape 04) |
| Mot en trop (« 74 **de** technologies ») | hallucination courte du TTS | `tools/cut_audio.py` (coupe franche dans le silence), re-vérifier |
| Sigle mal lu (BYD, R1) | lettres lues comme un mot | réécriture phonétique dans `build_tts.py` (`B-Y-D`, `R-1`) |
| Nombre mal dit | chiffres dans le texte | écrire les nombres en lettres dans `paras.json` |
| La vidéo et le son se décalent après une correction | `timeline.json` modifié sans tout relancer | `rebuild_narration.py` → `audio.py` → rendu complet |

## Images

| Symptôme | Cause | Solution |
|---|---|---|
| Taches vert vif dans un décor | feuillage raté confondu avec le vert chroma | `tools/inpaint_green.py` (original dans `images/orig/`) ou régénérer (seed + 100) |
| Décor presque vide | prompt trop abstrait (« faint traces ») | garder comme fond si des éléments le couvrent ; sinon décrire des formes grosses et contrastées |
| Frange verte autour d'une découpe | fond pas assez uni | régénérer ; le détourage (`vx.cutout`) gère un vert franc (G − max(R,B) > 58) |
| Objet vert disparu au détourage | objet vert dans une découpe | ne jamais demander un objet vert en découpe |
| Texte ou logo dans une image | le modèle a écrit | régénérer ; renforcer « no lettering » dans le subject |
| Image régénérée non prise en compte | cache `render/layers/` | supprimer `render/layers/<name>.png` |

## Montage / rendu

| Symptôme | Cause | Solution |
|---|---|---|
| Élément caché par les sous-titres | placé sous y ≈ 900 | remonter (film : compteurs de l'accroche à y 300 / 590 / 800 ; ch.5 +40 px vers le haut) |
| Carré vide à la place d'un caractère | glyphe absent (« ≈ » dans Instrument Serif) | `tools/check_glyphs.py` ; changer de texte ou de police |
| Valeur d'une barre coupée | `vmax` trop petit | `vmax` ≈ 1,3 × valeur max (film : 2,95 pour 2,26) |
| Sous-titre coupé dans un nombre (« 295 » / « 000 ») | découpe naïve des cues | `tools/make_cues.py` (colle les nombres et leurs unités) |
| Durée du MP4 ≠ durée de la timeline | segments manquants ou mauvais `-shortest` | compter les segments ; `assemble.sh mux` vérifie le nombre |

## Faits et droits

| Symptôme | Cause | Solution |
|---|---|---|
| Un fait du film est devenu faux (record 57:20 battu le 23/08/2026) | le monde a bougé après l'écriture | revérifier les faits datés juste avant publication ; dater à l'écran ; **DEMANDER** avant de corriger |
| L'utilisateur veut cacher l'origine IA des images | — | refuser poliment ; mention « images générées par IA, voix de synthèse » ; voir `LICENSE-NOTES.md` |
| Licence d'un modèle non commerciale | ex. Qwen-Image 2.1 = qwen-research | l'indiquer à l'utilisateur une fois ; il décide ; noter sa décision dans `PROGRESS.md` |

## Publication sur GitHub (ce dépôt)

| Symptôme | Cause | Solution |
|---|---|---|
| `remote: error: … exceeds GitHub's file size limit of 100.00 MB` | gros MP4 | ne pas committer les MP4 finaux : les mettre en **assets de release** ; pas de Git LFS |
| Avertissement > 50 Mo | gros WAV | convertir en FLAC (film : `mix.wav` 71 Mo → `mix.flac` 25 Mo) |
| `git push` vers github.com refusé (401) alors que l'API marche | dans le bac à sable Hark, le jeton n'est injecté que sur `api.github.com` / `uploads.github.com` | pousser par l'API Git Data (blobs → trees → commits → ref) ; c'est ce qui a été fait pour ce dépôt |
| `POST /git/blobs` → 422 « input was too large » | limite de taille de l'API blobs (échec dès ~18 Mo) | créer le fichier par l'API Contents (`PUT /contents/…` sur une branche temporaire : marche jusqu'à ~25 Mo), puis réutiliser son SHA ; au-delà (~45 Mo refusé) → asset de release |
