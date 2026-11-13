# tools/ — petits scripts du pipeline

Tous se lancent depuis `reference/doc-chine/` (ou depuis le dossier de ton nouveau film qui a la même structure).

| Script | Rôle | Statut |
|---|---|---|
| `rebuild_narration.py` | phrases TTS → `build/narration.wav` + `build/timeline.json` (0,6 s / 0,32 s / 2,5 s / 2,5 s) | reconstitué, **reproduit le film à l'échantillon près** |
| `cut_audio.py` | coupe un mot parasite dans une phrase TTS | reconstitué, **reproduit `p2_l09_fixed.wav` à l'échantillon près** |
| `whisper_check.sh` | transcrit chaque phrase avec whisper.cpp, vérifie les noms propres | reconstitué (commandes whisper.cpp standard) |
| `make_cues.py` | `captions_lines.json` + timeline → `render/cues.json` (sous-titres brûlés) | nouveau : mêmes règles, coupures pas identiques au film |
| `cues_to_srt.py` | cues → `.srt` (`--wrap 42` pour l'anglais) | reconstitué, reproduit `captions.srt` à l'identique, `captions_en.srt` au dernier saut de ligne près |
| `make_cues_en.py` | `en_lines.txt` + `cues.json` → `cues_en.json` | reconstitué, **identique** |
| `inpaint_green.py` | répare des taches vert chroma dans un décor | reconstitué, même méthode, résultat proche (pas au pixel) |
| `check_glyphs.py` | vérifie que les polices ont tous les caractères utilisés (« ≈ ») | nouveau |
| `render_plan.py` | découpe le rendu des segments en lots de < 100 s | nouveau |
| `assemble.sh` | `enc` (segments → 24 fps), `mux` (+ audio, faststart dans /tmp), `preview` (720p < 50 Mo) | reconstitué, mêmes réglages que le film |
| `make_still.py` | image fixe sans sous-titre (still festival) | reconstitué (écart moyen ~4/255 avec l'original : grain + JPEG) |
| `check_video.sh` | ffprobe + loudness + 12 images témoins | nouveau |

« Reconstitué » = le 27/10 ou le 11/11/2026 l'étape a été faite par des commandes tapées à la main, non sauvegardées ; le script refait la même chose. Les scripts « d'origine » (exécutés tels quels pour le film) sont dans `kaggle/` et `render/`.

Dépendances locales : `python3` (3.10+), `pip install numpy pillow soundfile opencv-python-headless fonttools httpx`, `ffmpeg`/`ffprobe` 6+ (le film : Lavf 61.7), whisper.cpp pour `whisper_check.sh`.
