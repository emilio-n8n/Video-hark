# 11 — Version festival (sous-titres anglais incrustés + dossier)

Référence : le dossier WAIFF Africa (Abidjan 2027, catégorie « AI Short Film ») préparé pour le film, dans `reference/doc-chine/waiff/` :
`captions_en.srt`, `still.jpg`, `presentation.md`, `journal-de-production.md`, `bio-TODO.md`. Le MP4 festival (338 Mo) est dans la release GitHub v1.0.
Rien n'a été déposé : le dépôt se fait par l'utilisateur ou avec son accord explicite.

## Entrées
- Film final validé (étapes 08-10), `render/cues.json`.
- Règlement du festival visé (lis-le en entier : durée, langues, format de fichier, nommage, champs du formulaire, date limite avec fuseau).

## A. Sous-titres anglais (mêmes minutages)

1. Écris `render/en_lines.txt` : **une ligne anglaise par cue française, dans le même ordre** (film : 135 lignes). Traduis le sens, garde les chiffres
   au format anglais (« 1.69-metre », « 7:30 in the morning », « 2.26 million »). Une ligne vide = interdit.
2. ```bash
   python3 tools/make_cues_en.py                                              # -> render/cues_en.json ; STOP si le nombre de lignes diffère
   python3 tools/cues_to_srt.py render/cues_en.json waiff/captions_en.srt --wrap 42
   ```
3. Les **étiquettes papier à l'écran restent en français** (décision du film : elles font partie de l'image ; les re-traduire = refaire la scène). Seuls les sous-titres changent.
4. **DEMANDER** à l'utilisateur de relire l'anglais (ou au moins le titre et les 10 premières lignes).

## B. Rendre la version anglaise

`render.py` lit trois variables d'environnement : `CUES` (fichier de sous-titres), `SEGDIR` (dossier des segments), `EMPH` (mots en jaune).
```bash
cd render
export CUES=$PWD/cues_en.json SEGDIR=$PWD/segs_en EMPH='DeepSeek|BYD|Huawei|Tencent|Shenzhen|Nvidia|Honor|Tesla|ASPI|R1|China|copied|copy|study'
python3 render.py still 20 100 200          # regarde : sous-titres anglais, pas de débordement
python3 ../tools/render_plan.py 12 100      # puis chaque lot :  python3 render.py seg …
cd ..
SEGDIR=render/segs_en ENC=/tmp/vh24_en OUT=waiff/<Pays>_<Nom>_<Prénom>_<Catégorie>_<Titre>.mp4 bash tools/assemble.sh enc $(seq 0 23)   # par lots
SEGDIR=render/segs_en ENC=/tmp/vh24_en OUT=waiff/<…>.mp4 bash tools/assemble.sh mux
unset CUES SEGDIR EMPH
```
(La valeur exacte d'`EMPH` utilisée le 11/11 n'a pas été sauvegardée ; celle ci-dessus est l'équivalent anglais de la liste française.)
`ENC` doit être un **autre dossier** que pour la version française, sinon `mux` mélange les segments.

Nommage du film (règle du festival WAIFF, appliquée) : `Senegal_Moreau_Emilio_AI-Short-Film_La-Chine-ne-copie-plus.mp4` → `Pays_Nom_Prénom_Catégorie_Titre`, sans espace ni accent.

## C. Le dossier

| Fichier | Contenu | Comment |
|---|---|---|
| `still.jpg` | image fixe 1920×1080 **sans sous-titre** | `python3 tools/make_still.py 365.8 waiff/still.jpg` (film : scène finale, robot qui dépasse le coureur) — choisis l'image la plus forte du film |
| `presentation.md` | titre FR + titre EN proposé, réalisateur (pays), catégorie, durée, format, langue ; synopsis court FR et EN (~120 mots chacun) | rédiger à partir du script ; aucun fait absent du film |
| `journal-de-production.md` | FR + EN : résumé du procédé ; tableau étape / outils / rôle de l'IA / **rôle humain** ; tableau des modèles et licences ; marques et personnalités citées ; part humaine | chaque ligne qui décrit le travail personnel de l'utilisateur est marquée **[À CONFIRMER PAR <NOM>]** : tu ne sais pas ce qu'il a fait lui-même |
| `bio-TODO.md` | gabarit de bio FR/EN avec des [CROCHETS] à remplir + liste des infos du formulaire | **n'invente rien** de la biographie |

Modèles exacts : copie ceux de `reference/doc-chine/waiff/` et remplace le contenu.

## D. Ce que l'utilisateur doit fournir (DEMANDER, une liste, une seule fois)
Bio, e-mail personnel pour l'inscription (pas un e-mail professionnel/scolaire s'il ne veut pas), date de naissance et pays (si le formulaire les exige),
pièce d'identité à garder sous la main, relecture des lignes [À CONFIRMER] et des sous-titres anglais. Rappelle la date limite **avec le fuseau**
(WAIFF Africa : 31/12/2026 23:59 GMT).

## Contrôles
- STOP si `en_lines.txt` n'a pas exactement le nombre de cues.
- STOP si un sous-titre anglais déborde (stills) ou dépasse 2 lignes dans le `.srt`.
- `bash tools/check_video.sh waiff/<…>.mp4 <TOTAL>` : mêmes critères que le film français.
- STOP si la durée du film sort des limites du festival (WAIFF AI Short Film : 5 à 15 min ; le film : 6 min 12).
- STOP si le journal de production affirme un travail humain non confirmé.

## Problèmes rencontrés et solutions
- **Même minutage, autre langue** : on a gardé les minutages français (cues) et remplacé le texte ligne à ligne ; c'est simple et toujours synchrone.
- **Encodage long** : comme pour le film français, par segments (`assemble.sh enc`), écriture dans `/tmp` (faststart).
- **Infos personnelles manquantes** : on prépare tout avec des cases à remplir et on n'invente rien ; on ne dépose rien.
