"""Digitize Fig. 6 (p. 5 of the PDF, journal p. 031104-4): WGP on PC film with Al deposited at 80 deg;
left panel "Transmission" (TM, TE vs wavelength), right panel "Extinction Ratio" (ER and its 200-point moving
average). Tier 3: one embedded Flate image (1750 x 621 px, 300 ppi); no vector paths on the page.

Calibration: x from the tick marks under each x axis (400 ... 900 nm), y from the tick marks left of each y axis
(left 10 ... 100 %, right 500 ... 4000), darkness centroids; the x-axis lines are checked as value 0.
Series by colour masks (OpenCV HSV): TM blue, TE red (on the x axis), ER purple (noisy: per pixel column the
lowest and highest value its ink reaches), "200 per. Mov. Avg. (ER)" thin black line (darkest smooth path,
dynamic programming, because the purple trace crosses it everywhere).
Writes figures/fig6left.csv, figures/fig6right.csv and work/fig6_overlay.png.

    python3 -I -B figures/fig6_extract.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "work"))
import digi  # noqa: E402

a = digi.image(5, (103.9, 247.1, 523.9, 396.1))
g = digi.gray(a)
hsv = digi.hsv(a)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]

# ---------------------------------------------------------------- left panel
xt = digi.ticks_x(g, (525, 531), 90, 860, thr=15)
assert len(xt) == 6, xt
fx, ix, rx, _ = digi.fit(xt, [400, 500, 600, 700, 800, 900])
yt = digi.ticks_y(g, (86, 93), 60, 520, thr=8)
assert len(yt) == 10, yt
fy, iy, ry, _ = digi.fit(yt, list(range(100, 0, -10)))
axis_row = 522.0
print("left: x res %.2f nm, y res %.2f %%, axis line -> %.2f %%" % (rx, ry, fy(axis_row)))

blue = (H >= 98) & (H <= 114) & (S > 90) & (V < 235)
red = ((H <= 8) | (H >= 172)) & (S > 120)
tm = digi.trace_line(blue, 95, 830, 60, 260, start_hint=None, max_jump=6)
te = digi.trace_line(red, 98, 830, 512, 532, start_hint=521, max_jump=4)
rows, pts_l = [], []
for name, tr in (("TM", tm), ("TE", te)):
    for c, mid, top, bot in tr:
        if mid != mid:
            continue
        rows.append([name, float(fx(c)), float(fy(mid)), float(fy(bot)), float(fy(top))])
        pts_l.append((c, mid))
hdr = [
    "Fig. 6, left panel 'Transmission' (ahn2013, PDF p. 5): WGP on PC film, Al deposited at 80 deg.",
    "Columns: series (TM, TE, as labelled in the panel), wavelength_nm, transmission_pct (centre of the line in that",
    "pixel column), transmission_min_pct / transmission_max_pct (lower / upper edge of the drawn line, about 5 px).",
    "Provenance: tier 3, digitized from the embedded Flate image (1750 x 621 px) with figures/fig6_extract.py; colour",
    "masks; one row per source pixel column (0.68 nm). x from 6 tick marks (max residual %.2f nm), y from 10 tick" % rx,
    "marks 10 ... 100 (max residual %.2f %%; the x-axis line maps to %.2f %%)." % (ry, fy(axis_row)),
    "Uncertainty: about 1 px: +-0.7 nm in x, +-0.25 % in y. The TM line ends in a dot at about 885 nm. 'Max. TR ~ 85%',",
    "the arrows and the labels TM / TE are annotations. TE lies on the x axis (about 0 %) over the whole range.",
]
digi.write_csv(os.path.join(HERE, "fig6left.csv"), hdr,
               ["series", "wavelength_nm", "transmission_pct", "transmission_min_pct", "transmission_max_pct"],
               rows, ["{}", "{:.1f}", "{:.2f}", "{:.2f}", "{:.2f}"])

# ---------------------------------------------------------------- right panel
xt2 = digi.ticks_x(g, (526, 532), 985, 1750, thr=15)
assert len(xt2) == 6, xt2
fx2, ix2, rx2, _ = digi.fit(xt2, [400, 500, 600, 700, 800, 900])
yt2 = digi.ticks_y(g, (984, 991), 60, 520, thr=8)
assert len(yt2) == 8, yt2
fy2, iy2, ry2, _ = digi.fit(yt2, list(range(4000, 0, -500)))
axis_row2 = 522.5
print("right: x res %.2f nm, y res %.1f, axis line -> %.0f" % (rx2, ry2, fy2(axis_row2)))

purple = (H >= 120) & (H <= 150) & (S > 25) & (V < 228)
purple[440:500, 1120:1470] = False   # colour fringes of the black annotation "ER > 3000 @ 700nm" (no data there)
top_row, bot_row = 66, 519       # 4000 at row ~69, axis line at ~522
legend = (1010, 1330, 75, 145)   # legend: two sample lines + "ER", "200 per. Mov. Avg. (ER)"
rows2, pts_p, pts_k = [], [], []
for c in range(996, 1745):
    col = purple[top_row - 4:bot_row + 1, c].copy()
    if legend[0] <= c <= legend[1]:
        col[legend[2] - (top_row - 4):legend[3] - (top_row - 4)] = False
    r = np.where(col)[0]
    if not len(r):
        continue
    t, b = top_row - 4 + r.min(), top_row - 4 + r.max()
    flag = []
    if t <= top_row:
        flag.append("reaches_top_of_plot")
    if b >= bot_row - 1:
        flag.append("reaches_axis_line")
    rows2.append(["ER", float(fx2(c)), "", float(fy2(b)), float(fy2(t)), "+".join(flag)])
    pts_p += [(c, t), (c, b)]

cost = np.where((V < 150) & (S < 100), V, 255).astype(float)
cost[legend[2]:legend[3], legend[0]:legend[1]] = 255
cost[440:500, 1120:1470] = 255      # the annotation "ER > 3000 @ 700nm" (black bold text)
# start / end of the moving average from the mask itself
dark = (V < 150) & (S < 100)
dark[legend[2]:legend[3], legend[0]:legend[1]] = False
dark[440:500, 1120:1470] = False
cols = [c for c in range(1000, 1745) if dark[70:518, c].any()]
kc0, kc1 = cols[0], cols[-1] + 1
path = digi.dp_path(cost, kc0, kc1, 66, 519, jump=12, lam=3.0)
for i, c in enumerate(range(kc0, kc1)):
    r = int(path[i])
    win = V[r - 3:r + 4, c].astype(float)
    if win.min() >= 150:
        continue
    w = np.clip(150 - win, 0, None)
    mid = r - 3 + float((np.arange(7) * w).sum() / w.sum())
    t = b = r - 3 + int(np.argmin(win))
    while t > 66 and V[t - 1, c] < 150:
        t -= 1
    while b < 518 and V[b + 1, c] < 150:
        b += 1
    rows2.append(["200 per. Mov. Avg. (ER)", float(fx2(c)), float(fy2(mid)), float(fy2(b)), float(fy2(t)), ""])
    pts_k.append((c, mid))
hdr2 = [
    "Fig. 6, right panel 'Extinction Ratio' (ahn2013, PDF p. 5): WGP on PC film, Al deposited at 80 deg.",
    "Columns: series (legend names), wavelength_nm, extinction_ratio (centre of the line; empty for the noisy 'ER'),",
    "er_min / er_max (lowest / highest value the series' ink reaches in that pixel column), flags.",
    "'ER' = purple trace, very noisy: each pixel column gives the range it covers; reaches_top_of_plot = runs past",
    "4000 (clipped there), reaches_axis_line = reaches the x-axis line (values below ~25 are hidden by it).",
    "'200 per. Mov. Avg. (ER)' = thin black line, followed as the darkest smooth path (dynamic programming), value =",
    "darkness-weighted centre, er_min / er_max = the dark run through it (its near-vertical end near 880 nm).",
    "Provenance: tier 3, digitized from the embedded Flate image (1750 x 621 px) with figures/fig6_extract.py; one row",
    "per source pixel column (0.68 nm). x from 6 tick marks (max residual %.2f nm), y from 8 tick marks 500 ... 4000" % rx2,
    "(max residual %.1f; the x-axis line maps to %.0f)." % (ry2, fy2(axis_row2)),
    "Uncertainty: about 1 px: +-0.7 nm in x, +-9 in ER. The legend box and the annotation 'ER > 3000 @ 700nm' are",
    "masked out; where the black line crosses dense purple ink the purple range includes the pixels under it.",
]
digi.write_csv(os.path.join(HERE, "fig6right.csv"), hdr2,
               ["series", "wavelength_nm", "extinction_ratio", "er_min", "er_max", "flags"],
               rows2, ["{}", "{:.1f}", "{:.0f}", "{:.0f}", "{:.0f}", "{}"])
digi.overlay(a, [((255, 0, 255), pts_l), ((0, 200, 0), pts_p), ((255, 140, 0), pts_k)],
             os.path.join(ROOT, "work", "fig6_overlay.png"))
print("rows", len(rows), len(rows2), "black cols", kc0, kc1)
