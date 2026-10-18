"""Digitize Fig. 1k of Kubota et al. 2018 (main PDF p. 3): pure water contact angle (PWCA) vs days after
plasma treatment, mean with SD error bars (n = 3).

Source: the embedded 300 ppi raster of panel k (416 x 297 px); tick labels are PDF text.
    python3 -I fig1k_extract.py  -> fig1k.csv (+ ../work/fig1k_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import pymupdf  # noqa: E402
from kubota_main_common import Img, calib, blobs, opened, WORK, PDF  # noqa: E402
from digitize_common import tick_positions, tick_positions_v, write_csv, overlay  # noqa: E402

im = Img(3, (368.1, 67.3, 468.0, 138.5))
d = im.g < 128
XAX, YAX = (283, 285), (10, 12)
xt = tick_positions(d, XAX, +1, 5, YAX[1] + 1, d.shape[1])
yt = tick_positions_v(d, YAX, -1, 5, 0, XAX[0])
labs = im.labels((340, 60, 470, 150), pattern=r"^\d+°?$")
# the x labels "–1 0 1 2 3" are one PDF text span with no space between "–1" and "0": take each digit's position
xl = [l for l in labs if l[2] > XAX[1] and l[0] in (7, 14)]   # "–10 1 2 3" is handled below
page = pymupdf.open(PDF)[2]
for b in page.get_text("rawdict", clip=pymupdf.Rect(370, 138, 410, 148))["blocks"]:
    for line in b["lines"]:
        for s in line["spans"]:
            chars = s["chars"]
            for i, ch in enumerate(chars):
                if ch["c"].isdigit():
                    neg = i > 0 and chars[i - 1]["c"] == "–"
                    x0 = chars[i - 1]["bbox"][0] if neg else ch["bbox"][0]
                    cx, cy = im.pt2px((x0 + ch["bbox"][2]) / 2, (ch["bbox"][1] + ch["bbox"][3]) / 2)
                    xl.append((-float(ch["c"]) if neg else float(ch["c"]), cx, cy, ch["c"]))
yl = [l for l in labs if l[1] < YAX[0]]
fx, rx, sx, xp, xv = calib(xt, xl, 1, tol=5)
fy, ry, sy, yp, yv = calib(yt, yl, 2)

m = d.copy()
m[XAX[0] - 2:, :] = False
m[:, :YAX[1] + 2] = False
disc = opened(m, 4)                      # the filled markers (~12 px); error bars and line are thinner
rows, pts = [], []
for cx, cy, area, box in sorted(blobs(disc, 30)):
    c = int(round(cx))
    # error-bar caps: rows (within +-45 px) whose dark run through column c is a short centred
    # horizontal run 8-16 px wide (caps and the marker itself; connecting lines are either too
    # thin (steep) or run on beyond c+-9 (shallow)); the outermost such rows are the caps' outer edges
    good = []
    for r in range(max(0, int(cy) - 45), min(XAX[0] - 2, int(cy) + 46)):
        if not m[r, c]:
            continue
        x0 = c
        while x0 > 0 and m[r, x0 - 1]:
            x0 -= 1
        x1 = c
        while x1 < m.shape[1] - 1 and m[r, x1 + 1]:
            x1 += 1
        if 8 <= x1 - x0 + 1 <= 16 and abs((x0 + x1) / 2 - c) <= 3:
            good.append(r)
    top, bot = float(min(good)), float(max(good))
    rtop, rbot = cy - top, bot - cy
    rad = (box[3] - box[1]) / 2
    hidden = rtop <= rad + 1 and rbot <= rad + 1
    # cap thickness ~2 px: the cap's centre is 1 px inside the run end
    rows.append((float(fx(cx)), float(fy(cy)), float(fy(top + 1)), float(fy(bot - 1)),
                 "caps at or inside the marker edge: SD about the marker radius or less" if hidden else ""))
    pts += [(cx, cy), (cx, top + 1), (cx, bot - 1)]
overlay(im.a, pts, os.path.join(WORK, "fig1k_overlay.png"))
write_csv(os.path.join(HERE, "fig1k.csv"), [
    "Kubota et al. 2018 Nat Commun 9:437, Fig. 1k: time course of the plasma treatment effect on the CNT-coated tape,",
    "  pure water contact angle (PWCA). Caption: 'Error bars denote SD'; 'n = 3' printed in the panel. Main PDF p. 3.",
    "Columns: days = x axis 'Days after plasma treatment' (the first point is at -1, i.e. before treatment);",
    "  pwca_deg = y axis 'Pure water contact angle' (degrees; top label printed as '80°'); sd_upper_deg / sd_lower_deg =",
    "  the ends (cap centres) of the SD error bar. Flag: where the caps sit at or inside the edge of the ~12 px",
    "  marker (no bar visible beyond it), the ends given are the outermost cap-like rows found; they only bound the",
    "  SD (about the marker radius, ~2 deg, or less).",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector plot paths in the PDF) by",
    "  fig1k_extract.py: marker centres by morphological opening + connected components; error-bar ends = outermost",
    "  rows (within +-45 px) with a centred 8-16 px horizontal run through the marker column (the caps), minus 1 px. Axes calibrated on the tick marks in the image paired",
    f"  with the PDF-text labels: x on {len(xp)} labelled ticks ({min(xv):g} to {max(xv):g}), max residual {rx:.3f} d;",
    f"  y on {len(yp)} labelled ticks ({min(yv):g}-{max(yv):g}), max residual {ry:.2f} deg. Ticks are 1 day and 10 deg apart.",
    f"Uncertainty: about +-{2 * abs(sx):.2f} day in x and +-{2 * abs(sy):.2f} deg in y (2 source pixels).",
], ["days", "pwca_deg", "sd_upper_deg", "sd_lower_deg", "flag"], rows, fmt=["{:.2f}", "{:.1f}", "{:.1f}", "{:.1f}", "{}"])
print(len(rows), "points; x", xp, xv, rx, "; y", yp, yv, ry)
for r in rows:
    print(r)
