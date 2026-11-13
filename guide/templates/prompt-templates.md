# Modèles de prompts (Qwen-Image 2.1, style collage papier)

Prompt final = `subject` [+ ` ` + CHROMA si cutout] + `\nStyle: ` + STYLE — assemblé automatiquement par `kaggle/build_img_prompts.py`.
Négatif : `text, letters, words, numbers, logo, watermark, signature, blurry, low quality` · 20 étapes · guidance 4.0.

## STYLE (ne jamais modifier)
Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.

## CHROMA (découpes seulement)
Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.

## Gabarits de `subject`
| Usage | Gabarit |
|---|---|
| Décor de lieu | `Full-frame 16:9 background plate: <lieu, époque, 3-4 détails concrets>, made of layered torn paper and halftone engraved photo cut-outs, <ciel/fond : pale dusty-blue sky with torn white paper clouds | aged cream paper sky>, <calm and empty center>.` |
| Décor « abstrait » sombre | `Full-frame 16:9 background plate: a dark <couleur> paper sheet printed with <motif gros et contrasté>, torn paper edges at the corners, subtle grain, calm and empty center.` (éviter « faint » : sortie presque vide) |
| Carte | `Full-frame 16:9 background plate: a vintage engraved map of <région> on aged paper (coastline and rivers only, no labels), <accent : red route line / torn yellow strips>, soft shadows.` |
| Objet compact (1024²) | `One <objet>, <vu de face/côté, incliné>, as a black-and-white halftone engraved photograph cut out with scissors, thin white paper border following its silhouette, <one warm-yellow accent on …>, centered.` |
| Objet posé au sol (1472×832) | `<objet> seen from the side, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, flat bottom edge, centered.` |
| Bande (1664×640) | `A long horizontal strip of <foule/rangée>, …, cut out with a thin white scissor border along the top, flat bottom edge.` |
| Objet haut (832×1248) | `One <tour/éolienne/pylône>, full height, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, flat bottom edge, vertical, centered.` |
| Miniature | `Full-frame 16:9 cinematic collage poster: <sujet choc> printed as black-and-white halftone engraved photograph(s) cut out with thin white scissor borders, on the right <half / two thirds>, over a torn deep-red paper background with <one warm-yellow torn paper element>, the left third left as plain empty red paper.` |

À éviter : texte, chiffres, marques, logos, personnes réelles, objets verts en découpe, « green trees » dans un décor.
