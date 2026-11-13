#!/usr/bin/env python3
"""Coupe un mot parasite dans une phrase TTS (wav PCM 16 bits).

Usage : python3 tools/cut_audio.py IN.wav OUT.wav DEBUT_S FIN_S
Exemple réel du film (le « de » parasite de « soixante-quatorze de technologies ») :
  python3 tools/cut_audio.py tts/lines/p2_l09.wav build/p2_l09_fixed.wav 3.242667 3.328
  -> enlève les échantillons 77824 à 79872 (2048 échantillons = 0,085 s à 24 kHz), coupe franche sans fondu.
     Reproduit les échantillons audio de build/p2_l09_fixed.wav à l'identique (vérifié ; seul l'en-tête WAV diffère). Les notes de l'époque disaient « 3,185-3,30 s » :
     c'était la fenêtre de recherche, la coupe réelle est celle-ci.
Comment trouver DEBUT/FIN : transcrire avec whisper.cpp en horodatage par mot (-ml 1 -oj), repérer le mot,
puis ajuster à l'oreille ET en relançant whisper sur OUT.wav jusqu'à ce que le mot ait disparu.
Toujours couper sur un passage proche de zéro (silence entre deux mots) pour éviter un clic.
"""
import sys, wave
src, dst, a, b = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
w = wave.open(src); sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth(); pcm = w.readframes(w.getnframes()); w.close()
fa, fb = round(a * sr), round(b * sr); bpf = ch * sw
out = pcm[:fa * bpf] + pcm[fb * bpf:]
o = wave.open(dst, 'wb'); o.setnchannels(ch); o.setsampwidth(sw); o.setframerate(sr); o.writeframes(out); o.close()
print(f'coupe {fa}-{fb} ({(fb - fa) / sr:.3f} s) ; {len(pcm) // bpf / sr:.3f} s -> {len(out) // bpf / sr:.3f} s')
