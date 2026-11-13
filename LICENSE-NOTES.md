# Notes de licences (composants utilisés)

Ce fichier liste, de façon factuelle, la licence de chaque composant tiers utilisé pour fabriquer le film de référence ou inclus dans ce dépôt.
Vérifié le 13/11/2026 sur les pages officielles indiquées. Chaque composant reste soumis à sa propre licence.

## Modèles utilisés pour le film

| Composant | Rôle | Licence | Source |
|---|---|---|---|
| Qwen-Image 2.1 (7B) | génération des 34 images | `qwen-research` (licence « other » sur Hugging Face) | https://huggingface.co/Qwen/Qwen-Image-2.1 (fichier `LICENSE`) |
| Poids quantifiés `DeepBeepMeep/Qwen_image_2` (`qwen_image_21_7B_int8_convrot.safetensors`, VAE) | version INT8 de Qwen-Image 2.1 chargée par Wan2GP | dérivés de Qwen/Qwen-Image-2.1 (`base_model`), licence du dépôt d'origine ; fichier `qwen_image_21/LICENSE` dans le dépôt | https://huggingface.co/DeepBeepMeep/Qwen_image_2 |
| Qwen3-VL-8B-Instruct (poids INT8 dans `DeepBeepMeep/Ideogram4`) | encodeur de texte de Qwen-Image 2.1 | Apache-2.0 (modèle d'origine Qwen) | https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct |
| Wan2GP (WanGP) | moteur d'inférence (notebook Kaggle) | WanGP Community License 2.0 | https://github.com/deepbeepmeep/Wan2GP (`LICENSE.txt`) |
| Qwen3-TTS-12Hz-1.7B-VoiceDesign | conception de la voix | Apache-2.0 | https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign |
| Qwen3-TTS-12Hz-1.7B-Base | lecture du script (clonage de la voix conçue) | Apache-2.0 | https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base |
| Whisper « turbo » (openai-whisper) | contrôle automatique de la voix sur Kaggle | MIT | https://github.com/openai/whisper |
| whisper.cpp + `ggml-large-v3-turbo-q5_0.bin` | contrôle de la prononciation en local | MIT | https://github.com/ggml-org/whisper.cpp |

## Essais abandonnés (aucune image du film n'en provient)

| Composant | Licence | Source |
|---|---|---|
| Qwen-Image (20B) | Apache-2.0 | https://huggingface.co/Qwen/Qwen-Image |
| `city96/Qwen-Image-gguf` (Q5_K_M) | dérivé de Qwen-Image | https://huggingface.co/city96/Qwen-Image-gguf |
| `lightx2v/Qwen-Image-Lightning` (LoRA 8 étapes) | voir la fiche du modèle | https://huggingface.co/lightx2v/Qwen-Image-Lightning |
| Stable Diffusion XL base 1.0 (secours prévu dans `build_img.py`) | CreativeML Open RAIL++-M | https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 |

## Fichiers tiers inclus dans ce dépôt

| Fichiers | Origine | Licence |
|---|---|---|
| `third_party/video-agent-skills/` (nappes `enquete/arpege/neon.mp3` générées par code, `tracks.json`, générateur `engine/music.mjs` + `engine/lib/{chill,chill-styles,chill-synth,dsp}.js` + `engine/platform.mjs`, bruitages `impact-boom/zhhh/riser.mp3`, docs des skills `studio-script`, `vox`, `short-editing`) | https://github.com/Melvynx/video-agent-skills (commit `4774fa4`), Melvyn Malherbe | MIT (`third_party/video-agent-skills/LICENSE`) |
| `third_party/video-agent-skills/fonts/Archivo.ttf`, `ArchivoBlack.ttf` | Google Fonts, distribuées avec video-agent-skills | SIL Open Font License 1.1 |
| `third_party/video-agent-skills/fonts/InstrumentSerif-Regular.ttf`, `InstrumentSerif-Italic.ttf` | Google Fonts, distribuées avec video-agent-skills | SIL Open Font License 1.1 |
| `reference/doc-chine/kaggle/qi21_orig.ipynb` | notebook Kaggle d'Emilio Moreau « Qwen-Image-2.1 7B on T4 x2 » | celui de son auteur |
| `reference/doc-chine/kaggle/kgw/kaggle_api.py` | client de la passerelle « kaggle-gateway » écrite pour Emilio Moreau | celui de son auteur |

## Données et faits
Les chiffres du film sont des faits cités avec leurs sources publiques (`reference/doc-chine/output/sources.md`). Les marques citées
(Honor, Huawei, Tencent, BYD, Tesla, Nvidia, DeepSeek) sont nommées à titre informatif ; aucun logo n'est reproduit.

## Mention utilisée dans la description du film
« Images d'illustration générées par IA (style collage papier). Voix de synthèse. »
