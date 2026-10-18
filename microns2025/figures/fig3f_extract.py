#!/usr/bin/env python3
"""Fig. 3f (p. 4): rasters of deconvolved calcium activity of three neurons (rows of boxes: oracle percentile 100, 79,
34) to the six oracle clips (columns of boxes), ten repeats each. One embedded raster image (1171 x 704 px, placed at
64..275 x 282..409 pt) holds all 18 boxes. -> fig3f.csv.

Box frames (black, 3 px) are found in the image; each box interior (183 x 201 px) is a grid of 10 repeat rows
(20.1 px) x 62 time bins (2.95 px; bin edges found from the colour changes in a dense box: they fit 62 bins, not 63).
Each cell value is the mean grey over its central half. There is NO colour bar and each repeat is normalized
independently (caption), so the value is an UNCALIBRATED darkness 1 - grey/255 (0 = white)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(mc.PDF), 4, bbox_near=(64, 282, 275, 409)).astype(float).mean(2)
dark = a < 80


def groups(v):
    g = []
    for i in v:
        if g and i - g[-1][-1] <= 1:
            g[-1].append(i)
        else:
            g.append([i])
    return [(x[0], x[-1]) for x in g]


cx = groups(np.where(dark.mean(0) > 0.5)[0])
cy = groups(np.where(dark.mean(1) > 0.5)[0])
assert len(cx) == 12 and len(cy) == 6, (cx, cy)
NREP, NBIN = 10, 62
PCT = [100, 79, 34]
rows = []
recon = np.full_like(a, 255)
for bi in range(3):
    y0, y1 = cy[2 * bi][1] + 1, cy[2 * bi + 1][0]
    for bj in range(6):
        x0, x1 = cx[2 * bj][1] + 1, cx[2 * bj + 1][0]
        rh, bw = (y1 - y0) / NREP, (x1 - x0) / NBIN
        for r in range(NREP):
            for b in range(NBIN):
                ya, yb = int(round(y0 + (r + 0.25) * rh)), int(round(y0 + (r + 0.75) * rh))
                xa, xb = int(round(x0 + (b + 0.25) * bw)), int(round(x0 + (b + 0.75) * bw))
                g = a[ya:yb, xa:max(xb, xa + 1)].mean()
                rows.append([PCT[bi], bj + 1, r + 1, b + 1, f"{1 - g / 255:.4f}"])
                recon[int(y0 + r * rh):int(y0 + (r + 1) * rh), int(x0 + b * bw):int(x0 + (b + 1) * bw)] = g
mc.write_csv(Path(__file__).with_name("fig3f.csv"), [
    "Fig. 3f (p. 4 of microns2025.pdf): rasters for three neurons x six oracle clips x ten repeats x 62 time bins.",
    "Provenance: tier 3, embedded raster; UNCALIBRATED (no colour bar; each repeat normalized independently per the caption).",
    "Columns: oracle_percentile (box row: 100 top, 79 middle, 34 bottom); clip (Oracle clip 1-6); repeat (1 = top row of the box);",
    "time_bin (1..62, left to right; the scale bar under the panel marks 10 s, i.e. one clip); darkness (1 - grey/255).",
    f"Box frames at image columns {[(int(p), int(q)) for p, q in cx]} and rows {[(int(p), int(q)) for p, q in cy]}.",
], ["oracle_percentile", "clip", "repeat", "time_bin", "darkness"], rows)
from PIL import Image  # noqa: E402
Image.fromarray(np.hstack([a, recon]).astype(np.uint8)).save(mc.K / "work" / "overlay_fig3f.png")
