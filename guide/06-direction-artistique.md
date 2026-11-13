# 06 — Direction artistique : le collage papier « façon Vox » et les 34 plans

Le style vient du skill `vox` du dépôt `video-agent-skills` (copie : `third_party/video-agent-skills/skills-docs/vox/references/look.md`).
**Un seul style pour tout le film.** C'est ce qui fait « premium ». Les 34 prompts réels du film : `guide/templates/prompts-doc-chine.md`.
Exemples d'images réussies : `reference/doc-chine/images/` ; images de contrôle du film rendu : `reference/doc-chine/qc-stills/`.

## Les règles du style (à respecter mot pour mot)

1. Tout prompt = `<subject>` [+ ` <CHROMA>` si c'est une découpe] + saut de ligne + `Style: <STYLE>`.
2. `STYLE` (identique pour les 34 images, ne change pas un mot) :
   ```text
   Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
   ```
3. `CHROMA` (seulement pour les découpes) :
   ```text
   Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
   ```
4. **Jamais de texte dans l'image** (ni lettres, ni chiffres, ni logo, ni marque). Tous les textes sont ajoutés au montage (étape 08) — le modèle d'image écrit mal et une marque dessinée pose un problème de droits. Écris « plain surface with no lettering », « plain dial without numbers ».
5. Personnes, bâtiments, objets = **photo en similigravure noir et blanc** découpée aux ciseaux avec un fin bord blanc. La couleur sert seulement d'accent : « one warm-yellow accent on … ».
6. **Aucune personne réelle identifiable** : foules, coureurs, ouvriers génériques. Les personnalités (Deng Xiaoping, Ray Dalio) sont nommées à l'écran, jamais dessinées.
7. Décors (`plate`) : laisse **le centre vide et calme** (« the center … left empty and calm ») pour poser compteurs et découpes par-dessus.
8. Miniatures (`thumb-a`, `thumb-b`) : fond **papier rouge profond déchiré**, sujet sur la droite, **le tiers gauche vide** pour le titre.

## Deux sortes d'images

| `kind` | Rôle | Tailles utilisées (multiples de 32) |
|---|---|---|
| `plate` (14) | décor plein cadre 16:9, gardé entier | 1664×928 |
| `cutout` (20) | un seul objet sur vert chroma, détouré automatiquement au montage | 1024×1024 (objet compact), 1472×832 (objet large), 1664×832 (ligne d'horizon), 1664×640 (bande très large : foule, panneaux solaires, train), 832×1248 (objet haut : éolienne, pylône, gratte-ciel) |

Une découpe = **un seul objet**. Pour 4 voitures à l'écran, une seule découpe `ev-car` posée 4 fois. Pour un objet qui « se pose au sol », écris « flat bottom edge ».

## Faire la liste des plans (`kaggle/shots.json`)

1. Relis les notes visuelles du script (étape 03). Pour chaque scène : 1 décor + 0 à 4 découpes.
2. Budget : **34 images maximum** (temps GPU : ~18 min par image sur Kaggle T4×2, voir étape 07). Film : 14 décors + 20 découpes ; 1 découpe (`stopwatch`) n'a finalement pas servi.
3. **Réutilise** : un décor peut servir à plusieurs scènes (film : `plate-race` dans 5 scènes, `plate-village` dans 3, `plate-map` et `plate-factory` dans 2). Une découpe aussi (`robot-run` 3 fois, `skyline-sz` 3 fois).
4. Seeds : un bloc de dizaines par partie (film : 11-12 miniatures ; 21-25 accroche ; 31-34 ch.1 ; 41-45 ch.2 ; 51-56 ch.3 ; 61-65 ch.4 ; 71-75 ch.5 ; 81-82 ajouts). Ça permet de retrouver et régénérer une image précise.
5. Format d'une entrée (gabarit : `guide/templates/shots-template.json`) :
   ```json
   {"name": "robot-run", "kind": "cutout", "w": 1024, "h": 1024, "seed": 22,
    "subject": "One sleek humanoid robot running, full body, side view, mid-stride with one knee raised and arms swinging, smooth white and grey panels, as a black-and-white halftone engraved photograph cut out with scissors, thin white paper border following its silhouette, centered."}
   ```
   `name` : minuscules et tirets, c'est le nom du PNG et le nom utilisé dans `scenes.py`. Pas d'espace, pas d'accent.

## Écrire un bon `subject` (recette)

`[cadrage] : [quoi, précis] , [vu comment] , [fait de quoi : halftone / papier déchiré] , [accent jaune éventuel] , [placement : centré / centre vide / flat bottom edge]`

Exemples réels du film :
- Décor : « Full-frame 16:9 background plate: a poor rural Chinese village landscape in the late 1970s, flooded rice paddies, low mud-brick houses with tiled roofs, distant green hills, made of torn paper layers and sepia halftone engraved photo cut-outs, aged cream paper sky, calm and empty center. »
- Découpe : « A container port with three tall ship-to-shore gantry cranes and stacked shipping containers, seen from the side, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, flat bottom edge, one warm-yellow accent on one container. »
- Miniature : « Full-frame 16:9 cinematic collage poster: a humanoid robot runner overtaking a human marathon runner, both side view, both printed as black-and-white halftone engraved photographs cut out with thin white scissor borders, the robot slightly ahead and larger, on the right two thirds of the frame, over a torn deep-red paper background with one warm-yellow torn paper finish-line ribbon, the left third left as plain empty red paper. »

## Couleurs et polices du montage (déjà dans `render/vx.py`, ne pas changer)

| Nom | RVB | Usage |
|---|---|---|
| `INK` | 28, 24, 22 | texte |
| `CREAM` | 240, 230, 208 | bandes et cartes par défaut |
| `PAPER` | 232, 220, 194 | papier |
| `YEL` | 238, 184, 52 | mise en avant (chiffres clés, mots surlignés des sous-titres) |
| `RED` | 188, 46, 38 | trait de feutre, barres, « Chapitre n » |
| `BLUE` | 120, 150, 170 | barre du concurrent |
| `SEPIA` | 150, 110, 70 | barre « avant » |
| `WHITE` | 250, 246, 236 | citations |

Polices (SIL OFL, dans `third_party/video-agent-skills/fonts/`) : **Archivo Black** (chiffres, noms, sous-titres 46 px),
**Instrument Serif** (bandes de texte), **Instrument Serif Italic** (légendes, « Chapitre n »), **Archivo** (libellés des barres).

## Sorties
- `kaggle/shots.json` (34 entrées), `kaggle/build_img_prompts.py` (inchangé : il assemble subject + CHROMA + STYLE).

## Contrôles
```bash
cd kaggle && python3 -c "
import json; from collections import Counter
s=json.load(open('shots.json')); print(len(s), Counter(x['kind'] for x in s))
assert len({x['name'] for x in s})==len(s), 'noms en double'
assert len({x['seed'] for x in s})==len(s), 'seeds en double'
for x in s:
  assert x['w']%32==0 and x['h']%32==0, x['name']
  assert x['kind'] in ('plate','cutout'), x['name']
  t=x['subject'].lower()
  for bad in ['text','logo','word','letter']:
    if bad in t and 'no ' + bad not in t and 'without' not in t: print('ATTENTION mot', bad, 'dans', x['name'])
print('ok')"
```
- STOP si plus de 34 images (ou alors coupe en 2 notebooks, étape 07).
- STOP si un `subject` demande un texte, une marque ou une personne réelle.
- STOP si une scène du plan n'a pas de décor.

## Problèmes rencontrés et solutions
- **Décor quasi vide** : `plate-circuit` (« dark navy-blue paper sheet printed with faint engraved circuit-board traces ») est sorti presque uni. Acceptable pour un fond sombre ; sinon décris des éléments plus gros et plus contrastés.
- **Taches vert vif dans un décor** : sur `plate-race`, deux grosses taches vertes (feuillage raté) sont apparues dans le ciel et les immeubles, alors que le prompt disait déjà « a few bare trees ». On ne peut pas l'empêcher à coup sûr : **regarde chaque décor** (étape 07) et répare avec `tools/inpaint_green.py` (étape 09), ou régénère avec une autre seed. Dans une **découpe**, ne demande pas d'objet vert (il serait détouré avec le fond).
