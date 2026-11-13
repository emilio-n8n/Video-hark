# usage: python3 render.py seg <i> [<i> ...]  |  still <t> [...]  |  list
import sys, json, os, math, subprocess, time
from vx import *
import scenes as SC

ROOTD = os.path.dirname(os.path.abspath(__file__))
CUES = json.load(open(os.environ.get('CUES') or os.path.join(ROOTD, 'cues.json')))
SCN = SC.scenes()
SEG = os.environ.get('SEGDIR') or os.path.join(ROOTD, 'segs'); os.makedirs(SEG, exist_ok=True)
STILL = os.path.join(ROOTD, 'stills'); os.makedirs(STILL, exist_ok=True)

def cue_at(t):
    for c in CUES:
        if c['start'] - 0.05 <= t < c['end'] + 0.12: return c['text']
    return None

def frame(t, fi=None):
    if fi is None: fi = int(t * FPS)
    tq = math.floor(t * FPS) / FPS
    s = next(x for x in SCN if x['a'] <= tq < x['b'] or x is SCN[-1])
    cam = Cam(tq - s['a'], s['b'] - s['a'], s['zoom'], s['drift'])
    fr = draw_plate(s['plate'], cam, s['pdepth'], s['dark']).convert('RGBA')
    for it in s['items']: it.draw(fr, tq, cam)
    c = cue_at(tq)
    if c: draw_caption(fr, c, os.environ.get('EMPH', SC.EMPH))
    return finish(fr.convert('RGB'), fi)

def frames_of(i):
    s = SCN[i]; f0 = math.ceil(s['a'] * FPS - 1e-6); f1 = math.ceil(s['b'] * FPS - 1e-6)
    if i == 0: f0 = 0
    return f0, f1

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'list':
        for i, s in enumerate(SCN): print(i, s['plate'], round(s['a'], 2), round(s['b'], 2), frames_of(i))
        print('total frames', math.ceil(SC.TOTAL * FPS))
    elif cmd == 'still':
        for a in sys.argv[2:]:
            t = float(a); frame(t).save(os.path.join(STILL, f's{t:07.2f}.jpg'), quality=88); print('still', t)
    elif cmd == 'seg':
        for a in sys.argv[2:]:
            i = int(a); f0, f1 = frames_of(i); t0 = time.time()
            out = os.path.join(SEG, f'seg{i:02d}.mp4')
            p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                  '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS), out + '.tmp.mp4'], stdin=subprocess.PIPE)
            for fi in range(f0, f1):
                p.stdin.write(frame(fi / FPS, fi).tobytes())
            p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out)
            print('seg', i, f1 - f0, 'frames', round(time.time() - t0, 1), 's', flush=True)
