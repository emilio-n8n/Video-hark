# Journal de production — *La Chine ne copie plus*

Réalisateur : Emilio Moreau (Dakar, Sénégal) · Catégorie : AI Short Film (documentaire) · 6 min 12 s · production octobre-novembre 2026

> Les passages marqués **[À CONFIRMER PAR EMILIO]** décrivent sa part de travail personnelle : il doit les relire, les préciser ou les corriger avant le dépôt.

## 1. Résumé du processus

Film de vulgarisation en collage de papier animé (style « stop-motion » à 12 images/s). Toutes les images sont générées par IA, la voix off est une voix de synthèse, et le montage est réalisé par un moteur de rendu Python écrit sur mesure pour ce film. Aucune prise de vue réelle, aucune image d'archive, aucune personne réelle n'est représentée (les foules, coureurs et ouvriers sont des figures génériques générées).

## 2. Étapes de production et outils

| Étape | Outils | Rôle de l'IA | Rôle humain |
|---|---|---|---|
| Sujet, angle, écriture du script | Assistant IA conversationnel (Hark) et méthode de scénarisation du dépôt open source *video-agent-skills* (structure accroche / relance / fin en boucle) | Recherche documentaire, premier jet du texte, propositions d'accroches notées | Choix du sujet et de l'angle (« du pays qui copiait au pays qu'on étudie »), validation et choix des accroches, relecture du texte **[À CONFIRMER PAR EMILIO]** |
| Vérification des faits | Sources primaires et presse (Banque mondiale, AIE, IFR, ASPI, World Athletics, Xinhua, Reuters, Bloomberg, CNBC, etc. — liste complète dans `sources.md`) | Aide à la collecte des sources | Chaque chiffre du film est relié à une source publique ; arbitrages éditoriaux (ex. coût DeepSeek présenté comme « annoncé » et « contesté ») **[À CONFIRMER PAR EMILIO]** |
| Voix off (français) | **Qwen3-TTS 1.7B** (Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign pour créer une voix de narrateur à partir d'une description, puis Qwen3-TTS-12Hz-1.7B-Base pour lire tout le texte avec cette voix), exécuté sur Kaggle (GPU) | Synthèse de toute la narration (voix entièrement synthétique, ne clone aucune personne réelle) | Description de la voix voulue, choix de la prise de référence, écoute |
| Contrôle de la narration | **Whisper** (OpenAI whisper « turbo » sur Kaggle ; whisper.cpp large-v3-turbo en local) | Transcription automatique de chaque phrase pour détecter les erreurs de prononciation | Correction manuelle : coupe d'un mot parasite (« de ») dans une phrase ; vérification des noms propres (DeepSeek, BYD, Huawei) |
| Images | **Qwen-Image 2.1 (7B)** via **Wan2GP** (poids quantifiés INT8 publiés par DeepBeepMeep), exécuté sur Kaggle (2 × GPU T4) à partir du notebook Kaggle d'Emilio | Génération des 34 images du film : 14 décors plein cadre et 20 éléments découpés (robot, baleine, puce, batterie, éolienne, voitures, navire hollandais, locomotive, etc.), 20 étapes, 1664×928 et autres formats | Direction artistique : style unique « collage de papier déchiré + photos en similigravure », palette (crème, rouge, jaune, bleu poussiéreux), écriture des 34 descriptions plan par plan, choix des images ; retouche d'un décor (taches vertes supprimées dans le décor de l'avenue de Pékin) |
| Animation et montage | Moteur de rendu sur mesure en **Python (Pillow, NumPy) + FFmpeg** | Aucune (code déterministe) | Découpage en 24 scènes calé au dixième de seconde sur la voix ; détourage des éléments, compteurs animés, graphiques en barres, bandes de papier, traits de feutre rouge, cartes de chapitres, mouvements de caméra, grain et vignettage ; sous-titres |
| Musique | 3 nappes musicales **générées par code (synthèse procédurale, sans IA)** par le moteur du dépôt open source *video-agent-skills* (licence MIT), une par chapitre | Aucune | Choix des nappes par chapitre, mixage |
| Bruitages | 3 effets fournis dans le dépôt *video-agent-skills* (licence MIT du dépôt) + un « choc de papier » synthétisé par code pour ce film | Aucune | Placement de 10 effets sur les moments clés |
| Mixage | FFmpeg : voix + musique atténuée sous la voix (sidechain), normalisation -14 LUFS / -1,5 dBTP | Aucune | Réglages |
| Sous-titres anglais | Traduction depuis les sous-titres français (assistée par IA), mêmes minutages | Traduction | Relecture **[À CONFIRMER PAR EMILIO]** |

## 3. Modèles, logiciels et éléments de tiers (et base de leur utilisation)

| Élément | Titulaire | Licence / base d'utilisation |
|---|---|---|
| Qwen-Image 2.1 (7B), modèle de génération d'images | Qwen (Alibaba) | Licence « qwen-research » (fiche Hugging Face Qwen/Qwen-Image-2.1) |
| Poids quantifiés Qwen-Image 2.1 et Qwen3-VL-8B (encodeur de texte) | DeepBeepMeep (dépôts Hugging Face) ; Qwen3-VL-8B-Instruct : Qwen | Licence du modèle d'origine ; Qwen3-VL-8B-Instruct : Apache 2.0 |
| Wan2GP (moteur d'inférence) | DeepBeepMeep | WanGP Community License 2.0 |
| Qwen3-TTS 1.7B (VoiceDesign et Base) | Qwen (Alibaba) | Apache 2.0 |
| Whisper large-v3-turbo / whisper.cpp | OpenAI / ggml | MIT |
| Dépôt *video-agent-skills* (méthode de script, nappes musicales générées par code, bruitages, polices) | Melvyn Malherbe | MIT |
| Polices Archivo, Archivo Black, Instrument Serif | Auteurs respectifs (Google Fonts) | SIL Open Font License |
| Données chiffrées | Sources publiques citées dans `sources.md` | Citation de faits, sources indiquées |

Marques citées dans le récit (Honor, Huawei, Tencent, BYD, Tesla, Nvidia, DeepSeek) : mentionnées à titre informatif, sans logo reproduit. Personnalités citées (Deng Xiaoping, Ray Dalio) : nommées, non représentées.

## 4. Part humaine

**[À CONFIRMER PAR EMILIO]** Concept et angle du film ; choix du sujet et de la structure en cinq chapitres ; validation du texte et des chiffres ; direction artistique (style collage papier, palette, composition de chaque scène) ; choix du modèle d'images et préparation du notebook Kaggle ; sélection des images ; montage : rythme, durée de chaque plan, entrée de chaque élément calée sur la voix ; choix musicaux et du mixage ; relecture des sous-titres.

---

# Production journal — *China No Longer Copies* (English version)

Director: Emilio Moreau (Dakar, Senegal) · Category: AI Short Film (documentary) · 6 min 12 s · produced October-November 2026

> Passages marked **[TO BE CONFIRMED BY EMILIO]** describe his personal contribution; he must review, specify or correct them before submitting.

## 1. Process summary

An explainer film in animated paper collage (stop-motion feel at 12 frames per second). All images are AI-generated, the voice-over is a synthetic voice, and the edit is produced by a custom Python renderer written for this film. No live-action footage, no archive images, and no real person is depicted (crowds, runners and workers are generic generated figures).

## 2. Production steps and tools

| Step | Tools | Role of AI | Human role |
|---|---|---|---|
| Topic, angle, scriptwriting | Conversational AI assistant (Hark) and the scripting method of the open-source *video-agent-skills* repository (hook / re-hook / looping ending) | Research, first draft, scored hook proposals | Choice of topic and angle ("from the country that copied to the country everyone studies"), hook selection, script review **[TO BE CONFIRMED BY EMILIO]** |
| Fact-checking | Primary sources and press (World Bank, IEA, IFR, ASPI, World Athletics, Xinhua, Reuters, Bloomberg, CNBC, etc. — full list in `sources.md`) | Help collecting sources | Every figure in the film is tied to a public source; editorial calls (e.g. DeepSeek's cost shown as "announced" and "disputed") **[TO BE CONFIRMED BY EMILIO]** |
| Voice-over (French) | **Qwen3-TTS 1.7B** (Qwen3-TTS-12Hz-1.7B-VoiceDesign to design a narrator voice from a text description, then Qwen3-TTS-12Hz-1.7B-Base to read the whole script in that voice), run on Kaggle GPUs | Synthesis of the entire narration (fully synthetic voice, no real person cloned) | Voice description, choice of reference take, listening checks |
| Narration check | **Whisper** (OpenAI whisper "turbo" on Kaggle; whisper.cpp large-v3-turbo locally) | Automatic transcription of every line to catch mispronunciations | Manual fix: one stray word cut from a line; proper names checked (DeepSeek, BYD, Huawei) |
| Images | **Qwen-Image 2.1 (7B)** through **Wan2GP** (INT8-quantised weights published by DeepBeepMeep), run on Kaggle (2 × T4 GPUs) from Emilio's Kaggle notebook | Generation of the film's 34 images: 14 full-frame backgrounds and 20 cut-out elements (robot, whale, chip, battery, wind turbine, cars, Dutch ship, steam locomotive, etc.), 20 steps | Art direction: one consistent "torn paper collage + halftone photo" style, palette (cream, red, yellow, dusty blue), writing the 34 shot-by-shot prompts, image selection; retouching of one background (green blotches removed from the Beijing avenue) |
| Animation and editing | Custom renderer in **Python (Pillow, NumPy) + FFmpeg** | None (deterministic code) | 24 scenes timed to the tenth of a second on the voice; cut-outs, animated counters, bar charts, paper strips, red marker strokes, chapter cards, camera moves, grain and vignette; subtitles |
| Music | 3 music beds **generated by code (procedural synthesis, no AI)** by the engine of the open-source *video-agent-skills* repository (MIT licence), one per chapter | None | Choice of bed per chapter, mixing |
| Sound effects | 3 effects shipped with the *video-agent-skills* repository (repository under MIT licence) + one "paper thud" synthesised by code for this film | None | Placement of 10 effects on key beats |
| Mix | FFmpeg: voice + music ducked under the voice (sidechain), loudness -14 LUFS / -1.5 dBTP | None | Settings |
| English subtitles | Translation from the French subtitles (AI-assisted), same timings | Translation | Review **[TO BE CONFIRMED BY EMILIO]** |

## 3. Third-party models, software and assets (and basis for use)

| Item | Owner | Licence / basis for use |
|---|---|---|
| Qwen-Image 2.1 (7B), image generation model | Qwen (Alibaba) | "qwen-research" licence (Hugging Face model card Qwen/Qwen-Image-2.1) |
| Quantised weights of Qwen-Image 2.1 and Qwen3-VL-8B (text encoder) | DeepBeepMeep (Hugging Face repositories); Qwen3-VL-8B-Instruct: Qwen | Licence of the original model; Qwen3-VL-8B-Instruct: Apache 2.0 |
| Wan2GP (inference engine) | DeepBeepMeep | WanGP Community License 2.0 |
| Qwen3-TTS 1.7B (VoiceDesign and Base) | Qwen (Alibaba) | Apache 2.0 |
| Whisper large-v3-turbo / whisper.cpp | OpenAI / ggml | MIT |
| *video-agent-skills* repository (script method, code-generated music beds, sound effects, fonts) | Melvyn Malherbe | MIT |
| Fonts Archivo, Archivo Black, Instrument Serif | Respective authors (Google Fonts) | SIL Open Font License |
| Figures and data | Public sources listed in `sources.md` | Factual citation, sources credited |

Brands mentioned in the narration (Honor, Huawei, Tencent, BYD, Tesla, Nvidia, DeepSeek) are cited for information only; no logos are reproduced. Public figures mentioned (Deng Xiaoping, Ray Dalio) are named, not depicted.

## 4. Human contribution

**[TO BE CONFIRMED BY EMILIO]** Concept and angle; choice of topic and five-chapter structure; approval of the script and figures; art direction (paper-collage style, palette, composition of every scene); choice of image model and preparation of the Kaggle notebook; image selection; editing: pacing, length of every shot, every element's entrance timed to the voice; music choices and mix; subtitle review.
