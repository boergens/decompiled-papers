#!/usr/bin/env python3
"""Fig. 7d (p. 10): first- and second-order synaptic output heat maps of seven layer 3 pyramidal cells. All heat maps and
colour bars are one embedded raster (3707 x 1250 px, 600 ppi, placed at 70.08..514.92 x 341.11..491.11 pt); labels are
vector text. -> fig7d.csv (one row per heat-map cell, all sub-maps).

Sub-maps (positions found in the image; cell grids are regular):
  left      : 'Number of L3a->order 1 excitatory partner synapses', 7 rows (L2P, L3P, L4P, L5ET, L5NP, L5IT, L6P) x
              7 columns (the seven L3 cells); grey bar 0 ... 250 synapses (0 at the first tick under the bar, 250 at the
              label centre near the bar end, 103.15 pt; the ticks are not at round values, so +-5 %).
  top       : grey heat map 'Number of L3a->order 1 inhibitory partner synapses', 7 rows (L3 cells) x 78 inhibitory partners
              (DTC 33, PTC 32, ITC 10, STC 3 columns, 39.2 px each); grey bar 0 ... 8 (tick marks at bar rows 53 ... 189).
  depth     : colour strip under the top map, soma depth of each inhibitory partner, colour bar Pia (top) ... WM (bottom)
              without numbers: given as the UNCALIBRATED fraction 0 (Pia) ... 1 (WM) along the bar.
  bottom    : 'Number of order 1 inhibitory partner->order 2 excitatory partners synapses', 7 rows (L2P ... L6P) x 78 partners,
              colour per group: DTC red and PTC blue, bars 0 ... >=4,000; ITC green and STC orange, bars 0 ... >=200
              (bar ends = 0 and the saturating maximum; values at the maximum mean '>= max').
Each cell value: mean colour of the cell's central half matched to the nearest colour of its bar (RGB distance reported)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(mc.PDF), 10, bbox_near=(70, 341, 515, 491)).astype(float)
S = 444.84 / 3707  # pt per px
ROWS7 = ["L2P", "L3P", "L4P", "L5ET", "L5NP", "L5IT", "L6P"]


def cellmean(x0, x1, y0, y1):
    xa, xb = int(round(x0 + 0.25 * (x1 - x0))), int(round(x0 + 0.75 * (x1 - x0)))
    ya, yb = int(round(y0 + 0.25 * (y1 - y0))), int(round(y0 + 0.75 * (y1 - y0)))
    return a[ya:max(yb, ya + 1), xa:max(xb, xa + 1)].reshape(-1, 3).mean(0)


def lut_h(x0, x1, row, vmax):
    cols = a[row - 6:row + 7, x0:x1 + 1].mean(0)
    return cols, np.linspace(0, vmax, len(cols))


def match(c, lut):
    cols, vals = lut
    d = np.sqrt(((cols - c) ** 2).sum(1))
    i = int(d.argmin())
    return vals[i], d[i]


# colour bars
LUT = {
    "DTC": lut_h(686, 1298, 1163, 4000), "PTC": lut_h(2087, 2685, 1163, 4000),
    "ITC": lut_h(3159, 3366, 1163, 200), "STC": lut_h(3464, 3560, 1163, 200),
}
gl = a[1105:1123, 66:275].mean(0)
x0pt = lambda px: 70.075 + (px + 0.5) * S
LUT["left"] = (gl, np.array([250 * (x0pt(px) - 80.35) / (103.15 - 80.35) for px in range(66, 275)]))
gv = a[53:190, 3600:3609].mean(1)
LUT["top"] = (gv, np.array([8 * (189 - r) / (189 - 53) for r in range(53, 190)]))
dv = a[284:404, 3600:3609].mean(1)
LUT["depth"] = (dv, np.linspace(0, 1, len(dv)))
# white = 0 for the count maps
for k in ("DTC", "PTC", "ITC", "STC", "left", "top"):
    cols, vals = LUT[k]
    LUT[k] = (np.vstack([cols, [[255, 255, 255]]]), np.append(vals, 0.0))

GROUPS = [("DTC", 462, 1754, 33), ("PTC", 1778, 3034, 32), ("ITC", 3050, 3442, 10), ("STC", 3455, 3569, 3)]
rows, worst = [], {}
qa = np.full_like(a, 255)


def put(sub, rlab, col, grp, x0, x1, y0, y1, key):
    c = cellmean(x0, x1, y0, y1)
    v, d = match(c, LUT[key])
    worst[key] = max(worst.get(key, 0), d)
    rows.append([sub, rlab, col, grp, f"{v:.3f}" if key in ("depth", "top") else f"{v:.0f}", f"{d:.1f}",
                 int(round(c[0])), int(round(c[1])), int(round(c[2]))])
    qa[int(y0):int(y1), int(x0):int(x1)] = c


# left matrix: frame 50..293, rows 304..1071
lx0, lx1, ly0, ly1 = 54, 288, 304, 1071
for i in range(7):
    for j in range(7):
        put("left", ROWS7[i], j + 1, "", lx0 + j * (lx1 - lx0) / 7, lx0 + (j + 1) * (lx1 - lx0) / 7,
            ly0 + i * (ly1 - ly0) / 7, ly0 + (i + 1) * (ly1 - ly0) / 7, "left")
col = 0
for g, x0, x1, n in GROUPS:
    w = (x1 - x0) / n
    for j in range(n):
        col += 1
        xa, xb = x0 + j * w, x0 + (j + 1) * w
        for i in range(7):
            put("top", f"L3 cell {i + 1}", col, g, xa, xb, 42 + i * 24, 42 + (i + 1) * 24, "top")
        put("depth", "", col, g, xa, xb, 230, 278, "depth")
        for i in range(7):
            put("bottom", ROWS7[i], col, g, xa, xb, 299 + i * (1066 - 299) / 7, 299 + (i + 1) * (1066 - 299) / 7, g)
mc.write_csv(Path(__file__).with_name("fig7d.csv"), [
    "Fig. 7d (p. 10 of microns2025.pdf): first- and second-order synaptic output heat maps (see fig7d_extract.py for the layout).",
    "Provenance: tier 3, digitized from the embedded raster; value from colour via each sub-map's colour bar.",
    "Columns: submap (left / top / depth / bottom); row (row label: cell type for left and bottom, 'L3 cell n' (top to bottom) for top);",
    "column (left: L3 cell 1-7 left to right; others: inhibitory partner 1-78 left to right, sorted in the figure by targeting",
    "type and soma depth); group (DTC/PTC/ITC/STC); value (synapses; depth: fraction Pia 0 ... WM 1, uncalibrated);",
    "colour_dist (RGB distance of the cell colour to the matched colour-bar entry); R, G, B (cell mean colour).",
    "Worst colour distance per bar: " + ", ".join(f"{k} {v:.1f}" for k, v in worst.items()) + ".",
    "Values at the bar maximum are '>= max' (bars end at >=4,000 and >=200).",
    "Caveat: the left map's 0-250 calibration uses the label centre for 250 (ticks are not at round values): +-5 %.",
], ["submap", "row", "column", "group", "value", "colour_dist", "R", "G", "B"], rows)
from PIL import Image  # noqa: E402
Image.fromarray(np.vstack([a, qa]).astype(np.uint8)).save(mc.K / "work" / "overlay_fig7d.png")
