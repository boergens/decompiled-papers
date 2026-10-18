"""Fig. 2 (kremer2015): digitize the length-scale axis of the schematic and the positions of its five pins.

Tier 3 (digitized). Reads the embedded image of Fig. 2 (p. 6, the only image on that page, 1080 x 818 px,
200 ppi) straight from ../source/kremer2015.pdf, finds the horizontal scale line (the longest dark row),
its eight tick marks (labelled 10^-2 m ... 10^-9 m from left to right) and the five pins (vertical lines
from the scale line down to an example image). Fits log10(length/m) = a + b * x_px through the tick
centres (least squares) and converts each pin's centre column.

Writes figures/fig2.csv and work/fig2_overlay.png (creates work/).
Run from anywhere: python3 -I -B figures/fig2_extract.py
"""
import csv
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PDF = ROOT / "source" / "kremer2015.pdf"
OUT = HERE / "fig2.csv"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)

doc = pymupdf.open(PDF)
page = doc[5]
xref = page.get_images()[0][0]
pix = pymupdf.Pixmap(doc, xref)
if pix.n - pix.alpha > 3:
    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
img = Image.frombytes("RGB" if pix.n >= 3 else "L", (pix.width, pix.height), pix.samples).convert("RGB")
g = np.asarray(img.convert("L")).astype(int)
H, W = g.shape


def runs(mask):
    out = []
    for x in np.where(mask)[0]:
        if out and x == out[-1][1] + 1:
            out[-1][1] = x
        else:
            out.append([x, x])
    return [(a + b) / 2 for a, b in out], out


# scale line: the row (in the lower half) with the most dark pixels
rows = range(H // 2, H - 100)
axis_y = max(rows, key=lambda r: int((g[r, :] < 100).sum()))
axis_y2 = axis_y + 1 if (g[axis_y + 1, :] < 100).sum() > 0.8 * (g[axis_y, :] < 100).sum() else axis_y
ax_runs = runs(g[axis_y, :] < 100)[1]
ax_x0, ax_x1 = max(ax_runs, key=lambda r: r[1] - r[0])

# ticks: dark columns 4..12 px above the line (tick marks extend above and below it)
above = np.all(g[axis_y - 12:axis_y - 3, :] < 120, axis=0)
ticks, _ = runs(above)
assert len(ticks) == 8, ticks
labels = [-2, -3, -4, -5, -6, -7, -8, -9]
b, a = np.polyfit(ticks, labels, 1)
res = np.array(labels) - (a + b * np.array(ticks))

# pins: dark columns 20..30 px below the line that are not ticks (ticks end ~12 px below)
below = np.all(g[axis_y2 + 20:axis_y2 + 30, :] < 120, axis=0)
pins, _ = runs(below)
pins = [p for p in pins if all(abs(p - t) > 3 for t in ticks)]
assert len(pins) == 5, pins

# lower end of each pin: follow the dark column down until it stops
pin_end = []
for p in pins:
    c = int(round(p))
    y = axis_y2 + 20
    while y + 1 < H and min(g[y + 1, c - 1:c + 2]) < 120:
        y += 1
    pin_end.append(y)

px_err = 1.0  # about one source pixel for line centres
targets = ["photograph of a whole yellow, lobed organ on black, with a small black-and-white round marker at its left edge",
           "green fluorescence image of an irregular tissue fragment",
           "greyscale SEM-type image of a cell with a dark rounded nucleus, on white background",
           "greyscale EM micrograph with a dark curved membrane-like band",
           "greyscale EM micrograph of membrane profiles (neuropil-like) with a dark-rimmed round profile"]
with open(OUT, "w", newline="") as f:
    f.write("# Fig. 2 (kremer2015, p. 6), single panel: length-scale axis of the schematic 'Summary of imaging modalities and scales'.\n")
    f.write("# Provenance: tier 3, digitized from the embedded raster (1080 x 818 px, 200 ppi) by figures/fig2_extract.py.\n")
    f.write("# The axis is logarithmic, decreasing from left to right; ticks labelled 10^-2 m ... 10^-9 m.\n")
    f.write(f"# Calibration: log10(length/m) = {a:.4f} + ({b:.6f}) * x_px, least squares on the 8 tick centres; residuals (decades): "
            + ", ".join(f"{r:+.3f}" for r in res) + "\n")
    f.write(f"# Uncertainty: about +/-1 px = +/-{abs(b):.4f} decade. The pins mark the scale of example images; the figure gives no numbers for them,\n")
    f.write("# so the pin values are only where the pin meets the axis. Tick labels sit slightly left of their tick marks; the tick marks are used.\n")
    f.write("# Columns: kind (tick/pin), index (left to right), x_px (column in the embedded image), log10_length_m, length_m,\n")
    f.write("#   label (printed tick label, for ticks), pin_bottom_y_px (row where the pin line ends at its image, for pins; axis row = "
            f"{axis_y}), target (the example image the pin leads to, decompiler's description)\n")
    w = csv.writer(f)
    w.writerow(["kind", "index", "x_px", "log10_length_m", "length_m", "label", "pin_bottom_y_px", "target"])
    for i, (t, l) in enumerate(zip(ticks, labels)):
        v = a + b * t
        w.writerow(["tick", i + 1, f"{t:.1f}", f"{v:.3f}", f"{10**v:.3g}", f"10^{l} m", "", ""])
    for i, (p, e, tg) in enumerate(zip(pins, pin_end, targets)):
        v = a + b * p
        w.writerow(["pin", i + 1, f"{p:.1f}", f"{v:.3f}", f"{10**v:.3g}", "", e, tg])

ov = img.copy()
d = ImageDraw.Draw(ov)
d.line([(ax_x0, axis_y), (ax_x1, axis_y)], fill=(0, 200, 255), width=1)
for t in ticks:
    d.line([(t, axis_y - 25), (t, axis_y + 25)], fill=(255, 0, 255), width=1)
for p, e in zip(pins, pin_end):
    d.ellipse([p - 5, axis_y - 5, p + 5, axis_y + 5], outline=(255, 0, 0), width=2)
    d.ellipse([p - 5, e - 5, p + 5, e + 5], outline=(255, 0, 0), width=2)
ov.save(WORK / "fig2_overlay.png")
print("axis row", axis_y, "ticks", ticks, "pins", pins, "pin ends", pin_end, "fit", a, b, "res", res)
