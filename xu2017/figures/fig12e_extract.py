"""Digitize Figure 12(e) of Xu et al. 2017 (PDF p. 23): nine histograms of counts per pixel (one per bias voltage).

Source: the embedded raster image of Figure 12 (3150 x 2326 px, ~441 ppi); panel e is the row of nine small plots.
    python3 -I -B figures/fig12e_extract.py  -> figures/fig12e.csv, figures/fig12e_markers.csv (+ work/fig12e_overlay.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import write_csv, overlay  # noqa: E402
from xu_helpers import load, work_path  # noqa: E402

a = load(23).astype(int)
d = a.mean(2) < 140
TOP, BOT = 1416, 1691                    # frame rows (centres of 1415-1417 and 1690-1692), all nine boxes
LEFTS = [178, 511.5, 845, 1178, 1511.5, 1845, 2178, 2511.5, 2845]   # left frame centres; right frame = left + 275
BIAS = [-600, -400, -200, 0, 200, 400, 500, 600, 800]
TABLE = {-600: (1270, 1380), -400: (1570, 1740), -200: (1949, 2161), 0: (2594, 2896), 200: (2911, 3229),
         400: (2983, 3337), 500: (1211, 1338), 600: (630, 720), 800: (458, 536)}   # (Nc, Nm) from panel f
# x axis: logarithmic. In box 1 the small inward ticks on the bottom frame sit at columns ~205, 226, 244, 260, 274, 287
# (1000, taller), 370.7 and 419.3, i.e. 500, 600, ..., 1000, 2000, 3000 on a log scale with 277.0 px per decade; the
# labels '500', '1000', '2000' are centred under 204, 288 and ~372. The nine boxes are identical copies shifted by
# their left-frame offset (the 1000 tick lies 108.5-109 px right of the left frame in every box; see the header of fig12e.csv).
PX_DEC, X1000 = 277.0, 109.0


def fx(c, left):
    return 10 ** (3 + (c - (left + X1000)) / PX_DEC)


def ticks_1000(left):
    """columns of the taller 1000 tick on the bottom frame of a box (rows just above the frame)."""
    band = d[BOT - 5:BOT - 2, int(left) + 4:int(left) + 272]
    full = np.nonzero(band.all(0))[0]
    return [int(left) + 4 + c for c in full]


hist_rows, mark_rows, pts, checks = [], [], [], []
for k, left in enumerate(LEFTS):
    b = BIAS[k]
    t = ticks_1000(left)
    near = [c for c in t if abs(c - (left + X1000)) < 4]
    checks.append(f"box {k + 1}: 1000 tick at left+{(np.mean(near) - left):.1f}" if near else f"box {k + 1}: 1000 tick hidden")
    for c in range(int(left) + 8, int(left) + 268):     # skip the y-axis ticks on the left and right frames
        col = d[TOP + 4:BOT - 2, c]
        r = np.nonzero(col)[0]
        # ignore the frame's own small ticks (<= 6 px tall at the bottom, <= 6 px at the top)
        r = r[(r > 6) & (r < (BOT - 2 - TOP - 4) - 7)] if len(r) else r
        if len(r) == 0:
            hist_rows.append((b, c, float(fx(c, left)), 0.0))
            continue
        top = TOP + 4 + r.min()
        hist_rows.append((b, c, float(fx(c, left)), float((BOT - top) / (BOT - TOP))))
        pts.append((c, top))
        # marker lines (Nc/Nm): a dark run rising from the bottom frame, separated by a white gap from the curve above
        run = 0
        for i in range(len(col) - 1, -1, -1):
            if col[i]:
                run += 1
            else:
                break
        if run > 15 and (top - TOP - 4) < len(col) - run - 3:
            mark_rows.append((b, c, run))
lines = []
for b in BIAS:
    cs = [(c, run) for bb, c, run in mark_rows if bb == b]
    groups = []
    for c, run in cs:
        if groups and c - groups[-1][-1][0] <= 2:
            groups[-1].append((c, run))
        else:
            groups.append([(c, run)])
    left = LEFTS[BIAS.index(b)]
    for gph in groups:
        cc = np.mean([c for c, _ in gph])
        h = max(run for _, run in gph) / (BOT - TOP)
        lines.append((b, float(fx(cc, left)), float(h)))
        pts += [(cc, BOT - 3), (cc, BOT - max(run for _, run in gph))]
overlay(a.astype(np.uint8), pts, work_path("fig12e_overlay.png"))
write_csv(str(HERE / "fig12e.csv"), [
    "Xu et al. 2017 eLife 6:e25916, Figure 12(e): 'Histogram of counts per pixel' of the nine images (bias -600 ... 800 V, left to right).",
    "Columns: sample_bias_V; x_px = column of the source image; counts_per_pixel = x position on the log x axis (electron counts);",
    "  height_frac = height of the histogram curve as a fraction of the box height (0 = bottom frame, 1 = top frame); the y axes have",
    "  small unlabelled ticks only, so the heights are uncalibrated (and each box may be scaled differently). 0 where the curve lies on",
    "  the bottom frame. One row per pixel column (topmost dark pixel of the outline).",
    "Provenance: tier 3, digitized from the embedded raster image (~441 ppi, no vector data in the PDF) by fig12e_extract.py.",
    f"  x: log10, {PX_DEC} px per decade, calibrated on the small bottom ticks 500 ... 1000, 2000, 3000 of box 1 (labels 500, 1000, 2000);",
    "  the other boxes use the same map shifted by their frame offset (" + "; ".join(checks) + ").",
    "  The frame spans about 400 to 4000 counts.",
    "Uncertainty: about +-0.4 % in counts per pixel column (1 px = 0.0036 decades); heights +-1 px = +-0.004 of the box height.",
], ["sample_bias_V", "x_px", "counts_per_pixel", "height_frac"], hist_rows, fmt=["{}", "{}", "{:.0f}", "{:.4f}"])
lr = []
for b, x, h in lines:
    nc, nm = TABLE[b]
    lr.append((b, x, h, nc, nm))
write_csv(str(HERE / "fig12e_markers.csv"), [
    "Xu et al. 2017 eLife 6:e25916, Figure 12(e): the short vertical lines in each histogram that mark Nc and Nm (text, p. 22:",
    "  'These values are also indicated as short vertical lines on the signal histograms in Figure 12e').",
    "Columns: sample_bias_V; counts_per_pixel = position of the line (log x calibration as in fig12e.csv); height_frac = its height",
    "  as a fraction of the box height; table_Nc / table_Nm = the values printed in panel f for that bias (for comparison).",
    "Provenance: tier 3, digitized by fig12e_extract.py (dark runs rising from the bottom frame below the histogram outline).",
    "  Lines that coincide with the steep sides of the histogram cannot be separated from the outline and are missing.",
], ["sample_bias_V", "counts_per_pixel", "height_frac", "table_Nc", "table_Nm"], lr, fmt=["{}", "{:.0f}", "{:.3f}", "{}", "{}"])
for r in lr:
    print(r)
print(checks)
