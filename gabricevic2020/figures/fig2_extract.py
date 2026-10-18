"""Digitize Figure 2 of Gabričević, Lente & Fábián 2020 (poc.4045.pdf p. 3): kinetic curves at 280 nm, long time scale.

Source: the embedded raster image of Figure 2 (1002 x 739 px). Each data set is plotted as densely packed small markers
that merge into a band (TCE green triangles, trans-DCE red circles, cis-DCE blue diamonds); a thin fit curve is drawn
on top of each band (pink on TCE and cis-DCE, cyan on trans-DCE).
    python3 -I fig2_extract.py   -> fig2.csv (+ ../work/fig2_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from gab_common import (load, gray, tick_positions, tick_positions_v, fit_axis, colour_mask, track,  # noqa: E402
                        write_csv, overlay, WORK)

a = load("fig2")
dark = gray(a) < 120
BOT, LEFT = (615, 616), (133, 135)
xt = tick_positions(dark, BOT, 1, 10, 136, 995)
yt = tick_positions_v(dark, LEFT, -1, 10, 7, 613)
assert len(xt) == 2 and len(yt) == 3, (xt, yt)
fx, rx, sx = fit_axis([134.0] + xt, [0, 5, 10])          # left frame = 0 (labelled)
fy, ry, sy = fit_axis(yt, [0.4, 0.3, 0.2])
box = (136, 7, 995, 613)
LEGEND = (430, 70, 690, 205)

PINK, CYAN = (255, 133, 255), (132, 255, 255)
series = [  # name, marker colour, fit colour, seed column, seed row (band), seed row (fit), longest band run
    ("TCE", (0, 128, 0), PINK, 600, 395, 399, 40),
    ("trans-DCE", (255, 0, 0), CYAN, 300, 476, 482, 150),     # steep start: allow long vertical runs
    ("cis-DCE", (0, 0, 255), PINK, 600, 512, 512, 80),
]
rows, pts, fpts = [], [], []
for name, ref, fref, c0, yb, yf, mr in series:
    data = colour_mask(a, ref, alpha_min=0.45, alpha_max=1.4, tol=60)
    fit = colour_mask(a, fref, alpha_min=0.5, alpha_max=1.4, tol=60)
    keep = np.zeros_like(data)
    keep[box[1]:box[3], box[0]:box[2]] = True
    keep[LEGEND[1]:LEGEND[3], LEGEND[0]:LEGEND[2]] = False
    # the fit curve is drawn on top of the band and splits it; close such gaps (up to ~6 px) vertically,
    # without adding fit pixels that lie outside the band
    band = cv2.morphologyEx((data & keep).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 1), np.uint8)).astype(bool)
    tr = track(band, c0, yb, box[0], box[2], box[1], box[3], max_jump=6, max_gap=8, max_run=mr)
    for c, (t, b) in tr.items():
        rows.append((name, "data band", float(fx(c)), float(fy((t + b) / 2)), float(fy(t)), float(fy(b))))
        pts += [(c, t), (c, b)]
    trf = track(fit & keep, c0, yf, box[0], box[2], box[1], box[3], max_jump=3, max_gap=10, max_run=6)
    for c, (t, b) in trf.items():
        y = float(fy((t + b) / 2))
        rows.append((name, "fit", float(fx(c)), y, "", ""))
        fpts.append((c, (t + b) / 2))
    print(name, "band x", fx(min(tr)), fx(max(tr)), "fit x", fx(min(trf)), fx(max(trf)), len(tr), len(trf))
overlay(a, pts, os.path.join(WORK, "fig2_overlay.png"))
from PIL import Image  # noqa: E402
overlay(np.array(Image.open(os.path.join(WORK, "fig2_overlay.png"))), fpts[::2], os.path.join(WORK, "fig2_overlay.png"),
        colour=(255, 160, 0))
write_csv(os.path.join(HERE, "fig2.csv"), [
    "Gabričević, Lente & Fábián 2020, J Phys Org Chem 33:e4045, Figure 2: representative kinetic curves on long time",
    "  scale, absorbance at 280 nm vs time.",
    "Columns: series (legend names); kind = 'data band' (the densely packed markers, which merge into a band) or 'fit'",
    "  (the thin curve drawn on top of each band: pink on TCE and cis-DCE, cyan on trans-DCE; the caption does not name it);",
    "  t_h = t (h); A_280 = A (280 nm), for 'data band' the middle of the band in this pixel column, with A_upper/A_lower",
    "  = the top and bottom edges of the band (scatter of the data plus about +-3 px of marker size).",
    "  One row per pixel column of the source image.",
    "Provenance: tier 3, digitized from the embedded raster image (1002 x 739 px; no vector data in the PDF) by",
    f"  fig2_extract.py. x calibrated on the left frame (0, labelled) and the ticks 5 and 10, max residual {rx:.2g} h;",
    f"  y on the 3 labelled ticks 0.2, 0.3, 0.4, max residual {ry:.2g}. Series found by colour masks and followed column by",
    "  column; where the cis-DCE and trans-DCE bands cross (t ~ 1.5-2 h) the red band is drawn over the blue one, so the",
    "  cis-DCE band has a gap there. Near t = 0 the bands are almost vertical and the first few markers (trans-DCE up to",
    "  A ~ 0.43, cis-DCE ~ 0.347) sit on the y axis line; the per-column trace starts at t = 0.026 h and misses some of them.",
    f"Uncertainty: about +-{2 * abs(sx):.3f} h in x and +-{2 * abs(sy):.4f} in A (2 px) for the fit curves; individual data",
    "  points cannot be separated (the markers overlap), so the band edges are the information that is there.",
], ["series", "kind", "t_h", "A_280", "A_upper", "A_lower"], rows, fmt="{:.5g}")
