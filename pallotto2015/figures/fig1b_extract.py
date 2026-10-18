"""Fig. 1B: ECS fraction (%) vs fix vehicle osmolarity (mOsm) for olfactory bulb (x), retina (o) and
cortex (square), with the dashed (olfactory bulb) and solid (cortex) linear fits. Tier 3, digitized from the
embedded 300-ppi JPEG of Fig. 1 (elife-08206-v3.pdf p. 3).

Markers: approximate centres picked by eye on a gridded 3x zoom, then refined by normalised
cross-correlation (+-4 px) with a template cut from a clean marker of the same kind. The x axis is broken
(//): "perfused" is a category left of the break; its markers are given with x = "perfused".
Fit lines: end points read on an 6x zoom (+-1 px).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *

a = load("fig1")
g = a.astype(np.float32).mean(2)
ax = Axis([(964.5, 200), (1072.5, 300), (1181.0, 400), (1289.5, 500)])
ay = Axis([(488.5, 0), (427.5, 5), (366.5, 10), (305.5, 15), (244.5, 20), (183.5, 25), (122.5, 30), (61.5, 35)])

def templ(x, y, h):
    return g[y - h:y + h + 1, x - h:x + h + 1], h

TX = templ(1081, 305, 7)      # a clean x
TO = templ(1078, 212, 10)     # a clean circle
TS = templ(1188, 263, 9)      # a clean square
approx = {
    "olfactory bulb (x)": (TX, [(961, 366), (961, 378), (960, 417), (968, 417), (1081, 152), (1081, 305), (1119, 124),
                                (1119, 178), (1119, 216), (1129, 349), (1195, 87), (1195, 115), (1195, 213), (1234, 198)]),
    "retina (o)": (TO, [(1008, 331), (1042, 291), (1077, 212)]),
    "cortex (square)": (TS, [(965, 489), (1016, 432), (1075, 390), (1150, 362), (1150, 412), (1188, 263), (1188, 367),
                             (1188, 398), (1240, 315)]),
}
rows, pts = [], []
for name, ((T, h), ap) in approx.items():
    for (x, y, s) in refine(g, T, h, ap, 4):
        rows.append([name, "", round(float(ax(x)), 1), round(float(ay(y)), 2), round(s, 2), ""])
        pts.append((x, y))
# perfused category (left of the axis break): overlapping markers at the axis origin, read on an 8x zoom
rows.append(["olfactory bulb (x)", "perfused", "", round(float(ay(482.5)), 2), "", "overlapping cluster; x-shaped marks span rows 475-490"])
rows.append(["cortex (square)", "perfused", "", round(float(ay(489.0)), 2), "", "square centred on the x axis"])
rows.append(["unresolved", "perfused", "", "", "", "further marks overlap inside the square (possibly the retina circle and more x); not separable"])
pts += [(802, 482.5), (802, 489)]
lines = {"olfactory bulb fit (dashed)": [(962, 380), (1223, 122)], "cortex fit (solid)": [(966, 472.5), (1239, 318)]}
for name, ends in lines.items():
    for (x, y) in ends:
        rows.append([name, "line end", round(float(ax(x)), 1), round(float(ay(y)), 2), "", ""])
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 1B: ECS fraction (%) vs Fix vehicle osmolarity (mOsm).",
       "Columns: series (marker as in the caption: olfactory bulb x, retina o, cortex square; or a fit line), category",
       "  ('perfused' = left of the axis break, no osmolarity; 'line end' = end point of a fit line), osmolarity_mOsm, ecs_fraction_pct,",
       "  match_score (template correlation of the refined marker centre), note.",
       "Provenance: tier 3, digitized from the embedded 300-ppi JPEG (elife-08206-v3.pdf p. 3); figures/fig1b_extract.py.",
       ax.describe("x") + ".", ay.describe("y") + ".",
       f"Uncertainty: +-1 px = +-{abs(ax.m):.2g} mOsm and +-{abs(ay.m):.2g} % for isolated markers; +-3 px where markers overlap",
       "  (the two x marks at ~200 mOsm / 5.9 %, and the circle at ~241 mOsm crossed by the dashed line).",
       "Caption: olfactory bulb R = 0.80, p = 0.0006; cortex R = 0.79, p = 0.0113 (linear fits)."]
write_csv(os.path.join(HERE, "fig1b.csv"), hdr, ["series", "category", "osmolarity_mOsm", "ecs_fraction_pct", "match_score", "note"],
          rows, "{}")
draw(a, pts, os.path.join(WORK, "fig1b_overlay.png"), lines=[(v, (0, 200, 0)) for v in lines.values()])
for r in rows: print(r)
