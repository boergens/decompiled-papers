"""Digitize Figure 2—figure supplement 2a of Templier 2019 (eLife 8:e45696): histogram of matching inliers.

Source: ../source/elife_figure_supplements/fig2-figsupp2.jpg (1027 x 1408 px, from
iiif.elifesciences.org; panel a is the top-left ~560 x 410 px). Raster only -> tier 3.
    python3 -I sfig2-2a_extract.py   -> sfig2-2a.csv (+ ../work/sfig2-2a_overlay.png)

Method
- y axis: tick marks left of the axis line at rows 27, 99.5, 172.5, 245, 318, 390.5 (found as dark rows in
  columns 52-57), labels 0, 4, 8 on every second tick -> ticks are 0, 2, 4, 6, 8, 10.
- x axis: tick marks below the axis at columns 146, 246, 346.5, 446.5, 547 (100 px apart); labels 1000 and
  2000 sit under 246 and 446.5, so the ticks are 500, 1000, 1500, 2000, 2500 (unlabelled ticks at 500,
  1500, 2500). The label "0" is printed under the y-axis line (column 59), which by the tick spacing is
  at x = 65, not 0 (see CSV header).
- bars: 60 equal bins between the y-axis line (column 59) and the right edge of the last bar (column 556);
  bar outlines checked against this grid. Each bar top is the dark outline row found by scanning up from
  the axis through the grey fill until the first near-white pixel, median over the inner columns of the bin.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))   # tools/digitize_common.py
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from digitize_common import fit_axis, write_csv, overlay  # noqa: E402

IMG = os.path.join(HERE, "../source/elife_figure_supplements/fig2-figsupp2.jpg")
a = np.asarray(Image.open(IMG).convert("RGB"))
g = a.astype(float).mean(2)


def tick_rows(col0, col1, r0, r1):
    band = g[r0:r1, col0:col1].mean(1)
    rows = np.where(band < 150)[0]
    groups = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
    return [r0 + float(np.average(q, weights=255 - band[q])) for q in groups if len(q)]


def tick_cols(row0, row1, c0, c1):
    band = g[row0:row1, c0:c1].mean(0)
    cols = np.where(band < 150)[0]
    groups = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1)
    return [c0 + float(np.average(q, weights=255 - band[q])) for q in groups if len(q)]


yt = tick_rows(52, 58, 15, 395)
assert len(yt) == 6, yt
fy, yres, ys = fit_axis(yt, [10, 8, 6, 4, 2, 0])
xt = tick_cols(393, 400, 100, 560)
assert len(xt) == 5, xt
fx, xres, xs = fit_axis(xt, [500, 1000, 1500, 2000, 2500])
AX_X, AX_Y = 59.0, float(yt[-1])          # y-axis line column, x-axis (zero) row
L, R, NB = 59.0, 556.0, 60
w = (R - L) / NB

rows, pts = [], []
for k in range(NB):
    c0, c1 = L + k * w, L + (k + 1) * w
    tops = []
    for c in range(int(np.ceil(c0 + 2)), int(np.floor(c1 - 2)) + 1):
        r = 386
        if g[r, c] >= 230:          # no bar in this column
            tops.append(None)
            continue
        while r > 5 and g[r, c] < 230:
            r -= 1
        tops.append(r + 1)
    if all(t is None for t in tops):
        top = AX_Y
    else:
        top = float(np.median([t for t in tops if t is not None]))
    v = float(fy(top))
    rows.append((float(fx(c0)), float(fx(c1)), v, int(round(v))))
    pts += [((c0 + c1) / 2, top), (c0 + 1, top), (c1 - 1, top)]

overlay(a, pts, os.path.join(HERE, "../work/sfig2-2a_overlay.png"))
dev = max(abs(r[2] - r[3]) for r in rows)
total = sum(r[3] for r in rows)
write_csv(os.path.join(HERE, "sfig2-2a.csv"), [
    "Templier 2019 eLife 8:e45696, Figure 2—figure supplement 2a: 'Histogram of the numbers of matching inliers found",
    "  for each of the 203 LM-EM pairs of Dataset 2.'",
    "Columns: bin_left, bin_right = bin edges in 'Number of inliers'; frequency_read = bar height read off the image",
    "  (Frequency axis units); frequency = the same rounded to the nearest integer (counts are integers).",
    "Provenance: tier 3, digitized from the eLife figure-supplement JPEG fig2-figsupp2.jpg (1027 x 1408 px) by",
    "  sfig2-2a_extract.py. No vector or source data available.",
    f"  y fitted on 6 ticks (0-10 in steps of 2; labels 0, 4, 8), max residual {yres:.3f}; x fitted on 5 ticks",
    f"  (500-2500 in steps of 500; labels 1000, 2000), max residual {xres:.2f} inliers.",
    f"  60 equal bins from the y-axis line to the right edge of the last bar; bin width {w * abs(xs):.1f} inliers.",
    f"Uncertainty: about +-{abs(ys):.3f} in frequency (1 px); largest deviation of a bar from an integer {dev:.3f}.",
    f"  Bin edges about +-{abs(xs):.0f} inliers (1 px).",
    f"Check: the integer bar heights sum to {total} (the caption says 203 LM-EM pairs).",
    "Oddity: the x tick label '0' is printed under the y-axis line, which by the regular 500-step ticks lies at",
    f"  x = {float(fx(AX_X)):.0f}; the histogram starts there (presumably at the smallest inlier count), not at 0.",
], ["bin_left", "bin_right", "frequency_read", "frequency"], rows, fmt="{:.4g}")
print("sfig2-2a.csv", len(rows), "bins; sum", total, "; max dev", dev, "; residuals", xres, yres, "; x at axis", fx(AX_X))
