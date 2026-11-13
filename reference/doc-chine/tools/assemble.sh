#!/usr/bin/env bash
# Assemble les segments 12 fps + le mix -> MP4 final 1080p 24 fps, puis l'aperçu 720p < 50 Mo.
# [Video-hark] commandes reconstituées (les originales n'ont pas été sauvegardées), mêmes réglages que le film :
#   H.264 High crf 20, yuv420p, 24 fps (chaque image 12 fps est montrée 2 fois), AAC 192 kb/s 48 kHz stéréo, +faststart.
#
# Trois étapes, chacune assez courte pour la limite de 120 s par commande du bac à sable Hark
# (un encodage 1080p complet d'un coup prend ~15 min sur 2 CPU : il DÉPASSE la limite -> on encode segment par segment) :
#   bash tools/assemble.sh enc 0 1 2 3     # ré-encode ces segments en 24 fps crf 20 dans /tmp/vh24 (relancer par petits lots ;
#                                          #   un segment déjà fait est sauté). ~1,8 s de calcul par seconde de vidéo sur 2 CPU ARM (seg20, 35 s de vidéo = ~60 s).
#   bash tools/assemble.sh mux             # concat SANS ré-encodage + audio AAC -> output/documentaire-chine.mp4
#   bash tools/assemble.sh preview         # output/preview.mp4 en 720p (~45 Mo), en 2 moitiés si besoin
# Variables : SEGDIR (défaut render/segs), OUT (défaut output/documentaire-chine.mp4), ENC (défaut /tmp/vh24)
# PIÈGE : écrire un MP4 avec +faststart directement sur /workspace (JuiceFS) échoue à la fin
#   (« Unable to re-open ... for shifting data ») -> on écrit toujours dans /tmp puis on copie.
set -euo pipefail
cd "$(dirname "$0")/.."
SEG=${SEGDIR:-render/segs}; OUT=${OUT:-output/documentaire-chine.mp4}; ENC=${ENC:-/tmp/vh24}; mkdir -p "$ENC"
case "${1:-}" in
enc)
  shift
  for i in "$@"; do
    s=$(printf 'seg%02d.mp4' "$i"); [ -s "$ENC/$s" ] && { echo "déjà fait $s"; continue; }
    ffmpeg -loglevel error -y -i "$SEG/$s" -vf fps=24 -c:v libx264 -preset medium -profile:v high -crf 20 -pix_fmt yuv420p -an "$ENC/$s.tmp.mp4"
    mv "$ENC/$s.tmp.mp4" "$ENC/$s"; echo "ok $s"
  done ;;
mux)
  n=$(ls "$SEG"/seg*.mp4 | wc -l); m=$(ls "$ENC"/seg*.mp4 | wc -l)
  [ "$n" = "$m" ] || { echo "STOP : $m segments encodés sur $n"; exit 1; }
  ( cd "$ENC" && ls seg*.mp4 | sort | sed "s/.*/file '&'/" > list.txt )
  ffmpeg -loglevel error -y -f concat -safe 0 -i "$ENC/list.txt" -i build/mix.wav -map 0:v:0 -map 1:a:0 \
    -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart /tmp/vh_final.mp4
  mkdir -p "$(dirname "$OUT")"; cp /tmp/vh_final.mp4 "$OUT"; ls -l "$OUT" ;;
preview)
  # débit visé ~0,85 Mb/s vidéo + 96 kb/s audio -> ~45 Mo pour 6 min 12 (GitHub, messageries : < 50 Mo)
  PREV="$(dirname "$OUT")/preview.mp4"; D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
  H=$(python3 -c "print(round($D/2,3))")
  for part in 0 1; do
    [ -s /tmp/vh_prev$part.mp4 ] && continue
    if [ $part = 0 ]; then R="-t $H"; else R="-ss $H"; fi
    ffmpeg -loglevel error -y $R -i "$OUT" -vf scale=1280:720 -c:v libx264 -preset veryfast -profile:v high \
      -b:v 850k -maxrate 1200k -bufsize 2400k -pix_fmt yuv420p -an /tmp/vh_prev$part.mp4
  done
  printf "file '/tmp/vh_prev0.mp4'\nfile '/tmp/vh_prev1.mp4'\n" > /tmp/vh_prev.txt
  ffmpeg -loglevel error -y -f concat -safe 0 -i /tmp/vh_prev.txt -i "$OUT" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 96k -shortest -movflags +faststart /tmp/vh_prev.mp4
  cp /tmp/vh_prev.mp4 "$PREV"; rm -f /tmp/vh_prev0.mp4 /tmp/vh_prev1.mp4; ls -l "$PREV" ;;
*) sed -n 2,16p "$0"; exit 1 ;;
esac
