"""Digitize Figure 12(b) of Xu et al. 2017 (PDF p. 23): intensity profile (electron counts) along the yellow line of 12(a).

Source: the embedded raster image of Figure 12 (3150 x 2326 px, ~441 ppi); panel b is the strip between rows ~375 and ~712.
    python3 -I -B figures/fig12b_extract.py  -> figures/fig12b.csv (+ work/fig12b_overlay.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import write_csv, overlay  # noqa: E402
from xu_helpers import load, lin, work_path  # noqa: E402

a = load(23).astype(int)
g = a.mean(2)
dark = g < 100
dark[395:446, 3000:3112] = False      # the scale-bar label '1 μm' of panel a, printed inside panel b's frame
# Frame: left col 150-157, right col 3141-3148, top row 375-382; the bottom frame merges with the black border of
# panel c (dark from row 704 down). Grey grid lines (no labels) at rows 459.0, 543.5, 627.5 (centres), spacing 84.25 px.
# The y axis has no numbers; the caption says the profile is shown 'over a 0 to 4000 count range'. Assuming the
# frame spans 0-4000 with the three grid lines at 1000, 2000, 3000 (four equal intervals), the map is:
fy = lin(627.5, 1000, 459.0, 3000)
XL, XR = 153.5, 3144.5
fx = lin(XL, 0.0, XR, 1.0)
BIAS = [-600, -400, -200, 0, 200, 400, 500, 600, 800]     # bias of the 9 images, left to right (panels a, f)
NE_TABLE = [(1380 + 1270) / 2, (1740 + 1570) / 2, (2161 + 1949) / 2, (2896 + 2594) / 2, (3229 + 2911) / 2,
            (3337 + 2983) / 2, (1338 + 1211) / 2, (720 + 630) / 2, (536 + 458) / 2]   # (Nm+Nc)/2 from panel f

cols = []
for c in range(int(XL) + 5, int(XR) - 4):
    r = np.nonzero(dark[384:703, c])[0]
    if len(r) == 0:
        cols.append((c, np.nan, np.nan, np.nan, False))
        continue
    top, bot = 384 + r.min(), 384 + r.max()
    edge = (bot - top) > 40 and bot >= 700          # vertical edge of a plateau, running down to the bottom frame
    cols.append((c, (top + bot) / 2, top, bot, edge))

# plateaus = runs of columns with a line above the bottom frame
seg, segs = [], []
for c, y, top, bot, edge in cols:
    if y == y:
        seg.append((c, y, top, bot, edge))
    elif seg:
        segs.append(seg)
        seg = []
if seg:
    segs.append(seg)
segs = [s for s in segs if len(s) > 50]
assert len(segs) == 9, len(segs)

rows, pts, summary = [], [], []
for k, s in enumerate(segs):
    vals = []
    for c, y, top, bot, edge in s:
        if edge:
            rows.append((BIAS[k], c, float(fx(c)), np.nan, float(fy(top)), np.nan, "vertical edge of the plateau (drops to 0)"))
            pts.append((c, top))
            continue
        # the line is ~8 px thick: shift top and bottom inwards by half the thickness
        t, b = top + 3.5, bot - 3.5
        if t > b:
            t = b = (top + bot) / 2
        rows.append((BIAS[k], c, float(fx(c)), float(fy(y)), float(fy(t)), float(fy(b)), ""))
        vals.append(float(fy(y)))
        pts += [(c, y)]
    summary.append((BIAS[k], float(np.median(vals)), NE_TABLE[k]))
overlay(a.astype(np.uint8), pts, work_path("fig12b_overlay.png"))
write_csv(str(HERE / "fig12b.csv"), [
    "Xu et al. 2017 eLife 6:e25916, Figure 12(b): 'Electron Counts' profile along the yellow line across the nine images of 12(a).",
    "Columns: sample_bias_V = bias of the image the plateau belongs to (-600 ... 800 V, left to right, as in panel f);",
    "  x_px = column of the source image; x_frac = position as a fraction of the frame width (no x scale in the figure);",
    "  counts_mid = centre of the ~8 px thick line in that column; counts_max/counts_min = top/bottom of the line's",
    "  centre band within the column (they differ where the line is steep); flag marks the vertical plateau edges.",
    "  Between the plateaus (the black gaps between the images) the line runs along the bottom frame (0 counts); those columns are omitted.",
    "Provenance: tier 3, digitized from the embedded raster image (~441 ppi, no vector data in the PDF) by fig12b_extract.py.",
    "  CALIBRATION ASSUMPTION: the y axis has no numbers. The caption says 'over a 0 to 4000 count range'; the three unlabelled",
    "  grey grid lines (rows 459.0, 543.5, 627.5, evenly spaced) are taken as 3000, 2000, 1000 counts, which puts 0 at row 711.75",
    "  (inside the merged bottom frame / panel-c border, rows 704-719) and 4000 at row 374.75 (outer edge of the top frame, rows 375-382).",
    "Uncertainty: +-12 counts per pixel row (84.25 px per 1000 counts) plus the line thickness; systematic +-50 counts from the",
    "  frame/grid ambiguity of the calibration.",
    "Check against panel f: median plateau value vs (Nm+Nc)/2 from the table (counts): " +
    "; ".join(f"{b} V: {m:.0f} vs {n:.0f}" for b, m, n in summary),
], ["sample_bias_V", "x_px", "x_frac", "counts_mid", "counts_max", "counts_min", "flag"], rows,
    fmt=["{}", "{}", "{:.4f}", "{:.0f}", "{:.0f}", "{:.0f}", "{}"])
print(summary)
