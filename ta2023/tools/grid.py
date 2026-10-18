"""Draw a labelled pixel grid over an image region (for choosing exclusion rectangles). Usage: grid.py in.png x0 y0 x1 y1 scale out.png"""
import sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert("RGB")
x0, y0, x1, y1 = map(int, sys.argv[2:6]); s = float(sys.argv[6])
c = im.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * s), int((y1 - y0) * s)), Image.LANCZOS)
d = ImageDraw.Draw(c)
step = 50 if (x1 - x0) > 300 else 20
for x in range((x0 // step + 1) * step, x1, step):
    X = (x - x0) * s; d.line([(X, 0), (X, c.height)], fill=(255, 0, 255) if x % 100 == 0 else (255, 180, 255), width=1)
    d.text((X + 2, 2), str(x), fill=(200, 0, 200))
for y in range((y0 // step + 1) * step, y1, step):
    Y = (y - y0) * s; d.line([(0, Y), (c.width, Y)], fill=(255, 0, 255) if y % 100 == 0 else (255, 180, 255), width=1)
    d.text((2, Y + 2), str(y), fill=(200, 0, 200))
c.save(sys.argv[7])
