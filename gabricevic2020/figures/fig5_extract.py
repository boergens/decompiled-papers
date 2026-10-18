"""Digitize Figure 5 of Gabričević, Lente & Fábián 2020 (poc.4045.pdf p. 5): k_obs of the fast step vs [OH-].

Source: the embedded raster image of Figure 5 (1003 x 729 px). Three marker series and one black fit line.
    python3 -I fig5_extract.py   -> fig5.csv (+ ../work/fig5_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from gab_common import (load, gray, tick_positions, tick_positions_v, fit_axis, scatter, colour_mask, track,  # noqa: E402
                        write_csv, cross_overlay, WORK)

a = load("fig5")
dark = gray(a) < 120
BOT, LEFT = (611, 612), (139, 140)            # frame lines found with frame_lines()
xt = tick_positions(dark, BOT, 1, 10, 142, 995)
yt = tick_positions_v(dark, LEFT, -1, 10, 8, 609)
assert len(xt) == 5 and len(yt) == 4, (xt, yt)
fx, rx, sx = fit_axis([139.5] + xt, [0.0, 0.02, 0.04, 0.06, 0.08, 0.10])   # left frame = 0.00 (labelled)
fy, ry, sy = fit_axis(yt + [611.5], [4, 3, 2, 1, 0])                     # bottom frame = 0 (labelled)

LEGEND = (470, 100, 760, 245)
series = [("trans-DCE", (255, 0, 0)), ("cis-DCE", (0, 0, 255)), ("TCE", (0, 128, 0))]
found = scatter(a, series, (143, 7, 995, 609), exclude=[LEGEND], close=5)
# The trans-DCE circle at [OH-] = 0.02 is almost completely covered by the TCE triangle and the cis-DCE diamond;
# only a thin red arc at its top shows (about 30 px). Its centre is estimated as the arc's mid column and
# the arc's top row + the median circle radius.
red = colour_mask(a, (255, 0, 0), alpha_min=0.3)
ys, xs = np.where(red[300:420, 240:340])
rad = np.median([h for n, x, y, w, h, f in found if n == "trans-DCE"]) / 2
found.append(("trans-DCE", (xs.min() + xs.max()) / 2 + 240, ys.min() + 300 + rad, int(xs.max() - xs.min() + 1),
              int(ys.max() - ys.min() + 1), "almost completely hidden; centre estimated from the visible top arc + radius"))
rows = [(n, "marker", float(fx(x)), float(fy(y)), w, h, f) for n, x, y, w, h, f in found]
pts = [(x, y) for n, x, y, w, h, f in found]

# the black fit line ("best fit to the formula give in Equation (1)"), drawn on top of the markers
blk = colour_mask(a, (0, 0, 0), alpha_min=0.6, alpha_max=1.2, tol=40)
blk[:, :146] = False
blk[606:, :] = False
blk[LEGEND[1]:LEGEND[3], LEGEND[0]:LEGEND[2]] = False
xs_seed = 600
col = np.where(blk[8:606, xs_seed])[0] + 8
seed = int(col.mean())
tr = track(blk, xs_seed, seed, 146, 995, 8, 606, max_jump=4, max_run=12)
line_pts = []
for c, (t, b) in tr.items():
    rows.append(("fit (Equation 1)", "line", float(fx(c)), float(fy((t + b) / 2)), "", "", ""))
    line_pts.append((c, (t + b) / 2))
cross_overlay(a, pts, os.path.join(WORK, "fig5_overlay.png"))
from gab_common import overlay  # noqa: E402
from PIL import Image  # noqa: E402
overlay(np.array(Image.open(os.path.join(WORK, "fig5_overlay.png"))), line_pts[::3], os.path.join(WORK, "fig5_overlay.png"),
        colour=(0, 255, 255))

# check: the paper's fit, k_obs = kacid [H+]/([H+] + 10^-pK), kacid = 4.3 s-1, pK = 12.0, pKw = 13.58 (text p. 5)
lx = np.array([r[2] for r in rows if r[1] == "line"])
ly = np.array([r[3] for r in rows if r[1] == "line"])
H = 10 ** -13.58 / lx
model = 4.3 * H / (H + 1e-12)
dev = ly - model
rows.sort(key=lambda r: (r[1] != "marker", r[0], r[2]))
write_csv(os.path.join(HERE, "fig5.csv"), [
    "Gabričević, Lente & Fábián 2020, J Phys Org Chem 33:e4045, Figure 5: dependence of k_obs on the pH (plotted against",
    "  [OH-]) for the complexation (fast) reaction of the chlorinated ethylenes with osmium(VIII).",
    "Columns: series (legend names; 'fit (Equation 1)' = the continuous black line); kind = marker or line;",
    "  OH_mol_dm3 = [OH-] (mol/dm3); kobs_s-1 = k_obs (s-1); marker_w_px/marker_h_px = marker blob size; note.",
    "Provenance: tier 3, digitized from the embedded raster image (1003 x 729 px; no vector data in the PDF) by",
    f"  fig5_extract.py. x calibrated on the left frame (0.00) and 5 labelled ticks, max residual {rx:.2g}; y on the bottom",
    f"  frame (0) and 4 labelled ticks, max residual {ry:.2g}. Markers: centre of the bounding box of the colour blob.",
    "  Line: centre of the black line in each pixel column (one row per column), followed from x = 0.01 to 0.10.",
    f"Uncertainty: about +-{2 * abs(sx):.4f} mol/dm3 in x and +-{2 * abs(sy):.3f} s-1 in y (2 px); flagged markers",
    "  (overlapping another marker) more.",
    f"Check: the traced line agrees with the paper's fit parameters (k_acid = 4.3 s-1, pK = 12.0, k_base = 0, pKw = 13.58,",
    f"  p. 5) to mean {dev.mean():+.3f}, max abs {np.abs(dev).max():.3f} s-1.",
], ["series", "kind", "OH_mol_dm3", "kobs_s-1", "marker_w_px", "marker_h_px", "note"], rows)
print("fig5:", len(found), "markers,", len(lx), "line columns; residuals", rx, ry, "line vs model", dev.mean(), np.abs(dev).max())
for r in rows:
    if r[1] == "marker":
        print(r)
