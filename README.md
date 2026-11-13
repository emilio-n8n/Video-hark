# Video-hark — fabriquer un mini-documentaire YouTube premium avec l'IA, pas à pas

Ce dépôt documente **exactement** comment a été fabriqué le documentaire **« La Chine ne copie plus : comment elle est devenue le pays qu'on étudie »**
(Emilio Moreau, novembre 2026) — et donne un guide si détaillé qu'un modèle d'IA, même faible, peut refaire une vidéo de la même qualité sur un autre sujet.

![Miniature du film](reference/doc-chine/output/thumbnail.png)

## Le résultat

| | |
|---|---|
| Film final 1080p (338 Mo) + version festival sous-titrée anglais | **[Release v1.0](https://github.com/emilio-n8n/Video-hark/releases/tag/v1.0)** |
| Aperçu 540p dans le dépôt (20,6 Mo) | [`reference/doc-chine/output/preview-540p.mp4`](reference/doc-chine/output/preview-540p.mp4) |
| Aperçu 720p d'origine (45,7 Mo) | asset `preview.mp4` de la [release v1.0](https://github.com/emilio-n8n/Video-hark/releases/tag/v1.0) |
| Miniature | [`reference/doc-chine/output/thumbnail.png`](reference/doc-chine/output/thumbnail.png) |
| Titre, description, chapitres, sources | [`reference/doc-chine/output/post.md`](reference/doc-chine/output/post.md) |

Fiche technique : 6 min 12 s (371,6 s) · français, sous-titres incrustés · 1920×1080, 24 fps, H.264 + AAC · -14 LUFS ·
voix Qwen3-TTS (Kaggle) · 34 images Qwen-Image 2.1 en collage papier façon Vox (Kaggle T4×2, Wan2GP) · 24 scènes animées en Python
(stop-motion 12 images/s : 4460 images) · 3 nappes musicales générées par code + 10 bruitages · chapitres 0:00 / 0:51 / 2:04 / 3:11 / 4:06 / 5:05 ·
une vingtaine de faits chiffrés, tous sourcés.

## Utiliser le guide avec un modèle d'IA

> **Donne `guide/00-LIRE-EN-PREMIER.md` à ton modèle**, avec l'accès à ce dépôt, puis dis-lui ton sujet.

Il suivra les étapes 01 → 13 dans l'ordre. Chaque étape contient les commandes exactes, les fichiers attendus, des contrôles « STOP si… »,
les règles de décision et les problèmes réellement rencontrés avec leur solution. Le dossier `reference/doc-chine/` sert de modèle concret à chaque étape.

## Carte du dépôt

```
README.md                      ce fichier
LICENSE-NOTES.md               licence de chaque composant (modèles, moteur, polices, musiques)
guide/                         LE GUIDE (en français, impératif, pas à pas)
  00-LIRE-EN-PREMIER.md        règles absolues, prérequis, carte des étapes
  01-cadrage-et-sujet.md       questions autorisées, thèse, structure accroche + 5 chapitres
  02-recherche-et-verification-des-faits.md
  03-ecriture-du-script.md     accroches notées, longueur (mots = minutes × 134), relance, humanize
  04-voix-tts.md               Qwen3-TTS sur Kaggle, contrôle Whisper, correction d'une phrase, assemblage
  05-montage-audio.md          nappes par chapitre, ducking, bruitages, -14 LUFS
  06-direction-artistique.md   style collage papier, 34 plans, écriture des prompts
  07-generation-images-kaggle.md  Qwen-Image 2.1 / Wan2GP sur T4×2, temps réels, plantages et correctifs, pagination
  08-rendu-video.md            moteur Python vx/scenes/render, 12 → 24 fps, sous-titres, encodage par segments
  09-controle-qualite.md       images, stills, MP4, faits — avec tout ce que le contrôle a trouvé
  10-miniature-et-publication-youtube.md
  11-version-festival.md       sous-titres anglais incrustés, dossier WAIFF
  12-depannage.md              tous les problèmes : symptôme → cause → solution
  13-checklist-finale.md
  templates/                   gabarits (script, paras.json, shots.json, scenes.py, post.md, sources) + les 34 prompts réels
reference/doc-chine/           tout le code, les données et les fichiers du film (voir son README.md et CHRONOLOGIE.md)
third_party/video-agent-skills/  extraits MIT utilisés : polices, 3 nappes + leur générateur, 3 bruitages, docs des skills
```

## Ce qui n'est pas dans le dépôt (et pourquoi)
- Les MP4 1080p (338 Mo chacun), `mix.wav` (71 Mo) et l'aperçu 720p d'origine (45,7 Mo) → assets de la release v1.0. Dans le dépôt : `mix.flac` et un aperçu 540p de 20,6 Mo (réencodé depuis le film final, uniquement pour le dépôt).
- Les poids des modèles (≈ 19 Go pour Qwen-Image 2.1, ~0,5 Go pour Whisper) : téléchargés par les notebooks / scripts.
- Les segments vidéo intermédiaires, les images de rendu brutes et le cache de détourage : régénérables (`render.py`).
- Le dépôt `video-agent-skills` complet (~390 Mo) et whisper.cpp : seulement les fichiers utilisés sont copiés, avec leur licence.
- Les identifiants (tokens Kaggle, etc.) : jamais dans le dépôt.

## Crédits
Réalisation : Emilio Moreau. Fabrication assistée par Hark. Méthode de script, style et ressources audio : [video-agent-skills](https://github.com/Melvynx/video-agent-skills) (MIT, Melvyn Malherbe).
Images : Qwen-Image 2.1 (licence qwen-research) via [Wan2GP](https://github.com/deepbeepmeep/Wan2GP). Voix : Qwen3-TTS (Apache-2.0). Détails : `LICENSE-NOTES.md`.
