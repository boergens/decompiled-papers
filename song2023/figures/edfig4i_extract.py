"""Extended Data Fig. 4i (right): sample expansion ratio vs duration in H2O (h), without / with the extra OsO4 step
-> edfig4i.csv. Tier 3 (digitized; no source data for this panel in the Edmond set). Raster PDF p. 16. Axes fitted
on tick marks (x: 0, 50, 100 h; y: 1.0..2.0 every 0.2). Markers (circles = No OsO4, squares = With OsO4) found as
blobs after a morphological opening; the first circle and square touch and form one blob, which is split at its
waist (narrowest row). Circle vs square told apart by their y order and fill ratio.
Run: python3 -I edfig4i_extract.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, WORK, dark_mask, find_markers, fit, overlay, page_image, write_csv  # noqa: E402

a = page_image(16)
px2x, x2px, rx = fit([1578.5, 1729, 1879], [0, 50, 100])
py2y, y2py, ry = fit([2382, 2425, 2468, 2511, 2554, 2597], [2.0, 1.8, 1.6, 1.4, 1.2, 1.0])
X0, Y0, X1, Y1 = 1582, 2405, 1960, 2594      # below the legend
d = dark_mask(a, 120, 60)
mk = find_markers(d[Y0:Y1, X0:X1], 6, 150, 3000)
pts = []
for x, y, ar in mk:
    x, y = x + X0, y + Y0
    if ar > 400:   # merged circle+square: split at the waist of the width profile
        xi = int(round(x))
        prof = d[int(y) - 25:int(y) + 25, xi - 10:xi + 11].sum(1)
        rows_ = np.where(prof > 0)[0]
        r0, r1 = rows_[0], rows_[-1]
        mid = r0 + 5 + int(np.argmin(prof[r0 + 5:r1 - 5]))
        base = int(y) - 25
        pts.append((x, base + (r0 + mid) / 2, "No OsO4", "split blob, upper part"))
        pts.append((x, base + (mid + 1 + r1) / 2, "With OsO4", "split blob, lower part"))
    else:
        pts.append((x, y, None, "marker centroid"))
# remaining single markers: the upper one at each x is the circle (No OsO4), squares lie on the lower line
pts = sorted(pts)
out = []
for x, y, s, how in pts:
    if s is None:
        s = "No OsO4" if py2y(y) > 1.4 else "With OsO4"
    out.append((s, x, y, how))
rows = [[s, f"{float(px2x(x)):.1f}", f"{float(py2y(y)):.3f}", how] for s, x, y, how in sorted(out, key=lambda t: (t[0], t[1]))]
write_csv(os.path.join(HERE, "edfig4i.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 4i (plot at right): Expansion Ratio of 2-mm samples kept in H2O vs",
    "  Duration (h), 'No OsO4' (circles) and 'With OsO4' (squares; extra OsO4 step after FeCN). Points joined by lines.",
    "Provenance: tier 3, digitized from the raster figure (PDF p. 16) by edfig4i_extract.py; uncertainty +-0.7 h, +-0.01.",
    f"  Axis fits: x max residual {rx:.2f} h, y max residual {ry:.4f}. Methods: imaging from 2 h to 100 h.",
    "Columns: series; duration_h; expansion_ratio; how.",
], ["series", "duration_h", "expansion_ratio", "how"], rows)
overlay(a, [(x, y) for _, x, y, _ in out], os.path.join(WORK, "edfig4i_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig4i_overlay_full.png")).crop((1540, 2330, 1968, 2711)).save(os.path.join(WORK, "edfig4i_overlay.png"))
for r in rows:
    print(r)
