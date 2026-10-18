#!/usr/bin/env python3
"""Fig. 6k (p. 8): heat maps of average dF/F (normalized activity) of the presynaptic neuron (one row, 'Presyn') and its
functionally co-registered postsynaptic targets ('Postsyn neurons', 80 rows) for oracle Clips 1-6. Three embedded
rasters: postsyn (2134 x 442 px), presyn (2134 x 70 px), colour bar (38 x 412 px). -> fig6k.csv.

Grid: in each clip panel (black frame found in the image) 63 time bins (5.10 px) x 80 rows (5.11 px) for the
postsynaptic map, found by fitting a regular grid to the colour edges; the presyn map has one row and the same columns
(same horizontal placement). Value: each cell's mean grey (central half) matched to the colour bar (grey scale, black = 1.0);
colour-bar tick marks at bar rows 2.5 (1.0), 205 (0.5), 408 (0.0) give value = (408 - row) / 405.5."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import digitize_common as dc  # noqa: E402

post = dc.embedded_image(str(mc.PDF), 8, bbox_near=(174, 500, 430, 553)).astype(float).mean(2)
pre = dc.embedded_image(str(mc.PDF), 8, bbox_near=(174, 492, 430, 500)).astype(float).mean(2)
cb = dc.embedded_image(str(mc.PDF), 8, bbox_near=(432, 502, 436, 551)).astype(float).mean(2)
lut_rows = np.arange(3, 408)
lut = cb[3:408, 7:20].mean(1)
lut_val = (408 - lut_rows) / 405.5


def val(g):
    i = int(np.abs(lut - g).argmin())
    return lut_val[i], abs(lut[i] - g)


def groups(v):
    g = []
    for i in v:
        if g and i - g[-1][-1] <= 1:
            g[-1].append(i)
        else:
            g.append([i])
    return [(x[0], x[-1]) for x in g]


fc = groups(np.where((post < 60).mean(0) > 0.5)[0])
fr = groups(np.where((post < 60).mean(1) > 0.5)[0])
assert len(fc) == 12 and len(fr) == 2, (fc, fr)
pr = groups(np.where((pre < 60).mean(1) > 0.5)[0])
NB, NR = 63, 80
rows, worst = [], 0
recon_post = np.full_like(post, 255)
y0, y1 = fr[0][1] + 1, fr[1][0]
py0, py1 = pr[0][1] + 1, pr[1][0]
for k in range(6):
    x0, x1 = fc[2 * k][1] + 1, fc[2 * k + 1][0]
    bw = (x1 - x0) / NB
    for b in range(NB):
        xa, xb = int(round(x0 + (b + 0.25) * bw)), int(round(x0 + (b + 0.75) * bw))
        g = pre[int(py0 + 0.25 * (py1 - py0)):int(py0 + 0.75 * (py1 - py0)) + 1, xa:xb].mean()
        v, dd = val(g); worst = max(worst, dd)
        rows.append(["presyn", 0, k + 1, b + 1, f"{v:.3f}", int(round(g))])
        rh = (y1 - y0) / NR
        for r in range(NR):
            g = post[int(round(y0 + (r + 0.25) * rh)):int(round(y0 + (r + 0.75) * rh)), xa:xb].mean()
            v, dd = val(g); worst = max(worst, dd)
            rows.append(["postsyn", r + 1, k + 1, b + 1, f"{v:.3f}", int(round(g))])
            recon_post[int(y0 + r * rh):int(y0 + (r + 1) * rh), int(x0 + b * bw):int(x0 + (b + 1) * bw)] = g
mc.write_csv(Path(__file__).with_name("fig6k.csv"), [
    "Fig. 6k (p. 8 of microns2025.pdf): average dF/F heat maps (colour bar 'Normalized activity', 0-1.0) of the presynaptic",
    "neuron (Fig. 6g, yellow) and 80 postsynaptic targets (sorted by synaptic strength, per the caption) for oracle clips 1-6.",
    "Provenance: tier 3, embedded rasters; grid fitted to the image (63 time bins per clip, 80 postsynaptic rows);",
    f"value from the cell grey via the colour bar (resolution ~0.0025; worst grey mismatch {worst:.1f} of 255).",
    "Columns: map (presyn/postsyn); row (postsynaptic row, 1 = top; 0 for presyn); clip (1-6); time_bin (1..63 within the clip;",
    "the 1 s scale bar under Clip 1 is 3.82 pt = about 6.2 bins); normalized_activity; grey (cell mean grey 0-255).",
], ["map", "row", "clip", "time_bin", "normalized_activity", "grey"], rows)
from PIL import Image  # noqa: E402
Image.fromarray(np.vstack([post, recon_post]).astype(np.uint8)).save(mc.K / "work" / "overlay_fig6k.png")
