# PROGRESS doc-chine (resume notes)
- Env: `. /workspace/work/doc-chine/env.sh` (LD_LIBRARY_PATH for Chromium libs extracted in libs/root, WHISPER_CLI, SK=engine skill dir). Engine setup OK (icons drawn) 2026-10-22 ~12:00 UTC.
- Kaggle: auth works with plain curl/kq.py through proxy; kernelSlug must be the bare slug (kq.py patched).
- Jobs launched ~11:50 UTC: doc-chine-tts-qwen3-prive, doc-chine-qwen-image-collage-prive. Status at 11:58 UTC: running.

## Status check 2026-10-22 ~21:00 UTC (review run)
- doc-chine-tts-qwen3-prive: COMPLETE → fetch outputs (narration.wav, timeline.json, qa.json).
- doc-chine-qwen-image-collage-prive: ERROR (no failure message) → fetch kernel.log, fix, re-push privately.

## Run 2026-10-27 (finisher)
- TTS outputs fetched to out_tts/tts/. QA "bad" lines were mostly whisper digit-normalisation false positives. Local whisper large-v3-turbo (models/) confirms DeepSeek, BYD, Huawei OK. p2_l09 had a parasitic "de" ("74 de technologies") -> cut 3.185-3.30 s -> build/p2_l09_fixed.wav (verified).
- build/narration.wav + build/timeline.json rebuilt from lines (+1.6 s at each chapter break), 371.6 s.
- Image kernel v2 error: diffusers import failed on torchao (FqnToConfig) -> added pip uninstall torchao. v3 error: transient pip read-timeout (bitsandbytes missing) -> retry loop + assert. v4 pushed ~16:15 (UTC-1), running.
- Render plan: custom Python/PIL frame renderer (engine needs whisper words + long chunked renders; not practical on 2-CPU sandbox) following vox/short-editing rules: paper collage, 12 fps stop-motion layer moves, push-in, counters/bars, captions, library beds per chapter, sparse SFX, -14 LUFS.
- 15:28 (UTC-1) Emilio switched images to Qwen-Image-2.1 7B (his Wan2GP kernel, licence accepted). 20B kernel v4 (still queued, no images) superseded by pushing a CPU no-op v5 (complete). New private kernel emiliomoreau/doc-chine-qwen-image-2-1-prive (kaggle/build_img21.py): his cells unchanged (weights to /kaggle/tmp instead of /kaggle/working), his pre-flight 1 image, then --batch 34 shots -> /kaggle/working/img. Attempt 1 pushed 15:30.
- Renderer ready (render/vx.py, scenes.py, render.py; ~13 fps at 12 fps stop-motion), audio mix ready (render/audio.py -> build/mix.wav, -14.2 LUFS, TP -1.5). Captions cues in render/cues.json + captions.srt.
- 2.1 attempt 1 (v1): same crash as Emilio's 30/09 run (cast of INT8 weights -> partial fp16 cast -> mmgp assert model_dtype==dtype -> profile skipped -> encoder on CPU -> index_select device error). Pre-flight failed, 0 images.
- 2.1 attempt 2 (v2, ~16:25 UTC-1): _fix_dtypes_for_t4 now skips quantized weights (type(p.data) is not torch.Tensor) so remaining float params are all fp16 and the mmgp profile can apply; fallback text_encoder.to(cuda:0) if profile still fails. If this fails -> report to Emilio, no further loop.
- Finisher run 2026-10-27 17:49–20:49 (UTC-1): polled doc-chine-qwen-image-2-1-prive (attempt 2/v2) every ~4 min for 3 h -> status 'running' the whole time (no failureMessage); output API returns nothing while running (peek fetch to /tmp = empty). Kernel has been running ~4h25 since push (16:25 UTC-1). Nothing rendered: render/img still -> img_ph (placeholders), render/layers untouched, no segs/mp4.
- Added output/sources.md (Sources section copied from post.md).
- NEXT: when status becomes complete -> follow steps (fetch to out_img21, relink render/img, delete render/layers/*, stills check, seg render in <120 s chunks [24 segs, 4460 frames @12 fps], concat, mux build/mix.wav @24 fps -> output/documentaire-chine.mp4, preview <50 MB, thumb.py). If error / 0 images -> report log tail to Emilio, no new attempt. Note: Kaggle GPU sessions cap at 12 h (would end ~04:25 UTC-1 on 28/10).
- Brief check 2026-10-28 19:45 (UTC-1): kernel doc-chine-qwen-image-2-1-prive = complete, log "BATCH DONE 34 of 34", images: 34. Note: kernel_output listing is capped at 500 files and is filled by Wan2GP/ clutter, so img/ files are not in the first page — need pagination (pageToken) or the kaggle CLI to download img/*. Render still to do. Need `pip install httpx` for kq.py.

## Run 2026-11-11 (final render + WAIFF pack) — DONE
- Images: 34/34 fetched from kernel output via pageToken pagination (page 7 of 7; Wan2GP clutter on pages 1-6) -> out_img21/img/ (script kaggle/fetch_img.py). No kernel relaunched.
- render/img -> ../out_img21/img ; render/layers regenerated from real images.
- Bad shot fixed: plate-race had big flat green blotches (failed foliage) in the sky/buildings -> inpainted (cv2 Telea at 1/4 res + borrowed high-freq detail); original kept in out_img21/orig/plate-race.png. Result: hazy buildings, acceptable. plate-circuit is almost empty dark navy (no circuit visible) — kept as a dark backdrop (fine with chip/whale/strips on top).
- Layout fixes in scenes.py: hook counters moved up (50:26 y300, 57:20 y590, "2025 vainqueur" strip y800) to clear captions; "≈" missing in Instrument Serif -> strip text "près des 3/4 du recul…"; BYD/Tesla bars vmax 2.95 (value label was clipped); ch.5 cut-outs/labels raised 40 px.
- render.py: env CUES / SEGDIR / EMPH (used for English-caption WAIFF render into render/segs_en).
- Mux note: writing mp4 with +faststart directly on /workspace (JuiceFS) fails at trailer ("Unable to re-open… for shifting data"); encode to /tmp then cp. Also sandbox sleeps/commands may return cached output: vary command text when polling.
- output/documentaire-chine.mp4: 1920x1080 H.264 high crf20 + AAC 192k, 24 fps, 371.60 s, 338 MB, -14.4 LUFS integrated, sample peak -1.1 dBFS.
- output/preview.mp4 (720p, <50 MB), output/captions.srt, output/thumbnail.png regenerated from real thumb-a.
- WAIFF (output/waiff/): Senegal_Moreau_Emilio_AI-Short-Film_La-Chine-ne-copie-plus.mp4 (English captions burned in place of French ones, same timings; on-screen paper labels stay French), captions_en.srt, still.jpg (thumb-b scene, 1920x1080), presentation.md (FR+EN), journal-de-production.md (FR+EN, human-role lines marked À CONFIRMER), bio-TODO.md.
- Still on screen: "57:20 — record humain, mars 2026" counter in the hook (scene 1, ~17-28 s) and narration "Le record du monde humain… est de 57 minutes et 20 secondes" (present tense). Kejelcha 56:51 (23/08/2026) makes it outdated; the on-screen date contextualises it, narration does not.
- Waiting on Emilio: bio, personal email for waiff-africa.com, birth date/country confirmation, review of journal [À CONFIRMER] lines + EN subtitles, upload (deadline 31/12/2026 23:59 GMT). Nothing submitted.
