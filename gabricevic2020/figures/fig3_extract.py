"""Digitize Figure 3 of Gabričević, Lente & Fábián 2020 (poc.4045.pdf p. 4): kinetic curves at 280 nm, short time scale.

Source: the embedded raster image of Figure 3 (1003 x 710 px). The y axis is broken (two '//' marks at about
A = 0.3073 / 0.2618): the upper segment (0.308-0.310 labelled) holds the TCE trace, the lower segment (0.256-0.260
labelled) the cis-DCE trace. Each trace is a band of densely packed markers (TCE green triangles, cis-DCE blue
diamonds) with a thin pink fit curve drawn on top.
    python3 -I fig3_extract.py   -> fig3.csv (+ ../work/fig3_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from gab_common import (load, gray, tick_positions, tick_positions_v, fit_axis, colour_mask, track,  # noqa: E402
                        write_csv, overlay, WORK)

a = load("fig3")
dark = gray(a) < 120
BOT, LEFT = (591, 592), (158, 160)
xt = tick_positions(dark, BOT, 1, 10, 161, 989)
yt = tick_positions_v(dark, LEFT, -1, 10, 6, 589)
assert len(xt) == 4 and len(yt) == 5, (xt, yt)
fx, rx, sx = fit_axis([159.0] + xt + [990.5], [0, 1, 2, 3, 4, 5])     # left frame = 0, right frame = 5 (labelled)
fy_up, ry_up, sy_up = fit_axis(yt[:2], [0.310, 0.308])                 # upper segment: 2 labelled ticks only
fy_lo, ry_lo, sy_lo = fit_axis(yt[2:], [0.260, 0.258, 0.256])          # lower segment
BREAK = 218                                                            # row of the axis-break marks
box = (161, 6, 989, 589)
LEGEND = (400, 285, 670, 385)
PINK = (255, 140, 255)
series = [("TCE", (0, 128, 0), 500, 180, 177, fy_up, 6, BREAK), ("cis-DCE", (0, 0, 255), 500, 545, 555, fy_lo, BREAK, 589)]
rows, pts, fpts = [], [], []
for name, ref, c0, yb, yf, fy, r0, r1 in series:
    data = colour_mask(a, ref, alpha_min=0.45, alpha_max=1.4, tol=60)
    fit = colour_mask(a, PINK, alpha_min=0.5, alpha_max=1.4, tol=70)
    keep = np.zeros_like(data)
    keep[max(box[1], r0):min(box[3], r1), box[0]:box[2]] = True
    keep[LEGEND[1]:LEGEND[3], LEGEND[0]:LEGEND[2]] = False
    band = cv2.morphologyEx((data & keep).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 1), np.uint8)).astype(bool)
    tr = track(band, c0, yb, box[0], box[2], r0, r1, max_jump=12, max_gap=15, max_run=90)
    for c, (t, b) in tr.items():
        rows.append((name, "data band", float(fx(c)), float(fy((t + b) / 2)), float(fy(t)), float(fy(b))))
        pts += [(c, t), (c, b)]
    # marker clusters that the column tracker did not reach (the first ~0.1 s of cis-DCE lies above the main band)
    covered = np.zeros_like(band)
    for c, (t, b) in tr.items():
        covered[t:b + 1, c] = True
    n, lab, st, _ = cv2.connectedComponentsWithStats(band.astype(np.uint8), connectivity=8)
    for i in range(1, n):
        comp = lab == i
        if st[i][4] >= 150 and not (comp & covered).any():
            for c in range(st[i][0], st[i][0] + st[i][2]):
                r = np.where(comp[:, c])[0]
                if len(r):
                    rows.append((name, "data band (separate cluster)", float(fx(c)), float(fy((r[0] + r[-1]) / 2)), float(fy(r[0])),
                                 float(fy(r[-1]))))
                    pts += [(c, r[0]), (c, r[-1])]
            print(name, "extra cluster", st[i])
    trf = track(fit & keep, c0, yf, box[0], box[2], r0, r1, max_jump=3, max_gap=10, max_run=6)
    for c, (t, b) in trf.items():
        rows.append((name, "fit", float(fx(c)), float(fy((t + b) / 2)), "", ""))
        fpts.append((c, (t + b) / 2))
    print(name, "band t", fx(min(tr)), fx(max(tr)), "fit t", fx(min(trf)), fx(max(trf)), len(tr), len(trf))
rows.sort(key=lambda r: (r[0] != "TCE", r[1], r[2]))
overlay(a, pts, os.path.join(WORK, "fig3_overlay.png"))
from PIL import Image  # noqa: E402
overlay(np.array(Image.open(os.path.join(WORK, "fig3_overlay.png"))), fpts[::2], os.path.join(WORK, "fig3_overlay.png"),
        colour=(255, 160, 0))
write_csv(os.path.join(HERE, "fig3.csv"), [
    "Gabričević, Lente & Fábián 2020, J Phys Org Chem 33:e4045, Figure 3: representative kinetic curves on short time",
    "  scale (stopped-flow), absorbance at 280 nm vs time. Broken y axis: TCE in the upper segment, cis-DCE in the lower.",
    "Columns: series (legend names); kind = 'data band' (densely packed markers merging into a band) or 'fit' (the thin",
    "  pink curve on each band; the caption does not name it) or 'data band (separate cluster)' (the first cis-DCE points,\n#   t < 0.08 s, which lie above the start of the main band); t_s = t (s); A_280 = A (280 nm), for 'data band' the middle",
    "  of the band in the pixel column, with A_upper/A_lower = the band's top and bottom edges (data scatter plus about",
    "  +-3 px of marker size). One row per pixel column of the source image.",
    "Provenance: tier 3, digitized from the embedded raster image (1003 x 710 px; no vector data in the PDF) by",
    f"  fig3_extract.py. x calibrated on the left and right frames (0 and 5, labelled) and 4 ticks, max residual {rx:.2g} s.",
    f"  y: separate linear maps for the two axis segments; upper on its two labelled ticks 0.310 and 0.308 ({abs(sy_up) * 1e3:.4f}",
    f"  x 10^-3 per px; no third tick to check it, but it matches the lower segment's {abs(sy_lo) * 1e3:.4f} x 10^-3 per px), lower on",
    f"  0.260, 0.258, 0.256 (max residual {ry_lo:.2g}).",
    f"Uncertainty: about +-{2 * abs(sx):.3f} s in x and +-{2 * abs(sy_lo):.5f} in A (2 px) for the fit curves.",
], ["series", "kind", "t_s", "A_280", "A_upper", "A_lower"], rows, fmt="{:.6g}")
