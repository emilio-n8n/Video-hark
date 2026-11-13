# Les 34 prompts réels du film Chine (Qwen-Image 2.1, 20 étapes, guidance 4.0)

Généré depuis `reference/doc-chine/kaggle/shots.json` + `build_img_prompts.py`. Prompt final = `subject` (+ CHROMA si `cutout`) + saut de ligne + `Style: ` + STYLE.
Négatif (pour toutes) : `text, letters, words, numbers, logo, watermark, signature, blurry, low quality`.

| # | name | kind | taille | seed | scènes (render.py list) | remarque |
|---|---|---|---|---|---|---|
| 1 | `thumb-a` | plate | 1664×928 | 11 | 2 |  |
| 2 | `thumb-b` | plate | 1664×928 | 12 | 23 |  |
| 3 | `plate-race` | plate | 1664×928 | 21 | 0, 1, 6, 8, 22 | taches vertes réparées (tools/inpaint_green.py), original dans images/orig/ |
| 4 | `robot-run` | cutout | 1024×1024 | 22 | 0, 1, 19 |  |
| 5 | `finish-arch` | cutout | 1472×832 | 23 | 1 |  |
| 6 | `crowd` | cutout | 1664×640 | 24 | 0 |  |
| 7 | `stopwatch` | cutout | 1024×1024 | 25 | — | générée mais non utilisée au montage |
| 8 | `plate-village` | plate | 1664×928 | 31 | 3, 4, 21 |  |
| 9 | `bicycles` | cutout | 1472×832 | 32 | 4 |  |
| 10 | `skyline-sz` | cutout | 1664×832 | 33 | 6, 8, 22 |  |
| 11 | `cranes` | cutout | 1472×832 | 34 | 6 |  |
| 12 | `plate-circuit` | plate | 1664×928 | 41 | 9, 10 | sortie presque vide (bleu nuit, pas de circuit visible) : gardée comme fond sombre |
| 13 | `whale` | cutout | 1472×832 | 42 | 9 |  |
| 14 | `chip` | cutout | 1024×1024 | 43 | 10 |  |
| 15 | `arrow-down` | cutout | 1024×1024 | 44 | 11 |  |
| 16 | `servers` | plate | 1664×928 | 45 | 11 |  |
| 17 | `plate-desert` | plate | 1664×928 | 51 | 13, 15 |  |
| 18 | `turbine` | cutout | 832×1248 | 52 | 14 |  |
| 19 | `solar` | cutout | 1664×640 | 53 | 15 |  |
| 20 | `pylon` | cutout | 832×1248 | 54 | 13 |  |
| 21 | `battery` | cutout | 1024×1024 | 55 | 16 |  |
| 22 | `solarfarm` | plate | 1664×928 | 56 | 14 |  |
| 23 | `plate-factory` | plate | 1664×928 | 61 | 16, 18 |  |
| 24 | `ev-car` | cutout | 1472×832 | 62 | 17 |  |
| 25 | `robot-arm` | cutout | 1024×1024 | 63 | 19 |  |
| 26 | `car-ship` | plate | 1664×928 | 64 | 17 |  |
| 27 | `weld-line` | plate | 1664×928 | 65 | 19 |  |
| 28 | `plate-map` | plate | 1664×928 | 71 | 12, 20 |  |
| 29 | `ship-dutch` | cutout | 1024×1024 | 72 | 20 |  |
| 30 | `train-steam` | cutout | 1472×832 | 73 | 20 |  |
| 31 | `skyscraper` | cutout | 832×1248 | 74 | 20 |  |
| 32 | `train-hsr` | cutout | 1664×640 | 75 | 20 |  |
| 33 | `assembly` | plate | 1664×928 | 81 | 7 |  |
| 34 | `border-river` | plate | 1664×928 | 82 | 5 |  |

## Prompts complets

### 1. `thumb-a` (plate, 1664×928, seed 11)

```text
Full-frame 16:9 cinematic collage poster: a sleek white humanoid robot sprinting toward the camera on a city road, mid-stride, leaning forward, printed as a black-and-white halftone engraved photograph cut out with a thin white scissor border, placed on the right half of the frame, over a bold torn deep-red paper background with a few torn warm-yellow paper strips and a faint halftone city skyline at the bottom, strong contrast, the left third of the frame left as plain empty red paper.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 2. `thumb-b` (plate, 1664×928, seed 12)

```text
Full-frame 16:9 cinematic collage poster: a humanoid robot runner overtaking a human marathon runner, both side view, both printed as black-and-white halftone engraved photographs cut out with thin white scissor borders, the robot slightly ahead and larger, on the right two thirds of the frame, over a torn deep-red paper background with one warm-yellow torn paper finish-line ribbon, the left third left as plain empty red paper.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 3. `plate-race` (plate, 1664×928, seed 21)

```text
Full-frame 16:9 background plate: a wide modern Beijing avenue on an early spring morning seen at street level, glass office towers and a few bare trees, crowd barriers along the sides, made of layered torn paper and halftone engraved photo cut-outs, pale dusty-blue morning sky with torn white paper clouds, the center of the road left empty and calm for runners to be placed later.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 4. `robot-run` (cutout, 1024×1024, seed 22)

```text
One sleek humanoid robot running, full body, side view, mid-stride with one knee raised and arms swinging, smooth white and grey panels, as a black-and-white halftone engraved photograph cut out with scissors, thin white paper border following its silhouette, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 5. `finish-arch` (cutout, 1472×832, seed 23)

```text
One wide inflatable finish-line arch over a road, seen from the front, plain surface with no lettering, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, flat bottom edge, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 6. `crowd` (cutout, 1664×640, seed 24)

```text
A long horizontal strip of cheering spectators behind metal crowd barriers, many people seen from the front at waist height, some raising phones, as a black-and-white halftone engraved photograph cut out with a thin white scissor border along the tops of their heads, flat bottom edge. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 7. `stopwatch` (cutout, 1024×1024, seed 25)

```text
One classic silver mechanical stopwatch with a plain dial without numbers, slightly tilted, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, one warm-yellow accent on the crown button, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 8. `plate-village` (plate, 1664×928, seed 31)

```text
Full-frame 16:9 background plate: a poor rural Chinese village landscape in the late 1970s, flooded rice paddies, low mud-brick houses with tiled roofs, distant green hills, made of torn paper layers and sepia halftone engraved photo cut-outs, aged cream paper sky, calm and empty center.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 9. `bicycles` (cutout, 1472×832, seed 32)

```text
A group of workers in 1970s blue work jackets riding old black bicycles, seen from the side, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, flat bottom edge, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 10. `skyline-sz` (cutout, 1664×832, seed 33)

```text
A dense modern skyline of very tall glass skyscrapers of a southern Chinese megacity, one supertall tower in the middle, seen from the front, as a black-and-white halftone engraved photograph cut out with a thin white scissor border along the rooftops, flat bottom edge. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 11. `cranes` (cutout, 1472×832, seed 34)

```text
A container port with three tall ship-to-shore gantry cranes and stacked shipping containers, seen from the side, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, flat bottom edge, one warm-yellow accent on one container. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 12. `plate-circuit` (plate, 1664×928, seed 41)

```text
Full-frame 16:9 background plate: a dark navy-blue paper sheet printed with faint engraved circuit-board traces and tiny dots, torn paper edges at the corners, subtle grain, calm and empty center.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 13. `whale` (cutout, 1472×832, seed 42)

```text
One large whale swimming, side view, as a black-and-white halftone engraved photograph cut out with scissors, thin white paper border following its silhouette, tinted in dusty blue, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 14. `chip` (cutout, 1024×1024, seed 43)

```text
One square computer processor chip with gold pins seen from above at a slight angle, plain top surface with no markings, as a halftone engraved photograph cut out with a thin white scissor border, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 15. `arrow-down` (cutout, 1024×1024, seed 44)

```text
One thick jagged red paper arrow pointing steeply downward like a crashing stock chart line, torn red paper with fibrous edges, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 16. `servers` (plate, 1664×928, seed 45)

```text
Full-frame 16:9 collage scene: a long data center aisle with rows of server racks and blinking lights receding into the distance, as black-and-white halftone engraved photograph layers on aged paper, a few dusty-blue torn paper accents, no text.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 17. `plate-desert` (plate, 1664×928, seed 51)

```text
Full-frame 16:9 background plate: a vast desert plain under a pale dusty-blue sky with a big warm-yellow torn paper sun, low sand dunes of torn sepia paper, distant mountains, made of layered torn paper, calm empty foreground.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 18. `turbine` (cutout, 832×1248, seed 52)

```text
One tall modern three-blade wind turbine, full height, front view, as a black-and-white halftone engraved photograph cut out with a thin white scissor border following its silhouette, vertical, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 19. `solar` (cutout, 1664×640, seed 53)

```text
A long row of tilted solar panels on metal frames seen from the side and slightly above, as a halftone engraved photograph cut out with a thin white scissor border, dusty-blue tint on the panels, flat bottom edge. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 20. `pylon` (cutout, 832×1248, seed 54)

```text
One tall steel high-voltage electricity pylon with hanging cables, full height, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, vertical, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 21. `battery` (cutout, 1024×1024, seed 55)

```text
One large cylindrical lithium-ion battery cell standing upright, plain metal casing without any label, a small warm-yellow lightning-bolt shaped paper piece stuck on it, as a halftone engraved photograph cut out with a thin white scissor border, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 22. `solarfarm` (plate, 1664×928, seed 56)

```text
Full-frame 16:9 collage scene: an immense solar farm covering desert hills seen from high above, endless rows of panels following the terrain, wind turbines on the horizon, as halftone engraved photograph layers on aged paper with dusty-blue and warm-yellow accents, no text.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 23. `plate-factory` (plate, 1664×928, seed 61)

```text
Full-frame 16:9 background plate: the inside of a huge bright modern car factory hall, steel roof trusses, rows of lights, made of layered torn paper and black-and-white halftone engraved photo cut-outs, calm empty center floor.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 24. `ev-car` (cutout, 1472×832, seed 62)

```text
One modern compact electric hatchback car, side view, generic design with no logo and no badges, as a black-and-white halftone engraved photograph cut out with a thin white scissor border following its silhouette, one warm-yellow accent on the charging port, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 25. `robot-arm` (cutout, 1024×1024, seed 63)

```text
One orange-and-grey six-axis industrial robot arm on its base, articulated pose reaching forward, as a halftone engraved photograph cut out with a thin white scissor border, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 26. `car-ship` (plate, 1664×928, seed 64)

```text
Full-frame 16:9 collage scene: a huge roll-on roll-off car carrier ship docked at a port, hundreds of new cars lined up on the quay waiting to board, as black-and-white halftone engraved photograph layers on aged paper, dusty-blue sea of torn paper, no text.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 27. `weld-line` (plate, 1664×928, seed 65)

```text
Full-frame 16:9 collage scene: a car body assembly line with many industrial robot arms welding car frames, bright sparks, as black-and-white halftone engraved photograph layers on aged paper with warm-yellow spark accents, no text, no people.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 28. `plate-map` (plate, 1664×928, seed 71)

```text
Full-frame 16:9 background plate: an antique engraved world map on aged cream paper, oceans in faded dusty blue, coastlines only, no labels and no lettering, a hand-drawn compass rose in a corner, torn paper edges, calm.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 29. `ship-dutch` (cutout, 1024×1024, seed 72)

```text
One seventeenth-century Dutch three-masted sailing ship with full sails, side view, as a black-and-white engraving cut out with a thin white scissor border, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 30. `train-steam` (cutout, 1472×832, seed 73)

```text
One nineteenth-century British steam locomotive with a tall chimney and puffs of smoke, side view, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, flat bottom edge, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 31. `skyscraper` (cutout, 832×1248, seed 74)

```text
One tall 1930s art deco American skyscraper with a stepped spire, full height, as a black-and-white halftone engraved photograph cut out with a thin white scissor border, vertical, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 32. `train-hsr` (cutout, 1664×640, seed 75)

```text
One sleek white modern high-speed bullet train with a long aerodynamic nose, side view, generic livery without any lettering, as a halftone engraved photograph cut out with a thin white scissor border, flat bottom edge, centered. Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, nothing else in the frame, generous green margin around the subject.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 33. `assembly` (plate, 1664×928, seed 81)

```text
Full-frame 16:9 collage scene: a 1990s electronics factory with long rows of workers in light uniforms assembling circuit boards at benches, seen from above at an angle, as black-and-white halftone engraved photograph layers on aged paper with dusty-blue accents, no text.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```

### 34. `border-river` (plate, 1664×928, seed 82)

```text
Full-frame 16:9 collage scene: a narrow river separating green fields and small houses on one bank from a row of high-rise towers on the other bank, as halftone engraved photograph layers on aged paper, dusty-blue torn paper water, no text.
Style: Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.
```
