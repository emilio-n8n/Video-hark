# Extraits de video-agent-skills (MIT)

Origine : https://github.com/Melvynx/video-agent-skills — commit `4774fa4f2601baa822fd513387202c26e4587902` (22/10/2026), © 2026 Melvyn Malherbe, licence MIT (`LICENSE`).
Seuls les fichiers réellement utilisés pour le film « La Chine ne copie plus » sont copiés ici (le dépôt complet cloné faisait ~390 Mo avec ses runtimes).

| Ici | Chemin d'origine | Utilisé pour |
|---|---|---|
| `fonts/Archivo.ttf`, `ArchivoBlack.ttf`, `InstrumentSerif-Regular.ttf`, `InstrumentSerif-Italic.ttf` (SIL OFL) | `skills/short-editing/engine/fonts/` | toutes les typos du montage, des sous-titres et de la miniature (`render/vx.py`) |
| `music/enquete.mp3`, `arpege.mp3`, `neon.mp3`, `tracks.json` | `skills/short-editing/assets/music/` (générés par `node engine/music.mjs` à l'installation, pas versionnés dans le dépôt d'origine) | nappes musicales (`render/audio.py`) |
| `engine/music.mjs`, `engine/platform.mjs`, `engine/lib/{chill,chill-styles,chill-synth,dsp}.js` | `skills/short-editing/engine/` | générateur procédural des nappes : `node music.mjs enquete arpege neon --out ../music` (reproduit `enquete.mp3` à l'octet près, vérifié) |
| `sfx/impact-boom.mp3`, `zhhh.mp3`, `riser.mp3` | `skills/short-editing/assets/sfx/` | bruitages (`render/audio.py`) |
| `skills-docs/studio-script/` | `skills/studio-script/` | méthode d'écriture du script (accroches, score, relance, humanize) |
| `skills-docs/vox/` | `skills/vox/` | règles du style collage papier (STYLE, CHROMA, kinds) |
| `skills-docs/short-editing/` (SKILL.md, references/music.md, sfx.md) | `skills/short-editing/` | choix des nappes et des bruitages, règles de mixage (-14 LUFS) |

Non copié : le moteur de rendu Chrome (`engine/short.mjs` etc.), Chromium, node_modules, whisper.cpp, les exemples. Le film n'a pas utilisé le moteur Chrome.
