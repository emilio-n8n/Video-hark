# 09 — Contrôle qualité (images, mise en page, son, faits)

Ce contrôle a trouvé, sur le film de référence : 2 images défectueuses, 4 problèmes de mise en page, 1 glyphe manquant, 1 mot parasite
dans la voix et 1 fait devenu faux. **Fais-le en entier à chaque film.** Exemples de stills de contrôle du film : `reference/doc-chine/qc-stills/`.

## A. Les 34 images sources (avant le rendu)

Pour chaque image de `images/`, ouvre-la et réponds :
1. Y a-t-il du texte, des lettres, un logo, un chiffre ? → régénérer.
2. Découpe : le fond est-il vert uni partout autour de l'objet ? l'objet est-il entier (pas coupé par le bord) ? → sinon régénérer.
3. Décor : y a-t-il des **taches vert vif** ? → réparer :
   ```bash
   mkdir -p images/orig && cp images/<decor>.png images/orig/<decor>.png
   python3 tools/inpaint_green.py images/orig/<decor>.png images/<decor>.png     # affiche le % de masque ; STOP si > 35 %
   ```
   puis regarde le résultat. Film : `plate-race` → ciel et immeubles brumeux, acceptable.
4. Décor presque vide ou raté ? Si des éléments se posent dessus et qu'il sert de fond, garder (film : `plate-circuit`). Sinon régénérer.
5. Personne réelle reconnaissable, main/visage monstrueux au premier plan ? → régénérer.

## B. Les stills du montage (avant d'encoder le film entier)

```bash
cd render
python3 render.py still 1 10 25 40 50 70 82 97 112 123 128 145 158 170 190 195 201 216 227 244 300 330 360
```
(Adapte la liste : **au moins 1 still par scène** + 1 sur chaque compteur, barre et carte de chapitre. Film : 20 stills, voir `qc-stills/`.)
Pour **chaque** still, vérifie et note OK/KO dans `PROGRESS.md` :

| # | Vérification | STOP si |
|---|---|---|
| 1 | Sous-titre lisible, en bas, une ou deux lignes | un élément (compteur, bande, découpe) touche ou passe sous le bandeau du sous-titre |
| 2 | Chiffres à l'écran = chiffres du script et des sources | une valeur, une unité ou une date diffère |
| 3 | Pas de carré vide (glyphe manquant) | un caractère s'affiche en □ → `python3 ../tools/check_glyphs.py` |
| 4 | Textes entiers | un texte ou une valeur de barre est coupé par le bord ou par la carte |
| 5 | Pas d'entassement | plus de 4 éléments de texte à la fois, ou deux éléments qui se chevauchent sans le vouloir |
| 6 | Découpes propres | frange verte visible autour d'un objet |
| 7 | Cohérence | l'élément montré correspond à ce que dit la voix à ce moment |

Après correction dans `scenes.py`, relance `still` aux mêmes temps et **re-regarde**.

## C. Le MP4 final

```bash
bash tools/check_video.sh output/documentaire-chine.mp4 <TOTAL>
```
Attendu (film) : `h264 High 1920x1080 24/1 yuv420p`, `aac 48000 2`, durée **371.60**, `I: -14.4 LUFS`, `Peak: ≤ -1.0 dBFS`
(film : -1,5 dBTP au mix ; -1,1 dBFS de crête mesurée après encodage AAC).
- STOP si la durée diffère de la timeline de plus de 0,1 s.
- STOP si I hors [-14,8 ; -13,5] ou Peak > -1,0.
- Ouvre les 12 images de `/tmp/vh_check/` : STOP si une image est noire hors de la coupure voulue (relance du ch.3), figée, ou décalée par rapport au son.
- Synchronisation : prends 3 moments où un compteur s'arrête et un bruitage tombe (film : 50:26 à `T('p0_l02') + 2.6`) ; extrais 2 s audio/vidéo et vérifie que les temps coïncident (`ffmpeg -ss <t-1> -t 2 -i output/documentaire-chine.mp4 /tmp/sync.mp4`).

## D. Les faits, une dernière fois (juste avant de montrer à l'utilisateur)

Pour chaque fait « record / premier / plus grand / dernier » : refais une recherche **datée d'aujourd'hui**.
Film : « Le record du monde humain … est de 57 minutes et 20 secondes » — exact en mars 2026, **dépassé** le 23/08/2026 (Kejelcha, 56:51).
L'écran dit « record humain, mars 2026 », la voix dit « est de » au présent. → **DEMANDER** à l'utilisateur : garder tel quel (le contexte de la course d'avril 2026 le justifie) ou corriger (régénérer la phrase `p0_l03` au passé : « … était alors de … », puis `rebuild_narration.py`, `audio.py`, rendu).

## E. Ce que tu signales à l'utilisateur avec l'aperçu
- Les retouches faites (images réparées, phrases coupées).
- Les phrases dont la prononciation reste douteuse (s'il y en a).
- Les faits datés qui ont bougé.
- Rien d'autre : pas le journal technique.

## Problèmes rencontrés et solutions
| Problème trouvé au contrôle | Solution appliquée |
|---|---|
| `plate-race` : 2 taches vertes | inpainting Telea (`tools/inpaint_green.py`), original dans `images/orig/` |
| `plate-circuit` : décor presque uni | gardé comme fond sombre (puce, baleine, bandes posées dessus) |
| Compteurs 50:26 / 57:20 sous les sous-titres | remontés (y 300 / 590, bande y 800) |
| « ≈ » en carré vide (Instrument Serif) | texte réécrit « près des 3/4 du recul… » |
| Valeur de la barre BYD coupée | `vmax` 2,95 |
| Étiquettes du ch.5 trop basses | remontées de 40 px |
| « 74 de technologies » (voix) | coupe audio de 0,085 s |
| Record 57:20 dépassé | signalé, décision laissée à l'utilisateur |
| Sous-titre coupé au milieu d'un nombre (« … installé 295 » / « 000 robots ») dans le film | non corrigé dans le film ; `tools/make_cues.py` ne coupe plus jamais dans un nombre |
