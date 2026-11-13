# Scene plan of "La Chine : du pays qui copiait au pays qu'on étudie". All times absolute (narration seconds).
import json, os
from vx import *

ROOTD = os.path.dirname(os.path.abspath(__file__))
TL = {x['id']: x for x in json.load(open(os.path.join(ROOTD, '..', 'build', 'timeline.json')))}
def T(i): return TL[i]['start']
def E(i): return TL[i]['end']
TOTAL = E('p5_l10') + 2.5

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

    # ---------------- HOOK
    sc(0, 'plate-race', [
        Strip(strip('Pékin · 19 avril 2026 · 7 h 30', 58, seed=2, rot=-1.5), 70, 120, at=0.5, enter='left', anchor='l', until=T('p0_l01') + 2.5),
        Cut('crowd', 960, 1080, 330, at=0.0, enter='none', anchor='b', depth=0.8),
        Cut('robot-run', 1900, 990, 640, at=T('p0_l01') + 0.2, enter='none', anchor='b', depth=1.0, bob=10),
        Fn(lambda fr, t, cam: None),
    ])
    # robot crossing from right to left during l01 (scripted with Fn below)
    rob = S_[-1]['items'][2]
    def robot_path(fr, t, cam, r=rob):
        p = min(1, max(0, (t - T('p0_l01')) / 4.2)); p = 1 - (1 - p) ** 2
        r.x = 2200 - 1100 * p
    S_[-1]['items'][3] = Fn(robot_path)
    S_[-1]['items'] = [S_[-1]['items'][3]] + S_[-1]['items'][:3]

    sc(T('p0_l02') - 0.2, 'plate-race', [
        Cut('finish-arch', 960, 700, 700, at=0, enter='none', depth=0.7),
        Cut('robot-run', 640, 1000, 560, at=0, enter='none', anchor='b', depth=1.0, bob=8),
        Counter(1380, 300, 0, 50 * 60 + 26, T('p0_l02') + 0.6, T('p0_l02') + 2.6, mmss, size=170, label='robot Honor, 2026', seed=7),
        Counter(1380, 590, 57 * 60 + 20, 57 * 60 + 20, T('p0_l03'), T('p0_l03') + 0.1, mmss, size=110, label='record humain, mars 2026', seed=8, at=T('p0_l03') + 3.5),
        Strip(strip('2025 : vainqueur robot en 2 h 40', 54, seed=9, rot=1.2), 1380, 800, at=T('p0_l04') + 0.3, enter='right', anchor='c'),
    ], zoom=0.05)

    sc(T('p0_l05') - 0.15, 'thumb-a', [
        Strip(strip('Honor', 120, fnt=BLACK, seed=11, rot=-2), 330, 330, at=T('p0_l05') + 3.6, enter='pop'),
        Strip(strip('fabricant chinois de smartphones', 48, fnt=SERIF_I, seed=12), 330, 470, at=T('p0_l05') + 5.0, enter='left'),
        Strip(strip('« La Chine copie »', 92, seed=13, rot=-3, color=WHITE), 380, 330, at=T('p0_l06') + 0.4, enter='pop', until=T('p0_l08')),
        Line((90, 350), (670, 300), at=T('p0_l07') + 0.3, width=16, until=T('p0_l08')),
    ], zoom=0.07, drift=(20, -10))
    # the Honor strips leave when the quote lands
    S_[-1]['items'][0].until = T('p0_l06'); S_[-1]['items'][1].until = T('p0_l06')

    sc(T('p0_l08') - 0.1, 'plate-village', [
        Strip(strip('moins de 0,50 $ par jour', 76, seed=14, color=YEL), 960, 300, at=T('p0_l08') + 4.8, enter='pop'),
    ], zoom=0.05, dark=0.0)

    # ---------------- CHAPTER 1
    c1 = E('p0_l08') + 0.25
    sc(c1, 'plate-village', [
        chapter_card(1, 'De la misère à Shenzhen', c1 + 0.1, T('p1_l00') + 0.6),
        Strip(strip('1978', 160, fnt=BLACK, seed=15, rot=-2), 400, 330, at=T('p1_l00') + 0.7, enter='pop', until=T('p1_l02')),
        Counter(1420, 360, 0, 157, T('p1_l01') + 4.0, T('p1_l01') + 5.6, money, size=150, label='revenu par habitant et par an', seed=16, until=T('p1_l03') + 3),
        Cut('bicycles', 820, 1020, 380, at=T('p1_l02'), enter='left', anchor='b', depth=1.0),
        Strip(strip('Deng Xiaoping : « réforme et ouverture »', 54, seed=17), 70, 120, at=T('p1_l02') + 0.6, enter='left', anchor='l', until=T('p1_l03') + 3),
    ])

    sc(T('p1_l04') - 0.15, 'border-river', [
        Strip(strip('Shenzhen', 70, fnt=BLACK, seed=18, color=YEL), 1450, 230, at=T('p1_l04') + 6.0, enter='pop'),
        Strip(strip('Hong Kong', 54, seed=19), 420, 230, at=T('p1_l04') + 2.4, enter='pop'),
        Strip(strip('zone économique spéciale · 1980', 46, fnt=SERIF_I, seed=20), 1450, 340, at=T('p1_l04') + 6.6, enter='right'),
    ], zoom=0.06, drift=(-40, 0))

    sc(T('p1_l05') - 0.15, 'plate-race', [
        Cut('skyline-sz', 960, 1080, 720, at=T('p1_l06') - 0.2, enter='up', anchor='b', depth=0.9),
        Counter(960, 330, 0, 300000, T('p1_l05') + 1.6, T('p1_l05') + 3.6, intsp, size=140, label='habitants en 1979', seed=21, until=T('p1_l06') - 0.3, exit='up'),
        Counter(960, 330, 300000, 18000000, T('p1_l06') + 0.6, T('p1_l06') + 2.8, lambda v: (f"{v/1e6:.1f}".replace('.', ',') + ' M') if v >= 1e6 else intsp(v), size=150, label='habitants fin 2025', seed=22, at=T('p1_l06')),
        Cut('cranes', 1600, 1090, 420, at=T('p1_l07') + 0.3, enter='right', anchor='b', depth=1.05),
    ], dark=0.0)

    sc(T('p1_l08') - 0.15, 'assembly', [
        Strip(strip('Huawei', 84, fnt=BLACK, seed=23, rot=-2), 420, 260, at=T('p1_l08') + 0.1, enter='pop', until=T('p1_l09')),
        Strip(strip('Tencent', 84, fnt=BLACK, seed=24, rot=1.5), 960, 300, at=T('p1_l08') + 0.8, enter='pop', until=T('p1_l09')),
        Strip(strip('BYD', 84, fnt=BLACK, seed=25, rot=-1), 1500, 260, at=T('p1_l08') + 1.7, enter='pop', until=T('p1_l09')),
        Counter(960, 340, 0, 800, T('p1_l09') + 2.2, T('p1_l09') + 3.8, lambda v: f"{int(round(v))} millions", size=130, label="sortis de l'extrême pauvreté", seed=26, at=T('p1_l09') + 0.2),
        Strip(strip('près des 3/4 du recul mondial de la pauvreté', 54, seed=27, color=YEL), 960, 620, at=T('p1_l10') + 1.4, enter='up'),
    ], zoom=0.05)

    sc(T('p1_l11') - 0.15, 'plate-race', [
        Cut('skyline-sz', 960, 1080, 600, at=0, enter='none', anchor='b', depth=0.8),
        Counter(960, 300, 157, 13800, T('p1_l11') + 3.0, T('p1_l11') + 5.0, money, size=150, label='revenu par habitant, 2025', seed=28),
        Strip(strip('× 90', 150, fnt=BLACK, seed=29, color=YEL, rot=-4), 1500, 560, at=T('p1_l12') + 0.3, enter='pop'),
    ])

    # ---------------- CHAPTER 2
    c2 = E('p1_l12') + 0.25
    sc(c2, 'plate-circuit', [
        chapter_card(2, "L'IA et le choc DeepSeek", c2 + 0.1, T('p2_l00') + 0.8),
        Strip(strip('« Elle fabrique, mais elle n\'invente pas »', 66, seed=30, color=WHITE, rot=-1.5), 960, 420, at=T('p2_l00') + 2.6, enter='pop', until=E('p2_l00')),
        Strip(strip('Janvier 2025', 80, fnt=BLACK, seed=31, color=YEL), 960, 260, at=T('p2_l01'), enter='pop', until=T('p2_l03') + 3),
        Cut('whale', 960, 650, 470, at=T('p2_l02') + 1.6, enter='right', depth=1.0, until=T('p2_l03') + 3),
        Strip(strip('DeepSeek · R1', 80, fnt=BLACK, seed=32), 960, 430, at=T('p2_l02') + 2.2, enter='left', until=T('p2_l03') + 3),
        Strip(strip('Hangzhou', 48, fnt=SERIF_I, seed=33), 1500, 260, at=T('p2_l02') + 1.0, enter='right', until=T('p2_l03') + 3),
    ], zoom=0.05)

    sc(T('p2_l04') - 0.15, 'plate-circuit', [
        Cut('chip', 1450, 600, 520, at=0, enter='up', depth=1.0),
        Counter(620, 380, 0, 5.6, T('p2_l04') + 2.2, T('p2_l04') + 3.8, lambda v: f"{v:.1f}".replace('.', ',') + ' M$*', size=150, label='coût de calcul annoncé', seed=34),
        Strip(strip('* chiffre contesté par des analystes', 42, fnt=SERIF_I, seed=35, color=WHITE), 620, 640, at=T('p2_l04') + 6.4, enter='left'),
        Strip(strip('puces bridées', 66, fnt=BLACK, seed=36, color=YEL, rot=-6), 1450, 330, at=T('p2_l05') + 1.6, enter='pop'),
    ], zoom=0.05)

    sc(T('p2_l06') - 0.15, 'servers', [
        Cut('arrow-down', 1450, 560, 640, at=T('p2_l06') + 2.6, enter='down', depth=1.0),
        Counter(640, 380, 0, -589, T('p2_l06') + 3.0, T('p2_l06') + 4.8, lambda v: f"−{abs(int(round(v)))} Md$" if v < -0.5 else '0 $', size=140, label='Nvidia en bourse, 27 janvier 2025', seed=37, numink=RED),
        Strip(strip('record historique sur une journée', 52, seed=38, color=YEL), 640, 640, at=T('p2_l07') + 0.6, enter='left'),
    ], zoom=0.07)

    sc(T('p2_l08') - 0.15, 'plate-map', [
        Strip(strip('ASPI · 74 technologies critiques', 64, seed=39), 960, 160, at=T('p2_l09') + 1.0, enter='down'),
        Bars(960, 600, [('2021-2025 : technologies où la Chine est en tête', 69, RED, T('p2_l10') + 5.0), ('2003-2007 : technologies où la Chine est en tête', 3, SEPIA, T('p2_l11') + 0.8)], 74, width=1000, fmt=lambda v: f"{int(round(v))}", at=T('p2_l10') + 0.2),
    ], zoom=0.04)

    # ---------------- CHAPTER 3 (re-hook: black cut, then the pylon)
    c3 = E('p2_l11') + 0.25
    sc(c3, 'plate-desert', [
        chapter_card(3, 'Énergie et batteries', c3 + 0.1, T('p3_l00') - 0.1),
        Black(T('p3_l00') - 0.05, T('p3_l00') + 2.0),
        Cut('pylon', 1400, 1100, 860, at=T('p3_l00') + 2.0, enter='up', anchor='b', depth=1.0),
        Strip(strip("sans électricité, pas d'IA", 60, seed=41, color=YEL), 520, 330, at=T('p3_l00') + 2.2, enter='left'),
    ], zoom=0.05)

    sc(T('p3_l02') - 0.15, 'solarfarm', [
        Cut('turbine', 1600, 1100, 820, at=T('p3_l02') + 3.0, enter='up', anchor='b', depth=1.0),
        Counter(620, 330, 0, 430, T('p3_l02') + 3.4, T('p3_l02') + 5.2, lambda v: f"{int(round(v))} GW", size=170, label='éolien + solaire raccordés en 2025', seed=42),
        Strip(strip('en une seule année', 62, fnt=SERIF_I, seed=43, color=YEL, rot=-2), 620, 600, at=T('p3_l03') + 0.1, enter='pop'),
        Strip(strip('vent + soleil > thermique', 58, fnt=BLACK, seed=44), 620, 760, at=T('p3_l04') + 2.0, enter='left'),
    ], zoom=0.06)

    sc(T('p3_l05') - 0.15, 'plate-desert', [
        Cut('solar', 960, 1080, 330, at=0, enter='up', anchor='b', depth=1.0),
        Counter(960, 300, 0, 4000, T('p3_l05') + 2.2, T('p3_l05') + 4.2, lambda v: f"≈ {intsp(v)} TWh", size=140, label='production renouvelable de la Chine, 2025', seed=45),
        Strip(strip("plus que toute la consommation de l'UE à 27", 56, seed=46, color=YEL), 960, 580, at=T('p3_l06') + 1.0, enter='up'),
    ])

    sc(T('p3_l07') - 0.15, 'plate-factory', [
        Cut('battery', 1500, 620, 600, at=T('p3_l07') + 0.5, enter='up', depth=1.0),
        Counter(640, 380, 0, 80, T('p3_l08') + 3.0, T('p3_l08') + 5.0, lambda v: f"> {int(round(v))} %", size=190, label='des cellules de batteries du monde, 2025', seed=47),
        Strip(strip('et encore plus pour les matériaux', 52, fnt=SERIF_I, seed=48, color=YEL), 640, 680, at=T('p3_l09') + 1.6, enter='left'),
    ])

    # ---------------- CHAPTER 4
    c4 = E('p3_l09') + 0.25
    def cars(fr, t, cam):
        pass
    sc(c4, 'car-ship', [
        chapter_card(4, 'Voitures et robots', c4 + 0.1, T('p4_l00') + 0.6),
        Strip(strip('≈ 3 voitures électriques sur 4', 68, fnt=BLACK, seed=50, color=YEL), 960, 200, at=T('p4_l01') + 3.5, enter='down'),
        Strip(strip('produites en Chine en 2025', 50, fnt=SERIF_I, seed=51), 960, 320, at=T('p4_l01') + 4.5, enter='down'),
    ] + [Cut('ev-car', 330 + i * 420, 860, 220, at=T('p4_l01') + 3.8 + i * 0.35, enter='left' if i < 3 else 'right', depth=1.0) for i in range(4)], zoom=0.05)

    sc(T('p4_l02') - 0.15, 'plate-factory', [
        Strip(strip('BYD · fondée à Shenzhen en 1995', 56, seed=52), 70, 120, at=T('p4_l02') + 1.0, enter='left', anchor='l'),
        Bars(960, 560, [('BYD', 2.26, RED, T('p4_l02') + 8.4), ('Tesla', 1.64, BLUE, T('p4_l03') + 0.6)], 2.95, width=1000, fmt=lambda v: f"{v:.2f}".replace('.', ',') + ' M', title='voitures 100 % électriques vendues en 2025', at=T('p4_l02') + 7.8),
        Strip(strip('dépassé', 72, fnt=BLACK, seed=53, color=YEL, rot=-7), 1560, 760, at=T('p4_l04') + 2.6, enter='pop'),
    ], zoom=0.04)

    sc(T('p4_l05') - 0.15, 'weld-line', [
        Cut('robot-arm', 1500, 1080, 640, at=T('p4_l05') + 0.6, enter='right', anchor='b', depth=1.0, until=T('p4_l09') - 0.2),
        Counter(640, 330, 0, 295000, T('p4_l06') + 3.2, T('p4_l06') + 5.2, intsp, size=150, label='robots industriels installés en 2024', seed=54, until=T('p4_l09') - 0.2),
        Strip(strip('> 1 sur 2 dans le monde', 64, fnt=BLACK, seed=55, color=YEL), 640, 600, at=T('p4_l07') + 0.4, enter='left', until=T('p4_l09') - 0.2),
        Strip(strip('majorité de marques chinoises', 52, fnt=SERIF_I, seed=56), 640, 730, at=T('p4_l08') + 1.4, enter='left', until=T('p4_l09') - 0.2),
        Cut('robot-run', 960, 1060, 640, at=T('p4_l09'), enter='up', anchor='b', depth=1.0, bob=8),
    ], zoom=0.05)

    # ---------------- CHAPTER 5
    c5 = E('p4_l09') + 0.25
    sc(c5, 'plate-map', [
        chapter_card(5, 'Ce que ça change', c5 + 0.1, T('p5_l00') + 0.4),
        Strip(strip('Ray Dalio · 500 ans d\'empires', 60, seed=60), 70, 110, at=T('p5_l00') + 1.0, enter='left', anchor='l', until=T('p5_l04') + 7),
        Cut('ship-dutch', 330, 520, 380, at=T('p5_l00') + 4.0, enter='up', depth=1.0, until=T('p5_l04') + 7),
        Strip(strip('Provinces-Unies', 40, seed=61), 330, 760, at=T('p5_l00') + 4.2, enter='up', until=T('p5_l04') + 7),
        Cut('train-steam', 760, 560, 250, at=T('p5_l00') + 5.6, enter='up', depth=1.0, until=T('p5_l04') + 7),
        Strip(strip('Royaume-Uni', 40, seed=62), 760, 760, at=T('p5_l00') + 5.8, enter='up', until=T('p5_l04') + 7),
        Cut('skyscraper', 1170, 520, 440, at=T('p5_l00') + 6.9, enter='up', depth=1.0, until=T('p5_l04') + 7),
        Strip(strip('États-Unis', 40, seed=63), 1170, 760, at=T('p5_l00') + 7.1, enter='up', until=T('p5_l04') + 7),
        Cut('train-hsr', 1640, 570, 150, at=T('p5_l04') + 4.6, enter='right', depth=1.0, until=T('p5_l04') + 7),
        Strip(strip('Chine ?', 48, fnt=BLACK, seed=64, color=YEL), 1640, 760, at=T('p5_l04') + 4.8, enter='up', until=T('p5_l04') + 7),
        Strip(strip('éduquer · innover · produire', 56, fnt=SERIF_I, seed=65), 960, 950 - 70, at=T('p5_l02') + 0.2, enter='up', until=T('p5_l03')),
        Strip(strip('dette · divisions · déclin', 56, fnt=SERIF_I, seed=66, color=WHITE), 960, 950 - 70, at=T('p5_l03') + 0.2, enter='up', until=T('p5_l04')),
    ], zoom=0.04, drift=(0, -6))

    sc(T('p5_l05') - 0.15, 'plate-village', [
        Strip(strip("Rien n'est écrit", 96, seed=67), 960, 220, at=T('p5_l05') + 0.1, enter='pop', until=T('p5_l07')),
        Strip(strip('population en recul en 2025', 52, seed=68, rot=-1.5), 520, 470, at=T('p5_l06') + 2.6, enter='left', until=T('p5_l07')),
        Strip(strip('immobilier en crise', 52, seed=69, rot=1.2), 1400, 470, at=T('p5_l06') + 4.3, enter='right', until=T('p5_l07')),
        Strip(strip('tensions commerciales', 52, seed=70, rot=-0.8), 960, 640, at=T('p5_l06') + 5.6, enter='up', until=T('p5_l07')),
    ], dark=0.15, zoom=0.04)

    sc(T('p5_l07') - 0.15, 'plate-race', [
        Cut('skyline-sz', 960, 1080, 640, at=0, enter='up', anchor='b', depth=0.85),
        Strip(strip('copier', 90, fnt=BLACK, seed=71, color=WHITE, rot=-2), 600, 300, at=T('p5_l08') + 0.8, enter='pop'),
        Line((440, 320), (770, 280), at=T('p5_l08') + 1.6, width=16),
        Strip(strip('étudier', 90, fnt=BLACK, seed=72, color=YEL, rot=2), 1320, 300, at=T('p5_l08') + 3.2, enter='pop'),
    ], zoom=0.05)

    sc(T('p5_l09') - 0.15, 'thumb-b', [
        Strip(strip('Le prochain record ?', 84, seed=73, color=WHITE, rot=-1.5), 70, 160, at=T('p5_l09') + 1.0, enter='left', anchor='l'),
        Strip(strip('Chine', 64, fnt=BLACK, seed=74, color=YEL), 300, 470, at=T('p5_l10') + 2.0, enter='pop'),
        Strip(strip('États-Unis', 64, fnt=BLACK, seed=75), 300, 600, at=T('p5_l10') + 2.6, enter='pop'),
        Strip(strip('Europe', 64, fnt=BLACK, seed=76, color=BLUE), 300, 730, at=T('p5_l10') + 3.4, enter='pop'),
    ], zoom=0.06, drift=(15, -8))

    for i, s in enumerate(S_):
        s['b'] = S_[i + 1]['a'] if i + 1 < len(S_) else TOTAL
    return S_

EMPH = 'DeepSeek|BYD|Huawei|Tencent|Shenzhen|Nvidia|Honor|Tesla|ASPI|R1|Chine|copiait|copier|étudient'
