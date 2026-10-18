#!/usr/bin/env python3
"""Fig. 3g (p. 4): trial-averaged raster of deconvolved calcium activity, 80 neurons (rows) x 16 Monet2 directions,
grouped by preferred direction with alternating blue shading. The heat map is one embedded raster image
(1678 x 1050 px, JPEG, placed at 347..549 x 275..401 pt). -> fig3g.csv (grid at native cell resolution).

The image is a grid of 80 rows x 64 columns of uniform cells (cell size 26.22 x 13.125 px, found from the colour
edges); 64 columns = 16 directions x 4 time bins (the caption: central 500 ms of each direction). Each cell's colour is
the mean over its central half (avoids JPEG ringing at the edges). There is NO colour bar: the values are the raw
pixel colours and an UNCALIBRATED darkness 1 - mean(RGB)/255. Rows alternate between grey and blue-tinted shading in
groups of 5 neurons (caption: alternating blue shading); blue_tint = B - (R + G)/2 marks this."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(mc.PDF), 4, bbox_near=(347, 275, 549, 401)).astype(float)
H, W, _ = a.shape
NR, NC = 80, 64
ch, cw = H / NR, W / NC
rows = []
for i in range(NR):
    for j in range(NC):
        y0, y1 = int(round((i + 0.25) * ch)), int(round((i + 0.75) * ch))
        x0, x1 = int(round((j + 0.25) * cw)), int(round((j + 0.75) * cw))
        c = a[y0:y1, x0:x1].reshape(-1, 3).mean(0)
        rows.append([i + 1, j + 1, j // 4 + 1, j % 4 + 1, f"{1 - c.mean() / 255:.4f}", f"{c[2] - (c[0] + c[1]) / 2:.1f}",
                     int(round(c[0])), int(round(c[1])), int(round(c[2]))])
mc.write_csv(Path(__file__).with_name("fig3g.csv"), [
    "Fig. 3g (p. 4 of microns2025.pdf): trial-averaged raster, 80 neurons x 16 directions x 4 time bins (grid read from the image).",
    "Provenance: tier 3, embedded raster; UNCALIBRATED (the figure has no colour bar): darkness = 1 - mean(R,G,B)/255,",
    "0 = white, larger = darker = more activity (the caption's grey scale has no stated range).",
    "Columns: neuron_row (1 = top); col (1 = left, 1..64); direction_index (1..16, left to right; the directions are the arrows",
    "drawn under the panel, see the description); time_bin (1..4 within a direction); darkness; blue_tint; R, G, B (cell mean colour).",
    f"Cell size {cw:.2f} x {ch:.3f} px; image {W} x {H} px.",
], ["neuron_row", "col", "direction_index", "time_bin", "darkness", "blue_tint", "R", "G", "B"], rows)
# QA: rebuild the image from the grid
im = np.zeros_like(a)
for r in rows:
    i, j = r[0] - 1, r[1] - 1
    im[int(i * ch):int((i + 1) * ch), int(j * cw):int((j + 1) * cw)] = r[6:9]
from PIL import Image  # noqa: E402
Image.fromarray(np.hstack([a, im]).astype(np.uint8)).save(mc.K / "work" / "overlay_fig3g.png")
