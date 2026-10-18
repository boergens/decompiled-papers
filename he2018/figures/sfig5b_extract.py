"""Extract Supplementary Figure 5b of He et al. 2018 (SI PDF p.7) from the PDF's vector paths -> sfig5b.csv.

All the work is in sfig5_vector.py (shared by panels b-e); see its docstring for the method.
Also draws the extracted points over a 4x render of the panel -> ../work/sfig5b_overlay.png.
    python3 -I sfig5b_extract.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pymupdf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
import sfig5_vector  # noqa: E402

info = sfig5_vector.write("b", HERE)
# overlay: render the panel at 4x and mark every marker centre (cyan) and trendline vertex (black dot)
box = sfig5_vector.PANELS["b"]["box"]
doc = pymupdf.open(os.path.join(HERE, "../source", sfig5_vector.PDF_NAME))
z = 4
pix = doc[6].get_pixmap(clip=pymupdf.Rect(*box), matrix=pymupdf.Matrix(z, z))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
for x, y in info["marker_xy"]:
    X, Y = (x - box[0]) * z, (y - box[1]) * z
    dr.ellipse((X - 3, Y - 3, X + 3, Y + 3), outline=(0, 255, 255), width=2)
for pts in info["curve_xy"].values():
    for x, y in pts:
        X, Y = (x - box[0]) * z, (y - box[1]) * z
        dr.point((X, Y), fill=(0, 0, 0))
im.save(os.path.join(HERE, "../work/sfig5b_overlay.png"))
