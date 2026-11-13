# Vox-style paper-collage frame renderer (PIL + numpy), 12 fps stop-motion clock, 1920x1080.
import math, os, json, random, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1920, 1080, 12
ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, 'img')          # raw generated images (png)
LAY = os.path.join(ROOT, 'layers')       # keyed cut-outs
# [Video-hark] polices : $VX_FONTS, sinon la copie du dépôt (third_party/), sinon le chemin d'origine (repo cloné)
FONTS = next(p for p in [os.environ.get('VX_FONTS') or '', os.path.join(ROOT, '..', '..', '..', 'third_party', 'video-agent-skills', 'fonts'),
                         os.path.join(ROOT, '..', 'repo', 'skills', 'short-editing', 'engine', 'fonts')] if p and os.path.isdir(p))
os.makedirs(LAY, exist_ok=True)

INK = (28, 24, 22); CREAM = (240, 230, 208); PAPER = (232, 220, 194); YEL = (238, 184, 52)
RED = (188, 46, 38); BLUE = (120, 150, 170); SEPIA = (150, 110, 70); WHITE = (250, 246, 236)

@functools.lru_cache(None)
def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)
SERIF = 'InstrumentSerif-Regular.ttf'; SERIF_I = 'InstrumentSerif-Italic.ttf'; BLACK = 'ArchivoBlack.ttf'; SANS = 'Archivo.ttf'

def S(x, w=14):
    return 0.0 if x <= 0 else 1 - (1 + w * x) * math.exp(-w * x)

def rng(seed):
    return random.Random(seed)

# ------------------------------------------------------------------ images
@functools.lru_cache(None)
def plate(name):
    p = os.path.join(IMG, name + '.png')
    im = Image.open(p).convert('RGB')
    # cover 16:9 then prescale to 1.12x for push-in headroom
    tw, th = int(W * 1.12), int(H * 1.12)
    r = max(tw / im.width, th / im.height)
    im = im.resize((math.ceil(im.width * r), math.ceil(im.height * r)), Image.LANCZOS)
    l, t = (im.width - tw) // 2, (im.height - th) // 2
    return im.crop((l, t, l + tw, t + th))

@functools.lru_cache(None)
def cutout(name):
    """chroma-key the green background, despill, crop, return RGBA."""
    cache = os.path.join(LAY, name + '.png')
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(os.path.join(IMG, name + '.png')):
        return Image.open(cache).convert('RGBA')
    a = np.asarray(Image.open(os.path.join(IMG, name + '.png')).convert('RGB')).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(r, b)
    gd = g - mx                                  # green dominance
    alpha = np.clip(1 - (gd - 18) / 40, 0, 1)    # >58 = fully keyed
    alpha[g < 60] = 1
    # despill
    g2 = np.where(gd > 0, mx + gd * 0.15, g)
    out = np.dstack([r, g2, b, alpha * 255]).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(out, 'RGBA')
    # clean speckles: erode/dilate alpha a bit
    al = im.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    im.putalpha(al)
    bb = al.point(lambda v: 255 if v > 40 else 0).getbbox()
    if bb: im = im.crop(bb)
    im.save(cache)
    return im

@functools.lru_cache(maxsize=512)
def scaled(name, h, flip=False, kind='cut'):
    im = cutout(name) if kind == 'cut' else name_img(name)
    w = max(1, round(im.width * h / im.height))
    s = im.resize((w, h), Image.LANCZOS)
    if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
    return with_shadow(s)

_named = {}
def name_img(n): return _named[n]

def with_shadow(im, off=(7, 10), blur=9, op=0.42):
    pad = blur * 2 + max(off)
    can = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (60, 40, 25, 0))
    sh.putalpha(im.getchannel('A').point(lambda v: int(v * op)))
    can.alpha_composite(sh, (pad + off[0], pad + off[1]))
    can = can.filter(ImageFilter.GaussianBlur(blur / 2))
    can.alpha_composite(im, (pad, pad))
    can.info['pad'] = pad
    return can

# ------------------------------------------------------------------ paper strips / cards
def torn_poly(w, h, seed, jag=7, step=18):
    R = rng(seed); pts = []
    for x in range(0, w + 1, step): pts.append((x, R.uniform(0, jag)))
    for y in range(0, h + 1, step): pts.append((w - R.uniform(0, jag), y))
    for x in range(w, -1, -step): pts.append((x, h - R.uniform(0, jag)))
    for y in range(h, -1, -step): pts.append((R.uniform(0, jag), y))
    return pts

def paper_tex(w, h, color, seed):
    R = np.random.default_rng(seed)
    n = R.normal(0, 1, (h // 4 + 1, w // 4 + 1)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 20) + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)).astype(np.float32) - 128
    f = R.normal(0, 6, (h, w)).astype(np.float32)
    base = np.array(color, np.float32)[None, None, :] + (n * 0.35 + f)[..., None]
    return Image.fromarray(base.clip(0, 255).astype(np.uint8), 'RGB')

def strip(text, size=64, fnt=SERIF, color=CREAM, ink=INK, padx=34, pady=18, seed=1, rot=0.0, w=None, lines=None, align='left', emph=None, emph_color=RED):
    """torn paper strip with text. lines: list of (text, size, font, ink)"""
    if lines is None: lines = [(text, size, fnt, ink)]
    dummy = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    meas = []
    for t, sz, fn, ik in lines:
        f = font(fn, sz); bb = dummy.textbbox((0, 0), t, font=f); meas.append((bb[2] - bb[0], sz))
    tw = max(m[0] for m in meas); th = sum(int(m[1] * 1.12) for m in meas)
    ww = w or tw + padx * 2; hh = th + pady * 2
    tex = paper_tex(ww, hh, color, seed).convert('RGBA')
    mask = Image.new('L', (ww, hh), 0); ImageDraw.Draw(mask).polygon(torn_poly(ww, hh, seed), fill=255)
    # white fibrous rim
    rim = Image.new('RGBA', (ww + 12, hh + 12), (0, 0, 0, 0))
    rmask = Image.new('L', (ww + 12, hh + 12), 0); ImageDraw.Draw(rmask).polygon([(x + 6 + rng(seed + 9).uniform(-3, 3), y + 6 + rng(int(x + y)).uniform(-3, 3)) for x, y in torn_poly(ww, hh, seed)], fill=255)
    rmask = rmask.filter(ImageFilter.MaxFilter(5))
    rim.paste((248, 244, 234, 255), (0, 0), rmask)
    tex.putalpha(mask)
    rim.alpha_composite(tex, (6, 6))
    d = ImageDraw.Draw(rim); y = pady + 6
    for (t, sz, fn, ik), (mw, _) in zip(lines, meas):
        f = font(fn, sz)
        x = 6 + (padx if align == 'left' else (ww - mw) // 2)
        bb = d.textbbox((0, 0), t, font=f)
        d.text((x - bb[0], y - bb[1] + int(sz * 0.06)), t, font=f, fill=ik)
        y += int(sz * 1.12)
    if rot: rim = rim.rotate(rot, Image.BICUBIC, expand=True)
    return with_shadow(rim, off=(5, 8), blur=8, op=0.38)

# ------------------------------------------------------------------ grain / vignette
@functools.lru_cache(None)
def grain(i):
    R = np.random.default_rng(100 + i)
    n = R.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    g = Image.fromarray((n * 40 + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    return g

@functools.lru_cache(None)
def vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    v = np.clip((d - 0.75) / 0.7, 0, 1) ** 1.6 * 0.42
    a = (v * 255).astype(np.uint8)
    im = Image.new('RGBA', (W, H), (40, 24, 12, 0)); im.putalpha(Image.fromarray(a)); return im

def finish(frame, fi):
    # grain in overlay-ish blend (cheap): add (g-128)*k
    a = np.asarray(frame, np.int16)
    g = np.asarray(grain(fi % 2), np.int16)[..., None] - 128
    a = (a + (g * 0.16)).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(a, 'RGB').convert('RGBA')
    im.alpha_composite(vignette())
    return im.convert('RGB')

# ------------------------------------------------------------------ camera
class Cam:
    def __init__(self, t, dur, zoom=0.06, drift=(-30, -8), seed=0):
        p = min(1.0, max(0.0, t / max(dur, 0.01)))
        self.z = 1 + zoom * p
        self.dx, self.dy = drift[0] * p, drift[1] * p
    def tr(self, x, y, depth):
        z = 1 + (self.z - 1) * depth
        return W / 2 + (x - W / 2) * z + self.dx * depth, H / 2 + (y - H / 2) * z + self.dy * depth, z

def draw_plate(name, cam, depth=0.4, dark=0.0, tint=None):
    im = plate(name)
    z = 1 + (cam.z - 1) * depth
    cw, ch = W / (z * 1.0), H / (z * 1.0)
    # the prescaled plate is 1.12x: base view = central W x H region
    cx, cy = im.width / 2 - cam.dx * depth, im.height / 2 - cam.dy * depth
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    fr = im.resize((W, H), Image.BILINEAR, box=box)
    if dark: fr = Image.blend(fr, Image.new('RGB', (W, H), (20, 16, 14)), dark)
    return fr

def paste(frame, im, x, y, anchor='c'):
    """paste RGBA (with shadow pad) so that the visible image's anchor is at x,y"""
    pad = im.info.get('pad', 0)
    vw, vh = im.width - 2 * pad, im.height - 2 * pad
    if anchor == 'c': ox, oy = x - vw / 2, y - vh / 2
    elif anchor == 'b': ox, oy = x - vw / 2, y - vh
    elif anchor == 'tl': ox, oy = x, y
    elif anchor == 'l': ox, oy = x, y - vh / 2
    elif anchor == 'r': ox, oy = x - vw, y - vh / 2
    frame.alpha_composite(im, (int(round(ox - pad)), int(round(oy - pad)))) if frame.mode == 'RGBA' else frame.paste(im, (int(round(ox - pad)), int(round(oy - pad))), im)

def enter_offset(style, e, dist=1300):
    k = 1 - e
    return {'left': (-dist * k, 0), 'right': (dist * k, 0), 'up': (0, 900 * k), 'down': (0, -900 * k), 'pop': (0, 0), 'none': (0, 0)}[style]

# ------------------------------------------------------------------ items
class Item:
    at = 0; until = 1e9
    def draw(self, fr, t, cam): pass

class Cut(Item):
    """a cut-out layer: name, centre (x,y) or bottom anchor, height, entrance"""
    def __init__(self, name, x, y, h, at=0, enter='up', until=1e9, exit='down', depth=1.0, anchor='c', flip=False, bob=0, wiggle=1, rot=0, w=10, swap=None):
        self.__dict__.update(locals()); del self.__dict__['self']
    def draw(self, fr, t, cam):
        if t < self.at or t > self.until + 0.8: return
        e = S(t - self.at, self.w) if self.enter != 'none' else 1
        ox, oy = enter_offset(self.enter, e)
        if t > self.until:
            e2 = S(t - self.until, 10); ex, ey = enter_offset(self.exit, 1 - e2); ox += ex; oy += ey
        sc = 1.0
        if self.enter == 'pop': sc = 0.6 + 0.4 * e
        fi = int(t * FPS)
        if self.bob: oy += self.bob * (math.sin(fi * 1.6) * 0.5 + 0.5) * -1
        if self.wiggle: R = rng(fi // 2 * 31 + hash(self.name) % 97); ox += R.uniform(-1, 1) * self.wiggle; oy += R.uniform(-1, 1) * self.wiggle
        x, y, z = cam.tr(self.x + ox, self.y + oy, self.depth)
        h = max(8, int(round(self.h * z * sc / 4) * 4))
        name = self.name
        if self.swap and (fi // 3) % 2: name = self.swap
        im = scaled(name, h, self.flip)
        if self.rot: im = im.rotate(self.rot, Image.BICUBIC, expand=True); im.info['pad'] = 0
        paste(fr, im, x, y, self.anchor)

class Strip(Item):
    def __init__(self, img, x, y, at=0, enter='left', until=1e9, exit='left', depth=1.1, anchor='c', w=12):
        self.__dict__.update(locals()); del self.__dict__['self']
    def draw(self, fr, t, cam):
        if t < self.at or t > self.until + 0.8: return
        e = S(t - self.at, self.w); ox, oy = enter_offset(self.enter, e, 1500)
        if t > self.until: ex, ey = enter_offset(self.exit, 1 - S(t - self.until, 10), 1500); ox += ex; oy += ey
        im = self.img
        if self.enter == 'pop' and e < 0.999:
            s = 0.7 + 0.3 * e; im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR); im.info['pad'] = int(self.img.info['pad'] * s)
        x, y, _ = cam.tr(self.x + ox, self.y + oy, self.depth)
        paste(fr, im, x, y, self.anchor)

class Counter(Item):
    """number on a paper card that counts from a to b between t0 and t1"""
    def __init__(self, x, y, a, b, t0, t1, fmt, size=150, label=None, at=None, until=1e9, color=CREAM, ink=INK, numink=None, w=None, seed=5, enter='pop', label_size=46, strike_at=None, exit='down'):
        self.__dict__.update(locals()); del self.__dict__['self']
        if self.at is None: self.at = t0 - 0.3
        f = font(BLACK, size); d = ImageDraw.Draw(Image.new('RGB', (4, 4)))
        wmax = max(d.textbbox((0, 0), fmt(v), font=f)[2] for v in (a, b, (a + b) / 2))
        lw = d.textbbox((0, 0), label, font=font(SERIF_I, label_size))[2] if label else 0
        self.cw = w or int(max(wmax, lw) + 90); self.ch = int(size * 1.08 + (label_size * 1.3 if label else 0) + 50)
        self.card = strip_card(self.cw, self.ch, color, seed)
    def val(self, t):
        if t <= self.t0: return self.a
        if t >= self.t1: return self.b
        p = (t - self.t0) / (self.t1 - self.t0); p = 1 - (1 - p) ** 3
        return self.a + (self.b - self.a) * p
    def draw(self, fr, t, cam):
        if t < self.at or t > self.until + 0.8: return
        e = S(t - self.at, 12); ox, oy = enter_offset(self.enter if self.enter != 'pop' else 'none', e, 1500)
        if t > self.until: ex, ey = enter_offset(self.exit, 1 - S(t - self.until, 10), 1500); ox += ex; oy += ey
        x, y, _ = cam.tr(self.x + ox, self.y + oy, 1.1)
        card = self.card.copy(); d = ImageDraw.Draw(card); pad = card.info['pad'] = self.card.info['pad']
        f = font(BLACK, self.size); s = self.fmt(self.val(t)); bb = d.textbbox((0, 0), s, font=f)
        tx = pad + (self.cw - (bb[2] - bb[0])) / 2 - bb[0]; ty = pad + 24 - bb[1]
        d.text((tx, ty), s, font=f, fill=self.numink or self.ink)
        if self.label:
            lf = font(SERIF_I, self.label_size); lb = d.textbbox((0, 0), self.label, font=lf)
            d.text((pad + (self.cw - (lb[2] - lb[0])) / 2 - lb[0], pad + 24 + self.size * 1.08 + 4 - lb[1]), self.label, font=lf, fill=self.ink)
        if self.strike_at is not None and t > self.strike_at:
            p = min(1, (t - self.strike_at) / 0.4)
            y0 = pad + 24 + self.size * 0.55
            d.line([(pad + 20, y0 + 14), (pad + 20 + (self.cw - 40) * p, y0 - 14)], fill=RED, width=max(10, self.size // 12))
        if self.enter == 'pop' and e < 0.999:
            s2 = 0.75 + 0.25 * e; card = card.resize((int(card.width * s2), int(card.height * s2)), Image.BILINEAR); card.info['pad'] = int(pad * s2)
        paste(fr, card, x, y)

@functools.lru_cache(None)
def strip_card(w, h, color, seed):
    tex = paper_tex(w, h, color, seed).convert('RGBA')
    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).polygon(torn_poly(w, h, seed, jag=9, step=22), fill=255)
    rim = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0))
    rmask = Image.new('L', (w + 12, h + 12), 0); ImageDraw.Draw(rmask).polygon([(x + 6, y + 6) for x, y in torn_poly(w, h, seed + 3, jag=9, step=22)], fill=255)
    rim.paste((248, 244, 234, 255), (0, 0), rmask.filter(ImageFilter.MaxFilter(7)))
    tex.putalpha(mask); rim.alpha_composite(tex, (6, 6))
    out = with_shadow(rim, off=(6, 9), blur=9, op=0.4)
    out.info['pad'] = out.info['pad'] + 6
    return out

class Bars(Item):
    """horizontal bars: items = [(label, value, color, at)], max value vmax"""
    def __init__(self, x, y, items, vmax, width=900, bh=78, gap=46, fmt=str, until=1e9, at=None, title=None):
        self.__dict__.update(locals()); del self.__dict__['self']
        if self.at is None: self.at = min(i[3] for i in items) - 0.3
        self.bg = strip_card(width + 120, len(items) * (bh + gap + 40) + (70 if title else 0) + 40, CREAM, 77)
    def draw(self, fr, t, cam):
        if t < self.at or t > self.until + 0.8: return
        e = S(t - self.at, 12); ox, oy = enter_offset('up', e)
        if t > self.until: ex, ey = enter_offset('down', 1 - S(t - self.until, 10)); ox += ex; oy += ey
        x, y, _ = cam.tr(self.x + ox, self.y + oy, 1.1)
        card = self.bg.copy(); d = ImageDraw.Draw(card); pad = card.info['pad'] = self.bg.info['pad']
        cy = pad + 30
        if self.title:
            tf = font(SERIF_I, 48); d.text((pad + 60, cy), self.title, font=tf, fill=INK); cy += 70
        for lab, v, col, at in self.items:
            lf = font(SANS, 38); d.text((pad + 60, cy), lab, font=lf, fill=INK); cy += 46
            p = S(t - at, 6)
            bw = int(self.width * (v / self.vmax) * p)
            if bw > 2:
                R = rng(int(v * 7)); pts = torn_poly(bw, self.bh, int(v), jag=5, step=16)
                d.polygon([(pad + 60 + a, cy + b) for a, b in pts], fill=col)
            vf = font(BLACK, 54); s = self.fmt(v * p)
            d.text((pad + 60 + bw + 18, cy + 6), s, font=vf, fill=INK)
            cy += self.bh + self.gap
        paste(fr, card, x, y)

class Line(Item):
    """red marker strike / underline between two points, drawn over time"""
    def __init__(self, p0, p1, at, dur=0.35, width=14, color=RED, until=1e9):
        self.__dict__.update(locals()); del self.__dict__['self']
    def draw(self, fr, t, cam):
        if t < self.at or t > self.until: return
        p = min(1, (t - self.at) / self.dur)
        x0, y0, _ = cam.tr(*self.p0, 1.1); x1, y1, _ = cam.tr(*self.p1, 1.1)
        ImageDraw.Draw(fr).line([(x0, y0), (x0 + (x1 - x0) * p, y0 + (y1 - y0) * p)], fill=self.color, width=self.width)

class Black(Item):
    def __init__(self, at, until, alpha=1.0):
        self.at, self.until, self.alpha = at, until, alpha
    def draw(self, fr, t, cam):
        if self.at <= t <= self.until: fr.paste((12, 10, 9), (0, 0, W, H))

class Fn(Item):
    def __init__(self, f, at=0, until=1e9): self.f, self.at, self.until = f, at, until
    def draw(self, fr, t, cam):
        if self.at <= t <= self.until: self.f(fr, t, cam)

# ------------------------------------------------------------------ captions
CAP_Y = 1008
@functools.lru_cache(maxsize=256)
def caption_img(text, emph):
    f = font(BLACK, 46)
    d = ImageDraw.Draw(Image.new('RGB', (4, 4)))
    words = text.split(); lines = []; cur = ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if d.textbbox((0, 0), test, font=f)[2] > 1500 and cur: lines.append(cur); cur = w
        else: cur = test
    lines.append(cur)
    lh = 60; hh = lh * len(lines) + 26
    ww = max(d.textbbox((0, 0), l, font=f)[2] for l in lines) + 56
    im = Image.new('RGBA', (ww, hh), (18, 15, 13, 214))
    dd = ImageDraw.Draw(im); y = 12
    em = set(emph.split('|')) if emph else set()
    for l in lines:
        lw = dd.textbbox((0, 0), l, font=f)[2]; x = (ww - lw) / 2
        for w in l.split(' '):
            col = YEL if w.strip('.,:;?!()') in em or any(ch.isdigit() for ch in w) else WHITE
            dd.text((x, y), w, font=f, fill=col); x += dd.textbbox((0, 0), w + ' ', font=f)[2]
        y += lh
    return im

def draw_caption(fr, text, emph=''):
    im = caption_img(text, emph)
    fr.paste(im, (int((W - im.width) / 2), int(CAP_Y - im.height)), im)
