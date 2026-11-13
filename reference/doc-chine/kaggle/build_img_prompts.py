import json, os
D=os.path.dirname(os.path.abspath(__file__))
def shots_with_prompts():
    STYLE = ("Vox explainer documentary collage, handmade analog paper cut-out look. Warm aged off-white paper with visible fibers and grain, "
             "torn paper edges with white fibrous rims, black-and-white halftone engraved photo cut-outs with a thin white scissor-cut border, "
             "subtle soft drop shadows between paper layers, muted vintage palette (dusty sky blue, cream, sepia, ink black, one warm yellow). "
             "Crisp, high detail, flat front-facing lighting, editorial magazine quality. Absolutely no text, no letters, no numbers, no logo, no watermark.")
    CHROMA = ("Isolated on a perfectly flat pure chroma green background (#00FF00), even color, no gradient, no shadow on the green, "
              "nothing else in the frame, generous green margin around the subject.")
    shots = json.load(open(os.path.join(D,'shots.json')))
    for s in shots:
        s['prompt'] = s['subject'] + (' ' + CHROMA if s['kind'] == 'cutout' else '') + '\nStyle: ' + STYLE
    return shots
