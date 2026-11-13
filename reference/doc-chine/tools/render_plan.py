#!/usr/bin/env python3
"""Découpe le rendu en lots de segments qui tiennent chacun sous ~100 s de calcul (limite 120 s par commande
dans le bac à sable Hark ; sur un PC normal tu peux tout lancer d'un coup).
Usage : python3 tools/render_plan.py [fps_mesurés=12] [secondes_max=100]
Affiche une commande par lot, à lancer une par une :  cd render && python3 render.py seg 0 1 2
"""
import os, sys, math
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'render'); sys.path.insert(0, D); os.chdir(D)
import render
fps = float(sys.argv[1]) if len(sys.argv) > 1 else 12; smax = float(sys.argv[2]) if len(sys.argv) > 2 else 100
lots, cur, n = [], [], 0
for i in range(len(render.SCN)):
    f0, f1 = render.frames_of(i); k = f1 - f0
    if cur and (n + k) / fps > smax: lots.append(cur); cur, n = [], 0
    cur.append(i); n += k
lots.append(cur)
for l in lots: print('python3 render.py seg ' + ' '.join(map(str, l)))
print('# total', math.ceil(render.SC.TOTAL * render.FPS), 'frames,', len(render.SCN), 'segments,', len(lots), 'lots')
