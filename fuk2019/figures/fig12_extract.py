"""Fig. 12: Young's modulus, experimental and simulated, bar chart -> figures/fig12.csv (tier 3).

Run from anywhere: python3 -I figures/fig12_extract.py. Reads the embedded raster image
(649 x 499 px, 220 ppi) on p. 12 of source/fuk2019.pdf.
Method: frame and inward y ticks 1-5 GPa in the black mask, linear fit. Bars: the non-white column
groups along a row near the bottom, split at the dark bar outlines. Bar top: the darkest of the
first rows (scanning down, below the legend) where >= 90 % of the bar's inner columns are non-white
(the top outline). Error bar: grey line at the bar centre; its upper cap is the top end of the
contiguous non-white run above the bar. The part of the error bar inside the hatched bar cannot
be told from the hatching, so the lower end is not measured; err_low is given as equal to err_high
(the bars are drawn symmetric in Origin by default; this is an assumption, stated in the CSV).
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402
import fukplot as fp  # noqa: E402

a = fp.load(12, (191.0, 603.8, 403.5, 767.3))
dark = a.max(2) < 100
rows = dc.frame_lines(dark, 1, 0.5)
cols = dc.frame_lines(dark, 0, 0.5)
top, bot, left = rows[0], rows[-1], cols[0]
yt = sorted(fp.inward_ticks_y(dark, left[1], 1, 4, top[1] + 2, bot[0] - 1), reverse=True)
YV = [1, 2, 3, 4, 5]
assert len(yt) == 5, yt
fy, ry, my = fp.fit(yt, YV)
nonwhite = a.min(2) < 200
r = bot[0] - 12
c = np.where(nonwhite[r, left[1] + 3:])[0] + left[1] + 3
groups = np.split(c, np.where(np.diff(c) > 1)[0] + 1)
inner = [cc[1] for cc in cols[1:-1]]      # outline columns between two touching bars
bars = []
for g in groups:
    if len(g) < 50:
        continue
    splits = [x for x in inner if g[0] + 20 < x < g[-1] - 20]
    edges = [g[0]] + splits + [g[-1]]
    for c0, c1 in zip(edges[:-1], edges[1:]):
        bars.append((int(c0), int(c1)))
assert len(bars) == 4, bars
names = [("DGEBA/MTHPA", "Experimental", "3.27"), ("DGEBA/MTHPA", "Simulated", "4.14"),
         ("DGEBA/NA", "Experimental", "3.75"), ("DGEBA/NA", "Simulated", "4.87")]
out, pts = [], []
for (c0, c1), (grp, ser, lab) in zip(bars, names):
    cs = slice(c0 + 3, c1 - 2)
    frac = nonwhite[:, cs].mean(1)
    cand = [rr for rr in range(120, bot[0]) if frac[rr] > 0.9][:3]
    rtop = min(cand, key=lambda rr: a[rr, cs].mean())
    cc = (c0 + c1) // 2
    band = nonwhite[:, cc - 1:cc + 2].any(1)
    rcap = rtop - 1
    while band[rcap - 1]:
        rcap -= 1
    v, cap = float(fy(rtop)), float(fy(rcap))
    out.append((grp, ser, v, cap - v, cap - v, lab, (c0 + c1) / 2, rtop, rcap))
    pts += [(x, rtop) for x in range(c0, c1)] + [(cc, rcap)]
print(dict(yt=yt, ry=ry, bars=bars))
hdr = [
    "Fig. 12 of Fu et al. 2019, Polymers 11, 975: simulated and experimental Young's modulus (bar chart).",
    "Provenance: tier 3, digitized from the embedded 220 ppi raster image on p. 12; no source data published.",
    "Columns: system = x-axis group; series = legend entry; modulus_GPa = bar top; err_high_GPa = upper error-bar cap minus bar top;",
    "err_low_GPa = ASSUMED equal to err_high (the lower half of the error bar is hidden in the hatched bar and was not measured);",
    "printed_label = the value printed above the bar; px_x = bar centre column, px_top / px_cap = rows of bar top and cap in the image.",
    "Axis fit on the inward y ticks 1-5 GPa (max residual %.4f GPa); 1 px = %.4f GPa." % (ry, abs(my)),
]
dc.write_csv(str(ROOT / "figures/fig12.csv"), hdr,
             ["system", "series", "modulus_GPa", "err_low_GPa", "err_high_GPa", "printed_label", "px_x", "px_top", "px_cap"],
             out, fmt=["{}", "{}", "{:.3f}", "{:.3f}", "{:.3f}", "{}", "{:.1f}", "{}", "{}"])
(ROOT / "work").mkdir(exist_ok=True)
dc.overlay(a, pts, str(ROOT / "work/fig12_overlay.png"))
