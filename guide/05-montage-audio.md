# 05 — Montage audio : voix + musique par chapitre + bruitages + -14 LUFS

Script d'origine : `reference/doc-chine/render/audio.py` (exécuté tel quel pour le film). Il lit `build/narration.wav` et les
minutages de `scenes.py` (qui lit `build/timeline.json`), et écrit `build/thud.wav`, `build/premix.wav`, `build/mix.wav`.

## Entrées
- `build/narration.wav` + `build/timeline.json` (étape 04).
- `render/scenes.py` existant (au minimum les fonctions `T()`, `E()` et `TOTAL` ; elles marchent dès que la timeline existe).
- Nappes musicales : `third_party/video-agent-skills/music/{enquete,arpege,neon}.mp3`. Bruitages : `.../sfx/{impact-boom,zhhh,riser}.mp3`.

## Les choix du film (à reprendre)

**Musique : une nappe par grande partie, à -15 dB, baissée automatiquement sous la voix (sidechain).**

| Partie | Nappe (`id`) | Démarre à | Décalage dans le fichier | Pourquoi |
|---|---|---|---|---|
| Accroche + chapitre 1 | `enquete` (90 BPM, drone, battement, piano feutré) | 0 s | 10,7 s | révélation, récit |
| Chapitres 2 + 3 | `arpege` (96 BPM, arpège synthé) | début ch.2 − 1 s | 8,0 s | technologie, IA |
| Chapitre 4 | `neon` (104 BPM, le plus énergique) | début ch.4 − 1 s | 9,2 s | victoires (BYD, robots) |
| Chapitre 5 | `enquete` | début ch.5 − 1 s | 42,7 s | réflexion, retour au ton du début |

Règles de choix (de `skills-docs/short-editing/references/music.md`) : `enquete` = défaut quand on hésite ; `arpege` = tech ;
`neon` = résultats/victoires ; `thriller` = alerte/drame ; **jamais `sonar` ni `compte-a-rebours` sous une voix** (rejetés à l'écoute).
Chaque nappe : fondu d'entrée 1 s (0,4 s pour la première), fondu de sortie 2 s, chevauchement de 2 s avec la suivante (fondu enchaîné),
fondu final de 2,5 s.

**Ducking** : `sidechaincompress=threshold=0.02:ratio=5:attack=40:release=450:makeup=1` (la musique baisse quand la voix parle).

**Bruitages : 10 en tout, seulement sur les vrais temps forts** (jamais un bruit à chaque entrée d'élément).

| Moment (référence `T(id)` = début de phrase, `E(id)` = fin) | Son | Gain |
|---|---|---|
| `T('p0_l02') + 2.6` : le compteur 50:26 s'arrête | `impact-boom` (pic aligné) | -9 dB |
| `E('p0_l08') + 0.3` : passage à l'histoire (fin de l'accroche) | `zhhh` (pic aligné) | -8 dB |
| `T('p1_l06') + 2.8` : 18 millions | `thud` (synthétisé) | -6 dB |
| `T('p1_l12') + 0.3` : × 90 | `thud` | -6 dB |
| `T('p2_l06') + 4.8` : Nvidia −589 Md$ | `impact-boom` | -10 dB |
| `T('p3_l00') − 2.6` : montée avant la relance | `riser` | -14 dB |
| `T('p3_l00') − 0.05` : coupure noire de la relance | `thud` | -4 dB |
| `T('p3_l02') + 5.2` : 430 GW | `thud` | -6 dB |
| `T('p4_l04') + 2.6` : « dépassé » | `thud` | -6 dB |
| `T('p5_l09') + 1.0` : « Le prochain record ? » | `thud` | -7 dB |

Le `thud` (papier posé sur une table) est **synthétisé** par `audio.py` (sinus 115 → 40 Hz qui décroît + bruit filtré, 0,45 s).

**Loudness** : normalisation en **2 passes** `loudnorm=I=-14:TP=-1.5:LRA=11` (`linear=true`). Film : prémix -21,85 LUFS → mix -14,2 LUFS
(mesure loudnorm) / -14,4 LUFS (mesure ebur128), true peak -1,5 dBTP.

## Actions

1. Pour un nouveau film, dans `render/audio.py`, adapte **uniquement** :
   - les bornes `c2`, `c4`, `c5` (fins de chapitres) et la liste `beds` (nappes + décalages) ;
   - la liste `sfx` (temps en `T()`/`E()` de **tes** phrases, 6 à 10 sons maximum).
2. Lance :
   ```bash
   cd films/<slug>/render && python3 audio.py          # ~30 s ; affiche « premix <LUFS> <TP> »
   ```
3. Mesure :
   ```bash
   ffmpeg -hide_banner -nostats -i ../build/mix.wav -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E "^\s+(I|Peak):"
   ```

### Régénérer les nappes (facultatif)
Elles sont fournies. Pour les refaire à l'identique (vérifié octet pour octet pour `enquete`) :
```bash
cd third_party/video-agent-skills/engine && node music.mjs enquete arpege neon --out ../music   # Node 22 + ffmpeg, ~20 s par nappe
```

## Sorties
`build/mix.wav` (48 kHz stéréo, durée = `TOTAL` arrondie au centième ; film : 371,60 s), `build/thud.wav`, `build/premix.wav`.

## Contrôles
- STOP si `I` n'est pas entre -14,8 et -13,5 LUFS ou si `Peak` > -1,0 dBFS.
- STOP si la durée de `mix.wav` diffère de `TOTAL` de plus de 0,05 s : `ffprobe -v error -show_entries format=duration -of csv=p=0 ../build/mix.wav`.
- STOP si plus de 10 bruitages, ou deux bruitages à moins de 5 s d'intervalle.
- Écoute impossible ? Vérifie au moins le niveau de musique seule entre deux chapitres : `ffmpeg -ss <fin_chapitre+0.5> -t 1.5 -i ../build/mix.wav -af volumedetect -f null -` → `mean_volume` doit être nettement plus bas que pendant la voix. Film : ≈ -22,7 dB entre deux chapitres (musique seule, ex. 246,4 s) contre ≈ -17 dB pendant la voix (ex. 100-110 s). STOP si l'écart est inférieur à 4 dB.

## Problèmes rencontrés et solutions
- **Un compteur ou une barre sans « impact »** : on ne met pas un son partout ; le film n'en a que 10 en 6 min. Respecte la règle des vrais temps forts.
- **Musique trop présente** : les nappes « chargées » (générées par IA) avaient été testées et rejetées par l'auteur du dépôt : garde les nappes calmes fournies, à -15 dB, avec ducking.
- **Dérive de durée** : si tu changes la narration (phrase corrigée), relance `rebuild_narration.py` **puis** `audio.py` **puis** le rendu : les trois dépendent de `timeline.json`.
