# 04 — Voix off (Qwen3-TTS sur Kaggle) + contrôle Whisper

Script d'origine : `reference/doc-chine/kaggle/build_tts.py` (pousse un notebook Kaggle privé). Client API : `kaggle/kq.py` + `kaggle/kgw/kaggle_api.py`.
Résultat du film : 65 phrases, voix d'homme grave et posée, 24 kHz mono, **371,6 s** après assemblage.

## Entrées
- `script/paras.json` validé (étape 03).
- Token Kaggle (`KAGGLE_USERNAME` + `KAGGLE_KEY`, ou `~/.kaggle/kaggle.json`). Compte Kaggle avec GPU activé (téléphone vérifié).

## Comment marche le notebook (à ne pas modifier sans raison)

1. Installe `transformers==4.57.3`, `accelerate>=1.2.0`, `soundfile`, `qwen-tts`, `openai-whisper` sur un GPU T4 (×2).
2. **Conçoit la voix** avec `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` à partir d'une description (`INSTRUCT`) :
   *« Male narrator, about 45 years old, deep warm baritone voice, calm and confident, speaking French with a neutral standard French accent, measured documentary narration pace, clear articulation, gentle gravitas, studio quality, no background noise. »*
   Il génère **5 candidates** (seeds 100 à 104) qui lisent la même phrase de référence (`REF_TEXT`), les transcrit avec Whisper « turbo », et note chacune :
   `score = 3 × taux d'erreur + |hauteur médiane − 105 Hz| / 60 + (0,5 si le débit sort de 11-16 caractères/s)`. La plus basse gagne.
   Film : candidate 2 (erreur 0,015 ; 100 Hz ; 15,9 car/s ; score 0,13). Fichiers : `tts/cands/`, `tts/cands.json`.
3. **Lit tout le script** avec `Qwen/Qwen3-TTS-12Hz-1.7B-Base` en clonant la candidate gagnante (`create_voice_clone_prompt`, `x_vector_only_mode=False`).
   Pour chaque phrase : jusqu'à **4 essais** (seeds 7, 38, 69, 100) ; un essai est « mauvais » si erreur Whisper > 0,12 ou débit < 9 ou > 20 car/s ;
   on s'arrête dès qu'un essai est bon avec erreur < 0,06 ; on garde le meilleur. Film : 157 générations pour 65 phrases, 31 phrases ont eu besoin de plus d'un essai.
4. Écrit `tts/lines/<id>.wav`, `tts/qa.json`, et un premier `narration.wav` + `timeline.json` (pauses 0,32 s / 0,9 s — **remplacés** plus bas).

Sigles réécrits **pour la voix seulement** dans `build_tts.py` : `BYD → B-Y-D`, ` R1 → R-1`. Ajoute les tiens sur la même ligne (`t = l.replace(...)`).

## Actions

```bash
cd films/<slug>/kaggle
pip install httpx                                   # requis par kgw/kaggle_api.py
export KAGGLE_USERNAME=<ton_nom_kaggle>             # + KAGGLE_KEY=<clé>  OU  ~/.kaggle/kaggle.json
# 1) adapte le nom du notebook à ton film : dernière ligne de build_tts.py
#    kq.push('<slug>-tts-qwen3', '<slug> TTS Qwen3 (prive)', [c1, c2])
python3 build_tts.py            # écrit tts_lines.json et pousse le notebook ; affiche un numéro de version
```

**Attention au nom réel du notebook** : Kaggle fabrique l'identifiant à partir du **titre**. Avec le titre `doc-chine TTS Qwen3 (prive)`,
le notebook s'appelle `doc-chine-tts-qwen3-prive` (et non `doc-chine-tts-qwen3`). Utilise toujours ce nom-là pour `status` et `fetch`.
Le plus simple : donne un titre dont la version « slug » est identique au slug poussé.

```bash
python3 kq.py status <slug>-tts-qwen3-prive          # ('running', '') ... jusqu'à ('complete', '')
python3 kq.py fetch  <slug>-tts-qwen3-prive ../out_tts   # télécharge kernel.log + tts/... (affiche la fin du log)
mkdir -p ../tts && cp -r ../out_tts/tts/* ../tts/
```
Durée : non chronométrée précisément pour le film (terminé dans l'après-midi du 22/10) ; compte 30 à 90 min. Vérifie le statut toutes les 10-15 min, pas plus souvent.

### Contrôle de prononciation (local, whisper.cpp)

Installation (une fois) :
```bash
git clone https://github.com/ggml-org/whisper.cpp && cd whisper.cpp
cmake -B build && cmake --build build -j --config Release
sh ./models/download-ggml-model.sh large-v3-turbo-q5_0      # -> models/ggml-large-v3-turbo-q5_0.bin (~0,5 Go)
export WHISPER_CLI=$PWD/build/bin/whisper-cli WHISPER_MODEL=$PWD/models/ggml-large-v3-turbo-q5_0.bin
```
Puis, depuis le dossier du film :
```bash
bash tools/whisper_check.sh tts/lines DeepSeek BYD Huawei Tencent Shenzhen Nvidia Honor Tesla ASPI
```
Lis **chaque ligne** du tableau et compare au script :
- un nombre transcrit en chiffres (« 2026 ») au lieu de lettres = **normal**, pas une erreur ;
- un nom propre absent ou déformé = **à corriger** ;
- un **mot en trop** ou **manquant** = à corriger.

### Corriger une phrase

Ordre de préférence :
1. **Mot parasite court** (cas du film : `p2_l09` disait « soixante-quatorze **de** technologies ») → couper :
   ```bash
   whisper-cli -m $WHISPER_MODEL -l fr -f /tmp/vh_whisper/p2_l09.16k.wav -ml 1 -oj -of /tmp/p2_l09   # horodatage mot par mot
   python3 tools/cut_audio.py tts/lines/p2_l09.wav build/p2_l09_fixed.wav 3.242667 3.328
   mkdir -p /tmp/fix && cp build/p2_l09_fixed.wav /tmp/fix/ && bash tools/whisper_check.sh /tmp/fix   # le mot doit avoir disparu
   ```
   Coupe dans un silence entre deux mots ; enlève le moins possible (film : 0,085 s). Le fichier corrigé s'appelle `build/<id>_fixed.wav` : `rebuild_narration.py` le prend automatiquement.
2. **Nom propre mal dit** → réécris-le phonétiquement dans `build_tts.py` (comme B-Y-D) et régénère **seulement** cette phrase (pousse un notebook avec une seule ligne dans `lines`, sinon tout est refait).
3. **Phrase ratée** (voix bizarre, débit absurde) → régénère-la avec d'autres seeds.

### Assembler la narration finale

```bash
python3 tools/rebuild_narration.py     # -> build/narration.wav + build/timeline.json
```
Règles fixes : 0,60 s de silence au début ; **0,32 s** entre phrases ; **2,50 s** entre chapitres (place pour la carte de chapitre) ; 2,50 s à la fin.
Film : 371,595 s, dernière phrase finit à 369,095 s. `timeline.json` = `[{id, start, end, text}]`, le texte étant celui de `paras.json`.

## Sorties
`tts/lines/*.wav`, `tts/qa.json`, `tts/cands/`, `build/<id>_fixed.wav` (si besoin), `build/narration.wav`, `build/timeline.json`.

## Contrôles
- STOP si le nombre de fichiers `tts/lines/*.wav` ≠ nombre de phrases de `paras.json` (film : 65).
- STOP si un nom propre surveillé manque dans une phrase qui le contient.
- STOP si une phrase dure plus de 13 s ou a un débit < 9 ou > 20 caractères/s : `python3 -c "import json;[print(x['id'],round(x['cps'],1)) for x in json.load(open('tts/qa.json')) if not 9<=x['cps']<=20]"`.
- STOP si `build/narration.wav` n'est pas 24 kHz mono : `ffprobe -v error -show_entries stream=sample_rate,channels -of csv=p=0 build/narration.wav` → `24000,1`.
- Tu ne peux pas « écouter » : la transcription mot à mot remplace l'écoute. Liste les phrases douteuses à l'utilisateur au moment de l'aperçu (étape 09).

## Problèmes rencontrés et solutions
| Symptôme | Cause | Solution |
|---|---|---|
| `qa.json` marque 22 phrases « bad » | Whisper écrit les nombres en chiffres, le texte est en lettres → écart artificiel | Ignorer le score ; re-transcrire en local et lire. Seul `p2_l09` était vraiment fautif. |
| « 74 de technologies » | hallucination courte du TTS | coupe de 2048 échantillons (`tools/cut_audio.py`) |
| `status` dit « not found » | mauvais identifiant : Kaggle l'a dérivé du titre | utiliser `<titre en slug>` (ex. `doc-chine-tts-qwen3-prive`) ; `kq.py` envoie le slug **nu** (sans `user/`) |
| L'API ne répond pas / 401 | token absent ou proxy | `KAGGLE_USERNAME` + `KAGGLE_KEY` ; `KGW_KAGGLE_AUTH=none` seulement derrière le proxy Hark |
| `ModuleNotFoundError: httpx` | dépendance du client | `pip install httpx` |
| Secours si Qwen3-TTS échoue 2 fois | — | OmniVoice (T4, gratuit) était le plan B prévu ; non utilisé |
