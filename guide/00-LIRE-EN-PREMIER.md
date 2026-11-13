# 00 — LIS CECI EN PREMIER (règles absolues)

Tu es un modèle d'IA chargé de fabriquer un **mini-documentaire YouTube de 5 à 7 minutes, en français, en 16:9 1080p**, avec :
une voix off de synthèse, 34 images générées par IA dans un style « collage papier façon Vox », un montage animé en Python
(stop-motion 12 images/s), des sous-titres incrustés, une musique par chapitre, quelques bruitages, un son à -14 LUFS.

La référence à égaler est le film **« La Chine ne copie plus »** (6 min 12 s). Tout son code, ses fichiers et ses résultats
sont dans `reference/doc-chine/`. Tu vas refaire **exactement le même procédé** sur un nouveau sujet.

## Comment utiliser ce guide

1. Lis ce fichier en entier. Puis lis `12-depannage.md` en entier (tu y reviendras à chaque erreur).
2. Fais les étapes **dans l'ordre** : 01 → 02 → … → 11, puis coche `13-checklist-finale.md`.
3. Chaque étape a : **Entrées** (ce qu'il te faut), **Actions** (commandes exactes), **Sorties** (fichiers attendus),
   **Contrôles** (avec des lignes « STOP si … »), **Problèmes rencontrés et solutions**.
4. Une étape n'est finie que quand **tous ses contrôles passent**. Sinon tu ne passes pas à la suivante.

## Les 12 règles (aucune exception)

1. **Ne saute jamais un contrôle.** « STOP si … » veut dire : tu t'arrêtes, tu corriges, tu refais le contrôle.
2. **Regarde chaque image** que tu génères ou rends (ouvre le fichier et décris ce que tu vois). Un fichier qui existe n'est pas une preuve qu'il est bon. Dans le film de référence, 2 images sur 34 avaient un défaut visible (taches vertes, décor vide) : tu ne les aurais pas vues sans regarder.
3. **N'invente aucun fait.** Chaque chiffre, date, nom et citation du script vient d'une source que tu as ouverte (pas un extrait de moteur de recherche). Pas de source = la phrase sort du script.
4. **Cite tes sources** : `output/sources.md` liste chaque fait avec son URL. Elles vont dans la description YouTube.
5. **Ne copie pas** la vidéo d'inspiration : reprends des thèmes, jamais des phrases, ni sa structure exacte, ni ses sponsors.
6. **Pose à l'utilisateur seulement les questions listées** dans `01-cadrage-et-sujet.md` (et celles marquées « DEMANDER » ailleurs). Pour tout le reste, applique les règles de ce guide.
7. **Ne boucle jamais plus de 2 fois sur la même erreur.** Deux essais de correction ratés sur le même problème = tu t'arrêtes et tu fais un rapport (erreur exacte, les 2 corrections tentées, les 20 dernières lignes du log, ce que tu proposes).
8. **Ne change pas ce qui marche.** Si l'utilisateur fournit son propre notebook / outil qui marche chez lui, tu le reprends tel quel et tu ne corriges que la ligne qui plante dans **ton** test.
9. **Garde les originaux.** Avant de retoucher une image, une phrase audio ou un fichier : copie l'original dans un dossier `orig/`.
10. **Écris tes notes de reprise** dans `PROGRESS.md` à chaque fin d'étape (ce qui est fait, ce qui reste, les pièges vus). Un autre modèle doit pouvoir reprendre ton travail.
11. **Ne mens pas sur les droits.** N'écris jamais qu'une image IA « vient de Google » ou d'ailleurs. Écris la vérité : « images générées par IA, voix de synthèse » (voir `LICENSE-NOTES.md`).
12. **Ne publie, n'envoie et ne dépose rien** (YouTube, festival, e-mail) sans l'accord explicite de l'utilisateur sur la version finale.

## Ce dont tu as besoin (vérifie avant de commencer)

| Besoin | Comment vérifier | Si absent |
|---|---|---|
| Un compte Kaggle avec GPU (T4) et son token API | `python3 -c "import os;print(os.environ.get('KAGGLE_USERNAME'))"` ou `~/.kaggle/kaggle.json` | DEMANDER à l'utilisateur de créer un token (kaggle.com → Settings → API → Create New Token) et de le mettre dans `~/.kaggle/kaggle.json`. Ne jamais l'écrire dans un fichier du dépôt. |
| Python 3.10+ avec `numpy pillow soundfile opencv-python-headless fonttools httpx` | `python3 -c "import numpy,PIL,soundfile,cv2,fontTools,httpx"` | `pip install numpy pillow soundfile opencv-python-headless fonttools httpx` |
| ffmpeg + ffprobe | `ffmpeg -version` | installer (`apt install ffmpeg`, `brew install ffmpeg`, `winget install Gyan.FFmpeg`) |
| whisper.cpp + modèle `ggml-large-v3-turbo-q5_0.bin` | `$WHISPER_CLI -h` | voir `04-voix-tts.md` § Installation |
| Les polices, musiques et bruitages | `ls third_party/video-agent-skills/{fonts,music,sfx}` | déjà dans ce dépôt |

## Carte des étapes (et durées réelles du film de référence)

| Étape | Fichier | Durée réelle |
|---|---|---|
| Cadrage | `01-cadrage-et-sujet.md` | 5 min |
| Recherche + vérification des faits | `02-recherche-et-verification-des-faits.md` | 30-60 min |
| Script | `03-ecriture-du-script.md` | 30 min |
| Voix (Kaggle) | `04-voix-tts.md` | 30-90 min de GPU (non chronométré) + 20 min de contrôle |
| Mixage audio | `05-montage-audio.md` | 10 min |
| Direction artistique + 34 prompts | `06-direction-artistique.md` | 30 min |
| Images (Kaggle) | `07-generation-images-kaggle.md` | **~10 h 30 de GPU** (lance-le tôt !) |
| Rendu vidéo | `08-rendu-video.md` | ~6 min de rendu + ~11 min d'encodage |
| Contrôle qualité | `09-controle-qualite.md` | 20 min |
| Miniature + publication | `10-miniature-et-publication-youtube.md` | 15 min |
| Version festival | `11-version-festival.md` | 40 min |

**Ordre conseillé pour gagner du temps** : dès que le script est validé (étape 03), lance **en même temps** la voix (04) et les images (07) sur Kaggle. Pendant que les images tournent (~10 h), fais 05, 06-bis (plan des scènes), et prépare le rendu avec des images provisoires.

## Arborescence d'un nouveau film

Copie la référence et travaille dans la copie :

```bash
cp -r reference/doc-chine films/<slug-du-film>      # ex. films/doc-inde
cd films/<slug-du-film>
rm -f images/*.png images/orig/*.png tts/lines/*.wav tts/cands/*.wav build/*.wav build/*.flac output/* waiff/*
```

Les chemins vers `third_party/` (polices, musiques) fonctionnent tant que ton film est à 2 niveaux sous la racine du dépôt
(`films/<slug>/` ou `reference/<slug>/`). Sinon exporte `VX_FONTS=<chemin>/third_party/video-agent-skills/fonts` et
`VX_ASSETS=<chemin>/third_party/video-agent-skills`.

| Dossier | Contenu |
|---|---|
| `script/` | `script.md` (script lisible + notes visuelles), `paras.json` (texte lu par la voix, par chapitre) |
| `kaggle/` | scripts qui fabriquent et poussent les notebooks Kaggle, `shots.json` (34 plans), client API |
| `tts/` | sorties de la voix : `lines/<id>.wav`, `qa.json`, `cands/` |
| `build/` | `narration.wav`, `timeline.json`, `mix.wav`, phrases corrigées `<id>_fixed.wav` |
| `images/` | les 34 PNG (+ `orig/` pour les originaux retouchés) ; `render/img` est un lien vers `../images` |
| `render/` | moteur (`vx.py`), plan des scènes (`scenes.py`), rendu (`render.py`), mixage (`audio.py`), miniature (`thumb.py`), sous-titres |
| `output/` | MP4 final, aperçu, miniature, `.srt`, `post.md`, `sources.md` |
| `waiff/` (ou `festival/`) | version sous-titrée anglais et dossier festival |
| `tools/` | petits scripts (voir `tools/README.md`) |
