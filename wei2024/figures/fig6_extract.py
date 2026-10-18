"""Digitize Fig. 6a (main plot and inset) and Fig. 6b of wei2024 (tier 3, raster).

Source: the embedded 1503 x 2026 px, 300 ppi JPEG on PDF page 11 (source/wei2024.pdf).
Writes figures/fig6a.csv, figures/fig6a_inset.csv, figures/fig6b.csv and overlays in work/.
Run: python3 -I -B figures/fig6_extract.py (any working directory).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage as ndi  # noqa: E402
import digitize_common as dc  # noqa: E402
import f2_common as fc  # noqa: E402

WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)
a = dc.embedded_image(str(ROOT / "source" / "wei2024.pdf"), 11)
g = dc.gray(a)
dark = g < 120

SERIES = ["0.10 Å/ps", "0.25 Å/ps", "0.50 Å/ps", "0.75 Å/ps", "1.00 Å/ps", "1.50 Å/ps", "2.00 Å/ps"]
# core colours of the legend markers (darkest pixels of each legend ball)
PAL = [(0, 0, 0), (250, 0, 0), (240, 0, 244), (0, 0, 250), (118, 117, 0), (122, 0, 0), (255, 121, 0)]
OVC = [(0, 255, 255), (0, 255, 0), (0, 128, 255), (255, 255, 0), (255, 0, 255), (0, 255, 128), (128, 0, 255)]
lab, _ = fc.classify(a, PAL)


def major_ticks_h(row, x0, x1, length=6):
    return dc.tick_positions(dark, row, -1, length, x0, x1)


def major_ticks_v(col, y0, y1, length=6):
    return dc.tick_positions_v(dark, col, 1, length, y0, y1)


def find_markers(roi, rmin_ok=3.9, cov_ok=0.8, rmin_doubt=3.5, cov_doubt=0.85):
    out = []
    for k in range(len(PAL)):
        for m in fc.markers_dt((lab == k) & roi, 3.0, 5):
            if m["r"] >= rmin_ok and m["cov"] >= cov_ok:
                m["flag"] = ""
            elif m["r"] >= rmin_doubt and m["cov"] >= cov_doubt:
                m["flag"] = "doubtful"
            else:
                continue
            m["k"] = k
            out.append(m)
    return out


def marker_free(k, roi, marks, rad=7):
    """Class-k pixels in roi with every detected marker (any class) blanked out."""
    m = (lab == k) & roi
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
    for q in marks:
        x, y = int(round(q["x"])), int(round(q["y"]))
        m[max(0, y - rad):y + rad + 1, max(0, x - rad):x + rad + 1] &= \
            ((xx[max(0, y - rad):y + rad + 1, max(0, x - rad):x + rad + 1] - q["x"]) ** 2 +
             (yy[max(0, y - rad):y + rad + 1, max(0, x - rad):x + rad + 1] - q["y"]) ** 2 > rad ** 2)
    return m


def trace_rtl(mask, xa, xb, y0, y1, seed_y, max_jump=10):
    """Follow a dashed line from column xb leftwards to xa, starting near seed_y."""
    xs, ys = [], []
    prev, prev_x = seed_y, xb
    for c in range(xb, xa - 1, -1):
        r = np.where(mask[y0:y1, c])[0]
        if len(r) == 0:
            continue
        runs = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
        cents = np.array([y0 + q.mean() for q in runs])
        j = int(np.argmin(np.abs(cents - prev)))
        if abs(cents[j] - prev) > max_jump + 0.5 * abs(prev_x - c):
            continue
        prev, prev_x = cents[j], c
        xs.append(c)
        ys.append(cents[j])
    return np.array(xs[::-1], float), np.array(ys[::-1], float)


rows_csv = {}

# ---------------------------------------------------------------- Fig. 6a main plot
# frame: left axis cols 82-83, bottom axis rows 471-472, top 13-14, right 704-705
xt = major_ticks_h((471, 472), 84, 700)            # inward major ticks 0..45
yt = major_ticks_v((82, 83), 20, 466)              # inward major ticks 14..0
xv = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
yv = [14, 12, 10, 8, 6, 4, 2, 0]
assert len(xt) == len(xv) and len(yt) == len(yv), (xt, yt)
fx, rx, _ = fc.fit_ticks(xt, xv)
fy, ry, sy = fc.fit_ticks(yt + [471.5], yv + [-2])
cal_a = (f"x: major ticks at px {', '.join(f'{t:.1f}' for t in xt)} = {xv} Å, max residual {rx:.3f} Å; "
         f"y: major ticks at px {', '.join(f'{t:.1f}' for t in yt)} = {yv} nN plus bottom frame row 471.5 = -2 nN, "
         f"max residual {ry:.3f} nN; 1 px = {abs(1 / (xt[1] - xt[0]) * 5):.3f} Å in x and {abs(sy):.3f} nN in y")

roi = np.zeros(lab.shape, bool)
roi[15:471, 84:704] = True
roi[15:210, 270:540] = False   # inset
roi[85:320, 120:330] = False   # legend
roi[240:330, 676:704] = False  # arrow to panel b
STEP = [1.0, 1.0, 1.0, 0.75, 1.0, 0.75, 1.0]   # h steps of the plotted points (0.75 and 1.50 Å/ps: 0.75 Å)
light = g > 215
roi[462:, :] = False            # keep the inward tick marks out of the black class
rows = []
ov = []
yy, xx = np.mgrid[0:lab.shape[0], 0:lab.shape[1]]
x45 = int(round(xt[-1]))
for k, s in enumerate(SERIES):
    m = (lab == k) & roi
    # 1) the dashed curve of this colour: chain dash blobs from h_z = 45 Å leftwards
    strict = [q for q in fc.markers_dt(m, 3.0, 5) if q["r"] >= 3.9 and q["cov"] >= 0.8]
    md = m.copy()
    for q in strict:
        md &= (xx - q["x"]) ** 2 + (yy - q["y"]) ** 2 > 6 ** 2
    md = ndi.binary_opening(md, structure=np.ones((2, 2)))
    cols = md[:, x45 - 6:x45 + 4]
    rr = np.where(cols.any(1))[0]
    pts = np.zeros((0, 2))
    if len(rr):
        sy = rr.min()
        sx = x45 - 6 + np.where(cols[sy])[0].mean()
        ch = fc.chain_dashes(md, (sx + 3, sy - 3), (-0.3, 1.0))
        if ch:
            pts = np.vstack([fc.blob_centreline(b) for b in ch])
            pts = pts[fx(pts[:, 0]) >= 32.0]          # beyond this the curves run together
            pts = pts[np.argsort(pts[:, 0])]
    for x, y in pts:
        rows.append([s, "dashed_curve", float(fx(x)), float(fy(y)), "trace"])
    ov.append((list(map(tuple, pts)), OVC[k], "dot"))
    zone = fc.curve_zone(lab.shape, pts[:, 0], pts[:, 1], 3) if len(pts) > 1 else np.zeros(lab.shape, bool)
    # 2) markers on the h_z grid of this series
    # 6a points sit at multiples of the step in h_z (for 0.75 and 1.50 Å/ps: h_z = 0.75 n; note that in
    # panel b the same series sit at h_c = 0.75 n, i.e. not at h_z - 20; see the CSV header)
    grid_v = STEP[k] * np.arange(0, int(45.6 / STEP[k]) + 1)
    grid_px = np.interp(grid_v, xv, xt, left=np.nan, right=np.nan)
    f_lin = np.polyfit(xv, xt, 1)
    grid_px = np.polyval(f_lin, grid_v)
    grid_px = grid_px[(grid_px > 88) & (grid_px < 700)]
    ms = fc.grid_markers(m & ~zone, grid_px, light, rmin=2.2, min_area=18)
    if len(pts) > 1:
        oc = fc.on_curve_markers(m, grid_px[(grid_px >= pts[:, 0].min()) & (grid_px <= pts[:, 0].max())],
                                 lambda xp: np.interp(xp, pts[:, 0], pts[:, 1]))
        ms += [q for q in oc if all((q["x"] - p["x"]) ** 2 + (q["y"] - p["y"]) ** 2 >= 25 for p in ms)]
    ms = sorted(ms, key=lambda q: q["x"])
    for q in ms:
        rows.append([s, "marker", float(fx(q["x"])), float(fy(q["y"])), q["flag"]])
    ov.append(([(q["x"], q["y"]) for q in ms], OVC[k], "ring"))
rows_csv["fig6a"] = (rows, cal_a)
fc.save_overlay(a, ov, str(WORK / "fig6a_overlay.png"), r=1)

# ---------------------------------------------------------------- Fig. 6a inset (0.1 Å/ps)
# axes: x axis rows 186-188 (ticks below), y axis cols 314-315 (ticks left)
col_prof = (g[189:191, 316:540] < 130).any(0)
xr = []
c = 0
while c < len(col_prof):
    if col_prof[c]:
        e = c
        while e + 1 < len(col_prof) and col_prof[e + 1]:
            e += 1
        if e - c >= 1:
            xr.append(316 + (c + e) / 2)
        c = e + 1
    else:
        c += 1
row_prof = g[20:186, 312] < 155   # major ticks reach col 312, minor ones only 313
yr = []
r = 0
while r < len(row_prof):
    if row_prof[r]:
        e = r
        while e + 1 < len(row_prof) and row_prof[e + 1]:
            e += 1
        yr.append(20 + (r + e) / 2)
        r = e + 1
    else:
        r += 1
ixv = [30, 40, 50]
iyv = [12, 8, 4, 0]
assert len(xr) == 3 and len(yr) == 4, (xr, yr)
fxi, rxi, sxi = fc.fit_ticks(xr + [314.5], ixv + [20])
fyi, ryi, syi = fc.fit_ticks(yr, iyv)
cal_i = (f"x: major ticks at px {', '.join(f'{t:.1f}' for t in xr)} = {ixv} Å plus the y axis (col 314.5) = 20 Å, "
         f"max residual {rxi:.3f} Å; y: major ticks at px {', '.join(f'{t:.1f}' for t in yr)} = {iyv} nN, "
         f"max residual {ryi:.3f} nN; 1 px = {abs(sxi):.3f} Å in x and {abs(syi):.3f} nN in y")
roi_i = np.zeros(lab.shape, bool)
roi_i[24:185, 317:540] = True
roi_i[35:70, 340:470] = False   # label "0.1 Å/ps"
blk = (lab == 0) & roi_i
mi = [m for m in fc.markers_dt(blk, 2.5, 4, close=0, cov_r=3.0) if m["cov"] >= 0.8]
rows = []
# points are at integer h_z: keep the strongest candidate per integer (a crossing of the dotted
# curve can give a second, weaker candidate next to a marker)
best = {}
for m in mi:
    key = int(round(float(fxi(m["x"]))))
    if key not in best or m["r"] > best[key]["r"]:
        best[key] = m
mi = sorted(best.values(), key=lambda m: m["x"])
for m in mi:
    rows.append(["0.1 Å/ps", "marker", float(fxi(m["x"])), float(fyi(m["y"])), ""])
# dotted curve: black pixels with markers blanked
cur = blk.copy()
yy, xx = np.mgrid[0:cur.shape[0], 0:cur.shape[1]]
for m in mi:
    cur &= (xx - m["x"]) ** 2 + (yy - m["y"]) ** 2 > 5.5 ** 2
xs, ys = fc.trace_class(cur, 317, 500, 24, 185, max_jump=6)
keep = fxi(xs) <= 45.3
xs, ys = xs[keep], ys[keep]
for x, y in zip(xs[::2], ys[::2]):
    rows.append(["0.1 Å/ps", "dotted_curve", float(fxi(x)), float(fyi(y)), ""])
rows_csv["fig6a_inset"] = (rows, cal_i)
fc.save_overlay(a, [([(m["x"], m["y"]) for m in mi], (255, 0, 255), "ring"),
                    (list(zip(xs, ys)), (0, 200, 255), "dot")], str(WORK / "fig6a_inset_overlay.png"), r=0)

# ---------------------------------------------------------------- Fig. 6b
# frame: left axis cols 871-872, bottom rows 471-472, ticks inward
xtb = major_ticks_h((471, 472), 874, 1490)
ytb = major_ticks_v((871, 872), 20, 466)
# majors on x are 0,5,...,25 (the 52 px ticks in between are minor)
xtb_major = xtb[0::2]
xvb = [0, 5, 10, 15, 20, 25]
# y ticks every 2 nN from 18 (row ~53) down to 0; labels 0,4,...,16 (20 = top frame)
yvb = list(np.arange(18, -0.1, -2))
assert len(xtb_major) == 6 and len(ytb) == len(yvb), (xtb, ytb)
fxb, rxb, sxb = fc.fit_ticks(xtb_major, xvb)
fyb, ryb, syb = fc.fit_ticks(ytb + [12.5], yvb + [20])
cal_b = (f"x: major ticks at px {', '.join(f'{t:.1f}' for t in xtb_major)} = {xvb} Å, max residual {rxb:.3f} Å; "
         f"y: ticks at px {', '.join(f'{t:.1f}' for t in ytb)} = 18..0 nN (step 2; labels on 0, 4, ..., 16) "
         f"plus top frame row 12.5 = 20 nN, max residual {ryb:.3f} nN; 1 px = {abs(sxb):.3f} Å in x and {abs(syb):.3f} nN in y")
roi_b = np.zeros(lab.shape, bool)
roi_b[15:471, 874:1495] = True
roi_b[15:250, 874:1300] = False   # legend block
roi_b[462:, :] = False
EQ = {"0.10 Å/ps": (0.069, 1.47, 0.78), "0.25 Å/ps": (0.034, 1.80, 0.91), "0.50 Å/ps": (0.097, 1.46, 0.95),
      "0.75 Å/ps": (0.056, 1.65, 0.92), "1.00 Å/ps": (0.041, 1.77, 0.94), "1.50 Å/ps": (0.064, 1.68, 0.96),
      "2.00 Å/ps": (0.094, 1.56, 0.94)}
inv_x = lambda v: (np.asarray(v) - fxb(0)) / sxb  # noqa: E731
inv_y = lambda v: (np.asarray(v) - fyb(0)) / syb  # noqa: E731
rows = []
ov = []
for k, s in enumerate(SERIES):
    A, n, _ = EQ[s]
    hc = np.linspace(0, 25.6, 300)
    zone = fc.curve_zone(lab.shape, inv_x(hc), inv_y(A * hc ** n), 3)
    grid_px = inv_x(STEP[k] * np.arange(0, int(25.6 / STEP[k]) + 1))
    ms = fc.grid_markers((lab == k) & roi_b & ~zone, grid_px, light, rmin=2.0, min_area=18)
    oc = fc.on_curve_markers((lab == k) & roi_b, grid_px, lambda xp: inv_y(A * max(float(fxb(xp)), 0) ** n))
    ms += [q for q in oc if all((q["x"] - p["x"]) ** 2 + (q["y"] - p["y"]) ** 2 >= 25 for p in ms)]
    ms = sorted(ms, key=lambda q: q["x"])
    for q in ms:
        rows.append([s, "marker", float(fxb(q["x"])), float(fyb(q["y"])), q["flag"]])
    ov.append(([(q["x"], q["y"]) for q in ms], OVC[k], "ring"))
    hcs = np.linspace(0, 25.5, 52)
    for h in hcs:
        rows.append([s, "fit_equation", float(h), float(A * h ** n), ""])
    ov.append((list(zip(inv_x(hcs), inv_y(A * hcs ** n))), OVC[k], "dot"))
rows_csv["fig6b"] = (rows, cal_b)
fc.save_overlay(a, ov, str(WORK / "fig6b_overlay.png"), r=1)

# ---------------------------------------------------------------- write CSVs
COMMON = [
    "Provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF page 11, image 1503 x 2026 px) by",
    "figures/fig6_extract.py with tools/f2_common.py. Each pixel is assigned to the legend colour whose",
    "white-mixing line it is closest to (the balls are shaded towards white). The plotted points sit on a fixed",
    "x grid (read from the isolated markers: steps of 1 Å for 0.10, 0.25, 0.50, 1.00 and 2.00 Å/ps, 0.75 Å for",
    "0.75 and 1.50 Å/ps); markers are searched only within +-2.5 px of these grid columns (distance-transform",
    "maxima >= 2 px, blob >= 18 px), after removing the series' own dashed line (+-3 px). The centre row comes",
    "from the marker's free edge(s): flag '' = both edges free (midpoint), 'top-edge' / 'bottom-edge' = only that",
    "edge free (centre = edge -+ 4 px), 'hidden-edges' = both edges covered (midpoint, least certain),",
    "'same-colour-stack' = two touching markers of one colour, 'on-curve' = marker lying on its own dashed line",
    "(found from a vertical run >= 8.5 px across the line). x is the measured centroid column.",
    "INCOMPLETE: markers completely hidden under markers or lines of other colours are missing (the panel shows",
    "far more points than can be seen); a few detections may be dash fragments of the same colour.",
]
DESC = {
    "fig6a": ["Fig. 6a (main plot): indenter force F_z (nN) vs displacement of indenter h_z (Å), seven loading rates.",
              "Columns: series = loading rate (legend label); kind = marker (one plotted data point) or dashed_curve",
              "(centre line of the dashed line of the same colour, followed dash by dash from h_z = 45 Å leftwards and",
              "kept only for h_z >= 32 Å; below that the seven curves run together; where curves touch, a trace may",
              "follow a neighbouring curve of similar colour: flag 'trace'); x_hz_A = h_z in Å; y_Fz_nN = F_z in nN; flag.",
              *COMMON,
              "In this panel the 0.75 and 1.50 Å/ps points sit at h_z = 0.75 n (last point h_z = 45.0 Å).",
              "For h_z below ~17 Å all seven series lie at F_z ~ 0 and their markers overlap into one band; only the topmost",
              "(mostly 2.00 and 1.50 Å/ps) are visible, so the low-h_z markers of the other series are not in this file.",
              "The 0.10 Å/ps point at h_z = 45 Å (10.5 nN in the inset) is hidden behind other markers here.",
              "The pink shaded background (h_z ~ 20-45 Å) is not data. The dashed curves are not the panel-b power laws.",
              "Uncertainty: about ±0.1 Å in x and ±0.05 nN in y for a fully visible marker (one source pixel = 0.08 Å,",
              "0.037 nN); ±0.15 nN for edge-based centres; ±0.1 nN for the dashed-curve trace."],
    "fig6a_inset": ["Fig. 6a inset: F_z (nN) vs h_z (Å) for 0.1 Å/ps only (axes 20-50 Å, 0-12 nN).",
                    "Columns: series; kind = marker or dotted_curve (the dotted black line through the points, traced",
                    "column by column with the markers blanked out, every 2nd column); x_hz_A; y_Fz_nN; flag.",
                    "Provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF page 11) by figures/fig6_extract.py;",
                    "markers = distance-transform maxima of the black mask (radius >= 2.5 px, >= 80 % fill of a 3 px disc),",
                    "one per integer h_z (the strongest). 25 markers, h_z = 21-45 Å; a point at h_z = 20 Å, if plotted,",
                    "is hidden by the y axis.",
                    "Uncertainty: about ±0.15 Å in x and ±0.1 nN in y (one source pixel = 0.14 Å, 0.087 nN)."],
    "fig6b": ["Fig. 6b: indenter force F_z (nN) vs indentation depth h_c (Å), seven loading rates, with power-law fits.",
              "Columns: series; kind = marker (digitized data point) or fit_equation (y = a x^m computed from the legend",
              "equation printed in the panel, 52 points from 0 to 25.5 Å; not digitized); x_hc_A = h_c in Å;",
              "y_Fz_nN = F_z in nN; flag. Legend equations (as printed): 0.10 Å/ps y = 0.069x^1.47, R^2 = 0.78;",
              "0.25 Å/ps y = 0.034x^1.80, R^2 = 0.91; 0.50 Å/ps y = 0.097x^1.46, R^2 = 0.95; 0.75 Å/ps y = 0.056x^1.65,",
              "R^2 = 0.92; 1.00 Å/ps y = 0.041x^1.77, R^2 = 0.94; 1.50 Å/ps y = 0.064x^1.68, R^2 = 0.96;",
              "2.00 Å/ps y = 0.094x^1.56, R^2 = 0.94. The equation curves were drawn over the source image",
              "(work/fig6b_overlay.png) and lie on the printed dashed lines.",
              *COMMON,
              "In this panel the 0.75 and 1.50 Å/ps points sit at h_c = 0.75 n (last point h_c = 25.5 Å), i.e. 0.5 Å",
              "to the right of h_z - 20 of the same points in panel a (the other series match h_c = h_z - 20).",
              "Uncertainty: about ±0.05 Å in x and ±0.05 nN in y for a fully visible marker (one source pixel = 0.048 Å,",
              "0.048 nN); ±0.15 nN for edge-based centres."],
}
XCOL = {"fig6a": "x_hz_A", "fig6a_inset": "x_hz_A", "fig6b": "x_hc_A"}
for name, (rows, cal) in rows_csv.items():
    dc.write_csv(str(HERE / f"{name}.csv"), DESC[name] + ["Calibration (linear least squares on tick marks found in the image): " + cal],
                 ["series", "kind", XCOL[name], "y_Fz_nN", "flag"], rows, fmt=["{}", "{}", "{:.3f}", "{:.3f}", "{}"])
    print(name, len(rows), "rows;", cal)
    for s in SERIES + ["0.1 Å/ps"]:
        n = sum(1 for r in rows if r[0] == s and r[1] == "marker")
        if n:
            print("   ", s, n, "markers")
