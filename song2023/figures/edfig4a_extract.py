"""Extended Data Fig. 4a (right): depth of OsO4 diffusion (mm) into a mouse hemisphere vs incubation time (h) at 4 degC
-> edfig4a.csv. Tier 3 (digitized; no source data in the Edmond set: its 'Extended Data Fig.4' folder holds only
images). Raster PDF p. 16 (embedded 300-ppi image). Axes fitted on tick marks (x: 0..40 h every 10; y: 0..2.5 mm
every 0.5). Markers = filled circles, located as blobs after a morphological opening that removes the line; the
first marker sits on the axis corner and is taken at the axis origin (0, 0) by eye.
Run: python3 -I edfig4a_extract.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, WORK, dark_mask, find_markers, fit, overlay, page_image, write_csv  # noqa: E402

a = page_image(16)
px2x, x2px, rx = fit([1608, 1678.5, 1750, 1821, 1892], [0, 10, 20, 30, 40])
py2y, y2py, ry = fit([252.5, 213, 173.5, 134, 95, 55], [0, 0.5, 1, 1.5, 2, 2.5])
X0, Y0, X1, Y1 = 1612, 30, 1960, 250
mk = find_markers(dark_mask(a, 120, 60)[Y0:Y1, X0:X1], 6, 40, 3000)
pts = [(1608.0, 252.5, "origin, by eye (marker on the axis corner)")] + [(x + X0, y + Y0, "marker centroid") for x, y, _ in mk]
rows = [[f"{float(px2x(x)):.2f}", f"{float(py2y(y)):.3f}", how] for x, y, how in pts]
write_csv(os.path.join(HERE, "edfig4a.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 4a (plot at right): Depth (mm) of OsO4 diffusion into a mouse",
    "  hemisphere at 4 degC (uCT) vs Incubation Time (h); points joined by straight lines.",
    "Provenance: tier 3, digitized from the raster figure (PDF p. 16) by edfig4a_extract.py; uncertainty +-0.3 h, +-0.02 mm.",
    f"  Axis fits: x max residual {rx:.2f} h, y max residual {ry:.3f} mm. Methods: time points 17, 24, 40 h.",
    "Columns: time_h; depth_mm; how.",
], ["time_h", "depth_mm", "how"], rows)
overlay(a, [(x, y) for x, y, _ in pts], os.path.join(WORK, "edfig4a_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig4a_overlay_full.png")).crop((1540, 20, 1968, 330)).save(os.path.join(WORK, "edfig4a_overlay.png"))
print(rows)
