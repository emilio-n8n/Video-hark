#!/usr/bin/env python3
"""Sous-titres anglais : une ligne de render/en_lines.txt par cue de render/cues.json, MÊMES minutages.
Usage : python3 tools/make_cues_en.py   -> render/cues_en.json
Règle : en_lines.txt doit avoir exactement autant de lignes que cues.json (135 dans le film). Sinon STOP.
[Video-hark] script reconstitué ; reproduit render/cues_en.json à l'identique (vérifié)."""
import json, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'render')
C = json.load(open(os.path.join(D, 'cues.json')))
EN = [l.rstrip('\n') for l in open(os.path.join(D, 'en_lines.txt'), encoding='utf-8') if l.strip()]
assert len(EN) == len(C), f'STOP : {len(EN)} lignes anglaises pour {len(C)} cues'
json.dump([dict(c, text=e) for c, e in zip(C, EN)], open(os.path.join(D, 'cues_en.json'), 'w'), ensure_ascii=False, indent=1)
print(len(C), 'cues anglais')
