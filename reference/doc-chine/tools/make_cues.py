#!/usr/bin/env python3
"""Fabrique render/cues.json (sous-titres brûlés) + output/captions.srt à partir de :
  - build/timeline.json         (début/fin de chaque phrase dite, en secondes)
  - render/captions_lines.json  ({id: texte AFFICHÉ}, chiffres en chiffres : « 19 avril 2026 », « 1,69 m », « 295 000 »)

[Video-hark] Les cues du film (render/cues.json) ont été découpées le 27/10/2026 par une commande non sauvegardée.
Ce script applique les mêmes règles mais ne reproduit PAS les coupures au caractère près. Pour le film Chine,
garder render/cues.json tel quel. Pour un NOUVEAU film, utiliser ce script.

Règles :
  1. une phrase de <= MAXC caractères (45) = une seule cue, de start à end de la phrase ;
  2. sinon couper en n = ceil(longueur/MAXC) morceaux de longueur équilibrée, à l'espace la plus proche de chaque cible,
     en préférant une coupure juste après , : ; . ? ! (pas de mot orphelin du type « secondes. ») ;
  3. ne JAMAIS couper à l'intérieur d'un nombre ni entre un nombre et son unité (« 295 000 », « 7 h 30 », « 100 % », « 50 minutes ») — défaut vu dans le film :
     « ... installé 295 » / « 000 robots industriels. » ;
  4. durée de chaque morceau proportionnelle à son nombre de caractères (approximation du débit de la voix).
Usage : python3 tools/make_cues.py [MAXC]
"""
import json, os, re, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MAXC = int(sys.argv[1]) if len(sys.argv) > 1 else 45
TL = json.load(open(os.path.join(D, 'build', 'timeline.json')))
CL = json.load(open(os.path.join(D, 'render', 'captions_lines.json')))
NUM_GLUE = re.compile(r'(?<=\d) (?=\d{3}\b)|(?<=\d) (?=[a-zà-ÿ%$M])|(?<=\bh) (?=\d)')  # 295 000 · 50 minutes · 7 h 30 · 100 % · 2,26 M

def split(text):
    """n = ceil(longueur / MAXC) morceaux équilibrés ; coupure à l'espace la plus proche de chaque cible,
    bonus de 8 caractères pour une coupure juste après une ponctuation ; jamais dans un nombre."""
    import math
    glued = NUM_GLUE.sub('\u00a0', text)
    if len(glued) <= MAXC: return [text]
    words = glued.split(' '); n = math.ceil(len(glued) / MAXC)
    ends = []; pos = 0
    for w in words[:-1]: pos += len(w); ends.append(pos); pos += 1   # position de fin de chaque mot (sauf le dernier)
    cuts = []
    for k in range(1, n):
        target = k * len(glued) / n
        best = min((i for i in range(len(ends)) if not cuts or i > cuts[-1]),
                   key=lambda i: abs(ends[i] - target) - (8 if words[i][-1:] in ',:;.?!' else 0))
        cuts.append(best)
    out = []; prev = 0
    for c in cuts + [len(words) - 1]:
        out.append(' '.join(words[prev:c + 1]).replace('\u00a0', ' ')); prev = c + 1
    return [o for o in out if o]

cues = []
for L in TL:
    parts = split(CL[L['id']]); tot = sum(len(p) for p in parts); t = L['start']; d = L['end'] - L['start']
    for i, p in enumerate(parts):
        e = L['end'] if i == len(parts) - 1 else round(t + d * len(p) / tot, 3)
        cues.append(dict(id=L['id'], start=round(t, 3), end=round(e, 3), text=p)); t = e
json.dump(cues, open(os.path.join(D, 'render', 'cues.json'), 'w'), ensure_ascii=False, indent=1)
print(len(cues), 'cues ; plus longue :', max(len(c['text']) for c in cues), 'caractères')
