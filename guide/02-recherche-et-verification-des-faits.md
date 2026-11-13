# 02 — Recherche et vérification des faits

Un documentaire ne vaut que par ses chiffres. Le film de référence a **20+ faits chiffrés** ; chacun est relié à une source
ouverte dans `reference/doc-chine/output/sources.md`. Fais pareil.

## Entrées
- Le plan de l'étape 01.

## Actions

1. Pour chaque chapitre, liste 3 à 5 **affirmations candidates** (un chiffre, une date, un nom, un record).
2. Pour chaque affirmation, trouve **une source primaire** (organisme qui produit la donnée) et si possible **une seconde source** (presse sérieuse) :

| Type de fait | Source primaire à privilégier (exemples du film) |
|---|---|
| PIB, revenu, pauvreté | Banque mondiale (`data.worldbank.org`, rapports) |
| Énergie, batteries, voitures électriques | AIE / IEA (Global EV Outlook), agences nationales (NEA via gov.cn) |
| Robots industriels | IFR World Robotics |
| Recherche / technologies critiques | ASPI Critical Technology Tracker |
| Records sportifs | World Athletics |
| Entreprises, bourse | rapports de l'entreprise, Bloomberg, Reuters, CNBC, Forbes, CnEVPost |
| Population d'une ville | bureau de statistiques local |
| Livre / théorie | référence complète (auteur, titre, éditeur, année) |

3. **Ouvre la page** de chaque source (pas seulement l'extrait du moteur de recherche) et recopie le chiffre exact + l'URL + la date de la donnée dans un brouillon `script/faits.md` :
   `- [chapitre] affirmation | valeur exacte | unité/date | URL 1 | URL 2`
4. Arrondis **à la baisse et honnêtement** dans le texte parlé, en gardant le vrai chiffre à l'écran ou dans les sources :
   - 314 100 habitants (1979) → « environ trois cent mille » ; 18,25 millions → « plus de dix-huit millions » ;
   - 13 862 $ → « dépasse treize mille huit cents dollars » ; 13 862 / 157 = 88,3 → « près de quatre-vingt-dix fois ».
5. **Chiffres contestés** : dis-le dans la phrase. Référence : « DeepSeek affirme avoir dépensé environ 5,6 millions de dollars… un chiffre que des analystes contestent » + à l'écran « 5,6 M$* » et « * chiffre contesté par des analystes ».
6. **Comparaisons** : vérifie que les deux côtés sont mesurés pareil (même année, même unité). Référence : Chine ~4 000 TWh renouvelables vs UE-27 ~3 800 TWh consommés (2025).
7. **Faits datés au présent** : ajoute la date à l'écran (« record humain, mars 2026 »). Et **refais la vérification juste avant publication** (étape 09).
8. Copie la liste finale dans `output/sources.md` (format : voir `reference/doc-chine/output/sources.md` et `guide/templates/sources-template.md`).

## Les faits du film de référence (exemples de bon niveau de précision)

| Fait dit | Valeur sourcée | Source |
|---|---|---|
| Robot Honor, semi-marathon de Pékin, 19/04/2026 | 50:26 ; vainqueur robot 2025 : 2:40:42 | Xinhua, Reuters, Korea Times |
| Record humain du semi-marathon | 57:20, Jacob Kiplimo, Lisbonne, 8/03/2026 (**battu depuis** : 56:51, Yomif Kejelcha, 23/08/2026) | World Athletics |
| Revenu par habitant Chine | 157 $ (1978) → 13 862 $ (2025), dollars courants | Banque mondiale |
| Population de Shenzhen | 314 100 (1979) → 18,25 M (fin 2025) | bureau des statistiques de Shenzhen |
| Pauvreté | ~800 M de personnes, ~3/4 du recul mondial | Banque mondiale (2022) |
| Nvidia le 27/01/2025 | −589 Md$ (record sur une journée) | Bloomberg, Forbes |
| ASPI | Chine en tête dans **69 des 74** technologies critiques (2021-2025) ; **3** en 2003-2007 | ASPI |
| Éolien + solaire 2025 | > 430 GW raccordés ; dépasse le thermique ; ~4 000 TWh renouvelables | Xinhua / NEA |
| Batteries / VE 2025 | > 80 % des cellules ; ~3/4 des VE produits | AIE, Global EV Outlook 2026 |
| BYD vs Tesla 2025 | 2,26 M VE vs 1,64 M livraisons | CnEVPost, CNBC |
| Robots industriels 2024 | 295 000 installés en Chine, 54 % du monde, 57 % de fournisseurs chinois | IFR |
| Ray Dalio | *Principles for Dealing with the Changing World Order* (2021) | livre |

## Sorties
- `script/faits.md` (brouillon) et `output/sources.md` (propre).

## Contrôles
- STOP si un fait du script n'a pas d'URL dans `sources.md`.
- STOP si une URL n'a pas été ouverte par toi.
- STOP si deux sources donnent des valeurs différentes et que tu n'as pas choisi la plus prudente (et noté pourquoi).
- STOP si un chiffre « record / premier / plus grand » n'a pas sa date.

## Problèmes rencontrés et solutions
- **ASPI « 3 contre 69 »** : il faut bien deux périodes distinctes (2003-2007 : la Chine menait dans 3 technologies ; 2021-2025 : 69 sur 74). Ne pas mélanger « 74 technologies suivies » et « 69 menées ». Le script dit : « suit soixante-quatorze technologies… en tête dans soixante-neuf… au milieu des années deux mille, elle n'en menait que trois ».
- **Un fait devient faux après l'écriture** : le record humain 57:20 (mars 2026) a été battu le 23/08/2026 (Kejelcha 56:51). Le film le dit encore au présent. Solution prévue : soit dater dans la voix (« le record de l'époque »), soit refaire la phrase TTS. **DEMANDER** à l'utilisateur laquelle avant publication ; ne pas corriger en douce.
- **Chiffre annoncé par l'entreprise elle-même** (coût DeepSeek) : toujours « affirme », « annoncé », + astérisque à l'écran.
