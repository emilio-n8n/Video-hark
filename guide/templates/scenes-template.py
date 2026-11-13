# Plan des scènes d'un nouveau film. Copie dans render/scenes.py et remplis. Tous les temps sont absolus (secondes de narration).
# Modèle complet et réel : reference/doc-chine/render/scenes.py
import json, os
from vx import *

ROOTD = os.path.dirname(os.path.abspath(__file__))
TL = {x['id']: x for x in json.load(open(os.path.join(ROOTD, '..', 'build', 'timeline.json')))}
def T(i): return TL[i]['start']          # début de la phrase i
def E(i): return TL[i]['end']            # fin de la phrase i
LAST = list(TL)[-1]
TOTAL = E(LAST) + 2.5

def money(v): return f"{int(round(v)):,}".replace(',', ' ') + ' $'
def intsp(v): return f"{int(round(v)):,}".replace(',', ' ')
def mmss(v):
    s = int(round(v)); return f"{s // 60}:{s % 60:02d}"

def chapter_card(n, title, at, until):
    img = strip('', lines=[(f'Chapitre {n}', 44, SERIF_I, RED), (title, 92, SERIF, INK)], seed=40 + n, padx=50, pady=26, align='center')
    return Strip(img, W / 2, 470, at=at, enter='pop', until=until, exit='up')

def scenes():
    S_ = []
    def sc(a, plate_, items, zoom=0.06, drift=(-30, -8), dark=0.0, pdepth=0.4):
        S_.append(dict(a=a, plate=plate_, items=items, zoom=zoom, drift=drift, dark=dark, pdepth=pdepth))

    # ---------------- ACCROCHE (scène 0 commence à 0)
    sc(0, 'plate-<lieu>', [
        Strip(strip('<Lieu · date · heure>', 58, seed=2, rot=-1.5), 70, 120, at=0.5, enter='left', anchor='l', until=T('p0_l01') + 2.5),
        Cut('<objet>', 960, 1060, 600, at=T('p0_l01') + 0.2, enter='up', anchor='b', bob=8),
        Counter(1380, 300, 0, 100, T('p0_l02') + 0.6, T('p0_l02') + 2.6, intsp, size=170, label='<légende datée>', seed=7),
    ], zoom=0.05)

    # ---------------- CHAPITRE 1 (commence 0,25 s après la fin de l'accroche, avec sa carte)
    c1 = E('p0_l08') + 0.25                      # <- remplace p0_l08 par la DERNIÈRE phrase de l'accroche
    sc(c1, 'plate-<decor>', [
        chapter_card(1, '<Titre du chapitre 1>', c1 + 0.1, T('p1_l00') + 0.6),
        # un élément nouveau toutes les 3 à 5 s, calé sur le mot dit ; rien d'important sous y ≈ 900
    ])
    # scène suivante dans le même chapitre : sc(T('p1_l04') - 0.15, '<autre décor>', [...])

    # ... chapitres 2 à 5 sur le même modèle ...

    for i, s in enumerate(S_):
        s['b'] = S_[i + 1]['a'] if i + 1 < len(S_) else TOTAL
    return S_

EMPH = '<NomPropre1>|<NomPropre2>|<mot-clé>'   # mots en jaune dans les sous-titres
