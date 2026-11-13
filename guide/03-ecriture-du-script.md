# 03 — Écriture du script

Méthode : skill `studio-script` du dépôt `video-agent-skills` (copie dans `third_party/video-agent-skills/skills-docs/studio-script/`),
adaptée au format long YouTube. Modèle rempli : `reference/doc-chine/script/script.md`. Gabarit vide : `guide/templates/script-template.md`.

## Entrées
- Plan (01) et faits sourcés (02).

## Règle de longueur (mesurée sur le film)

| Mesure | Valeur du film | Règle pour toi |
|---|---|---|
| Mots lus | 831 | **mots = minutes visées × 134** (ex. 5 min → 670 mots ; 6 min → 800 mots) |
| Débit de la voix seule | 148 mots/min, 15,4 caractères/s | sert à estimer une phrase : durée ≈ caractères / 15 |
| Durée finale | 371,6 s (6 min 12) | inclut les pauses (0,32 s entre phrases, 2,5 s entre chapitres) et 2,5 s de fin |
| Phrases | 65 (9 + 13 + 12 + 10 + 10 + 11) | **une phrase = une ligne = une respiration**, 4 à 25 mots, durée médiane 4,7 s, max 12,5 s |

## Structure obligatoire

```
[HOOK]                         ~9 phrases, ~50 s : scène précise + chiffre choc + contradiction + « pour comprendre, il faut revenir à… »
[CHAPITRE 1 — TITRE]           ~10-13 phrases chacun ; chaque chapitre = 1 pilier de la thèse, avec 2 à 4 chiffres
[CHAPITRE 2 — TITRE]
[CHAPITRE 3 — TITRE]           le 1er vers de ce chapitre (~50 % du film) = la RELANCE (re-hook)
[CHAPITRE 4 — TITRE]
[CHAPITRE 5 — TITRE]           « ce que ça change » : la lecture d'ensemble + les limites honnêtes + la phrase-thèse
                               + la question finale qui reboucle sur l'accroche + l'appel au commentaire avec UN mot exact
```

## Actions

1. **Écris 3 accroches** de 3 formules différentes (`skills-docs/studio-script/references/hooks.md`) et note-les /10 sur 5 critères (0-2 chacun) : spécifique, tension, spectateur, rapide, vrai (`script-rules.md`). Garde la meilleure (≥ 7). Référence :
   1. *Mid-scene* « Pékin, 19 avril 2026, sept heures et demie. Un robot s'élance sur un semi-marathon. » → **9/10, retenue**
   2. *Their words* « "La Chine copie, elle n'invente pas." En 2026, un robot chinois bat le record du monde humain. » → 8/10
   3. *Before/after* « Cent cinquante-sept dollars par an en 1978. Un robot plus rapide que l'homme en 2026. » → 7/10
2. Écris le texte parlé, chapitre par chapitre. Règles :
   - **Les nombres en toutes lettres** (la voix les lit mieux) : « deux mille vingt-six », « cinquante minutes et vingt-six secondes », « cinq virgule six millions ». Les sous-titres, eux, seront en chiffres (étape 08).
   - Une idée concrète par phrase ; jamais 3 phrases abstraites de suite.
   - Une seule vraie question, à la fin.
   - Relance à ~50 % : référence « Mais une IA sans électricité, ce n'est qu'un programme qui attend. »
   - Fin : la thèse en une phrase (« Le pays qu'on accusait de copier est devenu celui que les autres étudient. »), puis la question qui reboucle (« Alors, le prochain robot qui battra un record humain, il viendra d'où ? ») et l'appel précis (« Dites-le en commentaire : Chine, États-Unis ou Europe. »).
   - Chapitre 5 : **les limites** (référence : population en recul, immobilier, tensions commerciales). Un documentaire sans contre-point paraît de la propagande.
3. **Notes visuelles** sous le script : pour chaque chapitre, les mots exacts qui s'afficheront (compteurs, bandes, barres). Ex. « Ch.1 : compteur 157 $ → 13 862 $ ; carte Shenzhen/Hong Kong ; compteur 300 000 → 18 millions ; Huawei/Tencent/BYD ; 800 millions ».
4. **Passe « humanize »** (`skills-docs/studio-script/references/humanize.md` et `ai-tells.md`) :
   - caractères invisibles : `grep -nP '[\x{200B}\x{200C}\x{200D}\x{2060}\x{FEFF}\x{00AD}]' script/script.md` → aucune sortie ;
   - tirets cadratins (—) seulement dans les titres de chapitre (qui ne sont pas lus) ;
   - mots à bannir en français : « plonger », « crucial », « véritable », « révolutionner », « permettre de », « en effet », « ainsi », « dans un monde où » ;
   - pas de « question-réponse » rhétorique, pas de triplets d'adjectifs.
5. **Fabrique `script/paras.json`** : une entrée par partie, `id` = l'en-tête entre crochets, `lines` = les phrases dans l'ordre (voir `guide/templates/paras-template.json`). Les ids de phrases seront `p<partie>_l<numéro sur 2 chiffres>` (`p0_l00` … `p5_l10`).
6. **DEMANDER** à l'utilisateur : « Voici le script (X mots, ~Y min). Je lance la voix et les images ? » Attends son accord.

## Sorties
- `script/script.md` (accroches notées, script, notes visuelles, résultat humanize), `script/paras.json`.

## Contrôles
```bash
python3 - <<'EOF'
import json; p=json.load(open('script/paras.json'))
w=sum(len(l.split()) for x in p for l in x['lines']); n=sum(len(x['lines']) for x in p)
print('parties',len(p),'phrases',n,'mots',w,'durée estimée ~',round(w/134,1),'min')
import re
for x in p:
  for l in x['lines']:
    if re.search(r'\d',l): print('CHIFFRE EN CHIFFRES (à écrire en lettres) :',l)
    if len(l.split())>30: print('PHRASE TROP LONGUE :',l)
EOF
```
- STOP si la durée estimée sort de la cible ±15 %.
- STOP s'il reste un chiffre écrit en chiffres dans `paras.json` (sauf dans un nom propre comme « R1 », traité à l'étape 04).
- STOP si un fait n'est pas dans `output/sources.md`.
- STOP si l'accroche retenue a moins de 7/10.

## Problèmes rencontrés et solutions
- **Sigles mal lus par la voix** : « BYD », « R1 » → réécrits pour la voix seulement (« B-Y-D », « R-1 ») dans `kaggle/build_tts.py`, pas dans le script. Liste-les ici dès l'écriture.
- **Les titres de chapitre** (« CHAPITRE 1 — DE LA MISÈRE À SHENZHEN ») ne sont pas lus : ils deviennent des cartes à l'écran (étape 08).
