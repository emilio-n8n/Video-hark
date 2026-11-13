#!/usr/bin/env python3
"""Image fixe 1920x1080 SANS sous-titre (pour un festival / une affiche) : une frame du film rendue par render.py.
Usage : python3 tools/make_still.py [temps_s=365.8] [sortie=waiff/still.jpg]
Le still du WAIFF = scène 23 (décor thumb-b, robot qui dépasse le coureur, bande « Le prochain record ? »),
juste avant l'arrivée des bandes Chine / États-Unis / Europe (≈ 365,8 s).
[Video-hark] script reconstitué ; l'image produite diffère de waiff/still.jpg de ~4/255 en moyenne (grain + JPEG).
"""
import os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(D, 'render')); os.chdir(os.path.join(D, 'render'))
import render
render.CUES[:] = []                       # pas de sous-titre sur une image fixe
t = float(sys.argv[1]) if len(sys.argv) > 1 else 365.8
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(D, 'waiff', 'still.jpg')
render.frame(t).save(out, quality=92); print('still', t, '->', out)
