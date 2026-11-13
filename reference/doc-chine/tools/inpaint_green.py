#!/usr/bin/env python3
"""Répare un décor (plate) qui contient des taches vert chroma ratées (feuillage raté de Qwen-Image).

Cas réel : images/orig/plate-race.png (deux grosses taches vertes dans le ciel et les immeubles)
  -> images/plate-race.png. Méthode utilisée le 11/11/2026 : inpainting OpenCV Telea à 1/4 de résolution
  + détail haute fréquence « emprunté » ailleurs dans l'image pour que la zone ne soit pas lisse.
[Video-hark] Script reconstitué (la commande du 11/11 n'a pas été sauvegardée) : même méthode,
résultat très proche mais pas identique au pixel. Toujours garder l'original dans images/orig/.

Usage : python3 tools/inpaint_green.py images/orig/plate-race.png images/plate-race.png [seuil=8]
Dépendances : pip install opencv-python-headless numpy pillow
STOP si le masque couvre plus de 35 % de l'image : régénérer l'image (autre seed) au lieu de la réparer.
"""
import sys
import numpy as np, cv2
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]; thr = float(sys.argv[3]) if len(sys.argv) > 3 else 8
a = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
m = ((g - np.maximum(r, b)) > thr) & (g > 80)                      # pixels nettement verts
m = cv2.morphologyEx(m.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
m = cv2.dilate(m, np.ones((41, 41), np.uint8))                    # marge autour des taches (franges vertes)
cover = (m > 0).mean(); print(f'masque : {cover * 100:.1f} % de l\'image')
if cover > 0.35: sys.exit('STOP : trop de vert, régénérer l\'image')
H, W = m.shape; q = 4
small = cv2.resize(a.astype(np.uint8), (W // q, H // q), interpolation=cv2.INTER_AREA)
ms = cv2.resize(m, (W // q, H // q), interpolation=cv2.INTER_NEAREST)
fill = cv2.inpaint(small, ms, 9, cv2.INPAINT_TELEA)
fill = cv2.resize(fill, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)
# détail haute fréquence emprunté : même image décalée horizontalement (zone voisine sans tache)
hf = a - cv2.GaussianBlur(a, (0, 0), 3)
shift = W // 4
hf_b = np.where((np.roll(m, shift, 1) > 0)[..., None], np.roll(hf, -shift, 1), np.roll(hf, shift, 1))
out = fill + hf_b * 0.8
soft = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 6)[..., None]   # fondu des bords du masque
res = a * (1 - soft) + out * soft
Image.fromarray(res.clip(0, 255).astype(np.uint8)).save(dst); print('ok ->', dst)
