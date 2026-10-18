"""Digitize Fig. 4g of Yin et al. 2020, Nat. Commun. 11:4949 (PDF p. 7): histogram of the stage
step-and-settle time with a fitted curve.

The panel is an embedded raster image (JPEG, 300 ppi, 768 x 515 px; MATLAB-style plot with inward ticks on all
four sides); the tick labels are PDF text. The bars are light purple with thin dark outlines; a thick blue curve
is drawn over them.
    python3 -I fig4g_extract.py   -> fig4g.csv (+ ../work/fig4g_overlay.png for checking)
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from digitize_common import embedded_image, gray, fit_axis, write_csv, overlay  # noqa: E402

PDF = str(HERE.parent / "source" / "yin2020.pdf")
a = embedded_image(PDF, 7, bbox_near=(317.5, 381.0, 501.8, 504.6)).astype(int)
g = gray(a)
H, W = g.shape


def groups(idx):
    out = []
    for i in idx:
        if out and i <= out[-1][-1] + 1:
            out[-1].append(i)
        else:
            out.append([i])
    return [float(np.mean(q)) for q in out]


# ---- frame and ticks -------------------------------------------------------------------------------
LEFT = float(np.mean([c for c in range(0, 10) if (g[:, c] < 150).mean() > 0.8]))
RIGHT = float(np.mean([c for c in range(W - 10, W) if (g[:, c] < 150).mean() > 0.8]))
TOP = float(np.mean([r for r in range(0, 10) if (g[r] < 150).mean() > 0.8]))
BOT = float(np.mean([r for r in range(H - 10, H) if (g[r] < 150).mean() > 0.8]))
# y ticks: inward marks on the left and right frame (the same rows on both sides)
yl = groups([r for r in range(6, H - 8) if (g[r, 4:9] < 180).sum() >= 3])
yr = groups([r for r in range(6, H - 8) if (g[r, W - 11:W - 5] < 180).sum() >= 3])
assert len(yl) == len(yr) == 7, (yl, yr)
yt = [(p + q) / 2 for p, q in zip(yl, yr)]
yvals = [35, 30, 25, 20, 15, 10, 5]
# x ticks: inward marks below the top frame (the bottom ones are hidden by the bars); 0.00 and 0.18 are the frame
xt_raw = groups([c for c in range(int(LEFT) + 4, int(RIGHT) - 4) if (g[5:9, c] < 180).sum() >= 3])
xt = []
for c in xt_raw:                         # the curve crosses the 0.12 tick and splits it in two
    if xt and c - xt[-1] < 5:
        xt[-1] = (xt[-1] + c) / 2
    else:
        xt.append(c)
xvals = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16]
assert len(xt) == len(xvals), xt
fx, rx, sx = fit_axis([LEFT] + xt + [RIGHT], [0.0] + xvals + [0.18])
fy, ry, sy = fit_axis([BOT] + yt + [TOP], [0] + yvals + [40])
cy, *_ = fit_axis([0] + yvals + [40], [BOT] + yt + [TOP])     # inverse map, counts -> row

# ---- colour classes ---------------------------------------------------------------------------------
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
curve = (R < 100) & (B > 150) & (B - R > 70) & (G >= R + 5)    # thick blue fitted curve (the dark bar outlines have G <= R)
white = g > 235
edge = (g < 120) & ~curve                                      # dark bar outlines (vertical edges overlap)

# ---- bin edges: columns where a dark vertical outline runs down through the tall bars -----------------
ybar0, ybar1 = int(cy(8)), int(BOT) - 6                        # rows covered by bars of >= 8 counts
cand = groups([c for c in range(int(LEFT) + 3, int(RIGHT) - 3) if edge[ybar0:ybar1, c].mean() > 0.5])
d = np.diff(cand)
w0 = float(np.median(d))
w0 = (cand[-1] - cand[0]) / round((cand[-1] - cand[0]) / w0)  # mean spacing (single-pixel jitter makes the median biased)
k = np.round((np.array(cand) - cand[0]) / w0)
(wb, e0), *_ = np.linalg.lstsq(np.vstack([k, np.ones_like(k)]).T, np.array(cand), rcond=None)
edge_res = float(np.max(np.abs(wb * k + e0 - np.array(cand))))


def outline_candidates(c):
    """Rows in column c where a bar's top outline may start: light background two rows above (white or the pale
    JPEG fringe of the curve), a darker outline row here, and 4 of the next 5 rows (3-7 below) bar fill, which is
    light purple with G - R <= 4 (the curve and its blurred edge have G - R >= 6)."""
    out = []
    for r in range(int(TOP) + 11, int(BOT) - 8):
        if g[r - 2, c] > 200 and g[r - 1, c] > 170 and g[r:r + 3, c].min() < 205:
            fill = [(140 < g[q, c] < 216) and (G[q, c] - R[q, c] <= 4) for q in range(r + 3, r + 8)]
            if sum(fill) >= 4:
                out.append(r)
    return out


def bar_top_run(inner):
    """Topmost horizontal outline: a candidate row repeated (+-1 px) in >= 2 adjacent columns of the bin."""
    C = {c: outline_candidates(c) for c in inner}
    best = None
    for c in inner:
        for r in C[c]:
            n, cc = 1, c + 1
            while cc in C and any(abs(q - r) <= 1 for q in C[cc]):
                n, cc = n + 1, cc + 1
            if n >= 2 and (best is None or r < best):
                best = r
    return best


def curve_band(inner):
    """Median top and bottom row of the curve in these columns (the curve is a ~8-20 px thick band)."""
    tops, bots = [], []
    for c in inner:
        q = np.where(curve[int(TOP) + 11:int(BOT) - 3, c])[0]
        if len(q):
            runs = np.split(q, np.where(np.diff(q) > 2)[0] + 1)
            run = max(runs, key=len)
            tops.append(int(TOP) + 11 + run[0])
            bots.append(int(TOP) + 11 + run[-1])
    if not tops:
        return None
    return float(np.median(tops)), float(np.median(bots))


bins = []
kmin = -int((e0 - LEFT - 10) // wb)                             # stay clear of the y tick marks on both frames
kmax = int((RIGHT - 10 - e0) // wb)
for kk in range(kmin, kmax):
    l, r = e0 + kk * wb, e0 + (kk + 1) * wb
    inner = list(range(int(np.ceil(l + 1.5)), int(np.floor(r - 1.5)) + 1))
    top = bar_top_run(inner)
    if top is not None:
        bins.append((l, r, top + 1.0, ""))                      # the outline is ~2-3 px thick; its centre is the top
        continue
    # no visible outline: is there bar fill under the curve in this bin?
    band = curve_band(inner)
    if band is None:
        continue
    below = int(band[1]) + 3
    fill = np.mean([(140 < g[q, c] < 216) and (G[q, c] - R[q, c] <= 4) for c in inner for q in range(below, min(below + 4, int(BOT) - 3))]) if below < BOT - 4 else 0
    if fill < 0.3:
        continue
    mid = (band[0] + band[1]) / 2
    note = "top hidden under the curve: curve band centre given, bar top between %.1f and %.1f counts" % (
        float(fy(band[1])), float(fy(band[0])))
    bins.append((l, r, mid, note))

rows_out, pts = [], []
for l, r, top, note in bins:
    cnt = float(fy(top))
    rows_out.append(["bars", float(fx(l)), float(fx(r)), float(fx((l + r) / 2)), cnt, note])
    for c in range(int(np.ceil(l + 2)), int(np.floor(r - 2)) + 1):
        pts.append((c, top))
    pts.append((l, BOT - 4))

# ---- fitted curve: centre of the thick blue line in each column -------------------------------------
curve_rows = []
prev = None
for c in range(int(LEFT) + 3, int(RIGHT) - 2):
    q = np.where(curve[int(TOP) + 3:int(BOT) - 3, c])[0]
    note = ""
    if len(q):
        runs = np.split(q, np.where(np.diff(q) > 2)[0] + 1)
        if prev is None:
            run = max(runs, key=len)
        else:                                                   # the run that continues the line from the last column
            run = min(runs, key=lambda u: 0 if u[0] - 3 <= prev - int(TOP) - 3 <= u[-1] + 3
                      else min(abs(u[0] + int(TOP) + 3 - prev), abs(u[-1] + int(TOP) + 3 - prev)))
        yc = int(TOP) + 3 + run.mean()
        if len(run) > 12:
            note = "steep (run %d px)" % len(run)
    else:
        # flat tails: the line lies on the bottom frame; its upper half shows as bluish rows just above the frame
        tail = [r for r in range(int(BOT) - 5, int(BOT) - 1) if B[r, c] - R[r, c] > 50 and g[r, c] < 215]
        if not tail:
            continue
        yc = float(np.mean(tail)) + 1.0
        note = "tail on the baseline, merged with the frame line"
    prev = yc
    curve_rows.append(["fit_curve", float(fx(c)), "", "", float(fy(yc)), note])
    pts.append((c, yc))

(HERE.parent / "work").mkdir(exist_ok=True)
overlay(a.astype(np.uint8), pts, str(HERE.parent / "work" / "fig4g_overlay.png"))
total = sum(r[4] for r in rows_out)
write_csv(str(HERE / "fig4g.csv"), [
    "Yin et al. 2020 Nat. Commun. 11:4949, Fig. 4g: 'Example of stage step-and-settle time distribution for GridStage'.",
    "x axis 'Stage step and settle time (s)' 0.00-0.18, y axis 'Counts' 0-40, both linear.",
    "Two series: 'bars' = histogram bars (light purple with dark outlines); 'fit_curve' = the thick blue curve drawn over",
    "  them (the paper does not say what function it is).",
    "Columns: series; x_s = bin left edge (bars) or curve abscissa (fit_curve), s; x_right_s, x_centre_s = bin right edge",
    "  and centre (bars only); y_counts = bar height or curve height in Counts as read; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi JPEG (no vector data in the PDF; tick labels are PDF text) by",
    "  fig4g_extract.py. Calibration: linear fit on the frame (x 0.00 and 0.18, y 0 and 40) and the inward tick marks",
    f"  (8 x ticks along the top frame, 7 y ticks averaged left/right); max residual {rx:.4f} s and {ry:.2f} counts (the 35 tick",
    "  sits about 2 px lower than the even spacing of the others).",
    f"Bins: {len(rows_out)} bins of {wb:.2f} px = {abs(wb * sx):.5f} s on a regular grid fitted to {len(cand)} dark vertical bar",
    f"  outlines (max deviation {edge_res:.1f} px). Bar top = the topmost horizontal grey outline (seen in >= 2 adjacent pixel",
    "  columns, light background above, bar fill below). Where the thick curve covers the whole bar top, the centre of the",
    "  curve band is given and the note gives the range the top can lie in. Bars too low to see under the curve where it",
    "  runs along the baseline (x < ~0.075 s and x > ~0.14 s) are not listed.",
    f"Uncertainty: x about +-{abs(sx):.4f} s (1 px); visible bar tops about +-{2 * abs(sy):.2f} counts (2 px). The bar heights are",
    "  not all close to whole numbers (e.g. ~26.6 at 0.0924 s), so they are given as read, not rounded.",
    "  Curve: centre of the blue line, about +-0.3 counts (the line is ~8-10 px thick); on the steep flanks one pixel",
    "  column spans many rows (flagged 'steep').",
    f"Sum of the bar heights as read: {total:.1f}.",
], ["series", "x_s", "x_right_s", "x_centre_s", "y_counts", "note"], rows_out + curve_rows,
    fmt=["{}", "{:.5f}", "{:.5f}", "{:.5f}", "{:.2f}", "{}"])
print(len(rows_out), "bins, total", total, "edges", len(cand), "w", round(wb, 2), "res", rx, ry)
