#!/usr/bin/env bash
# Transcrit chaque phrase TTS avec whisper.cpp (large-v3-turbo) pour vérifier la prononciation des noms propres.
# Usage : WHISPER_CLI=/chemin/whisper-cli WHISPER_MODEL=/chemin/ggml-large-v3-turbo-q5_0.bin bash tools/whisper_check.sh [tts/lines] [mots...]
# Sortie : /tmp/vh_whisper/<id>.txt + un tableau id | transcription. Les mots surveillés absents sont signalés « A ECOUTER ».
# Rappel : whisper écrit les nombres en chiffres (« 2026 ») alors que le script les écrit en lettres :
#   un écart sur un nombre N'EST PAS une erreur (faux positifs du QA automatique du notebook). Seuls les mots comptent.
set -uo pipefail
DIR=${1:-tts/lines}; shift || true
WORDS=${*:-"DeepSeek BYD Huawei Tencent Shenzhen Nvidia Honor Tesla ASPI Hangzhou Xiaoping"}
: "${WHISPER_CLI:?définir WHISPER_CLI}"; : "${WHISPER_MODEL:?définir WHISPER_MODEL}"
mkdir -p /tmp/vh_whisper
for f in "$DIR"/*.wav; do
  id=$(basename "$f" .wav)
  ffmpeg -loglevel error -y -i "$f" -ar 16000 -ac 1 -c:a pcm_s16le /tmp/vh_whisper/$id.16k.wav
  "$WHISPER_CLI" -m "$WHISPER_MODEL" -l fr -nt -np -f /tmp/vh_whisper/$id.16k.wav -otxt -of /tmp/vh_whisper/$id >/dev/null 2>&1
  printf '%s | %s\n' "$id" "$(tr '\n' ' ' < /tmp/vh_whisper/$id.txt)"
done
echo "--- mots surveillés : $WORDS"
for w in $WORDS; do n=$(grep -il -- "$w" /tmp/vh_whisper/*.txt | wc -l); echo "$w : trouvé dans $n phrase(s)"; done
echo "Pour chaque phrase qui DOIT contenir un mot surveillé et où il manque : A ECOUTER, puis corriger (guide/04-voix-tts.md)."
