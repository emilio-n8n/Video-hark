# Chronologie complète du film « La Chine ne copie plus »

Reconstituée à partir de `PROGRESS.md` (notes de reprise écrites pendant le travail), des journaux des notebooks Kaggle (`kaggle/logs/`) et de l'historique de la conversation avec Emilio.
Heures en UTC sauf mention contraire. Attention : `PROGRESS.md` note certaines heures en **UTC-1** (heure locale d'Emilio, au Cap-Vert) ; ici tout est converti en UTC.

## Jour 1 — mercredi 22 octobre 2026 : demande, script, lancement Kaggle

| Heure | Ce qui s'est passé | Décision / leçon |
|---|---|---|
| 11:39 | Emilio : « Clone et utilise https://github.com/Melvynx/video-agent-skills pour faire un documentaire sur la Chine de 5 min qui s'inspire de https://youtu.be/9FTKLQcbdIM, tu peux utiliser Kaggle. » | Seules contraintes données : sujet, durée ~5 min, inspiration, Kaggle autorisé. |
| 11:42 | Dépôt `video-agent-skills` cloné (commit `4774fa4`). Transcription de la vidéo de référence analysée (thèmes : semi-marathon des robots de Pékin, sortie de la pauvreté, Shenzhen, DeepSeek, énergie, batteries, BYD, robots, cycles de puissance). | **On ne copie rien** de la vidéo de référence : on garde les thèmes, on écrit un script original, on ignore son segment sponsor. |
| ~11:44 | Installation du moteur `short-editing` : Chromium headless ARM64 refusait de démarrer (`libatk-1.0.so.0: cannot open shared object file`) → bibliothèques `.deb` extraites dans `libs/root` + `LD_LIBRARY_PATH` (voir `env.sh.original`). whisper.cpp compilé (`whisper-cli`), modèle `ggml-large-v3-turbo-q5_0.bin` téléchargé. Les 8 nappes musicales générées par code (`node engine/music.mjs`, -16 LUFS chacune). | Ces installations n'ont finalement servi qu'à : whisper.cpp (contrôle de la voix) et les nappes/bruitages/polices. Le moteur Chrome n'a pas servi au rendu (voir 27/10). |
| ~11:45-11:54 | Script écrit avec la méthode `studio-script` : 3 accroches de formules différentes, notées /10 (9, 8, 7) → accroche « mid-scene » 9/10 retenue. Relance (« re-hook ») à ~50 %. Fin en boucle + question en commentaire avec un mot exact. Passe « humanize » (0 caractère invisible, pas de mots IA). ~830 mots, 6 parties. Chaque chiffre vérifié sur une source ouverte (`output/sources.md`). | Les nombres sont écrits **en lettres** dans le texte lu par la voix. |
| ~11:50 | Deux notebooks Kaggle **privés** lancés : `doc-chine-tts-qwen3-prive` (Qwen3-TTS 1.7B, voix off) et `doc-chine-qwen-image-collage-prive` (Qwen-Image 20B GGUF + LoRA Lightning, 34 images). | Qwen-Image 20B choisi pour sa licence Apache-2.0 (chaîne monétisée). Qwen-Image 2.1 écarté à ce moment pour sa licence « research ». Secours prévu pour la voix : OmniVoice. |
| 11:56 | Point d'étape envoyé à Emilio : script fait, notebooks en cours, montage à faire. | — |
| ~21:00 | Contrôle : TTS **COMPLETE** ; images **ERROR** sans message. | Toujours aller lire `kernel.log`, le statut seul ne dit rien. |

## Jour 2 — mardi 27 octobre 2026 : voix validée, bascule vers Qwen-Image 2.1, moteur de rendu maison

| Heure | Ce qui s'est passé | Décision / leçon |
|---|---|---|
| 16:07 | Emilio : « Finis vidéo Chine ». | — |
| ~16:10 | Sorties TTS récupérées (65 phrases, `qa.json`). Le QA automatique du notebook marque 22 phrases « bad ». Vérification : ce sont presque toutes des **faux positifs** (Whisper écrit « 2026 » en chiffres, le texte l'écrit en lettres → écart de caractères). | Ne jamais refaire une phrase sur la foi d'un score : écouter + retranscrire localement. |
| ~16:12 | whisper.cpp large-v3-turbo en local : DeepSeek, BYD, Huawei bien prononcés. **Un vrai défaut** : `p2_l09` dit « soixante-quatorze **de** technologies ». Coupe franche de 2048 échantillons (3,243 → 3,328 s) → `build/p2_l09_fixed.wav`, re-vérifiée à l'oreille et par Whisper. | Script : `tools/cut_audio.py`. |
| ~16:17 | Narration réassemblée : 0,32 s entre phrases, **2,5 s** entre chapitres (0,9 s + 1,6 s pour laisser la place à la carte de chapitre), 0,6 s au début, 2,5 s à la fin → **371,595 s**. `build/timeline.json` = début/fin de chaque phrase. | Script : `tools/rebuild_narration.py` (reproduit le fichier à l'identique). |
| avant 16:22 | Images 20B : v1 = `AttributeError: 'NoneType' object has no attribute 'cpu'` (le masque de prompt renvoyé est `None`) → corrigé. v2 = import de diffusers cassé par `torchao` (`FqnToConfig`) → `pip uninstall -y torchao`. v3 = coupure réseau pendant `pip` (bitsandbytes absent) → boucle de 4 essais + `assert`. v4 poussée, restée **en file d'attente**. | 3 échecs différents, 3 corrections ciblées. |
| ~16:20 | Décision de rendu : **moteur Python/PIL écrit pour ce film** (`render/vx.py`, `scenes.py`, `render.py`) au lieu du moteur Chrome du dépôt. Raison : le moteur attend des mots horodatés par Whisper et des rendus longs découpés, irréaliste sur un bac à sable 2 CPU. Règles de style reprises des skills `vox` et `short-editing`. | ~13 images/s à 12 fps « stop-motion ». |
| ~16:24 | Mixage prêt (`render/audio.py` → `build/mix.wav`, -14,2 LUFS mesuré par loudnorm, true peak -1,5 dBTP). Sous-titres prêts (`render/cues.json`, `captions.srt`). | — |
| 16:23-16:28 | Emilio demande quel modèle image est utilisé ; il dit ne pas se soucier des licences et propose de dire que les images « viennent de Google ». Refus de cette fausse attribution (un festival demande de garantir les droits). Puis : « Utilise qwen 2.1 putain » → **bascule vers Qwen-Image 2.1 (7B)**, son notebook Kaggle `qwen-image-2-1-7b-on-t4-x2` (Wan2GP, poids INT8 de DeepBeepMeep). Emilio : « Y a pas de bug avec lui, j'ai fait des tonnes d'images avec ». | Prendre **son** notebook tel quel ; ne corriger que si le test réel échoue. Licence `qwen-research` acceptée en connaissance de cause par Emilio ; on ne re-débat plus. |
| ~16:30 | Kernel 20B v4 (toujours en file) remplacé par une v5 « no-op » CPU (pour libérer le GPU). Nouveau kernel privé `doc-chine-qwen-image-2-1-prive` (`kaggle/build_img21.py`) : cellules d'Emilio inchangées, poids dans `/kaggle/tmp` (sinon 18,7 Go remplissent les 20 Go de sortie), pré-test 1 image, puis `--batch` des 34 plans. | — |
| ~16:30-17:20 | Tentative 1 : **même plantage que son run du 30/09** : `ValueError: The dtype of a weights Tensor cannot be changed` (cast des poids INT8) → cast partiel → `assert model_dtype == dtype` dans mmgp → profil mémoire sauté → encodeur texte resté sur CPU → `RuntimeError: Expected all tensors to be on the same device ... index_select`. Pré-test échoué, 0 image. | La cause : le correctif « fp16 pour T4 » du notebook essayait de convertir aussi les poids quantifiés. |
| ~17:25 | Tentative 2 : on **saute les poids quantifiés** (`type(p.data) is not torch.Tensor`) dans la conversion fp16 + repli `text_encoder.to("cuda:0")` si le profil échoue encore. Règle fixée : si ça échoue → rapport à Emilio, pas de 3e boucle. | **Ça a marché** (log : « mmgp profile applied », « PRE-FLIGHT OK »). |
| 18:49-21:49 | Suivi toutes les ~4 min pendant 3 h : statut `running` en continu, aucune sortie visible avant la fin (l'API ne liste les fichiers qu'une fois le kernel terminé). Tâche planifiée horaire créée pour finir automatiquement. | Un batch Qwen-Image 2.1 de 34 images prend **~10 h 18** sur T4×2 (13,5 à 22,7 min par image). Limite Kaggle : 12 h par session. |

## Jour 3 — mercredi 28 octobre 2026 : images terminées

| Heure | Ce qui s'est passé | Décision / leçon |
|---|---|---|
| ~20:40 | Kernel `complete`, log « BATCH DONE 34 of 34 », « images: 34 ». Emilio est prévenu. **Mais** la liste des fichiers de sortie de l'API est plafonnée à **500 fichiers par page** et les 6 premières pages sont remplies par le dossier `Wan2GP/` cloné dans `/kaggle/working` → les `img/*.png` n'apparaissent pas en page 1. Il faut paginer (`pageToken`). `kq.py` demande aussi `pip install httpx`. | Ne jamais cloner un dépôt dans `/kaggle/working` si on récupère les sorties par l'API ; sinon paginer. |

## Jour 4 — mercredi 11 novembre 2026 : rendu final + dossier festival

| Heure | Ce qui s'est passé | Décision / leçon |
|---|---|---|
| 21:29 | Emilio : « Oui » (terminer le montage + préparer le dossier WAIFF Africa). | — |
| ~21:39 | 34/34 images récupérées par pagination (`kaggle/fetch_img.py`) : elles étaient en page **7 sur 7**. Aucun kernel relancé. `render/img` → images réelles, `render/layers/` (détourages en cache) régénéré. | — |
| ~21:40 | Contrôle visuel de chaque image : `plate-race` a deux grosses **taches vertes** (feuillage raté) dans le ciel et les immeubles → inpainting OpenCV Telea à 1/4 de résolution + détail haute fréquence emprunté ; original gardé dans `images/orig/`. `plate-circuit` est presque vide (bleu nuit, pas de circuit) → gardé comme fond sombre (la puce, la baleine et les bandes sont posées dessus). | Script : `tools/inpaint_green.py`. |
| ~21:41-21:43 | Stills de contrôle (`render.py still …`) → corrections de mise en page dans `scenes.py` : compteurs de l'accroche remontés (50:26 à y=300, 57:20 à y=590, bande « 2025 » à y=800) pour ne plus toucher les sous-titres ; « ≈ » absent de la police Instrument Serif (carré vide) → bande réécrite « près des 3/4 du recul… » ; barres BYD/Tesla `vmax` 2,95 (l'étiquette de valeur était coupée) ; découpes et étiquettes du chapitre 5 remontées de 40 px. | Script : `tools/check_glyphs.py`. |
| ~21:43-21:58 | Rendu des 24 segments (4460 images à 12 fps), concaténation, mux avec `build/mix.wav` en 24 fps. **Piège** : écrire le MP4 avec `+faststart` directement sur `/workspace` (JuiceFS) échoue à la fin (« Unable to re-open … for shifting data ») → encoder dans `/tmp` puis copier. Autre piège du bac à sable : une commande identique répétée peut renvoyer une sortie en cache → varier le texte de la commande quand on surveille. | Scripts : `tools/render_plan.py`, `tools/assemble.sh`. |
| ~21:44-22:23 | Version festival : sous-titres anglais (`render/en_lines.txt`, 135 lignes = 135 cues, mêmes minutages → `cues_en.json`), rendu dans `render/segs_en` avec `CUES=cues_en.json SEGDIR=… EMPH=…`. Les étiquettes papier à l'écran restent en français. Dossier WAIFF : still 1920×1080, présentation FR/EN, journal de production FR/EN (lignes « À CONFIRMER PAR EMILIO »), modèle de bio. | — |
| 22:23-22:28 | Livraison : `output/documentaire-chine.mp4` (1920×1080, H.264 High crf 20, AAC 192 k, 24 fps, 371,60 s, 338 Mo, -14,4 LUFS intégré, crête -1,1 dBFS), `preview.mp4` 720p < 50 Mo, miniature refaite depuis la vraie image `thumb-a`, `captions.srt`. | — |
| 22:28 | Point signalé à Emilio : la narration dit au présent que le record humain est de 57:20 ; or Yomif Kejelcha a couru **56:51** le 23/08/2026 (Buenos Aires). L'écran date le chiffre (« record humain, mars 2026 »), la voix non. Correction proposée, **pas encore décidée**. | Une vérification des faits se refait **juste avant publication**, pas seulement à l'écriture. |

## Ce qui n'a pas été fait / reste ouvert (au 13/11/2026)

- Phrase « record humain 57:20 » : non corrigée (décision d'Emilio en attente).
- Dossier WAIFF Africa : non déposé (bio, e-mail personnel, pièce d'identité à fournir par Emilio ; clôture 31/12/2026 23:59 GMT).
- Le moteur Chrome de `video-agent-skills` n'a pas été utilisé pour le rendu (remplacé par le moteur Python).
