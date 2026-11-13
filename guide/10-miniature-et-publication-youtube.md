# 10 — Miniature et préparation de la publication YouTube

Fichiers d'origine : `reference/doc-chine/render/thumb.py`, `output/thumbnail.png`, `output/post.md`, `output/sources.md`.
Gabarit : `guide/templates/post-template.md`.

## A. Miniature (1280×720)

Recette du film (`thumb.py`) :
- fond = l'image `thumb-a` (robot en similigravure sur papier rouge, tiers gauche vide), recadrée en 1280×720 ;
- dégradé sombre sur la gauche (opacité max 45 %) pour la lisibilité ;
- 3 bandes de papier déchiré : **« LA CHINE NE COPIE PLUS »** (Archivo Black 46, blanc, encre rouge, y = 95), **« 50:26 »** (Archivo Black 190, jaune, rotation -3°, y = 300), **« plus vite que l'homme »** (Instrument Serif 70, crème, y = 500) ;
- grain + vignette du film (`finish`).

Règles : 1 chiffre choc énorme, ≤ 6 mots en tout, le sujet (robot) à droite, aucune police autre que celles du film.

```bash
cd render && python3 thumb.py thumb-a        # -> output/thumbnail.png ; "thumbnail ok"
```
Pour un nouveau film : change les 3 textes dans `thumb.py` (et l'image source en argument). Regarde le résultat **réduit à 320×180** (taille réelle sur YouTube) :
`python3 -c "from PIL import Image; Image.open('../output/thumbnail.png').resize((320,180)).save('/tmp/thumb_small.png')"`.
- STOP si le chiffre ou le titre est illisible à 320×180.
- STOP si un texte touche le coin bas droit (YouTube y affiche la durée).

## B. `output/post.md` (titre, description, chapitres, sources)

1. **Titre** : la thèse en ≤ 70 caractères, avec un mot fort. Film : « La Chine ne copie plus : comment elle est devenue le pays qu'on étudie » + 2 variantes notées dessous.
2. **Description** : (a) l'accroche en 2 phrases avec le chiffre choc ; (b) le contenu en 1 paragraphe ; (c) la question finale reprise ; (d) la mention honnête : **« Images d'illustration générées par IA (style collage papier). Voix de synthèse. »**
3. **Chapitres** : un par carte de chapitre, temps = début de la scène de la carte **arrondi à la seconde inférieure**, le premier à `0:00`.
   ```bash
   cd render && python3 -c "
   import scenes as S, render as R
   for i,s in enumerate(R.SCN):   # une carte de chapitre = Strip centré (960, 470), entrée pop, sortie up
     if i==0 or any(type(it).__name__=='Strip' and it.enter=='pop' and it.exit=='up' and it.x==960 and it.y==470 for it in s['items']):
       t=int(s['a']); print(f'{t//60}:{t%60:02d}', s['plate'])"
   ```
   Film : `0:00` Un robot plus rapide que l'homme · `0:51` De la misère à Shenzhen · `2:04` L'IA et le choc DeepSeek · `3:11` Énergie et batteries · `4:06` Voitures et robots · `5:05` Ce que ça change.
   (YouTube exige : premier chapitre à 0:00, au moins 3 chapitres, chacun ≥ 10 s.)
4. **Mots-clés** : 5 hashtags maximum (film : `#Chine #DeepSeek #BYD #Robotique #Géopolitique`).
5. **Sources** : copie intégrale de `output/sources.md`.

## C. Remise à l'utilisateur
Envoie : `output/preview.mp4` (< 50 Mo), `output/thumbnail.png`, le titre et la description. Le MP4 1080p (338 Mo pour le film) se transmet par un lien
(release GitHub, Drive…) car il dépasse les limites des messageries.
**DEMANDER** : « Je publie / tu publies ? » — ne mets rien en ligne sans accord explicite (règle 12).

Au moment de la mise en ligne (par l'utilisateur ou avec son accord) : fichier `documentaire-chine.mp4`, miniature, titre, description avec chapitres,
sous-titres `captions.srt` (langue français), et répondre honnêtement à la question YouTube sur le contenu modifié ou synthétique
(voix de synthèse, images générées : en cas de doute, déclarer).

## Sorties
`output/thumbnail.png`, `output/post.md`, `output/sources.md`, `output/captions.srt`, `output/preview.mp4`.

## Contrôles
- STOP si un chiffre du titre ou de la miniature n'est pas dans le film et dans les sources.
- STOP si les chapitres ne tombent pas sur les cartes de chapitre (vérifie avec `render.py still <temps+1>`).
- STOP si la mention « générées par IA / voix de synthèse » manque.

## Problèmes rencontrés et solutions
- **Miniature faite avant les vraies images** : la première miniature (27/10) utilisait une image provisoire ; elle a été **refaite** le 11/11 depuis la vraie `thumb-a`. Refais toujours la miniature après l'étape 07.
- **Proposition de dire que les images viennent « de Google »** : refusée. C'est faux et ça équivaut à revendiquer des images protégées. La mention honnête est obligatoire (règle 11).
