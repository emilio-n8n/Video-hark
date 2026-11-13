import json, sys
sys.path.insert(0, '.')
import kq
STYLE = ("Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, "
         "torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, "
         "subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). "
         "Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.")
CHROMA = ("Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, "
          "nothing else in the frame, generous green margin around the subject.")
shots = json.load(open('shots.json'))
only = sys.argv[1:]  # optional subset
for s in shots:
    s['prompt'] = s['subject'] + (' ' + CHROMA if s['kind'] == 'cutout' else '') + '\nStyle: ' + STYLE
if only: shots = [s for s in shots if s['name'] in only]
c1 = r'''
import subprocess
def sh(c): print('$', c); r = subprocess.run(c, shell=True, capture_output=True, text=True); print(r.stdout[-2500:], r.stderr[-2500:]); return r.returncode
sh('nvidia-smi --query-gpu=name,memory.total --format=csv; df -h /tmp /kaggle/working; free -g')
for _ in range(4):
    if sh('pip install -q --timeout 120 --retries 8 -U diffusers transformers accelerate gguf bitsandbytes peft') == 0: break
sh('pip uninstall -y torchao')
import importlib.util; assert importlib.util.find_spec('bitsandbytes') and importlib.util.find_spec('gguf'), 'deps missing'
sh('pip list 2>/dev/null | grep -iE "^(diffusers|transformers|torch|accelerate|peft|gguf|bitsandbytes) "')
'''
c2 = "import json\nSHOTS = json.loads(%r)\n" % json.dumps(shots, ensure_ascii=False) + r'''
import os, time, math, gc, traceback
import torch, numpy as np
from huggingface_hub import snapshot_download, hf_hub_download
t0 = time.time()
BASE = snapshot_download('Qwen/Qwen-Image', allow_patterns=['model_index.json', 'scheduler/*', 'text_encoder/*', 'tokenizer/*', 'vae/*', 'transformer/config.json'], local_dir='/tmp/qi')
GG = hf_hub_download('city96/Qwen-Image-gguf', 'qwen-image-Q5_K_M.gguf', local_dir='/tmp/gg')
LORA = hf_hub_download('lightx2v/Qwen-Image-Lightning', 'Qwen-Image-Lightning-8steps-V2.0-bf16.safetensors', local_dir='/tmp/lora')
print('downloads', round(time.time() - t0), 's', flush=True)
OUT = '/kaggle/working/img'; os.makedirs(OUT, exist_ok=True)
# ---------- phase A: prompt embeddings (text encoder nf4, fp32 compute) ----------
from transformers import Qwen2_5_VLForConditionalGeneration, BitsAndBytesConfig
from diffusers import QwenImagePipeline, QwenImageTransformer2DModel, GGUFQuantizationConfig, FlowMatchEulerDiscreteScheduler
te = Qwen2_5_VLForConditionalGeneration.from_pretrained(BASE, subfolder='text_encoder', torch_dtype=torch.float32,
        quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_compute_dtype=torch.float32), device_map={'': 0})
enc = QwenImagePipeline.from_pretrained(BASE, transformer=None, vae=None, text_encoder=te, torch_dtype=torch.float32)
EMB = {}
for s in SHOTS:
    with torch.inference_mode():
        pe, pm = enc.encode_prompt(prompt=s['prompt'], device='cuda:0', num_images_per_prompt=1)
    EMB[s['name']] = (pe.float().cpu(), None if pm is None else pm.cpu())
    print('emb', s['name'], tuple(pe.shape), float(pe.abs().max()), bool(torch.isnan(pe).any()), flush=True)
del enc, te; gc.collect(); torch.cuda.empty_cache()
# ---------- phase B: GGUF transformer split over the two T4 + Lightning LoRA ----------
SCHED = FlowMatchEulerDiscreteScheduler.from_config({"base_image_seq_len": 256, "base_shift": math.log(3), "invert_sigmas": False,
    "max_image_seq_len": 8192, "max_shift": math.log(3), "num_train_timesteps": 1000, "shift": 1.0, "shift_terminal": None,
    "stochastic_sampling": False, "time_shift_type": "exponential", "use_beta_sigmas": False, "use_dynamic_shifting": True,
    "use_exponential_sigmas": False, "use_karras_sigmas": False})
def mover(dev):
    def mv(x):
        if torch.is_tensor(x): return x.to(dev, non_blocking=True)
        if isinstance(x, tuple): return tuple(mv(i) for i in x)
        if isinstance(x, list): return [mv(i) for i in x]
        if isinstance(x, dict): return {k: mv(v) for k, v in x.items()}
        return x
    return mv
def build(dtype):
    tr = QwenImageTransformer2DModel.from_single_file(GG, quantization_config=GGUFQuantizationConfig(compute_dtype=dtype),
            torch_dtype=dtype, config=BASE, subfolder='transformer')
    pipe = QwenImagePipeline.from_pretrained(BASE, transformer=tr, text_encoder=None, tokenizer=None, scheduler=SCHED, torch_dtype=dtype)
    lora_ok = True
    try:
        pipe.load_lora_weights(LORA); print('lora loaded', flush=True)
    except Exception:
        traceback.print_exc(); lora_ok = False
    n = len(tr.transformer_blocks); half = n // 2 + 2
    ngpu = torch.cuda.device_count()
    tr.to('cuda:0') if ngpu == 1 else None
    if ngpu > 1:
        for name, mod in tr.named_children():
            if name != 'transformer_blocks' and name not in ('norm_out', 'proj_out'): mod.to('cuda:0')
        mv1 = mover('cuda:1')
        for i, b in enumerate(tr.transformer_blocks):
            if i < half: b.to('cuda:0')
            else:
                b.to('cuda:1'); b.register_forward_pre_hook(lambda m, a, k: (mv1(a), mv1(k)), with_kwargs=True)
        for name in ('norm_out', 'proj_out'):
            m = getattr(tr, name); m.to('cuda:1'); m.register_forward_pre_hook(lambda m, a, k: (mv1(a), mv1(k)), with_kwargs=True)
        orig = tr.forward; mv0 = mover('cuda:0')
        def fwd(*a, **k):
            return mv0(orig(*a, **k))
        tr.forward = fwd
    pipe.vae.to('cuda:0'); pipe.vae.enable_tiling()
    for i in range(ngpu): print('gpu', i, round(torch.cuda.memory_allocated(i) / 2**30, 2), 'GiB', flush=True)
    return pipe, lora_ok
DTYPE = torch.float16
try:
    pipe, LORA_OK = build(DTYPE)
except Exception:
    traceback.print_exc(); pipe = None; LORA_OK = False
STEPS = 8 if LORA_OK else 20
def gen(s, seed_shift=0):
    pe, pm = EMB[s['name']]
    g = torch.Generator('cuda:0').manual_seed(s['seed'] + seed_shift)
    with torch.inference_mode():
        out = pipe(prompt_embeds=pe.to('cuda:0', DTYPE), prompt_embeds_mask=None if pm is None else pm.to('cuda:0'), width=s['w'], height=s['h'],
                   num_inference_steps=STEPS, true_cfg_scale=1.0, generator=g, output_type='pil')
    return out.images[0]
done = 0
fails = 0
for idx, s in enumerate(SHOTS if pipe is not None else []):
    if fails >= 3 and done == 0: print('qwen failing, giving up'); break
    t1 = time.time()
    try:
        img = gen(s)
        a = np.asarray(img)
        if a.mean() < 4 or a.std() < 2:
            print('BLACK/NaN image -> switching to fp32 compute', flush=True)
            del pipe; gc.collect(); torch.cuda.empty_cache()
            DTYPE = torch.float32; pipe, LORA_OK = build(DTYPE); img = gen(s); a = np.asarray(img)
        img.save(f"{OUT}/{s['name']}.png"); done += 1
        print(f"IMG {idx+1}/{len(SHOTS)} {s['name']} {s['w']}x{s['h']} {time.time()-t1:.0f}s mean={a.mean():.0f} total={time.time()-t0:.0f}s", flush=True)
    except Exception:
        traceback.print_exc(); torch.cuda.empty_cache(); fails += 1
print('DONE', done, 'of', len(SHOTS), 'in', round(time.time() - t0), 's')
'''

c3 = r"""
# fallback: SDXL base 1.0 (CreativeML Open RAIL++-M, commercial use allowed) for any shot Qwen-Image did not produce
import os, gc, torch, time, traceback
OUT = '/kaggle/working/img'; os.makedirs(OUT, exist_ok=True)
missing = [s for s in SHOTS if not os.path.exists(f"{OUT}/{s['name']}.png")]
print('missing for fallback:', len(missing), flush=True)
if missing:
    try: del pipe
    except Exception: pass
    gc.collect(); torch.cuda.empty_cache()
    from diffusers import StableDiffusionXLPipeline
    sd = StableDiffusionXLPipeline.from_pretrained('stabilityai/stable-diffusion-xl-base-1.0', torch_dtype=torch.float16, variant='fp16', use_safetensors=True).to('cuda:0')
    sd.vae.enable_tiling()
    for s in missing:
        t1 = time.time()
        w, h = (1344, 768) if s['w'] > s['h'] * 1.4 else ((832, 1216) if s['h'] > s['w'] * 1.2 else (1024, 1024))
        style = 'paper collage, black and white halftone engraved photo cut-out with white scissor border, torn paper, aged cream paper texture, muted vintage colors, editorial'
        pr = s['subject'][:300] + (' Isolated on flat pure green background.' if s['kind'] == 'cutout' else '')
        try:
            img = sd(prompt=pr, prompt_2=style, negative_prompt='text, letters, words, logo, watermark, numbers', width=w, height=h,
                     num_inference_steps=30, guidance_scale=6.0, generator=torch.Generator('cuda:0').manual_seed(s['seed'])).images[0]
            img.save(f"{OUT}/{s['name']}.png"); print('SDXL', s['name'], round(time.time() - t1), 's', flush=True)
        except Exception: traceback.print_exc()
print('FINAL', len(os.listdir(OUT)), 'images')
"""

print(kq.push('doc-chine-qwen-image-collage-prive', 'doc-chine Qwen-Image collage (prive)', [c1, c2, c3]))
