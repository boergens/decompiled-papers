"""Figure 2-figure supplement 1A: split/merger curves (Mergers / Object vs Splits / Object) for the four
ECS fractions, with shaded SEM bands and circles at the minimum total splits + mergers. Tier 3,
digitized from the eLife JPEG elife-08206-fig2-figsupp1-v3.jpg.

Lines: colour masks of the four legend colours; in each pixel column the centre of the colour run
nearest to the previous column's value (predicted linearly from the last 6 accepted columns across hidden stretches; runs further than 8 px + 0.3 px per skipped column are rejected). Where curves cross or lie on top of each
other, the lower-drawn colour is hidden and its columns are missing. Band edges are given only for the
0.6 % ECS curve (its band is isolated); the three other bands overlap one another and cannot be separated
by colour. Minimum circles: centres read on a 4x gridded zoom (+-2 px).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *

a = load("fig2-figsupp1")
A = a.astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
ax = Axis([(146.0, 0), (235.0, 0.1), (324.0, 0.2), (413.0, 0.3), (502.0, 0.4), (591.0, 0.5)])
ay = Axis([(587.0, 0), (498.0, 0.1), (409.0, 0.2), (320.0, 0.3), (231.0, 0.4), (142.0, 0.5)])
M = {"0.6% ECS": (R > 40) & (R < 115) & (G > 30) & (G < 100) & (B > 100) & (B < 180) & (B - G > 40),
     # 5.8%: olive where free, brownish where the red band lies over it
     "5.8% ECS": (((R > 55) & (R < 125) & (G > 80) & (G < 140) & (B > 15) & (B < 85) & (G - B > 30) & (G - R > 8))
                  | ((R > 115) & (R < 160) & (G > 60) & (G < 100) & (B < 40))),
     # 11.3%: pure orange, or orange tinted by the overlying bands (still R - B > 140, G - B > 50)
     "11.3% ECS": ((R > 220) & (G > 105) & (G < 175) & (B < 70)) | ((R > 215) & (G > 120) & (G < 165) & (B < 75) & (R - B > 150)),
     "23.9% ECS": (R > 95) & (R < 175) & (G < 45) & (B < 45)}
band06 = (B > 175) & (B < 225) & (R > 170) & (R < 215) & (G > 165) & (G < 210) & (B - G > 8)
X0, X1, Y0, Y1 = 149, 678, 50, 584
SEED = {"0.6% ECS": 52, "5.8% ECS": 411, "11.3% ECS": 313, "23.9% ECS": 384}   # y where tracing starts
START = {"0.6% ECS": X0, "5.8% ECS": 304, "11.3% ECS": X0, "23.9% ECS": X0}   # 5.8%: its upper-left part lies under the orange line
rows, pts = [], []
for s, m in M.items():
    m = m.copy()
    m[:, :X0] = False
    m[:160, 480:] = False if s != "0.6% ECS" else m[:160, 480:]   # keep legend (top right) out
    m[:150, 470:] = False
    prev, lastc, slope = SEED[s] - Y0, START[s], 0.0      # start of the curve (left end), read on the zoom
    hist = []
    for c in range(START[s], X1):
        rr = runs(m[Y0:Y1, c])
        if not rr:
            continue
        pred = prev + slope * (c - lastc)            # linear prediction across gaps (hidden stretches)
        r = min(rr, key=lambda q: abs(q.mean() - pred))
        if len(r) < 2 or abs(r.mean() - pred) > 8 + 0.3 * (c - lastc):
            continue
        hist.append((c, r.mean()))
        if len(hist) >= 6:
            slope = np.polyfit(*zip(*hist[-6:]), 1)[0]
        prev, lastc = r.mean(), c
        y = Y0 + r.mean()
        lo = hi = np.nan
        if s == "0.6% ECS":
            t, b = band_extent(band06, m, c, y, Y0, Y1)
            lo, hi = ay(b), ay(t)
        rows.append([s, "curve", ax(c), ay(y), lo, hi])
        pts.append((c, y))
for s, (x, y) in {"0.6% ECS": (434, 183), "5.8% ECS": (313, 410), "11.3% ECS": (277, 365), "23.9% ECS": (297, 389)}.items():
    rows.append([s, "circle (mean of the minimum total splits + mergers)", ax(x), ay(y), "", ""])
    pts.append((x, y))
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 2-figure supplement 1A: Mergers / Object vs Splits / Object, curves parameterized by",
       "  the network output threshold; lines = mean, shaded = standard error of the mean, circles = mean of the minimum total",
       "  splits + mergers per object (caption).",
       "Columns: series (legend), kind (curve sample per pixel column, or circle), splits_per_object, mergers_per_object,",
       "  band_low, band_high (edges of the shaded band in that column; 0.6% ECS only).",
       "Provenance: tier 3, digitized from elife_figure_supplements/elife-08206-fig2-figsupp1-v3.jpg; figures/sfig2-1a_extract.py.",
       ax.describe("x") + ".", ay.describe("y") + ".",
       f"Uncertainty: +-1.5 px = +-{1.5 * abs(ay.m):.2g} per object; circles +-2 px. The 0.6% ECS curve leaves the plot at the top",
       "  (y = 0.6) and all curves are clipped at x = 0.6 (right frame). Curves of 5.8, 11.3 and 23.9% overlap; columns where a",
       "  colour is hidden are missing. The 5.8% ECS line is traced only from x ~ 0.18 on: further up-left it runs under the",
       "  orange 11.3% line (its start, like the other lower curves, is near splits ~0.12-0.13, mergers ~0.3)."]
write_csv(os.path.join(HERE, "sfig2-1a.csv"), hdr, ["series", "kind", "splits_per_object", "mergers_per_object", "band_low", "band_high"],
          rows, ["{}", "{}", "{:.4f}", "{:.4f}", "{:.4f}", "{:.4f}"])
draw(a, pts, os.path.join(WORK, "sfig2-1a_overlay.png"), r=1)
from collections import Counter
print(Counter(r[0] for r in rows))
