# 13 — Checklist finale (tout doit être coché avant de montrer le film)

Copie cette liste dans `PROGRESS.md` et coche chaque ligne **après l'avoir vérifiée toi-même** (commande lancée, fichier ouvert).

## Fond
- [ ] Thèse en une phrase, accroche notée ≥ 7/10, 1 accroche + 5 chapitres, relance vers 50 %, fin qui reboucle + question avec mots exacts.
- [ ] Chaque fait du script a une source ouverte et listée dans `output/sources.md`.
- [ ] Faits datés revérifiés **aujourd'hui** ; tout écart signalé à l'utilisateur.
- [ ] Aucune phrase copiée de la vidéo d'inspiration.
- [ ] Limites / contre-arguments présents dans le dernier chapitre.

## Voix
- [ ] `tts/lines/*.wav` = nombre de phrases de `paras.json`.
- [ ] Transcription whisper.cpp de chaque phrase lue ; noms propres OK ; aucun mot parasite.
- [ ] `build/narration.wav` 24 kHz mono ; `build/timeline.json` à jour (0,6 / 0,32 / 2,5 / 2,5 s).

## Audio
- [ ] `build/mix.wav` : I entre -14,8 et -13,5 LUFS, true peak ≤ -1,0 dB, durée = `TOTAL`.
- [ ] Une nappe par grande partie, -15 dB, ducking ; ≤ 10 bruitages, seulement sur des temps forts.

## Images
- [ ] 34 images (ou moins), noms = `shots.json`, toutes ouvertes et regardées une par une.
- [ ] Aucun texte/logo/personne réelle ; découpes sur vert uni ; défauts réparés (original dans `images/orig/`) ou régénérés.

## Montage
- [ ] `render.py list` : scènes entre 3 et 40 s ; total frames = ceil(TOTAL × 12).
- [ ] Un still par scène regardé ; rien sous les sous-titres ; pas de carré vide (`check_glyphs.py`) ; pas de texte coupé.
- [ ] Chiffres à l'écran = script = sources ; légendes datées.
- [ ] Cartes de chapitre aux bons endroits.

## Fichiers finaux
- [ ] `bash tools/check_video.sh output/documentaire-chine.mp4 <TOTAL>` : h264 High 1920×1080 24 fps yuv420p, AAC 48 kHz stéréo, durée OK, loudness OK.
- [ ] Les 12 images témoins de `/tmp/vh_check/` regardées.
- [ ] `output/preview.mp4` < 50 Mo.
- [ ] `output/thumbnail.png` 1280×720, lisible en 320×180.
- [ ] `output/post.md` : titre, description avec mention IA, chapitres (0:00 + temps des cartes), 5 hashtags max, sources.
- [ ] `output/captions.srt` = `render/cues.json`.

## Version festival (si demandée)
- [ ] `en_lines.txt` = même nombre de lignes que les cues ; relu par l'utilisateur.
- [ ] MP4 nommé selon le règlement ; `still.jpg` sans sous-titre ; présentation FR/EN ; journal de production avec [À CONFIRMER] ; bio non inventée.

## Avant d'envoyer
- [ ] `PROGRESS.md` à jour (fait / reste / pièges).
- [ ] Message à l'utilisateur : aperçu + miniature + ce qui a été retouché + ce qu'il doit décider (faits datés, publication). Rien publié ni déposé sans son accord.

## Valeurs du film de référence (pour comparer)
371,6 s · 65 phrases · 831 mots · 24 scènes · 4460 images à 12 fps · 24 fps à la sortie · 34 images (14 décors + 20 découpes) ·
-14,4 LUFS (ebur128) / -14,2 (loudnorm) · TP -1,5 dBTP · 338 Mo · chapitres 0:00 / 0:51 / 2:04 / 3:11 / 4:06 / 5:05 · 135 sous-titres.
