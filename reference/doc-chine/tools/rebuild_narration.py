#!/usr/bin/env python3
"""Reconstruit build/narration.wav + build/timeline.json à partir des phrases TTS (tts/lines/<id>.wav).

[Video-hark] Script reconstitué : le 27/10/2026 cette étape a été faite en ligne de commande, sans fichier.
Il reproduit À L'ÉCHANTILLON PRÈS les fichiers du film (vérifié). Règles :
  - 0,60 s de silence au début
  - 0,32 s entre deux phrases d'un même chapitre
  - 2,50 s entre deux chapitres (0,9 s prévus par le notebook + 1,6 s ajoutées pour la carte de chapitre)
  - 2,50 s de silence à la fin
  - une phrase corrigée (ex. p2_l09) est prise dans build/<id>_fixed.wav si ce fichier existe
Usage : python3 tools/rebuild_narration.py   (depuis reference/doc-chine/ ou n'importe où)
"""
import json, os, wave, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LINES = json.load(open(os.path.join(D, 'kaggle', 'tts_lines.json')))   # [{id, para, text}] dans l'ordre
HEAD, GAP_LINE, GAP_CHAP, TAIL = 0.60, 0.32, 2.50, 2.50
SR = 24000  # Qwen3-TTS sort du 24 kHz mono 16 bits

def read(p):
    w = wave.open(p); assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2, p
    return w.readframes(w.getnframes())
parts = [b'\0\0' * round(HEAD * SR)]; t = HEAD; prev = None; tl = []
for L in LINES:
    if prev is not None:
        g = GAP_CHAP if L['para'] != prev else GAP_LINE
        parts.append(b'\0\0' * round(g * SR)); t += g
    fx = os.path.join(D, 'build', f"{L['id']}_fixed.wav")
    pcm = read(fx if os.path.exists(fx) else os.path.join(D, 'tts', 'lines', f"{L['id']}.wav"))
    d = len(pcm) / 2 / SR
    tl.append(dict(id=L['id'], start=round(t, 3), end=round(t + d, 3), text=None)); parts.append(pcm); t += d; prev = L['para']
parts.append(b'\0\0' * round(TAIL * SR))
# le texte de la timeline = texte du script (paras.json), sans les réécritures phonétiques (B-Y-D, R-1)
paras = json.load(open(os.path.join(D, 'script', 'paras.json')))
txt = {f"p{pi}_l{li:02d}": l for pi, p in enumerate(paras) for li, l in enumerate(p['lines'])}
for x in tl: x['text'] = txt[x['id']]
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, 'build')
os.makedirs(out, exist_ok=True)
w = wave.open(os.path.join(out, 'narration.wav'), 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(b''.join(parts)); w.close()
json.dump(tl, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('narration', round(t + TAIL, 3), 's ;', len(tl), 'phrases ; derniere fin', tl[-1]['end'])
