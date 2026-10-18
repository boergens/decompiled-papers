"""Figure 1-figure supplement 1A: slice thickness (um), mean +/- SEM, versus fix vehicle osmolarity (mOsm),
with a 'perfused' category left of the axis break. Tier 3, digitized from the eLife full-size JPEG
elife-08206-fig1-figsupp1-v3.jpg (same pixels as the image on p. 3 of elife-08206-figures-v3.pdf).

Markers: connected components of dark pixels (grey < 128) inside the plot area with a filled core
(opening with a 7x7 square removes the thin error bars); centre = centroid of the core. Error-bar ends:
outermost dark rows in the marker's column window (+-3 px), moved 1 px inward to the cap centre.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *
from scipy import ndimage

a = load("fig1-figsupp1")
g = a.astype(float).mean(2)
ax = Axis([(503.5, 200), (624.5, 300), (745.5, 400), (867.5, 500)])
ay = Axis([(609.5, 0), (521.5, 100), (433.75, 200), (345.75, 300), (258.25, 400), (170.25, 500), (82.5, 600)])
X0, Y0, X1, Y1 = 205, 70, 890, 600
dark = g[Y0:Y1, X0:X1] < 128
core = ndimage.binary_opening(dark, np.ones((7, 7)))
lab, n = ndimage.label(core)
rows, pts = [], []
comps = sorted(range(1, n + 1), key=lambda i: np.where(lab == i)[1].mean())
for i in comps:
    ys, xs = np.where(lab == i)
    xc, yc = X0 + xs.mean(), Y0 + ys.mean()
    win = dark[:, int(round(xc)) - X0 - 3:int(round(xc)) - X0 + 4].any(1)
    rr = np.where(win)[0]
    # contiguous run through the marker centre
    runs_ = np.split(rr, np.where(np.diff(rr) > 1)[0] + 1)
    r = next(q for q in runs_ if Y0 + q[0] <= yc <= Y0 + q[-1])
    top, bot = Y0 + r[0] + 1.0, Y0 + r[-1] - 1.0
    cat = "perfused" if xc < 400 else ""
    rows.append([cat, "" if cat else ax(xc), ay(yc), ay(bot), ay(top)])
    pts += [(xc, yc), (xc, top), (xc, bot)]
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 1-figure supplement 1A: Slice thickness (um) vs Fix vehicle osmolarity (mOsm).",
       "Columns: category ('perfused' = left of the axis break), osmolarity_mOsm (marker centre; empty for perfused),",
       "  thickness_um (mean, marker centre), err_low_um, err_high_um (error-bar ends; caption: mean +/- SEM).",
       "Provenance: tier 3, digitized from elife_figure_supplements/elife-08206-fig1-figsupp1-v3.jpg; figures/sfig1-1a_extract.py.",
       ax.describe("x") + ".", ay.describe("y") + ".",
       f"Uncertainty: +-1 px = +-{abs(ax.m):.2g} mOsm and +-{abs(ay.m):.2g} um. The point at ~407 mOsm shows no error bar outside its",
       "  marker (ends = marker edges). Caption: nominal thickness 500 um; n = 20 slices from 6 animals; one-way ANOVA p = 0.46."]
write_csv(os.path.join(HERE, "sfig1-1a.csv"), hdr, ["category", "osmolarity_mOsm", "thickness_um", "err_low_um", "err_high_um"],
          rows, ["{}", "{:.1f}", "{:.1f}", "{:.1f}", "{:.1f}"])
draw(a, pts, os.path.join(WORK, "sfig1-1a_overlay.png"))
for r in rows: print(r)
