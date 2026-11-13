# 08 — Rendu vidéo : le moteur Python (stop-motion 12 fps → MP4 24 fps)

Code d'origine (exécuté pour le film) : `reference/doc-chine/render/vx.py` (moteur), `scenes.py` (plan des 24 scènes), `render.py` (rendu).
Pourquoi un moteur maison et pas le moteur Chrome du dépôt `video-agent-skills` : ce dernier attend des mots horodatés par Whisper et des
rendus longs découpés, irréaliste sur une machine à 2 CPU. Le moteur Python fait ~12-13 images/s en 1920×1080.

## Entrées
- `images/*.png` (étape 07) — `render/img` est un lien vers `../images`.
- `build/timeline.json` (étape 04), `build/mix.wav` (étape 05).
- `render/captions_lines.json` : `{ "<id>": "<texte affiché>" }` pour chaque phrase, **chiffres en chiffres** (ex. `"p0_l01": "Un robot humanoïde d'1,69 m s'élance sur un semi-marathon."`).

## Architecture (à comprendre avant de toucher à `scenes.py`)

```
timeline.json ──► scenes.py : T(id)=début de la phrase, E(id)=fin ; liste de scènes {a: début, plate: décor, items: [...], zoom, drift, dark}
                     │
images/*.png ──► vx.py : plate() (décor recadré 16:9 + 12 % de marge pour le zoom) ; cutout() (détourage du vert, cache dans render/layers/)
                     │   Cut / Strip / Counter / Bars / Line / Black / Fn  = éléments animés ; Cam = caméra ; finish() = grain + vignette
cues.json ─────► render.py : frame(t) = décor + éléments + sous-titre, temps arrondi à 1/12 s ; "seg i" = encode la scène i en MP4 12 fps
```

Réglages fixes du moteur (`vx.py`, ne pas changer) :
- **1920×1080, horloge à 12 images/s** (effet stop-motion) ; le MP4 final est en **24 fps** (chaque image affichée 2 fois).
- Entrées en ressort : `S(x, w) = 1 − (1 + w·x)·e^(−w·x)` (w = 14 pour les découpes, 12 pour les bandes, 6 pour les barres).
- « Wiggle » : chaque découpe tremble de ±1 px, nouveau tirage toutes les 2 images (le côté fait-main).
- Caméra : zoom lent de `zoom` (0,04 à 0,07) sur toute la scène + dérive `drift` (px) ; parallaxe par `depth` (décor 0,4 ; découpes 0,7 à 1,1).
- Détourage chroma : `gd = G − max(R, B)` ; alpha = `clip(1 − (gd − 18)/40)` (vert franc > 58 = transparent) ; suppression du débord vert ; érosion/dilatation 3 px ; flou 0,7 ; recadrage à l'objet.
- Ombres portées douces (décalage 7,10 px, flou 9, opacité 0,42) sur tout ce qui est posé.
- Grain : 2 trames de bruit alternées (amplitude 0,16) + vignette brune.
- Sous-titres : Archivo Black 46 px, blanc sur bandeau sombre (18,15,13, alpha 214), **mots contenant un chiffre + mots de la liste `EMPH` en jaune**, largeur max 1500 px, bas du bandeau à y = 1008.

## Les éléments disponibles (constructeurs de `vx.py`)

| Élément | Signature utile | Exemple réel du film |
|---|---|---|
| `Cut` (découpe) | `Cut(name, x, y, h, at=0, enter='up', until=1e9, exit='down', depth=1.0, anchor='c', flip=False, bob=0, swap=None)` | `Cut('robot-run', 640, 1000, 560, at=0, enter='none', anchor='b', bob=8)` |
| `Strip` (bande de papier avec texte) | `Strip(strip(texte, taille, fnt=SERIF, color=CREAM, seed=n, rot=deg), x, y, at=, enter='left', until=, anchor='c')` | `Strip(strip('Honor', 120, fnt=BLACK, seed=11, rot=-2), 330, 330, at=T('p0_l05')+3.6, enter='pop')` |
| `Counter` (nombre qui défile) | `Counter(x, y, a, b, t0, t1, fmt, size=150, label=None, seed=, at=None, until=, numink=None, strike_at=None, exit='down')` | `Counter(1420, 360, 0, 157, T('p1_l01')+4.0, T('p1_l01')+5.6, money, label='revenu par habitant et par an', seed=16)` |
| `Bars` (barres horizontales) | `Bars(x, y, [(libellé, valeur, couleur, at)], vmax, width=900, fmt=str, title=None, at=None)` | `Bars(960, 560, [('BYD', 2.26, RED, t1), ('Tesla', 1.64, BLUE, t2)], 2.95, width=1000, fmt=…, title='voitures 100 % électriques vendues en 2025')` |
| `Line` (trait de feutre rouge) | `Line((x0, y0), (x1, y1), at, dur=0.35, width=14)` | barrer « La Chine copie » |
| `Black` (écran noir) | `Black(at, until)` | coupure noire de la relance (début ch.3) |
| `Fn` (fonction libre) | `Fn(lambda fr, t, cam: …)` | déplacer le robot de droite à gauche dans la 1re scène |
| `chapter_card(n, titre, at, until)` | carte « Chapitre n » + titre, au centre | `chapter_card(1, 'De la misère à Shenzhen', c1 + 0.1, T('p1_l00') + 0.6)` |

`enter` / `exit` : `'left' 'right' 'up' 'down' 'pop' 'none'`. `anchor` : `'c'` centre, `'b'` bas (objets posés au sol, `y` = 1080 ou plus), `'l'` gauche, `'r'`, `'tl'`.
Polices : `BLACK` (Archivo Black), `SERIF` (Instrument Serif), `SERIF_I` (italique), `SANS` (Archivo). Couleurs : `INK CREAM YEL RED BLUE SEPIA WHITE`.
Formats prêts dans `scenes.py` : `money(v)` → « 13 800 $ », `intsp(v)` → « 295 000 », `mmss(v)` → « 50:26 ».

## Écrire `scenes.py` pour un nouveau film (procédure)

1. Garde l'en-tête (imports, `TL`, `T`, `E`, `TOTAL = E('<dernière phrase>') + 2.5`, `money`, `intsp`, `mmss`, `chapter_card`, `sc(...)`).
2. **Une scène = un décor**. Nouvelle scène quand le décor change. Film : 24 scènes pour 6 min 12 (≈ 15 s par scène, de 7,8 s à 34,8 s).
   Une scène commence en général à `T('<phrase>') - 0.15` (juste avant la phrase) ; la première de chaque chapitre à `c_n = E('<dernière phrase du chapitre précédent>') + 0.25`, avec sa `chapter_card`.
3. Dans chaque scène, **un élément visuel nouveau toutes les 3 à 5 s**, calé sur le mot dit : `at=T('p1_l01') + 4.0` = 4 s après le début de la phrase (cherche le moment du mot dans `tts/lines/<id>.wav` avec Whisper mot à mot, ou estime : position du mot en caractères / 15).
4. Chaque chiffre important du script devient un `Counter` (ou des `Bars` pour une comparaison), avec sa **légende datée** (`label='record humain, mars 2026'`).
5. Retire les éléments avant qu'ils s'entassent : `until=T('<phrase suivante>')`.
6. **Zone interdite** : rien d'important sous y ≈ 900 (les sous-titres occupent ~930-1008). Film : les compteurs de l'accroche ont dû être remontés à y = 300 et 590, la bande « 2025 » à y = 800.
7. Liste `EMPH` en bas de `scenes.py` : mots à colorer en jaune dans les sous-titres (noms propres, mots-clés de la thèse), séparés par `|`.
8. Teste **à chaque scène écrite** avec des images fixes (pas besoin des vraies images : des images provisoires du même nom suffisent).

## Sous-titres

- `render/captions_lines.json` : texte affiché par phrase, nombres en chiffres, typographie française (« 7 h 30 », « 1,69 m », « 295 000 », « 80 % »).
- Découpe en cues : `python3 tools/make_cues.py` → `render/cues.json` (morceaux ≤ ~45 caractères, jamais coupés dans un nombre, durée proportionnelle aux caractères). Le film a 135 cues.
- `.srt` : `python3 tools/cues_to_srt.py render/cues.json output/captions.srt`.

## Actions (commandes exactes)

```bash
cd films/<slug>/render
python3 render.py list                       # liste : n° de scène, décor, début, fin, (image début, image fin) ; dernière ligne « total frames N »
python3 render.py still 1 20 60 100 200      # images de contrôle dans render/stills/sXXXX.XX.jpg  → OUVRE-LES ET REGARDE
python3 ../tools/render_plan.py 12 100       # lots de segments qui tiennent sous ~100 s chacun
python3 render.py seg 0 1 2 3 4 5 6          # rend les segments render/segs/segNN.mp4 (12 fps, crf 16, veryfast) ; 1 lot par commande
#   ... lancer chaque lot affiché par render_plan.py ...
cd ..
bash tools/assemble.sh enc 0 1 2 3 4 5       # ré-encode en 24 fps crf 20 (lots de ~60 s de vidéo par commande sur 2 CPU)
#   ... jusqu'au dernier segment ...
bash tools/assemble.sh mux                   # concat + audio AAC 192k + faststart (dans /tmp puis copie) -> output/documentaire-chine.mp4
bash tools/assemble.sh preview               # output/preview.mp4 720p ~45 Mo (relancer si coupé : les moitiés faites sont gardées)
```

Film de référence : `render.py list` → 24 scènes, **4460 images** à 12 fps ; lots : `seg 0-6`, `7-12`, `13-18`, `19-23` ; MP4 final 1920×1080,
H.264 High crf 20, yuv420p, 24 fps, AAC 192 kb/s 48 kHz, **371,60 s, 338 Mo** ; aperçu 1280×720 ~45,7 Mo.
Sur un PC normal, tu peux enchaîner sans lots : `python3 render.py seg $(seq 0 23)` puis `assemble.sh enc $(seq 0 23)`.

## Sorties
`render/segs/seg00.mp4` … `segNN.mp4`, `output/documentaire-chine.mp4`, `output/preview.mp4`, `output/captions.srt`, `render/stills/*.jpg`.

## Contrôles
- STOP si `render.py list` montre une scène de moins de 3 s ou de plus de 40 s.
- STOP si le nombre de `segNN.mp4` ≠ nombre de scènes.
- STOP si la durée du MP4 ≠ `TOTAL` (± 0,1 s) — `bash tools/check_video.sh output/documentaire-chine.mp4 <TOTAL>`.
- Regarde les stills : voir la liste complète à l'étape 09.

## Problèmes rencontrés et solutions
| Symptôme | Cause | Solution |
|---|---|---|
| Compteurs de l'accroche cachés par les sous-titres | placés trop bas | remonter (y = 300 / 590 / 800) ; règle : rien d'important sous y ≈ 900 |
| Un carré vide à la place de « ≈ » | glyphe absent d'Instrument Serif | `python3 tools/check_glyphs.py` ; réécrire le texte (« près des 3/4 du recul… ») ou utiliser `BLACK` qui a « ≈ » |
| Étiquette de valeur d'une barre coupée à droite | `vmax` = valeur max → barre pleine largeur, plus de place pour le texte | `vmax` ≈ 1,3 × la plus grande valeur (BYD 2,26 → `vmax` 2,95) |
| Découpes + étiquettes du ch.5 trop basses | collision avec sous-titres | remontées de 40 px |
| Encodage final > 120 s (limite d'une commande dans le bac à sable) | 1080p H.264 ≈ 1,8 s de calcul par seconde de vidéo sur 2 CPU | encoder segment par segment (`assemble.sh enc`), concaténer sans ré-encoder |
| `Unable to re-open … for shifting data` à la fin d'un encodage | `+faststart` sur `/workspace` (JuiceFS) | écrire dans `/tmp`, puis `cp` |
| Une commande de surveillance renvoie la même sortie que la précédente | sortie en cache du bac à sable | changer le texte de la commande (ex. ajouter `; date`) |
| Une image régénérée n'apparaît pas | `render/layers/<name>.png` (cache du détourage) plus récent | le cache est recalculé si l'image est plus récente ; sinon supprime `render/layers/*` |
