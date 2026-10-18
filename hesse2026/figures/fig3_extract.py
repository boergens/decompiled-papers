#!/usr/bin/env python3
"""fig3_extract.py -- recover the data of Figure 3 (PDF page 37) from the vector paths / embedded images.

Writes the fig3*.csv files and the panel-e PNGs into this folder (run from anywhere; paths are
resolved relative to this file). The redraw scripts fig3<p>.py read only the CSVs.

Notes on the PDF: every panel is a Form XObject. pdfplot.drawings(page, clip) silently drops paths
whose bounding rect is degenerate (a horizontal 2-point line has zero height, and fitz.Rect.intersects
returns False for empty rects), which is the case for every spike in panel b. We therefore take the
unclipped drawing list and filter by the centre of each path's rect ourselves. Dashed lines are not
strokes with a dash array but "outlined" fills (one polygon per dash); their centre lines are
recovered from pairs of anti-parallel polygon edges one line-width apart (see dashed_vertices()).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "tools"))
import fitz  # noqa: E402
import numpy as np  # noqa: E402
import pdfplot as pp  # noqa: E402

PDF = os.path.join(ROOT, "source", "2026.10.15.759299v1.full.pdf")
PAGE = 37
page = pp.open_page(PDF, PAGE)
ALL = pp.drawings(page, None)  # unclipped, see module docstring
PROV = f"Source: Hesse et al. 2026 bioRxiv 10.64898/2026.10.15.759299v1, Figure 3, PDF page {PAGE}; extracted by fig3_extract.py from vector paths (PDF points, origin top-left)"


def out(name):
    return os.path.join(HERE, name)


def inclip(clip):
    """Paths whose rect centre lies in clip (robust to zero-height/width rects)."""
    res = []
    for d in ALL:
        x0, y0, x1, y1 = d["rect"]
        if clip.contains(fitz.Point((x0 + x1) / 2, (y0 + y1) / 2)):
            res.append(d)
    return res


def hcaps(draws, xlo, xhi, max_len=2.5):
    """y of short horizontal thin fills (axis end caps / ticks) whose centre x is in [xlo, xhi]."""
    ys = []
    for s in pp.thin_segments(draws):
        if s["orient"] == "h" and s["len"] <= max_len:
            cx = (s["x0"] + s["x1"]) / 2
            if xlo <= cx <= xhi:
                ys.append(s["y0"])
    return sorted(ys)


def axis_report(name, ax):
    print(f"  {name}: slope={ax.slope:.6g} intercept={ax.intercept:.6g} resid={ax.resid:.2e} pairs={[(round(p,2), v) for p, v in ax.pairs]}")


# ------------------------------------------------------------------ dashed lines (outlined fills)

def dashed_vertices(polys, xgrid, width=None, tol_w=None, min_edge=0.05, eps=0.03, par_tol=0.006):
    """Recover the centre line of a dashed polyline that was exported as filled dash polygons.

    polys: list of closed polygons [(x,y),...] (each one dash = outline of a stroke of `width`; width=None
    measures it as the shortest edge of the first 4-point dash).
    xgrid: ascending pixel x of the polyline's vertices (the line is straight between consecutive xgrid).
    Each polygon edge is an offset copy (+-width/2) of a piece of the centre line; two anti-parallel
    edges `width` apart (same perpendicular offset at both ends of the overlap, so really parallel, not
    just nearly: consecutive steep segments of a spike are nearly anti-parallel too) bound the same
    piece, and their mid-line IS the centre line there. Each piece is extended to the vertices at both
    ends of the grid interval(s) it lies in. Estimates are weighted by 1/sigma^2 with sigma = the
    extrapolated distance along the line times the angular precision (0.0015 pt / overlap length).
    Returns (est, meta): est[k] = list of (y, weight) for vertex k.
    """
    if width is None:
        for poly in polys:
            if len(poly) in (4, 5):
                q = poly
                width = min(math.hypot(q[i + 1][0] - q[i][0], q[i + 1][1] - q[i][1]) for i in range(len(q) - 1))
                break
        assert width is not None, "no 4-point dash to measure the width"
    tol_w = tol_w if tol_w is not None else max(0.02, 0.06 * width)
    K = len(xgrid)
    est = [[] for _ in range(K)]
    n_pairs = 0
    for poly in polys:
        pts = [p for p in poly]
        if len(pts) > 1 and abs(pts[0][0] - pts[-1][0]) < 1e-9 and abs(pts[0][1] - pts[-1][1]) < 1e-9:
            pts = pts[:-1]
        n = len(pts)
        edges_all = []
        for i in range(n):
            p0, p1 = pts[i], pts[(i + 1) % n]
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            L = math.hypot(dx, dy)
            edges_all.append((p0, p1, (dx / L, dy / L) if L > 1e-12 else (0.0, 0.0), L))
        # butt caps: an edge about `width` long whose polygon neighbours are anti-parallel to each other and
        # perpendicular to it (the two sides of the dash's end piece). Caps must not pair with join edges.
        edges = []
        m = len(edges_all)
        for i, (p0, p1, u, L) in enumerate(edges_all):
            if L < min_edge:
                continue
            if abs(L - width) < 0.15 * width:
                _, _, up, Lp = edges_all[(i - 1) % m]
                _, _, un, Ln = edges_all[(i + 1) % m]
                if Lp > 1e-6 and Ln > 1e-6 and (up[0] * un[0] + up[1] * un[1]) < -0.98 \
                        and abs(u[0] * up[0] + u[1] * up[1]) < 0.15 and abs(u[0] * un[0] + u[1] * un[1]) < 0.15:
                    continue  # cap
            edges.append((p0, p1, u, L))
        for a in range(len(edges)):
            p0, p1, u, L = edges[a]
            nx, ny = -u[1], u[0]
            for b in range(a + 1, len(edges)):
                q0, q1, v, M = edges[b]
                dot = u[0] * v[0] + u[1] * v[1]
                if dot > -0.99:
                    continue  # not anti-parallel
                off0 = (q0[0] - p0[0]) * nx + (q0[1] - p0[1]) * ny  # signed distance of q0 from line a
                off1 = (q1[0] - p0[0]) * nx + (q1[1] - p0[1]) * ny
                if abs(off0 - off1) > par_tol:
                    continue  # not parallel (different segments)
                off = (off0 + off1) / 2
                if abs(abs(off) - width) > tol_w:
                    continue
                s0 = (q0[0] - p0[0]) * u[0] + (q0[1] - p0[1]) * u[1]
                s1 = (q1[0] - p0[0]) * u[0] + (q1[1] - p0[1]) * u[1]
                lo, hi = max(0.0, min(s0, s1)), min(L, max(s0, s1))
                if hi - lo < min_edge:
                    continue
                n_pairs += 1
                mx0, my0 = p0[0] + off / 2 * nx, p0[1] + off / 2 * ny  # mid-line: m(s) = (mx0, my0) + s*u
                if abs(u[0]) < 1e-4:
                    continue  # (near-)vertical piece: no usable x extent
                xa, xb = sorted([mx0 + lo * u[0], mx0 + hi * u[0]])
                smid = (lo + hi) / 2
                sig_ang = 0.0015 / (hi - lo)
                for k in range(K - 1):
                    gx0, gx1 = xgrid[k], xgrid[k + 1]
                    if xb < gx0 + eps or xa > gx1 - eps:
                        continue  # piece does not lie in this interval (a piece spanning several intervals = merged collinear run)
                    for kk, gx in ((k, gx0), (k + 1, gx1)):
                        s = (gx - mx0) / u[0]
                        sig = abs(s - smid) * sig_ang + 0.002
                        est[kk].append((my0 + s * u[1], 1.0 / sig ** 2))
    spreads = [max(y for y, w in e) - min(y for y, w in e) for e in est if len(e) > 1]
    meta = dict(n_pairs=n_pairs, max_spread=max(spreads) if spreads else 0.0,
                n_vertices_with_estimates=sum(1 for e in est if e), width=width)
    return est, meta


def dashed_values(polys, xgrid, width, yax, label=""):
    """dashed_vertices + averaging; returns (values, flags) with flags 'dash' (recovered from dash geometry)
    or 'gap' (vertex lies inside a gap between dashes: linearly interpolated, approximate) or 'none'."""
    est, meta = dashed_vertices(polys, xgrid, width)
    vals = np.full(len(xgrid), np.nan)
    flags = ["none"] * len(xgrid)
    sig = np.full(len(xgrid), np.nan)
    for k, e in enumerate(est):
        if e:
            ys = np.array([y for y, w in e]); ws = np.array([w for y, w in e])
            vals[k] = yax(float(np.sum(ys * ws) / np.sum(ws)))
            sig[k] = (1.0 / math.sqrt(np.sum(ws))) * abs(yax.slope)  # data units
            flags[k] = "dash"
    meta["max_sigma"] = float(np.nanmax(sig)) if np.any(~np.isnan(sig)) else 0.0
    meta["spread"] = np.array([(max(y for y, w in e) - min(y for y, w in e)) * abs(yax.slope) if len(e) > 1 else (0.0 if e else np.nan) for e in est])
    # interpolate gaps between recovered vertices
    idx = np.where(~np.isnan(vals))[0]
    if len(idx) >= 2:
        for k in range(idx[0], idx[-1] + 1):
            if np.isnan(vals[k]):
                vals[k] = np.interp(k, idx, vals[idx])
                flags[k] = "gap"
    n_gap = flags.count("gap")
    print(f"  dashed {label}: width {meta['width']:.3f}, {meta['n_pairs']} edge pairs, {meta['n_vertices_with_estimates']}/{len(xgrid)} vertices from dashes, "
          f"{n_gap} interpolated in gaps, max spread between estimates of one vertex {meta['max_spread']:.3f} pt "
          f"(= {abs(meta['max_spread'] * yax.slope):.3f} data units), max weighted sigma {meta['max_sigma']:.3f} data units")
    return vals, flags, meta


def line_points(d, min_dx=0.05):
    """Vertices of a line stroke, dropping points closer than min_dx (in x) to the previous one
    (the exported lines end with a 0.005-0.01 pt tail segment that is not a data point)."""
    pts = []
    for p in d["points"]:
        if pts and abs(p[0] - pts[-1][0]) < min_dx:
            continue
        pts.append(p)
    return pts


def vertical_extent(poly, x, tol=1e-6):
    """y values where the vertical line at x crosses the edges of polygon poly (list of (x, y))."""
    ys = []
    n = len(poly)
    for i in range(n - 1):
        (xa, ya), (xb, yb) = poly[i], poly[i + 1]
        if abs(xb - xa) < tol:
            if abs(xa - x) < tol:
                ys += [ya, yb]
            continue
        if min(xa, xb) - tol <= x <= max(xa, xb) + tol:
            ys.append(ya + (yb - ya) * (x - xa) / (xb - xa))
    return ys


def polys_of(d):
    """Closed polygons (subpaths) of a fill path."""
    return [sp for sp in d["subpaths"] if len(sp) >= 4]


# ================================================================== panel a: box plot
def panel_a():
    print("panel a")
    clip = pp.R(40, 20, 95, 86)
    dr = inclip(clip)
    yax = pp.axis_from_ticks(dr, "y", [0, 0.2, 0.4, 0.6, 0.8], region=pp.R(43, 20, 45.6, 85))
    axis_report("y", yax)
    circles = [d for d in dr if d["kind"] == "fill" and d["has_curves"] and d["n_items"] == 4 and pp.hexcolor(d["fill"]) == "#262626"]
    pts = sorted([((d["rect"][0] + d["rect"][2]) / 2, (d["rect"][1] + d["rect"][3]) / 2) for d in circles], key=lambda p: -p[1])
    print(f"  {len(pts)} session points")
    box = [d for d in dr if d["kind"] == "fill" and not d["has_curves"] and d["n_items"] == 4 and pp.hexcolor(d["fill"]) == "#262626"][0]
    bx0, by0, bx1, by1 = box["rect"]
    strokes = [d for d in dr if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == "#262626"]
    horiz = sorted([d["rect"][1] for d in strokes if abs(d["rect"][3] - d["rect"][1]) < 0.01 and (d["rect"][2] - d["rect"][0]) > 2])
    # horizontal strokes: whisker caps (top, bottom) and the median (inside the box)
    median_y = [y for y in horiz if by0 < y < by1][0]
    cap_top, cap_bot = min(horiz), max(horiz)
    zero = [d for d in dr if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#808080"][0]
    zero_y = (zero["rect"][1] + zero["rect"][3]) / 2
    print(f"  box y0={by0:.2f} y1={by1:.2f} median={median_y:.2f} caps={cap_top:.2f},{cap_bot:.2f} zero line y={zero_y:.2f} -> {yax(zero_y):.4f}")
    com = [PROV, "Panel a: box plot of per-session gain in log-likelihood (two-state minus one-state model), n=19 sessions.",
           "Box geometry from the box fill rect, the median stroke and the whisker cap strokes (all #262626).",
           f"y axis calibrated from 5 tick marks at values 0,0.2,0.4,0.6,0.8 (max residual {yax.resid:.1e}).",
           f"Dashed reference line at y={yax(zero_y):.4f} (nominally 0). Precision ~0.002 (0.1 pt).",
           "Legend: boxes = median and interquartile range, whiskers = range."]
    rows = [["whisker_low_min", round(yax(cap_bot), 4)], ["q1", round(yax(by1), 4)], ["median", round(yax(median_y), 4)],
            ["q3", round(yax(by0), 4)], ["whisker_high_max", round(yax(cap_top), 4)]]
    pp.write_csv(out("fig3a_box.csv"), ["statistic", "log_likelihood_diff"], rows, com)
    com2 = [PROV, "Panel a: the 19 individual session points (filled circles, diameter 2.24 pt), sorted by value (descending).",
            "The figure does not identify sessions; point_index is just a rank. x_jitter_pt = horizontal offset of the",
            "point from the box centre in PDF points (the points are jittered horizontally in the figure).",
            f"y axis calibrated from tick marks at 0,0.2,0.4,0.6,0.8 (max residual {yax.resid:.1e}); precision ~0.002."]
    bcx = (bx0 + bx1) / 2
    rows2 = [[i + 1, round(yax(y), 4), round(x - bcx, 2)] for i, (x, y) in enumerate(pts)]
    pp.write_csv(out("fig3a_points.csv"), ["point_index", "log_likelihood_diff", "x_jitter_pt"], rows2, com2)
    print("  values:", [r[1] for r in rows2])


# ================================================================== panels b, c, d: rasters
def raster_b(name, clip, xregion, cap_xlo, cap_xhi, n_rows, label):
    print(f"panel b {name}")
    dr = inclip(clip)
    xax = pp.axis_from_ticks(dr, "x", [-50, 0, 50], region=xregion)
    axis_report("x", xax)
    caps = hcaps(dr, cap_xlo, cap_xhi)
    y_top, y_bot = caps[0], caps[-1]
    pitch = (y_bot - y_top) / (n_rows + 1)  # MATLAB ylim = [0, n+1]
    spikes = [d for d in dr if d["kind"] == "stroke" and abs(d["width"] - 0.3) < 0.01 and d["n_items"] == 1]
    rows = []
    worst_row, worst_t = 0.0, 0.0
    for d in spikes:
        x0, y0, x1, y1 = d["rect"]
        r = (y0 - y_top) / pitch
        t = xax(x0)
        worst_row = max(worst_row, abs(r - round(r)))
        worst_t = max(worst_t, abs(t - round(t)))
        rows.append([int(round(r)), int(round(t))])
    rows.sort()
    rs = [r for r, t in rows]
    assert min(rs) >= 1 and max(rs) <= n_rows, (min(rs), max(rs))
    sep = [d for d in dr if d["kind"] == "stroke" and abs(d["width"] - 0.5) < 0.01][0]
    sep_row = (sep["rect"][1] - y_top) / pitch
    dur = np.median([d["rect"][2] - d["rect"][0] for d in spikes]) / xax.slope
    print(f"  {len(spikes)} spikes, rows {min(rs)}..{max(rs)} of {n_rows}, pitch {pitch:.5f} pt, worst row offset {worst_row:.3f}, worst time offset {worst_t:.3f} ms, "
          f"spike drawn width {dur:.2f} ms, separator line at row {sep_row:.2f}")
    com = [PROV, f"Panel b ({label}): spike raster, one row per spike; {n_rows} cell-transitions (rows), held-out half of neurons.",
           f"Spikes are drawn as 0.3-pt-thick horizontal marks {dur:.2f} ms (0.43 pt) long whose left end sits exactly on an integer ms",
           f"(spike times binned at 1 ms, 100 distinct bins); time_ms is that integer (-50..49) relative to the state transition.",
           f"x axis calibrated from 3 tick marks at -50, 0, 50 ms (max residual {xax.resid:.1e}); worst deviation of a spike from an integer ms {worst_t:.3f} ms.",
           f"Row index from the y position: y-axis spans {y_top:.2f}..{y_bot:.2f} pt = rows 0..{n_rows + 1} (MATLAB ylim), pitch {pitch:.4f} pt; worst deviation from an integer row {worst_row:.3f}.",
           f"Rows are numbered from the top (row 1 = top of the raster). Cells are sorted by modulation index; the solid horizontal line in the figure sits at row {sep_row:.1f} (cells above prefer the conscious face, below the suppressed face).",
           "Vertical dashed line at 0 ms = state transition. Spikes drawn with alpha 0.7 in the figure."]
    pp.write_csv(out(f"fig3b_{name}.csv"), ["row_index", "time_ms"], rows, com)
    return dict(n_rows=n_rows, sep_row=sep_row, n_spikes=len(spikes))


def raster_cd(panel, name, clip, xregion, yregion, n_rows, label):
    print(f"panel {panel} {name}")
    dr = inclip(clip)
    xax = pp.axis_from_ticks(dr, "x", [-50, 0, 50], region=xregion)
    yax = pp.axis_from_ticks(dr, "y", [n_rows, 1], region=yregion)  # bottom tick = n, top tick = 1
    axis_report("x", xax)
    axis_report("y", yax)
    spikes = [d for d in dr if d["kind"] == "stroke" and abs(d["width"] - 0.14) < 0.01 and d["n_items"] == 1
              and abs(d["rect"][2] - d["rect"][0]) < 0.01]
    rows = []
    worst = 0.0
    for d in spikes:
        x0, y0, x1, y1 = d["rect"]
        r = yax((y0 + y1) / 2)
        worst = max(worst, abs(r - round(r)))
        rows.append([int(round(r)), round(xax(x0), 2)])
    rows.sort()
    rs = [r for r, t in rows]
    assert min(rs) >= 1 and max(rs) <= n_rows, (min(rs), max(rs))
    print(f"  {len(spikes)} spikes, rows {min(rs)}..{max(rs)} of {n_rows}, worst row offset {worst:.3f}; time precision ~{0.01 / xax.slope:.2f} ms per 0.01 pt")
    com = [PROV, f"Panel {panel} ({label}): spike raster of one example cell, one row per spike (vertical 0.14-pt tick marks).",
           f"{n_rows} transitions (rows); row 1 = top row of the raster (y-axis tick '1' at the top, '{n_rows}' at the bottom).",
           f"x axis calibrated from 3 tick marks at -50, 0, 50 ms (max residual {xax.resid:.1e}); spike time = x of the tick mark, precision ~0.02 ms.",
           f"y axis calibrated from the two y tick marks (rows 1 and {n_rows}, max residual {yax.resid:.1e}); worst deviation from an integer row {worst:.3f}.",
           "Vertical dashed line at 0 ms = state transition."]
    pp.write_csv(out(f"fig3{panel}_{name}.csv"), ["row_index", "time_ms"], rows, com)


# ================================================================== panel e: face images
def panel_e():
    print("panel e")
    ims = pp.images(page, pp.R(5, 140, 250, 415))
    cols = ["gt_conscious", "recon_state1", "gt_suppressed", "recon_state2"]
    rows_y = sorted(set(round(i["bbox"][1] / 10) for i in ims))
    for im in ims:
        r = rows_y.index(round(im["bbox"][1] / 10)) + 1
        c = int(round((im["bbox"][0] - 13.86) / 59.83))
        name = f"fig3e_r{r}_{cols[c]}.png"
        w, h = pp.extract_image(page, im["xref"], out(name))
        print(f"  {name}: xref {im['xref']} {w}x{h} px placed at {[round(v, 1) for v in im['bbox']]} ({im['bbox'][2] - im['bbox'][0]:.1f} pt wide)")


# ================================================================== panel f: explained variance
def panel_f():
    print("panel f")
    clip = pp.R(270, 120, 390, 245)
    dr = inclip(clip)
    xax = pp.axis_from_ticks(dr, "x", [10, 20, 30, 40, 50], region=pp.R(286, 239.9, 390, 243.5))
    yax = pp.axis_from_ticks(dr, "y", [-100, -50, 0, 50, 100], region=pp.R(285, 126, 288.97, 241))
    axis_report("x", xax)
    axis_report("y", yax)
    series = {}
    xgrid = None
    for d in dr:
        if d["kind"] == "stroke" and len(d["points"]) == 51 and not d["has_curves"]:
            c = pp.hexcolor(d["color"])
            pts = line_points(d)
            assert len(pts) == 50, len(pts)
            xs = [xax(x) for x, y in pts]
            ys = [yax(y) for x, y in pts]
            assert max(abs(x - round(x)) for x in xs) < 0.02, xs
            feat = [int(round(x)) for x in xs]
            assert feat == list(range(1, 51))
            series[c] = ys
            xgrid = [x for x, y in pts]
    # dashed series (outlined fills)
    dash_polys = {}
    for d in dr:
        if d["kind"] == "fill" and d["n_items"] > 100 and pp.hexcolor(d["fill"]) in ("#fcae34", "#543379"):
            dash_polys.setdefault(pp.hexcolor(d["fill"]), []).extend(polys_of(d))
    # bracket extents (Shape / Appearance) for the record
    br = [d for d in dr if d["kind"] == "stroke" and d["has_curves"] and abs(d["width"] - 0.5) < 0.01]
    for b in br:
        print(f"  bracket x {xax(b['rect'][0]):.2f}..{xax(b['rect'][2]):.2f} features")
    sup1, f1, m1 = dashed_values(dash_polys["#fcae34"], xgrid, 1.0, yax, "suppressed state 1 (orange)")
    sup2, f2, m2 = dashed_values(dash_polys["#543379"], xgrid, 1.0, yax, "suppressed state 2 (purple)")
    ymin_axis = -100.0
    com = [PROV, "Panel f: explained variance (%) of the 50 face features (1-20 shape, 21-50 appearance) by features predicted from",
           "neural activity of the held-out half of neurons. Solid lines are stroke paths with 50 vertices (one per feature, exact).",
           "Dashed lines are exported as filled dash polygons; their vertices were recovered from the dash geometry (pairs of",
           "anti-parallel polygon edges 1 pt apart = the two sides of the 1-pt stroke; each piece extrapolated to the integer",
           "feature at both ends of its interval). *_recovery: 'dash' = at least one dash piece lies in an adjacent unit interval",
           "(exact to ~0.1 pt = 0.4 %), 'gap' = vertex lies between two dashes with no coverage on either side: linearly",
           "interpolated between neighbours (approximate), 'none' = no estimate (first/last vertex lies beyond the first/last",
           "dash), 'clipped_at_axis_min' = the figure clips the line at -100 there (the exported line is split into fragments with",
           "the clipped vertex projected onto the axis limit): value left empty, true value <= -100 (the figure draws it at -100).",
           f"x axis calibrated from ticks 10..50 (max residual {xax.resid:.1e}); y axis from ticks -100..100 (max residual {yax.resid:.1e}).",
           f"max spread between independent estimates of one dashed vertex: orange {m1['max_spread'] * abs(yax.slope):.2f} %, purple {m2['max_spread'] * abs(yax.slope):.2f} %.",
           "Colours: priming_average #1c0f29, state1 #fcae34, state2 #543379."]
    hdr = ["feature_index", "feature_type", "priming_average_pct", "binocular_conscious_state1_pct", "binocular_conscious_state2_pct",
           "binocular_suppressed_state1_pct", "binocular_suppressed_state1_recovery", "binocular_suppressed_state2_pct", "binocular_suppressed_state2_recovery"]
    rows = []
    for k in range(50):
        v1, fl = sup1[k], f1[k]
        if not np.isnan(v1) and v1 < ymin_axis + 0.1 and fl == "dash":
            v1, fl = np.nan, "clipped_at_axis_min"  # the figure clips the line at -100 (vertex projected onto the axis limit); true value unknown (<= -100)
        rows.append([k + 1, "shape" if k < 20 else "appearance", round(series["#1c0f29"][k], 2), round(series["#fcae34"][k], 2),
                     round(series["#543379"][k], 2), round(float(v1), 2) if not np.isnan(v1) else "", fl,
                     round(float(sup2[k]), 2) if not np.isnan(sup2[k]) else "", f2[k]])
    pp.write_csv(out("fig3f.csv"), hdr, rows, com)
    print("  priming avg first/last:", rows[0][2], rows[-1][2], "| sup1 min", np.nanmin(sup1), "| sup2 range", np.nanmin(sup2), np.nanmax(sup2))


# ================================================================== panel g: decoding accuracy vs number of faces
def panel_g():
    print("panel g")
    clip = pp.R(398, 120, 512, 245)
    dr = inclip(clip)
    xax = pp.axis_from_ticks(dr, "x", [0, 20, 40, 60], region=pp.R(412, 239.5, 510, 243))
    yax = pp.axis_from_ticks(dr, "y", [0, 20, 40, 60, 80, 100], region=pp.R(410, 126, 413.75, 241))
    axis_report("x", xax)
    axis_report("y", yax)
    names = {"#1c0f29": "priming_average", "#fcae34": "state1", "#543379": "state2"}
    solid, bands, dashes, xgrid = {}, {}, {}, None
    for d in dr:
        c = pp.hexcolor(d["color"] if d["kind"] == "stroke" else d["fill"])
        if c not in names:
            continue
        if d["kind"] == "stroke" and len(d["points"]) == 60:
            pts = line_points(d)
            assert len(pts) == 60, len(pts)
            xs = [xax(x) for x, y in pts]
            assert max(abs(x - round(x)) for x in xs) < 0.02
            assert [int(round(x)) for x in xs] == list(range(1, 61))
            solid[c] = [yax(y) for x, y in pts]
            xgrid = [x for x, y in pts]
        elif d["kind"] == "fill" and max(len(sp) for sp in d["subpaths"]) >= 50:
            bands.setdefault(c, []).append(d)
        elif d["kind"] == "fill" and d["n_items"] > 100:
            dashes.setdefault(c, []).extend(polys_of(d))
    # bands: envelope per integer x; identify which band belongs to the solid vs dashed series by proximity to the line
    band_env = {}
    for c, lst in bands.items():
        for d in lst:
            # vertical extent of the (possibly clipped) band polygon at each integer x: intersect every subpath
            # with the vertical line x = xgrid[k]; clipped bands then give lo = 0 / hi = 100 at the clip
            xs, lo, hi = [], [], []
            for k, gx in enumerate(xgrid):
                ys = []
                for sp in d["subpaths"]:
                    ys += vertical_extent(sp, gx)
                if len(ys) >= 2:
                    xs.append(k + 1)
                    lo.append(yax(max(ys)))
                    hi.append(yax(min(ys)))
            band_env.setdefault(c, []).append((xs, lo, hi, d))
    sup1, fl1, m1 = dashed_values(dashes["#fcae34"], xgrid, 1.0, yax, "suppressed state 1 (orange)")
    sup2, fl2, m2 = dashed_values(dashes["#543379"], xgrid, 1.0, yax, "suppressed state 2 (purple)")
    lines = {"priming_average": solid["#1c0f29"], "conscious_state1": solid["#fcae34"], "conscious_state2": solid["#543379"],
             "suppressed_state1": sup1, "suppressed_state2": sup2}
    # assign bands to lines: band whose midpoint is closest to the line (over x>=10, where bands are unclipped)
    assign = {}
    cand = {"priming_average": "#1c0f29", "conscious_state1": "#fcae34", "suppressed_state1": "#fcae34", "conscious_state2": "#543379", "suppressed_state2": "#543379"}
    for ln, c in cand.items():
        best = None
        for j, (xs, lo, hi, d) in enumerate(band_env[c]):
            mid = {x: (l + h) / 2 for x, l, h in zip(xs, lo, hi)}
            err = np.nanmean([abs(mid[x] - lines[ln][x - 1]) for x in range(10, 61) if x in mid])
            if best is None or err < best[0]:
                best = (err, j)
        assign[ln] = best[1]
        xs, lo, hi, d = band_env[c][best[1]]
        print(f"  band for {ln}: path with {len(d['points'])} pts, mean |band midpoint - line| over faces 10-60 = {best[0]:.2f} %, x range {xs[0]}..{xs[-1]}")
    assert len(set((cand[l], j) for l, j in assign.items())) == 5, assign
    # the bands are symmetric about the mean (solid lines match their band midpoints to 0.00 %): where a dashed vertex
    # falls in a gap between dashes, use the band midpoint (unclipped bands only) instead of interpolating
    for ln, vals, fl in (("suppressed_state1", sup1, fl1), ("suppressed_state2", sup2, fl2)):
        xs, lo, hi, d = band_env[cand[ln]][assign[ln]]
        for k in range(60):
            if fl[k] == "gap" and (k + 1) in xs:
                i = xs.index(k + 1)
                if lo[i] > 0.05 and hi[i] < 99.95:
                    vals[k] = (lo[i] + hi[i]) / 2
                    fl[k] = "band_midpoint"
    hdr = ["number_of_faces"]
    for ln in lines:
        hdr += [f"{ln}_pct", f"{ln}_lo_pct", f"{ln}_hi_pct", f"{ln}_band_clip"]
        if ln.startswith("suppressed"):
            hdr += [f"{ln}_recovery"]
    rows = []
    for k in range(60):
        n = k + 1
        row = [n]
        for ln in lines:
            xs, lo, hi, d = band_env[cand[ln]][assign[ln]]
            if n in xs:
                i = xs.index(n)
                clipflag = "+".join(f for f, c in (("lo", lo[i] <= 0.05), ("hi", hi[i] >= 99.95)) if c)
                l, h = round(min(max(lo[i], 0.0), 100.0), 2), round(min(max(hi[i], 0.0), 100.0), 2)
            else:
                l, h, clipflag = "", "", ""
            v = lines[ln][k]
            row += [round(float(v), 2) if not np.isnan(v) else "", l, h, clipflag]
            if ln == "suppressed_state1":
                row += [fl1[k]]
            if ln == "suppressed_state2":
                row += [fl2[k]]
        rows.append(row)
    com = [PROV, "Panel g: decoding accuracy (%) vs number of faces (target + distractors), held-out half of neurons. Mean lines",
           "(solid = stroke paths with 60 vertices at 1..60 faces, exact) and shaded bands (filled polygons, alpha 0.2: upper",
           "and lower edge at each integer x, written as *_lo_pct / *_hi_pct). The legend of Fig. 3 does not say what the band",
           "is (Fig. 2c/d use SD across sessions); it is symmetric about the mean where unclipped. Bands and lines are clipped",
           "to the 0..100 axis range in the figure: *_lo_pct / *_hi_pct are the VISIBLE band edges (clipped to 0/100), and",
           "*_band_clip says 'lo' / 'hi' / 'lo+hi' where the edge sits on the axis limit (true extent unknown beyond it; at",
           "1 face all series are exactly 100 with a zero-width band, which is also flagged 'hi').",
           "Dashed lines (suppressed) are outlined fills; vertices recovered from pairs of anti-parallel dash edges 1 pt apart,",
           "*_recovery 'dash' = recovered from dash geometry (exact to ~0.1 pt = 0.2 %), 'band_midpoint' = vertex lies in a gap",
           "between dashes, value taken as the midpoint of the (symmetric, unclipped) band, 'gap' = in a gap and band clipped at 0:",
           "linearly interpolated between recovered neighbours (approximate), 'none' = no estimate (last vertex beyond the last dash).",
           f"x axis calibrated from ticks 0,20,40,60 (max residual {xax.resid:.1e}); y axis from ticks 0..100 (max residual {yax.resid:.1e}).",
           f"max spread between independent estimates of one dashed vertex: orange {m1['max_spread'] * abs(yax.slope):.2f} %, purple {m2['max_spread'] * abs(yax.slope):.2f} %.",
           "Colours: priming_average #1c0f29, state1 #fcae34, state2 #543379."]
    pp.write_csv(out("fig3g.csv"), hdr, rows, com)
    # consistency: dashed line vs band midpoint
    for ln in ("suppressed_state1", "suppressed_state2"):
        xs, lo, hi, d = band_env[cand[ln]][assign[ln]]
        diffs = [(x, lines[ln][x - 1] - (l + h) / 2) for x, l, h in zip(xs, lo, hi) if l > 0.05 and h < 99.95 and not np.isnan(lines[ln][x - 1])]
        if diffs:
            print(f"  {ln}: dashed line - band midpoint (unclipped x): max |diff| {max(abs(v) for x, v in diffs):.2f} % over {len(diffs)} points")
    print("  first row:", rows[0][:4], " last row:", rows[-1][:4])


# ================================================================== panel h: single-trial decoding time courses
def panel_h():
    print("panel h")
    subs = {
        "average": dict(clip=pp.R(270, 285, 335, 345), xreg=pp.R(284, 333.3, 329, 335.5), yreg=pp.R(281.5, 287, 283.6, 334), col="#808080"),
        "state1": dict(clip=pp.R(270, 350, 335, 410), xreg=pp.R(284, 398.5, 329, 400.5), yreg=pp.R(281.5, 352, 283.5, 399), col="#fcae34"),
        "state2": dict(clip=pp.R(332, 350, 392, 410), xreg=pp.R(344, 398.2, 389, 400.5), yreg=pp.R(342, 352, 343.9, 399), col="#543379"),
    }
    for name, s in subs.items():
        dr = inclip(s["clip"])
        xax = pp.axis_from_ticks(dr, "x", [0, 1, 2], region=s["xreg"])
        yax = pp.axis_from_ticks(dr, "y", [0, 50, 100], region=s["yreg"])
        print(f" {name}:")
        axis_report("x", xax)
        axis_report("y", yax)
        solid = [d for d in dr if d["kind"] == "stroke" and len(d["points"]) == 212 and pp.hexcolor(d["color"]) == s["col"]][0]
        spts = line_points(solid)
        assert len(spts) == 211, len(spts)
        xgrid = [x for x, y in spts]
        t = [xax(x) for x in xgrid]
        assert max(abs(v * 100 - round(v * 100)) for v in t) < 0.05, "time grid not 10 ms"
        t = [round(v, 2) for v in t]
        con = [yax(y) for x, y in spts]
        dpolys = []
        for d in dr:
            if d["kind"] == "fill" and d["n_items"] > 300 and pp.hexcolor(d["fill"]) == s["col"]:
                dpolys.extend(polys_of(d))
        sup, fl, meta = dashed_values(dpolys, xgrid, 1.0, yax, f"{name} suppressed")
        # do not interpolate across gaps for this jagged line: keep only dash-recovered samples
        sup = np.array([v if f == "dash" else np.nan for v, f in zip(sup, fl)])
        n_dash = int(np.sum(~np.isnan(sup)))
        com = [PROV, f"Panel h ({name}): single-trial decoding accuracy (%) vs time from flash for an example session, held-out half of neurons.",
               "The x axis label in the figure reads 'Time from flash (ms)', but the range 0..2 with the 200-ms sliding window is seconds; column is time_from_flash_s.",
               "conscious_pct: solid line (stroke path, 211 samples at 10-ms steps from -0.1 to 2.0 s; exact).",
               "suppressed_pct: dashed line exported as filled dash polygons; samples recovered where a dash covers the sample",
               "(centre line from pairs of anti-parallel dash edges 1 pt apart, extended to the sample times at both ends of each",
               "10-ms interval); empty = inside a gap between dashes (not visible in the figure, not recoverable).",
               f"{n_dash} of 211 suppressed samples recovered. suppressed_estimate_spread_pct = max-min of the independent estimates of that",
               "sample (0 = single estimate): the dash outlines of this jagged line (samples 0.2 pt apart, stroke 1 pt wide) overlap themselves,",
               f"so samples with a large spread are uncertain by about that amount; max spread {meta['max_spread'] * abs(yax.slope):.2f} %, typical < 0.5 %.",
               f"x axis calibrated from ticks 0,1,2 (max residual {xax.resid:.1e}); y axis from ticks 0,50,100 (max residual {yax.resid:.1e}). Precision ~0.2 % (0.1 pt).",
               f"Colour: {s['col']}."]
        spread = meta["spread"]
        rows = [[t[i], round(con[i], 2), round(float(sup[i]), 2) if not np.isnan(sup[i]) else "",
                 round(float(spread[i]), 2) if not np.isnan(sup[i]) else ""] for i in range(211)]
        pp.write_csv(out(f"fig3h_{name}.csv"), ["time_from_flash_s", "conscious_pct", "suppressed_pct", "suppressed_estimate_spread_pct"], rows, com)
        print(f"  conscious range {min(con):.1f}..{max(con):.1f}, suppressed recovered {n_dash}/211, range {np.nanmin(sup):.1f}..{np.nanmax(sup):.1f}")


# ================================================================== panel i: paired plot
def panel_i():
    print("panel i")
    clip = pp.R(405, 283, 512, 402)
    dr = inclip(clip)
    yax = pp.axis_from_ticks(dr, "y", [0, 20, 40, 60, 80, 100], region=pp.R(410, 285, 413.6, 399))
    axis_report("y", yax)
    xt = pp.tick_marks(dr, "x", region=pp.R(420, 397.8, 500, 401.5))
    xcat = [t["pos"] for t in xt]
    assert len(xcat) == 3, xcat
    print(f"  category x: {[round(x, 2) for x in xcat]}")
    cats = ["average", "state1", "state2"]
    thin_solid = [d for d in dr if d["kind"] == "stroke" and abs(d["width"] - 0.14) < 0.01 and d["n_items"] == 2]
    thick_solid = [d for d in dr if d["kind"] == "stroke" and abs(d["width"] - 1.0) < 0.01 and d["n_items"] == 2][0]
    black_fills = [d for d in dr if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#000000" and d["n_items"] >= 30]
    # thick vs thin dashed: width of the dash quads (length of the shortest edge of the first quad)
    def quad_width(d):
        q = d["subpaths"][0]
        return min(math.hypot(q[i + 1][0] - q[i][0], q[i + 1][1] - q[i][1]) for i in range(len(q) - 1))
    thick_dash = [d for d in black_fills if quad_width(d) > 0.5]
    thin_dash = [d for d in black_fills if quad_width(d) <= 0.5]
    assert len(thick_dash) == 1 and len(thin_dash) == 10 and len(thin_solid) == 10, (len(thick_dash), len(thin_dash), len(thin_solid))
    def line_vals(d):
        pts = d["points"]
        assert all(abs(p[0] - x) < 0.05 for p, x in zip(pts, xcat))
        return [yax(p[1]) for p in pts]
    rows = []
    con = [line_vals(d) for d in thin_solid]
    for i, v in enumerate(con):
        rows.append([f"session_{i + 1}", "conscious", "dash"] + [round(x, 2) for x in v])
    sup = []
    for i, d in enumerate(thin_dash):
        v, fl, meta = dashed_values(polys_of(d), xcat, None, yax, f"thin dashed line {i + 1}")
        sup.append(v)
        rows.append([f"session_{i + 1}", "suppressed", "+".join(fl)] + [round(float(x), 2) for x in v])
    mean_con = line_vals(thick_solid)
    mean_sup, fl, meta = dashed_values(polys_of(thick_dash[0]), xcat, 1.0, yax, "thick dashed mean line")
    rows.append(["mean_line", "conscious", "dash"] + [round(x, 2) for x in mean_con])
    rows.append(["mean_line", "suppressed", "+".join(fl)] + [round(float(x), 2) for x in mean_sup])
    # markers
    mk = []
    for d in dr:
        c = pp.hexcolor(d["fill"])
        if d["kind"] == "fill" and d["has_curves"] and c in ("#808080", "#fcae34", "#543379", "#ffffff") and 4 <= d["n_items"] <= 8 and d["rect"][2] - d["rect"][0] < 6:
            mk.append(d)
    filled = {}
    openm = {}
    for d in mk:
        cx, cy = (d["rect"][0] + d["rect"][2]) / 2, (d["rect"][1] + d["rect"][3]) / 2
        k = min(range(3), key=lambda j: abs(xcat[j] - cx))
        c = pp.hexcolor(d["fill"])
        if c == "#ffffff":
            openm[cats[k]] = yax(cy)
        elif d["n_items"] == 4:
            filled[cats[k]] = yax(cy)
    rows.append(["mean_marker_filled", "conscious", "marker"] + [round(filled[c], 2) for c in cats])
    rows.append(["mean_marker_open", "suppressed", "marker"] + [round(openm[c], 2) for c in cats])
    sess_mean_con = np.mean(con, axis=0)
    sess_mean_sup = np.nanmean(np.array(sup, dtype=float), axis=0)
    rows.append(["mean_of_session_values", "conscious", "computed"] + [round(float(x), 2) for x in sess_mean_con])
    rows.append(["mean_of_session_values", "suppressed", "computed"] + [round(float(x), 2) for x in sess_mean_sup])
    print("  thick solid line:", [round(x, 2) for x in mean_con], " filled markers:", [round(filled[c], 2) for c in cats], " mean of sessions:", np.round(sess_mean_con, 2))
    print("  thick dashed line:", [round(float(x), 2) for x in mean_sup], " open markers:", [round(openm[c], 2) for c in cats], " mean of sessions:", np.round(sess_mean_sup, 2))
    com = [PROV, "Panel i: single-trial decoding accuracy (%) per session (n=10) for Average / State 1 / State 2, conscious (thin solid",
           "lines, filled markers) and suppressed (thin dashed lines, open markers); thick lines = mean across sessions.",
           "The figure does not link a conscious line to its session's suppressed line: session_k is the k-th thin line in PDF",
           "path order within each condition (probably, but not verifiably, the same session order for both conditions).",
           "Thin solid lines are 3-vertex stroke paths (exact). Dashed lines are outlined fills; their vertices were recovered",
           "from pairs of anti-parallel dash edges (0.14 pt apart for thin, 1 pt for the thick mean line) extrapolated to the",
           "category x positions; recovery lists per vertex 'dash' (recovered) or 'gap'. mean_marker_* rows are the centres of",
           "the large circles; mean_of_session_values rows are computed here from the session rows as a consistency check.",
           f"y axis calibrated from ticks 0..100 (max residual {yax.resid:.1e}); precision ~0.2 %.",
           "Colours: markers grey #808080 (Average), orange #fcae34 (State 1), purple #543379 (State 2); lines black; thin lines alpha 0.5."]
    pp.write_csv(out("fig3i.csv"), ["line", "condition", "recovery", "average_pct", "state1_pct", "state2_pct"], rows, com)


if __name__ == "__main__":
    panel_a()
    b1 = raster_b("state2_to_state1", pp.R(120, 20, 190, 100), pp.R(133, 82.6, 178, 85.2), 132.8, 134.6, 1196, "State 2 -> State 1, left raster")
    b2 = raster_b("state1_to_state2", pp.R(190, 20, 252, 100), pp.R(201, 82.7, 246, 85.3), 200.6, 202.5, 988, "State 1 -> State 2, right raster")
    pp.write_csv(out("fig3b_meta.csv"), ["raster", "n_rows", "separator_row_y", "n_spikes"],
                 [["state2_to_state1", b1["n_rows"], round(b1["sep_row"], 1), b1["n_spikes"]], ["state1_to_state2", b2["n_rows"], round(b2["sep_row"], 1), b2["n_spikes"]]],
                 [PROV, "Panel b: number of rows (cell-transitions) per raster and the row position of the solid horizontal separator line",
                  "(cells above prefer the conscious face, cells below the suppressed face). separator_row_y is the y of that line in row units",
                  "(row k's spike marks are centred at y = k; the line is drawn at an integer row position, i.e. on top of that row)."])
    raster_cd("c", "state2_to_state1", pp.R(286, 20, 336, 100), pp.R(289.5, 83.5, 335, 85.5), pp.R(288.5, 25, 290.7, 85), 21, "State 2 -> State 1, left raster; example ML cell preferring the conscious face")
    raster_cd("c", "state1_to_state2", pp.R(346, 20, 396, 100), pp.R(349, 83.5, 395, 85.5), pp.R(348, 25, 350.3, 85), 18, "State 1 -> State 2, right raster; example ML cell preferring the conscious face")
    raster_cd("d", "state2_to_state1", pp.R(411, 20, 459, 100), pp.R(414, 83.4, 458.5, 85.4), pp.R(413, 25, 415, 85), 26, "State 2 -> State 1, left raster; example AM cell preferring the suppressed face")
    raster_cd("d", "state1_to_state2", pp.R(466, 20, 514, 100), pp.R(469, 83.4, 513.5, 85.4), pp.R(468, 25, 470, 85), 20, "State 1 -> State 2, right raster; example AM cell preferring the suppressed face")
    panel_e()
    panel_f()
    panel_g()
    panel_h()
    panel_i()
