"""Digitize Fig. 5 (p. 5 of the PDF, journal p. 031104-4): bilayer WGP on film, transmission (left panel) and
extinction ratio (right panel) vs wavelength. Tier 3: the figure is one embedded JPEG (1725 x 550 px, 300 ppi);
no vector paths on the page.

Calibration: x from the tick marks under the x axis (400 ... 900 nm, darkness centroids); y from the centres of
the tick labels (the y axes have no visible tick marks), checked against the x-axis line (value 0).
Series by colour masks (OpenCV HSV), one value per pixel column, following the line from column to column:
  left:  TM (blue), TE (red, along the x axis);
  right: ER(L-B) (purple, the legend's only entry; a very noisy trace: per column the lowest and highest value
         the purple ink reaches), and an unlabelled thin black line (a smoothed curve through the purple data).
Writes figures/fig5left.csv, figures/fig5right.csv and the overlay work/fig5_overlay.png.

    python3 -I -B figures/fig5_extract.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "work"))
import digi  # noqa: E402

a = digi.image(5, (106.9, 59.8, 520.9, 191.8))
g = digi.gray(a)
hsv = digi.hsv(a)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]

# ---------------------------------------------------------------- left panel
xt = digi.ticks_x(g, (451, 457), 100, 860)
assert len(xt) == 6, xt
fx, ix, rx, _ = digi.fit(xt, [400, 500, 600, 700, 800, 900])
yl = digi.label_centres_y(g, (40, 98), 0, 470)
assert len(yl) == 11, yl
fy, iy, ry, my = digi.fit(yl, list(range(100, -1, -10)))
axis_row = 448.0
print("left: x ticks", np.round(xt, 1), "res %.2f nm; y labels res %.2f %%; axis line -> %.2f %%" % (rx, ry, fy(axis_row)))

blue = (H >= 98) & (H <= 114) & (S > 90) & (V < 235)
red = ((H <= 8) | (H >= 172)) & (S > 120)
tm = digi.trace_line(blue, 108, 800, 100, 340, start_hint=None, max_jump=6)
te = digi.trace_line(red, 112, 800, 440, 456, start_hint=448, max_jump=4)
rows = []
pts_l = []
for name, tr in (("TM", tm), ("TE", te)):
    for c, mid, top, bot in tr:
        if mid != mid:
            continue
        rows.append([name, float(fx(c)), float(fy(mid)), float(fy(bot)), float(fy(top))])
        pts_l.append((c, mid))
hdr = [
    "Fig. 5, left panel (ahn2013, PDF p. 5): transmission vs wavelength of the 50 mm x 50 mm bilayer WGP on film.",
    "Columns: series (TM, TE, as labelled in the panel), wavelength_nm, transmission_pct (centre of the line in that",
    "pixel column), transmission_min_pct / transmission_max_pct (lower / upper edge of the drawn line; the line is",
    "about 5 px = 1.1 % thick).",
    "Provenance: tier 3, digitized from the embedded JPEG (1725 x 550 px) with figures/fig5_extract.py; colour masks;",
    "one row per source pixel column (0.71 nm). x from 6 tick marks (max residual %.2f nm), y from the 11 tick-label" % rx,
    "centres 0 ... 100 (max residual %.2f %%; the x-axis line maps to %.2f %%)." % (ry, fy(axis_row)),
    "Uncertainty: about 1 px: +-0.7 nm in x, +-0.3 % in y. The TM line ends in a dot at about 885 nm. The panel's",
    "annotations 'Max TR = 80%', the arrows and the labels TM / TE are not data. TE lies on the x axis (about 0 %)",
    "over the whole range; its values near 0 are limited by the line width.",
]
digi.write_csv(os.path.join(HERE, "fig5left.csv"), hdr,
               ["series", "wavelength_nm", "transmission_pct", "transmission_min_pct", "transmission_max_pct"],
               rows, ["{}", "{:.1f}", "{:.2f}", "{:.2f}", "{:.2f}"])

# ---------------------------------------------------------------- right panel
xt2 = digi.ticks_x(g, (450, 458), 1005, 1600)
assert len(xt2) == 5, xt2
xl2 = digi.label_centres_x(g, (475, 505), 980, 1725)
assert len(xl2) == 6, xl2
fx2, ix2, rx2, _ = digi.fit(list(xt2) + [xl2[-1]], [400, 500, 600, 700, 800, 900])
yl2 = digi.label_centres_y(g, (930, 1005), 0, 470)
assert len(yl2) == 8, yl2
# faint tick marks left of the y axis (the 6000 tick is not found); the x-axis line (row 446) lies 3-4 px above the
# position of 0 given by the ticks and by the '0' label (row 449.5)
yt2 = digi.ticks_y(g, (1003, 1008), 0, 445, thr=4)
assert len(yt2) == 6, yt2
fy2, iy2, ry2, _ = digi.fit(yt2, [7000, 5000, 4000, 3000, 2000, 1000])
axis_row2 = 446.0
print("right: x res %.2f nm, y res %.1f" % (rx2, ry2), "0-label at %.1f -> %.0f, axis line -> %.0f, 6000-label -> %.0f"
      % (yl2[-1], fy2(yl2[-1]), fy2(axis_row2), fy2(yl2[1])))

purple = (H >= 120) & (H <= 150) & (S > 25) & (V < 228)
black = (V < 125) & (S < 100)
top_row, bot_row = 14, 444      # plot area (7000 at row ~13, axis line at 446)
rows2, pts_p, pts_k = [], [], []
legend = (1195, 1370, 130, 175)  # legend sample + text "ER(L-B)"
for c in range(1017, 1700):
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
    rows2.append(["ER(L-B)", float(fx2(c)), "", float(fy2(b)), float(fy2(t)), "+".join(flag)])
    pts_p += [(c, t), (c, b)]
# black line: darkest smooth path (dynamic programming over columns), since purple spikes cross it everywhere;
# columns where the path pixel is not dark (V >= 150) are dropped (line hidden or absent there)
cost = np.where((V < 150) & (S < 100), V, 255).astype(float)
cost[legend[2]:legend[3], legend[0]:legend[1]] = 255
kc0, kc1 = 1043, 1681
path = digi.dp_path(cost, kc0, kc1, 20, 443, jump=12, lam=3.0)
for i, c in enumerate(range(kc0, kc1)):
    r = int(path[i])
    win = V[r - 3:r + 4, c].astype(float)
    if win.min() >= 150:
        continue
    w = np.clip(150 - win, 0, None)
    mid = r - 3 + float((np.arange(7) * w).sum() / w.sum())
    # vertical extent of the dark run through the path (near-vertical stretches of the line near 860-885 nm)
    t = b = r - 3 + int(np.argmin(win))
    while t > 20 and V[t - 1, c] < 150:
        t -= 1
    while b < 442 and V[b + 1, c] < 150:
        b += 1
    rows2.append(["black line (no legend entry)", float(fx2(c)), float(fy2(mid)), float(fy2(b)), float(fy2(t)), ""])
    pts_k.append((c, mid))
hdr2 = [
    "Fig. 5, right panel (ahn2013, PDF p. 5): extinction ratio vs wavelength of the bilayer WGP on film.",
    "Columns: series, wavelength_nm, extinction_ratio (centre of the line; empty for the noisy purple series),",
    "er_min / er_max (lowest / highest value the series' ink reaches in that pixel column), flags.",
    "Series: 'ER(L-B)' = the purple trace, the only legend entry; it is very noisy, so each pixel column gives the",
    "range it covers (its spikes run past the top of the plot, 7000, near 660-880 nm: flag reaches_top_of_plot, value",
    "clipped there; where it reaches the x-axis line, drawn at ER ~ 60, flag reaches_axis_line: er_min is then ~95,",
    "the lowest value visible above that line). 'black line (no legend entry)' = a thin black curve that",
    "follows the purple data smoothly (the panel does not say what it is).",
    "Provenance: tier 3, digitized from the embedded JPEG (1725 x 550 px) with figures/fig5_extract.py; colour masks;",
    "one row per source pixel column (0.73 nm). x from 5 tick marks + the '900' label centre (max residual %.2f nm);" % rx2,
    "y from 6 faint tick marks left of the y axis, 1000 ... 7000 without 6000 (max residual %.1f); they put 0 at the" % ry2,
    "'0' label (%.0f there); the x-axis line itself is drawn 3-4 px higher (it maps to %.0f)." % (fy2(yl2[-1]), fy2(axis_row2)),
    "The black line was followed as the darkest smooth path through the plot (dynamic programming, one row per",
    "column), its value is the darkness-weighted centre near the path, er_min / er_max the dark run through it",
    "(captures its near-vertical stretches near 860-885 nm); columns where it is not visible are left out (e.g.",
    "under the red arrow near 665-690 nm).",
    "Uncertainty: about 1 px: +-0.7 nm in x, +-16 in ER. Where the black line crosses dense purple ink the purple",
    "range includes the pixels under it. The legend box (sample line and text) is masked out. 'ER > 4500' and the",
    "red arrow are annotations, not data; the red arrow covers the purple trace near 690-700 nm.",
]
digi.write_csv(os.path.join(HERE, "fig5right.csv"), hdr2,
               ["series", "wavelength_nm", "extinction_ratio", "er_min", "er_max", "flags"],
               rows2, ["{}", "{:.1f}", "{:.0f}", "{:.0f}", "{:.0f}", "{}"])

digi.overlay(a, [((255, 0, 255), pts_l), ((0, 200, 0), pts_p), ((255, 140, 0), pts_k)],
             os.path.join(ROOT, "work", "fig5_overlay.png"))
print("rows", len(rows), len(rows2))
