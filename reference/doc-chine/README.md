# Référence : « La Chine ne copie plus » (doc YouTube FR, 6 min 12)

Tout ce qui a servi à fabriquer le film, tel quel (sauf les ajouts marqués `[Video-hark]` dans le code : chemins relatifs, nom de notebook paramétrable).
Chronologie complète des décisions et des problèmes : `CHRONOLOGIE.md`. Notes de reprise d'origine : `PROGRESS.md`.

| Dossier / fichier | Contenu |
|---|---|
| `script/script.md` | accroches notées, script parlé (nombres en lettres), notes visuelles, résultat humanize |
| `script/paras.json` | texte lu par la voix, 6 parties, 65 phrases |
| `kaggle/build_tts.py` | notebook voix (Qwen3-TTS VoiceDesign → Base, QA Whisper) |
| `kaggle/build_img21.py` + `build_img_prompts.py` + `qi21_orig.ipynb` | notebook images Qwen-Image 2.1 / Wan2GP (celui utilisé) |
| `kaggle/build_img.py` | notebook Qwen-Image 20B (abandonné après 4 versions, gardé pour l'historique) |
| `kaggle/kq.py`, `kaggle/fetch_img.py`, `kaggle/kgw/kaggle_api.py` | client API Kaggle : push / status / fetch / pagination |
| `kaggle/shots.json`, `kaggle/tts_lines.json` | 34 plans ; 65 phrases envoyées au TTS |
| `kaggle/logs/` | journaux réels des notebooks (TTS ; 20B v1 ; Qwen-Image 2.1 tentative 1 en échec ; tentative 2 réussie) |
| `tts/` | sorties TTS : 65 phrases `lines/*.wav`, 5 voix candidates `cands/`, `qa.json`, `cands.json` |
| `build/` | `narration.wav` (371,6 s), `timeline.json`, `p2_l09_fixed.wav`, `thud.wav`, `mix.flac` (= `mix.wav` en FLAC ; le WAV 71 Mo est dans la release) |
| `images/` | les 34 images Qwen-Image 2.1 (14 décors + 20 découpes) ; `orig/plate-race.png` = avant retouche |
| `render/` | `vx.py` moteur, `scenes.py` 24 scènes, `render.py`, `audio.py` mix, `thumb.py` miniature, sous-titres FR/EN (`cues*.json`, `captions_lines.json`, `en_lines.txt`, `captions.srt`) ; `render/img` → `../images` |
| `tools/` | petits scripts (voir `tools/README.md`) |
| `qc-stills/` | 20 images de contrôle du montage (réduites à 960×540) |
| `output/` | `preview-540p.mp4` (960×540, 20,6 Mo, réencodé pour le dépôt), `thumbnail.png`, `captions.srt`, `post.md`, `sources.md` ; l'aperçu 720p d'origine `preview.mp4` (45,7 Mo) est dans la release |
| `waiff/` | dossier festival : `captions_en.srt`, `still.jpg`, `presentation.md`, `journal-de-production.md`, `bio-TODO.md` |
| `env.sh.original` | variables d'environnement du bac à sable d'origine (chemins absolus, pour mémoire) |

Les MP4 1080p (film + version festival), `mix.wav` et `preview.mp4` (720p) sont dans la **release v1.0** du dépôt.

## Refaire le rendu de ce film depuis ce dossier
```bash
pip install numpy pillow soundfile opencv-python-headless fonttools
cd reference/doc-chine/render
python3 render.py list                          # 24 scènes, total frames 4460
python3 render.py still 20                      # -> render/stills/s0020.00.jpg
ffmpeg -i ../build/mix.flac ../build/mix.wav    # (ou python3 audio.py pour refaire le mix)
python3 render.py seg $(seq 0 23)               # ~6 min sur 2 CPU
cd .. && bash tools/assemble.sh enc $(seq 0 23) && bash tools/assemble.sh mux && bash tools/assemble.sh preview
```
