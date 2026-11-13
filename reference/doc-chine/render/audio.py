# builds build/mix.wav: narration + chapter beds (ducked) + sparse SFX, then loudnorm -14 LUFS / -1.5 dBTP
import json, os, subprocess, wave, numpy as np
import scenes as SC
T, E = SC.T, SC.E
R = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(R, '..', 'build')
# [Video-hark] musiques/bruitages : $VX_ASSETS (doit contenir music/ et sfx/), sinon third_party/, sinon le repo cloné d'origine
SKA = next(p for p in [os.environ.get('VX_ASSETS') or '', os.path.join(R, '..', '..', '..', 'third_party', 'video-agent-skills'),
                       os.path.join(R, '..', 'repo', 'skills', 'short-editing', 'assets')] if p and os.path.isdir(os.path.join(p, 'music')))
TOTAL = SC.TOTAL
def sh(*a): subprocess.run(a, check=True)

# synthesized paper thud
sr = 48000; n = int(0.45 * sr); t = np.arange(n) / sr
f = 75 * np.exp(-t * 3) + 40
th = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 11)
noise = np.convolve(np.random.default_rng(1).normal(0, 1, n), np.ones(40) / 40, 'same') * np.exp(-t * 30) * 0.5
th = (th + noise); th = th / np.abs(th).max() * 0.9
w = wave.open(os.path.join(B, 'thud.wav'), 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((th * 32767).astype(np.int16).tobytes()); w.close()

c2 = E('p1_l12') + 0.25; c4 = E('p3_l09') + 0.25; c5 = E('p4_l09') + 0.25
beds = [(0, c2, 'enquete', 10.7), (c2, c4, 'arpege', 8.0), (c4, c5, 'neon', 9.2), (c5, TOTAL, 'enquete', 42.7)]
# sfx: (time, file, gain dB, peak-align)
sfx = [
    (T('p0_l02') + 2.6, 'impact-boom', -9, True),
    (E('p0_l08') + 0.3, 'zhhh', -8, True),
    (T('p1_l06') + 2.8, 'thud', -6, False),
    (T('p1_l12') + 0.3, 'thud', -6, False),
    (T('p2_l06') + 4.8, 'impact-boom', -10, True),
    (T('p3_l00') - 2.6, 'riser', -14, False),
    (T('p3_l00') - 0.05, 'thud', -4, False),
    (T('p3_l02') + 5.2, 'thud', -6, False),
    (T('p4_l04') + 2.6, 'thud', -6, False),
    (T('p5_l09') + 1.0, 'thud', -7, False),
]
peak_off = {'impact-boom': 0.12, 'zhhh': 0.55}
inputs = ['-i', os.path.join(B, 'narration.wav')]; fc = []
fc.append(f"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad=whole_dur={TOTAL:.2f}[vo]")
fc.append("[vo]asplit=2[voa][vok]")
bl = []
for i, (a, b, bed, off) in enumerate(beds):
    inputs += ['-i', os.path.join(SKA, 'music', bed + '.mp3')]
    k = i + 1; dur = b - a + 2.0
    fc.append(f"[{k}:a]atrim={off}:{off + dur},asetpts=PTS-STARTPTS,aresample=48000,volume=-15dB,afade=t=in:d={0.4 if i == 0 else 1.0},afade=t=out:st={dur - 2.0}:d=2.0,adelay={int(max(0, a - 1.0) * 1000)}|{int(max(0, a - 1.0) * 1000)}[m{i}]")
    bl.append(f"[m{i}]")
fc.append(''.join(bl) + f"amix=inputs={len(bl)}:normalize=0,atrim=0:{TOTAL:.2f},afade=t=out:st={TOTAL - 2.5:.2f}:d=2.5[bed]")
fc.append("[bed][vok]sidechaincompress=threshold=0.02:ratio=5:attack=40:release=450:makeup=1[bedd]")
sl = []
for j, (at, nm, g, pk) in enumerate(sfx):
    k = len(beds) + 1 + j
    p = os.path.join(B, 'thud.wav') if nm == 'thud' else os.path.join(SKA, 'sfx', nm + '.mp3')
    inputs += ['-i', p]
    st = at - (peak_off.get(nm, 0) if pk else 0)
    if nm == 'riser': st = at
    ms = int(max(0, st) * 1000)
    fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms}[s{j}]")
    sl.append(f"[s{j}]")
fc.append('[voa][bedd]' + ''.join(sl) + f"amix=inputs={2 + len(sl)}:normalize=0,atrim=0:{TOTAL:.2f}[mix]")
pre = os.path.join(B, 'premix.wav')
sh('ffmpeg', '-loglevel', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', '[mix]', '-ar', '48000', pre)
# two-pass loudnorm
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', pre, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
js = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
af = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true"
sh('ffmpeg', '-loglevel', 'error', '-y', '-i', pre, '-af', af, '-ar', '48000', os.path.join(B, 'mix.wav'))
print('premix', js['input_i'], js['input_tp'])
