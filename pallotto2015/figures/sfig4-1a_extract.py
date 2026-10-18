"""Figure 4-figure supplement 1A: convex hull volume (voxels) vs surface area (voxels), log-log, for cleft
contacts (grey x), AII amacrine cell tight contacts (blue dots) and cone bipolar cell tight contacts
(green dots). Tier 3, digitized from elife_figure_supplements/elife-08206-fig4-figsupp1-v3.jpg (709 x 703 px).

Dots: normalised cross-correlation of a filled-disc template (radius 4.5 px) with the blue / green colour
masks, peaks >= 0.45, non-maximum suppression 4 px. x marks: correlation of a template cut from an isolated
x (centre 273, 340; 13 x 13 px) with a mask of grey pixels, peaks >= 0.4, suppression 4 px; the dots are
drawn on top of the x marks, so x marks under dots are missed, and in the dense band along the diagonal
overlapping x marks are only partly separated. Expected counts (text p. 8-9): 150 cleft contacts,
4 AII tight contacts, 17 cone bipolar tight contacts.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *

a = load("fig4-figsupp1")
A = a.astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
ax = Axis([(123.25, 10), (264.5, 100), (406.5, 1e3), (547.5, 1e4), (689.0, 1e5)], log=True)
ay = Axis([(614.5, 10), (473.5, 100), (331.5, 1e3), (190.5, 1e4), (48.5, 1e5)], log=True)
green = ((G > 170) & (R < 120) & (B < 120)).astype(np.float32)
blue = ((B > 150) & (R < 80) & (G < 80)).astype(np.float32)
grey = ((np.abs(R - G) < 25) & (np.abs(G - B) < 25) & (R > 60) & (R < 200)).astype(np.float32)
yy, xx = np.mgrid[:13, :13]
disc = (np.hypot(xx - 6, yy - 6) <= 4.5).astype(np.float32)
REG = (126, 30, 700, 612)
rows, pts = [], []
for name, m in (("AII amacrine cell tight contact (blue)", blue), ("cone bipolar cell tight contact (green)", green)):
    for x, y, s in match_peaks(m, disc, 6, REG, 0.45, 4):
        rows.append([name, ax(x), ay(y), s])
        pts.append((x, y))
tx = grey[340 - 6:340 + 7, 273 - 6:273 + 7].copy()
for x, y, s in match_peaks(grey, tx, 6, REG, 0.4, 4):
    rows.append(["cleft contact (grey x)", ax(x), ay(y), s])
    pts.append((x, y))
from collections import Counter
cnt = Counter(r[0] for r in rows)
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 4-figure supplement 1A: Convex hull volume (voxels) vs Surface area (voxels).",
       "Columns: series, surface_area_voxels, convex_hull_volume_voxels, match_score (template correlation).",
       "Provenance: tier 3, digitized from elife_figure_supplements/elife-08206-fig4-figsupp1-v3.jpg; figures/sfig4-1a_extract.py.",
       ax.describe("x") + ".", ay.describe("y") + ".",
       f"Uncertainty: +-1 px = +-{abs(ax.m):.2g} decade on either axis (about +-1.6 %).",
       f"Markers found: {dict(cnt)}. Expected from the text: 150 cleft, 4 AII, 17 cone bipolar contacts. Missing x marks are hidden",
       "  under dots or under other x marks in the dense band; two overlapping dots may be counted as one (or vice versa)."]
write_csv(os.path.join(HERE, "sfig4-1a.csv"), hdr, ["series", "surface_area_voxels", "convex_hull_volume_voxels", "match_score"], rows,
          ["{}", "{:.4g}", "{:.4g}", "{:.2f}"])
draw(a, pts, os.path.join(WORK, "sfig4-1a_overlay.png"), r=1)
print(dict(cnt))
