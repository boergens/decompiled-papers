"""Extended Data Fig. 4f: Fe wt.% (EDS) at Periphery and Center of samples from d,e, 'no CaC' (dashed) vs 'CaC wash'
(solid) -> edfig4f.csv. Tier 3 (digitized; no source data for this panel in the Edmond set). Raster PDF p. 16. y axis
fitted on its 3 tick marks (0, 0.05, 0.1). Error bars: rows of the two caps of each bar in the bar's centre column;
value = midpoint, half-bar = half the cap distance. The 'no CaC' Center point has no visible error bar; its value is
the end of the dashed line.
Run: python3 -I edfig4f_extract.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, WORK, dark_mask, fit, overlay, page_image, write_csv  # noqa: E402

a = page_image(16)
py2y, y2py, ry = fit([1587, 1485, 1380.5], [0, 0.05, 0.1])
d = dark_mask(a, 120, 60)


def runs(col, y0=1370, y1=1584):
    r = np.where(d[y0:y1, col])[0] + y0
    return [(int(q[0]), int(q[-1])) for q in np.split(r, np.where(np.diff(r) > 1)[0] + 1)] if len(r) else []


rows, ov = [], []
# caps appear as short runs 8 px left and right of the bar centre (the bar itself is a long run in the centre column)
for loc, xc in (("Periphery", 1698), ("Center", 1872)):
    caps = sorted(set(r for r in runs(xc - 8) if r[1] - r[0] <= 4) & set(r for r in runs(xc + 8) if r[1] - r[0] <= 4) |
                  set(r for r in runs(xc - 8) if r[1] - r[0] <= 4 and any(abs(r[0] - q[0]) <= 2 for q in runs(xc + 8))))
    caps = [((c0 + c1) / 2) for c0, c1 in caps]
    caps = sorted(set(round(c) for c in caps))
    # pair consecutive caps whose span is covered by the centre-column run
    centre = runs(xc)
    for c0, c1 in centre:
        inside = [c for c in caps if c0 - 2 <= c <= c1 + 2]
        if len(inside) >= 2:
            lo, hi = py2y(max(inside)), py2y(min(inside))
            series = "no CaC" if (lo + hi) / 2 > 0.065 or loc == "Center" and False else "CaC wash"
            rows.append([series, loc, f"{(lo + hi) / 2:.4f}", f"{(hi - lo) / 2:.4f}", "error-bar caps"])
            ov += [(xc, y2py((lo + hi) / 2)), (xc, y2py(lo)), (xc, y2py(hi))]
# no-CaC center: end of the dashed line (lowest dark run just left of the centre column)
end = [r for r in runs(1866) if r[0] > 1540]
ye = (end[-1][0] + end[-1][1]) / 2
rows.append(["no CaC", "Center", f"{float(py2y(ye)):.4f}", "", "end of dashed line (no error bar visible)"])
ov.append((1866, ye))
write_csv(os.path.join(HERE, "edfig4f.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 4f: Fe wt.% (EDS) at Periphery and Center of the samples of d,e;",
    "  'no CaC' (dashed line) and 'CaC wash' (solid line), mean +- s.d. (Methods: s.d. as obtained from the EDS system).",
    "Provenance: tier 3, digitized from the raster figure (PDF p. 16) by edfig4f_extract.py; uncertainty +-0.002 wt.%.",
    f"  y axis fitted on 3 ticks (max residual {ry:.4f}). No source data for this panel in the Edmond data set.",
    "Columns: series; location; fe_wt_pct; half_errorbar; how.",
], ["series", "location", "fe_wt_pct", "half_errorbar", "how"], sorted(rows))
overlay(a, ov, os.path.join(WORK, "edfig4f_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig4f_overlay_full.png")).crop((1540, 1360, 1968, 1700)).save(os.path.join(WORK, "edfig4f_overlay.png"))
for r in sorted(rows):
    print(r)
