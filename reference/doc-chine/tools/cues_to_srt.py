#!/usr/bin/env python3
"""cues.json -> .srt  (mêmes minutages, numérotés à partir de 1).
Usage : python3 tools/cues_to_srt.py render/cues.json output/captions.srt
        python3 tools/cues_to_srt.py render/cues_en.json waiff/captions_en.srt --wrap 42
--wrap N : un texte de plus de N caractères est coupé en 2 lignes à l'espace le plus proche du milieu
           (utilisé pour la version anglaise du festival ; la version française n'est pas coupée).
[Video-hark] script reconstitué ; reproduit captions.srt à l'identique et captions_en.srt au dernier saut de ligne près (vérifié)."""
import json, sys
def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
C = json.load(open(sys.argv[1]))
WRAP = int(sys.argv[sys.argv.index('--wrap') + 1]) if '--wrap' in sys.argv else 0
def wrap(t):
    if not WRAP or len(t) <= WRAP: return t
    sp = [i for i, ch in enumerate(t) if ch == ' ']; i = min(sp, key=lambda i: abs(i - len(t) / 2))
    return t[:i] + '\n' + t[i + 1:]
out = ''.join(f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{wrap(c['text'])}\n\n" for i, c in enumerate(C, 1))
open(sys.argv[2], 'w').write(out); print(len(C), 'sous-titres ->', sys.argv[2])
