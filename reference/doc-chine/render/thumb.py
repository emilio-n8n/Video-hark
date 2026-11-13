import sys
from vx import *
TW, TH = 1280, 720
src = sys.argv[1] if len(sys.argv) > 1 else 'thumb-a'
im = Image.open(os.path.join(IMG, src + '.png')).convert('RGB')
r = max(TW / im.width, TH / im.height)
im = im.resize((math.ceil(im.width * r), math.ceil(im.height * r)), Image.LANCZOS)
l, t = (im.width - TW) // 2, (im.height - TH) // 2
fr = im.crop((l, t, l + TW, t + TH)).convert('RGBA')
# darken left side slightly for legibility
grad = Image.linear_gradient('L').rotate(90).resize((TW, TH))
shade = Image.new('RGBA', (TW, TH), (20, 12, 8, 0)); shade.putalpha(grad.point(lambda v: int(v * 0.45)))
fr.alpha_composite(shade)
a = strip('50:26', 190, fnt=BLACK, color=YEL, seed=91, rot=-3, padx=40, pady=10)
b = strip("plus vite que l'homme", 70, fnt=SERIF, color=CREAM, seed=92, rot=2)
c = strip('LA CHINE NE COPIE PLUS', 46, fnt=BLACK, color=WHITE, seed=93, rot=-1.5, ink=RED)
paste(fr, c, 40, 95, 'l')
paste(fr, a, 40, 300, 'l')
paste(fr, b, 60, 500, 'l')
out = finish(fr.convert('RGB').resize((W, H)), 0).resize((TW, TH), Image.LANCZOS)
out.save(os.path.join(ROOT, '..', 'output', 'thumbnail.png'))
print('thumbnail ok')
