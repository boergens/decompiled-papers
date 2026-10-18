"""Digitize Fig 5(f) of Lee et al. 2018 (PLoS ONE 13:e0206172) -> fig5f.csv (tier 3).

Scatter plot of section centroid positions (x, y in mm, both -0.7..0.7) with marginal histograms: x positions
on top (count 0-100), y positions on the right (count 0-100, bars pointing right), a dashed box and dashed
guide lines. Embedded 300 ppi image on p. 11 (xref 167).
  - axes: x ruler ticks -0.7/0/0.7 at columns 1240/1450/1659.5; y ruler ticks 0.7/0/-0.7 at rows 435/644/854;
    top histogram count ticks 0..100 (step 20) at rows 359.5..35; right histogram count ticks 0..100 at columns 1731..2056
    (all located with tick_positions in the image).
  - histograms: bins are separated by thin light lines; a regular grid (start, width) is fitted to them, and each
    bar's end is the sub-pixel position where the grey level crosses 128 (median over the bin's inner pixel lines).
  - scatter: the x markers overlap heavily in the centre; isolated markers are found by normalized template matching
    (template = one isolated marker); the dense core cannot be resolved into single markers.
  - dashed lines: positions of the vertical and horizontal dashed lines (the box edges).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(ROOT / "source/lee2018_lasso.pdf"), 11)
g = dc.gray(a)
d = g < 160
xt = dc.tick_positions(d, (898, 900), -1, 8, 1220, 1680, 0.7)
yt = dc.tick_positions_v(d, (1191, 1193), +1, 8, 420, 870, 0.7)
ht = dc.tick_positions_v(d, (1239, 1241), +1, 8, 20, 370, 0.7)      # top histogram count axis
vt = dc.tick_positions(d, (434, 436), +1, 8, 1720, 2070, 0.7)       # right histogram count axis
assert len(xt) == 3 and len(yt) == 3 and len(ht) == 6 and len(vt) == 6, (xt, yt, ht, vt)
fx, rx, sx = dc.fit_axis(xt, [-0.7, 0, 0.7])
fy, ry, sy = dc.fit_axis(yt, [0.7, 0, -0.7])
fhc, rhc, shc = dc.fit_axis(ht, [100, 80, 60, 40, 20, 0])   # ht is sorted top to bottom
fvc, rvc, svc = dc.fit_axis(vt, [0, 20, 40, 60, 80, 100])
inv_x = lambda v: (v - fx(0)) / sx       # mm -> column
inv_y = lambda v: (v - fy(0)) / sy


def crossing(profile, start, step):
    """Sub-pixel position where the profile (grey levels) first rises to >= 128 walking from start by step."""
    i = start
    while 0 <= i + step < len(profile) and profile[i] < 128:
        i += step
    if profile[i] < 128:
        return float(i)
    j = i - step
    v0, v1 = float(profile[j]), float(profile[i])
    return j + step * (128 - v0) / (v1 - v0) if v1 != v0 else float(i)


def fit_grid(prof, lo, hi, w_range):
    """Fit separator lines (bright local maxima of 'prof' inside bars) with a regular grid."""
    best = None
    for w in np.arange(w_range[0], w_range[1], 0.005):
        for s in np.arange(lo, lo + w, 0.1):
            pos = np.arange(s, hi, w)
            v = np.mean([prof[int(round(p))] for p in pos if int(round(p)) < len(prof)])
            if best is None or v > best[0]:
                best = (v, s, w)
    return best[1], best[2]


rows = []
# ---- top histogram (x positions): bars on baseline row ~359.6, bins along columns
base_top = float(np.mean([r for r in range(355, 365) if (g[r, 1250:1650] < 128).mean() > 0.9]))
sep_prof = np.zeros(2100)
for c in range(1420, 1490):          # inside the tall bars, separators are light columns
    sep_prof[c] = g[300:350, c].mean()
s0, w = fit_grid(sep_prof, 1420, 1490, (6.8, 7.2))
s0 = s0 - w * np.floor((s0 - 1240) / w)
edges_x = np.arange(s0, 1660, w)
for e0, e1 in zip(edges_x[:-1], edges_x[1:]):
    cs = range(int(np.ceil(e0 + 1.5)), int(np.floor(e1 - 1.5)) + 1)
    ends = []
    for c in cs:
        prof = g[30:358, c]
        if prof[-1] >= 128:          # empty bin in this column
            ends.append(None)
            continue
        ends.append(30 + crossing(prof, len(prof) - 1, -1) - 0.0)
    ends = [e for e in ends if e is not None]
    cnt = float(fhc(np.median(ends))) if len(ends) >= 2 else 0.0
    # count axis fitted on the tick marks (0 at the 0 tick); bar end = where the bar's dark edge meets the white
    rows.append(["x_histogram", "", "", float(fx(e0)), float(fx(e1)), round(cnt, 2), int(round(cnt)), ""])
# ---- right histogram (y positions): bars from baseline column ~1731 to the right, bins along rows
sep_prof = np.zeros(2100)
for r in range(600, 690):
    sep_prof[r] = g[r, 1745:1790].mean()
s0y, wy = fit_grid(sep_prof, 600, 690, (8.5, 9.3))   # the y histogram has wider bins than the x histogram
s0y = s0y - wy * np.floor((s0y - 435) / wy)
edges_y = np.arange(s0y, 855, wy)
for e0, e1 in zip(edges_y[:-1], edges_y[1:]):
    rs = range(int(np.ceil(e0 + 1.5)), int(np.floor(e1 - 1.5)) + 1)
    ends = []
    for r in rs:
        prof = g[r, 1734:2060]
        if prof[0] >= 128:
            continue
        ends.append(1734 + crossing(prof, 0, +1))
    cnt = float(fvc(np.median(ends))) if len(ends) >= 2 else 0.0
    rows.append(["y_histogram", "", "", float(fy(e1)), float(fy(e0)), round(cnt, 2), int(round(cnt)), ""])
# ---- dashed lines
dash_cols = sorted({c for c in range(1245, 1655) if (g[72:115, c] < 100).mean() > 0.3})      # above the tallest bar (lines start at row 72)
dash_rows = sorted({r for r in range(440, 850) if (g[r, 1996:2022] < 100).mean() > 0.3})      # beyond the longest bar (lines end at column 2021)
grp = lambda v: [float(np.mean(k)) for k in np.split(np.array(v), np.where(np.diff(v) > 2)[0] + 1)]
dx, dy = grp(dash_cols), grp(dash_rows)
for v in dx:
    rows.append(["dashed_line_x", float(fx(v)), "", "", "", "", "", "vertical dashed line"])
for v in dy:
    rows.append(["dashed_line_y", "", float(fy(v)), "", "", "", "", "horizontal dashed line"])
# ---- scatter markers
ink = (255 - g).astype(np.float32)
T = ink[499:507, 1441:1449].copy()             # an isolated marker centred at (1444.5, 502.5)
R0, R1, C0, C1 = 437, 853, 1242, 1658
sub = ink[R0:R1, C0:C1].copy()
for c in dx:
    c = int(round(c)); sub[:, c - 3 - C0:c + 4 - C0] = np.where(sub[:, c - 3 - C0:c + 4 - C0] > 200, 0, sub[:, c - 3 - C0:c + 4 - C0])
for r in dy:
    r = int(round(r)); sub[r - 3 - R0:r + 4 - R0, :] = np.where(sub[r - 3 - R0:r + 4 - R0, :] > 200, 0, sub[r - 3 - R0:r + 4 - R0, :])
res = cv2.matchTemplate(sub, T, cv2.TM_CCOEFF_NORMED)
mx = cv2.dilate(res, np.ones((5, 5), np.uint8))
inkmax = cv2.dilate(sub, np.ones((8, 8), np.uint8))[4:4 + res.shape[0], 4:4 + res.shape[1]]
pk = np.argwhere((res == mx) & (res > 0.5) & (inkmax > 60))   # ink test: blank paper noise can correlate too
pts = [(C0 + p[1] + 3.5, R0 + p[0] + 3.5) for p in pk]
dens = cv2.blur((ink > 60).astype(np.float32), (25, 25))
for (px, py) in sorted(pts, key=lambda p: (p[1], p[0])):
    crowded = dens[int(round(py)), int(round(px))] > 0.25
    rows.append(["scatter", float(fx(px)), float(fy(py)), "", "", "", "", "in dense core (unreliable)" if crowded else ""])
core = np.argwhere(dens[R0:R1, C0:C1] > 0.25)
hdr = [
    "Lee et al. 2018, PLoS ONE 13(10):e0206172, Fig 5(f): section centroid positions (scatter, x markers) with x- and y-centroid",
    "  position distributions (histograms); axes 'Section centroid x-position [mm]' and 'y-position [mm]', both -0.7..0.7;",
    "  histogram count axes 0-100. Caption: dashed box = centroids whose whole section lies within the aperture (587/631, 93%).",
    "Columns: series; x_mm, y_mm (scatter markers and dashed-line positions); bin_low_mm, bin_high_mm, count (bar length in counts),",
    "  count_rounded (nearest integer) for the histograms (x_histogram = top, bins along x; y_histogram = right, bins along y); flag.",
    "Provenance: tier 3, digitized by fig5f_extract.py from the embedded 300 ppi raster (p. 11); no vector or source data.",
    f"  Axis fits: x {rx:.4f} mm, y {ry:.4f} mm, count axes {rhc:.2f} / {rvc:.2f} counts max residual.",
    f"  Histogram bins: regular grid fitted to the separator lines: x bins {w * 1.4 / (xt[-1] - xt[0]):.4f} mm wide, y bins {wy * 1.4 / (yt[-1] - yt[0]):.4f} mm wide.",
    "  Bar end = sub-pixel position where the grey level crosses 128 (median over the bin's inner pixel lines).",
    f"  Scatter: {sum(1 for r in rows if r[0] == 'scatter')} markers found by template matching (score > 0.5, darkest pixel ink > 60). INCOMPLETE: the paper analysed",
    "  631 centroids; most of them overlap in the dense core (x about -0.15..0.15, y about -0.15..0.2 mm), where single markers",
    "  cannot be separated; markers flagged 'in dense core' are approximate and many core markers are missing. The isolated",
    "  outer markers are complete as far as visible. Use the histograms for the distributions.",
    "Uncertainty: scatter positions +-0.005 mm (1 px = 0.0033 mm); histogram counts +-0.5; bin edges +-0.003 mm.",
]
dc.write_csv(str(HERE / "fig5f.csv"), hdr, ["series", "x_mm", "y_mm", "bin_low_mm", "bin_high_mm", "count", "count_rounded", "flag"], rows,
             fmt=["{}", "{:.4f}", "{:.4f}", "{:.4f}", "{:.4f}", "{:.2f}", "{}", "{}"])
(ROOT / "work").mkdir(exist_ok=True)
over = list(pts)
for r in rows:
    if r[0] == "x_histogram" and r[5] > 0:
        rowpix = (r[5] - fhc(0)) / shc
        over += [(c, rowpix) for c in np.arange(inv_x(r[3]) + 1, inv_x(r[4]) - 1, 1.0)]
    if r[0] == "y_histogram" and r[5] > 0:
        colpix = (r[5] - fvc(0)) / svc
        over += [(colpix, rr) for rr in np.arange(inv_y(r[4]) + 1, inv_y(r[3]) - 1, 1.0)]
dc.overlay(a, over, str(ROOT / "work/fig5f_overlay.png"))
tx = sum(r[6] for r in rows if r[0] == "x_histogram"); ty = sum(r[6] for r in rows if r[0] == "y_histogram")
print("bins", w, wy, "totals", tx, ty, "markers", len(pts), "dash", [round(float(fx(v)), 3) for v in dx], [round(float(fy(v)), 3) for v in dy])
