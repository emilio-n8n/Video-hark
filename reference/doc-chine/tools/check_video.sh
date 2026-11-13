#!/usr/bin/env bash
# Contrôle technique d'un MP4 : format, durée, loudness, true peak, + 12 images témoins dans /tmp/vh_check/.
# Usage : bash tools/check_video.sh output/documentaire-chine.mp4 [durée_attendue_s=371.6]
# Attendu pour le film : h264 High 1920x1080 24/1 yuv420p · aac 48000 Hz 2 canaux · 371.60 s ·
#   Integrated ≈ -14 LUFS (film : -14.4 mesuré par ebur128, -14.2 par loudnorm) · True peak <= -1.0 dBFS.
set -euo pipefail
F=$1; EXP=${2:-371.6}
ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels -show_entries format=duration,size -of compact "$F"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F")
python3 -c "import sys; d,e=float('$D'),float('$EXP'); print('durée', d, 'OK' if abs(d-e)<0.1 else 'STOP : durée différente de la timeline')"
ffmpeg -hide_banner -nostats -i "$F" -map 0:a -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E "^\s+(I|Peak|LRA):"
mkdir -p /tmp/vh_check; rm -f /tmp/vh_check/*.jpg
for i in $(seq 0 11); do t=$(python3 -c "print(round($D*($i+0.5)/12,2))"); ffmpeg -loglevel error -y -ss $t -i "$F" -frames:v 1 -vf scale=960:-2 /tmp/vh_check/f$(printf %02d $i)_${t}s.jpg; done
ls /tmp/vh_check
echo "-> OUVRE ET REGARDE CHAQUE IMAGE de /tmp/vh_check (voir guide/09-controle-qualite.md)"
