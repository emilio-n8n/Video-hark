# 01 — Cadrage et sujet

## Entrées
- La demande de l'utilisateur (dans le film de référence : « un documentaire sur la Chine de 5 min qui s'inspire de https://youtu.be/9FTKLQcbdIM, tu peux utiliser Kaggle »).

## Les SEULES questions que tu as le droit de poser (une seule fois, dans un seul message)

Pose uniquement celles dont la réponse manque dans la demande. Propose la valeur par défaut pour qu'un « oui » suffise.

| # | Question | Valeur par défaut (celle du film) |
|---|---|---|
| Q1 | Quel sujet, et quel angle (la thèse en une phrase) ? | Chine : « du pays qui copiait au pays qu'on étudie » |
| Q2 | Quelle durée ? | 5 à 6 min (le film fait 6 min 12) |
| Q3 | Une vidéo d'inspiration ? | aucune obligatoire |
| Q4 | Langue de la voix et des sous-titres ? | français, sous-titres français incrustés |
| Q5 | Une échéance (festival, date de sortie) ? | aucune |

Tu ne demandes **pas** : le style visuel (c'est le collage papier, étape 06), le modèle de voix ou d'image (étapes 04 et 07),
la musique (étape 05), le titre (étape 10). Tu les choisis avec les règles du guide.

Autres questions marquées « DEMANDER » plus loin (et seulement elles) : token Kaggle (00), accord sur le script (03), choix d'une
correction de fait sensible (02/09), accord avant publication (10), infos personnelles pour un festival (11).

## Actions

1. Si une vidéo d'inspiration est donnée : récupère sa transcription (sous-titres YouTube, ou analyse vidéo) et sauve-la dans
   `script/inspiration.txt`. Note ses **thèmes** (liste à puces). Ne garde aucune phrase.
   - Film de référence : thèmes retenus = semi-marathon des robots de Pékin, sortie de la pauvreté, Shenzhen, DeepSeek et l'IA,
     énergies renouvelables, batteries, BYD et voitures électriques, robots industriels, cycles de puissance (Ray Dalio).
   - Écarté : le segment sponsor de la vidéo, ses formulations, son ordre exact.
2. Écris la **thèse** en une phrase et le **fil rouge** (le fait spectaculaire du début qui sera repris à la fin).
   - Référence : thèse « le pays qu'on accusait de copier est devenu celui que les autres étudient » ; fil rouge = un robot chinois plus rapide que le record humain du semi-marathon.
3. Découpe en **accroche + 5 chapitres** (c'est la structure qui a marché) : chaque chapitre = un pilier de la thèse, du plus ancien au plus récent, puis un chapitre « ce que ça change » avec les limites (contre-arguments honnêtes).
   - Référence : Accroche (le robot) · 1 De la misère à Shenzhen · 2 L'IA et le choc DeepSeek · 3 Énergie et batteries · 4 Voitures et robots · 5 Ce que ça change.
4. Écris tout ça en tête de `PROGRESS.md`.

## Sorties
- `PROGRESS.md` avec : sujet, thèse, fil rouge, durée cible, liste des 6 parties, thèmes de l'inspiration.

## Contrôles
- STOP si la thèse tient en plus d'une phrase.
- STOP si un chapitre n'a pas au moins 2 faits chiffrables (sinon tu n'auras rien à animer).
- STOP si le plan suit l'ordre exact de la vidéo d'inspiration.

## Problèmes rencontrés et solutions
- **L'utilisateur donne peu d'infos** (cas du film) : ne pas le noyer de questions ; appliquer les valeurs par défaut ci-dessus et l'annoncer en une phrase (« je pars sur 6 chapitres, ~6 min, voix off, collages papier »).
- **Tentation de copier l'inspiration** : interdit (règle 5). Le film de référence n'a repris aucune phrase.
