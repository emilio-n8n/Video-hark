import json, sys
sys.path.insert(0, '.')
import kq
paras = json.load(open('../script/paras.json'))
lines = []
for pi, p in enumerate(paras):
    for li, l in enumerate(p['lines']):
        t = l.replace('BYD', 'B-Y-D').replace(' R1', ' R-1')
        lines.append({"id": f"p{pi}_l{li:02d}", "para": pi, "text": t})
json.dump(lines, open('tts_lines.json', 'w'), ensure_ascii=False, indent=1)
CFG = {"lines": lines}
c1 = r'''
import subprocess, sys
def sh(c): print('$', c); r = subprocess.run(c, shell=True, capture_output=True, text=True); print(r.stdout[-3000:], r.stderr[-3000:]); return r.returncode
sh('nvidia-smi --query-gpu=name,memory.total --format=csv')
sh('pip install -q "transformers==4.57.3" "accelerate>=1.2.0" soundfile qwen-tts openai-whisper')
'''
c2 = "import json\nCFG = json.loads(%r)\n" % json.dumps(CFG, ensure_ascii=False) + r'''
import os, time, inspect, re, unicodedata, traceback, gc
import numpy as np, soundfile as sf, torch
OUT = '/kaggle/working/tts'; os.makedirs(OUT + '/lines', exist_ok=True); os.makedirs(OUT + '/cands', exist_ok=True)
from qwen_tts import Qwen3TTSModel
import whisper, librosa
asr = whisper.load_model('turbo', device='cuda:1' if torch.cuda.device_count() > 1 else 'cuda:0')
def norm(s):
    s = unicodedata.normalize('NFKD', s.lower()); s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()
def cer(a, b):
    a, b = norm(a), norm(b)
    import difflib
    return 1 - difflib.SequenceMatcher(None, a, b).ratio()
def transcribe(path):
    return asr.transcribe(path, language='fr', fp16=True, temperature=0)['text']
def f0med(wav, sr):
    f0, vf, _ = librosa.pyin(wav.astype(np.float32), fmin=60, fmax=300, sr=sr, frame_length=2048)
    f0 = f0[~np.isnan(f0)]
    return float(np.median(f0)) if len(f0) else 0.0
def kw(fn, d):
    p = inspect.signature(fn).parameters
    return {k: v for k, v in d.items() if k in p or any(x.kind == x.VAR_KEYWORD for x in p.values())}
REF_TEXT = "Il y a des histoires qui changent la façon dont on regarde le monde. Celle-ci commence dans un pays pauvre, et se termine dans une course que personne n'avait vue venir."
INSTRUCT = ("Male narrator, about 45 years old, deep warm baritone voice, calm and confident, speaking French with a neutral "
            "standard French accent, measured documentary narration pace, clear articulation, gentle gravitas, studio quality, no background noise.")
design = Qwen3TTSModel.from_pretrained('Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign', device_map='cuda:0', dtype=torch.float16, attn_implementation='sdpa')
print('design sig', inspect.signature(design.generate_voice_design))
cands = []
for i in range(5):
    torch.manual_seed(100 + i)
    with torch.inference_mode():
        wavs, sr = design.generate_voice_design(**kw(design.generate_voice_design, dict(text=REF_TEXT, instruct=INSTRUCT, language='French')))
    w = np.asarray(wavs[0], dtype=np.float32); p = f'{OUT}/cands/cand{i}.wav'; sf.write(p, w, sr)
    tr = transcribe(p); c = cer(REF_TEXT, tr); f0 = f0med(w, sr); dur = len(w) / sr
    cps = len(REF_TEXT) / dur
    score = c * 3 + abs(f0 - 105) / 60 + (0 if 11 <= cps <= 16 else 0.5)
    cands.append(dict(i=i, path=p, cer=c, f0=f0, dur=dur, cps=cps, score=score, tr=tr)); print(cands[-1])
best = min(cands, key=lambda x: x['score']); print('BEST', best)
json.dump(cands, open(f'{OUT}/cands.json', 'w'), ensure_ascii=False, indent=1)
del design; gc.collect(); torch.cuda.empty_cache()
base = Qwen3TTSModel.from_pretrained('Qwen/Qwen3-TTS-12Hz-1.7B-Base', device_map='cuda:0', dtype=torch.float16, attn_implementation='sdpa')
print('clone sig', inspect.signature(base.generate_voice_clone))
prompt = base.create_voice_clone_prompt(ref_audio=best['path'], ref_text=REF_TEXT, x_vector_only_mode=False)
qa = []
for L in CFG['lines']:
    tries = []
    for k in range(4):
        torch.manual_seed(7 + 31 * k)
        try:
            with torch.inference_mode():
                wavs, sr = base.generate_voice_clone(**kw(base.generate_voice_clone, dict(text=L['text'], voice_clone_prompt=prompt, language='French')))
        except Exception as e:
            traceback.print_exc(); continue
        w = np.asarray(wavs[0], dtype=np.float32)
        p = f"{OUT}/lines/{L['id']}_t{k}.wav"; sf.write(p, w, sr)
        tr = transcribe(p); c = cer(L['text'].replace('-', ' '), tr); dur = len(w) / sr; cps = len(L['text']) / max(dur, .1)
        bad = c > .12 or cps < 9 or cps > 20
        tries.append(dict(k=k, path=p, cer=c, dur=dur, cps=cps, tr=tr, bad=bad))
        if not bad and c < .06: break
    good = min(tries, key=lambda x: x['cer'] + (1 if x['bad'] else 0))
    os.replace(good['path'], f"{OUT}/lines/{L['id']}.wav")
    for t in tries:
        if os.path.exists(t['path']): os.remove(t['path'])
    qa.append(dict(id=L['id'], para=L['para'], text=L['text'], **{k: good[k] for k in ('cer', 'dur', 'cps', 'tr', 'bad')}, tries=len(tries)))
    print(qa[-1]['id'], round(good['cer'], 3), round(good['dur'], 2), good['tr'][:80], flush=True)
json.dump(qa, open(f'{OUT}/qa.json', 'w'), ensure_ascii=False, indent=1)
# assemble: 0.32 s between lines, 0.9 s between paragraphs
SR = sr; parts = []; t = 0.6; timeline = []
parts.append(np.zeros(int(.6 * SR), np.float32)); prev = None
for q in qa:
    if prev is not None:
        gap = .9 if q['para'] != prev else .32
        parts.append(np.zeros(int(gap * SR), np.float32)); t += gap
    w, _ = sf.read(f"{OUT}/lines/{q['id']}.wav", dtype='float32')
    timeline.append(dict(id=q['id'], start=round(t, 3), end=round(t + len(w) / SR, 3), text=q['text'])); parts.append(w); t += len(w) / SR; prev = q['para']
parts.append(np.zeros(int(1.2 * SR), np.float32))
sf.write(f'{OUT}/narration.wav', np.concatenate(parts), SR)
json.dump(timeline, open(f'{OUT}/timeline.json', 'w'), ensure_ascii=False, indent=1)
print('TOTAL', t, 'bad lines', [q['id'] for q in qa if q['bad']])
'''
print(kq.push('doc-chine-tts-qwen3', 'doc-chine TTS Qwen3 (prive)', [c1, c2]))
