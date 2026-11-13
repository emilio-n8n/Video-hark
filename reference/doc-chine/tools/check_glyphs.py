#!/usr/bin/env python3
"""Vérifie que chaque caractère spécial écrit dans scenes.py / thumb.py / les cues existe dans les polices.
Pourquoi : « ≈ » n'existe pas dans Instrument Serif -> il s'affichait comme un carré vide (corrigé le 11/11/2026 :
la bande est devenue « près des 3/4 du recul… »). Archivo Black, elle, a « ≈ » (« ≈ 4 000 TWh » est correct).
Usage : python3 tools/check_glyphs.py      (pip install fonttools)
Sortie : pour chaque police, la liste des caractères ABSENTS. STOP si un caractère absent est utilisé avec cette police.
"""
import os, re, json, glob
from fontTools.ttLib import TTFont
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
import sys; sys.path.insert(0, os.path.join(D, 'render'))
from vx import FONTS
txt = ''
for p in ['render/scenes.py', 'render/thumb.py']: txt += open(os.path.join(D, p), encoding='utf-8').read()
for p in ['render/cues.json', 'render/cues_en.json']:
    if os.path.exists(os.path.join(D, p)): txt += ''.join(c['text'] for c in json.load(open(os.path.join(D, p))))
chars = sorted(set(ch for ch in txt if ord(ch) > 126))
print('caractères non-ASCII utilisés :', ''.join(chars))
for f in sorted(glob.glob(os.path.join(FONTS, '*.ttf'))):
    cmap = TTFont(f).getBestCmap(); miss = [c for c in chars if ord(c) not in cmap]
    print(f'{os.path.basename(f):32s} absents : {"".join(miss) or "aucun"}')
