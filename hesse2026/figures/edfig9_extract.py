"""Extraction script for Extended Data Figure 9 (PDF page 49) -- writes the CSVs and the panel-b images.

Run from anywhere:  python3 edfig9_extract.py
Reads only the PDF (via tools/pdfplot.py); writes into this folder.  Original 300-dpi crops for the QA
comparison images are written to ORIG_DIR (scratch); the compare images are composed by make_compare.sh.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import math
import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "tools"))
import pdfplot as pp  # noqa: E402

PDF = os.path.join(ROOT, "source", "2026.10.15.759299v1.full.pdf")
OUT = os.path.join(ROOT, "figures")
ORIG_DIR = os.environ.get("EDFIG9_ORIG_DIR", OUT)
os.makedirs(ORIG_DIR, exist_ok=True)
PAGE_NO = 49

page = pp.open_page(PDF, PAGE_NO)
ALL = pp.drawings(page)  # whole page; clip tests drop zero-height spike strokes, so filter by position here


def inbox(d, x0, y0, x1, y1):
    r = d["rect"]
    return r[0] >= x0 - 1e-6 and r[2] <= x1 + 1e-6 and r[1] >= y0 - 1e-6 and r[3] <= y1 + 1e-6


def region(x0, y0, x1, y1):
    return [d for d in ALL if inbox(d, x0, y0, x1, y1)]


def axis_pairs(draws, orientation, values, region_rect):
    ax = pp.axis_from_ticks(draws, orientation, values, region=region_rect)
    assert ax.resid / abs(ax.slope) < 0.05, ax  # residual in PDF points
    return ax


def hx(d):
    return pp.hexcolor(d["color"] if d["kind"] == "stroke" else d["fill"])


def r4(v):
    return "" if (v is None or (isinstance(v, float) and math.isnan(v))) else round(float(v), 4)


PROV = f"Source: Hesse et al. 2026 bioRxiv 10.64898/2026.10.15.759299v1, Extended Data Figure 9, PDF page {PAGE_NO}; coordinates recovered from vector paths with PyMuPDF (tools/pdfplot.py)."

# ======================================================================================= panel a: raster
A = region(5, 14, 262, 142)
xax_a = axis_pairs(A, "x", [-1, -0.5, 0, 0.5, 1], pp.R(15, 114.5, 240, 118))
spikes = [d for d in A if d["kind"] == "stroke" and d["n_items"] == 1 and hx(d) == "#000000"
          and d["width"] is not None and abs(d["width"] - 1.0) < 1e-3]
sx = np.array([(d["subpaths"][0][0][0] + d["subpaths"][0][1][0]) / 2 for d in spikes])
sy = np.array([(d["subpaths"][0][0][1] + d["subpaths"][0][1][1]) / 2 for d in spikes])
# row lattice: cluster distinct y, fit pitch/offset by least squares, number rows from the upper y-axis tick
ys = np.unique(np.round(sy, 3))
clusters = [[ys[0]]]
for v in ys[1:]:
    (clusters[-1].append(v) if v - clusters[-1][-1] < 0.08 else clusters.append([v]))
cy = np.array([np.mean(c) for c in clusters])
dcy = np.diff(cy)
pitch0 = np.median(dcy[dcy < 0.3])
idx = np.concatenate([[0], np.cumsum(np.round(dcy / pitch0))]).astype(int)
(pitch, off), *_ = np.linalg.lstsq(np.vstack([idx, np.ones_like(idx)]).T, cy, rcond=None)
lat_resid = float(np.abs(idx * pitch + off - cy).max())
yticks_a = pp.tick_marks(A, "y", max_len=4.0, min_len=1.0, region=pp.R(14, 15, 18.5, 116))
ytop, ybot = yticks_a[0]["pos"], yticks_a[-1]["pos"]
top_row_f = (ytop - off) / pitch  # lattice index of the upper tick (about -8)
row_of = lambda y: int(round((y - off) / pitch - top_row_f)) + 1  # upper tick = row 1
rows = np.array([row_of(y) for y in sy])
t_sp = xax_a(sx)
sep = [d for d in A if d["kind"] == "stroke" and d["n_items"] == 1 and d["width"] and abs(d["width"] - 0.25) < 1e-3]
sep_row = (sep[0]["rect"][1] - off) / pitch - top_row_f + 1
flash = [d for d in A if d["kind"] == "stroke" and d["n_items"] == 1 and d["width"] and abs(d["width"] - 0.5) < 1e-3]
print(f"[a] spikes {len(spikes)}, rows with spikes {len(cy)}, lattice pitch {pitch:.5f} pt, resid {lat_resid:.4f} pt, "
      f"upper tick at lattice {top_row_f:.3f}, lower tick row {(ybot - off) / pitch - top_row_f + 1:.3f}, "
      f"separator row {sep_row:.3f}, flash line x->t {xax_a(flash[0]['rect'][0]):.4f}, rows used {rows.min()}..{rows.max()}")
order = np.lexsort((t_sp, rows))
pp.write_csv(os.path.join(OUT, "edfig9a_spikes.csv"), ["row_index", "time_s"],
             [[int(rows[i]), r4(t_sp[i])] for i in order],
             [PROV, "Panel a: raster of an example trial; one row per spike (black 1-pt-wide, 0.1-pt-long stroke segments; "
              "time = segment centre).",
              f"x axis calibrated from the 5 tick marks at -1,-0.5,0,0.5,1 s (resid {xax_a.resid:.2e}); time precision about 0.5 ms.",
              f"row_index: spike y positions lie on a lattice with pitch {pitch:.5f} pt (fit residual {lat_resid:.4f} pt); "
              "row 1 is the row at the upper y-axis tick, rows increase downwards; the lower y-axis tick is row 412; "
              f"the thin horizontal ML/AM separator line lies between rows {int(math.floor(sep_row))} and {int(math.ceil(sep_row))} (ML above, AM below).",
              f"{len(cy)} distinct rows contain spikes (the axis label says 429 cells; rows 1-8 and rows without spikes are empty). "
              "Which cell number each row corresponds to is not recoverable from the figure.",
              f"Vertical flash-onset line at t = {xax_a(flash[0]['rect'][0]):.3f} s."])
# state shading: two independent 20 %-opacity tilings (orange/purple = conscious/suppressed; white/black = On/Off)
def tiling(col):
    sel = [d for d in A if d["kind"] == "fill" and hx(d) == col and abs(d["rect"][1] - 18.11) < 0.2 and d["rect"][3] > 100]
    return sorted([(d["rect"][0], d["rect"][2]) for d in sel])
til = {c: tiling(c) for c in ["#fcae34", "#543379", "#ffffff", "#000000"]}
percept = sorted([(a, b, "conscious") for a, b in til["#fcae34"]] + [(a, b, "suppressed") for a, b in til["#543379"]])
onoff = sorted([(a, b, "On") for a, b in til["#ffffff"]] + [(a, b, "Off") for a, b in til["#000000"]])
for name, T in [("percept", percept), ("onoff", onoff)]:
    gaps = [(T[i][1], T[i + 1][0]) for i in range(len(T) - 1) if abs(T[i][1] - T[i + 1][0]) > 0.02]
    assert not gaps, (name, gaps)
edges = sorted(set([e for a, b, _ in percept + onoff for e in (a, b)]))
def lookup(T, x):
    best = min(T, key=lambda t: 0.0 if t[0] <= x <= t[1] else min(abs(x - t[0]), abs(x - t[1])))
    dist = 0.0 if best[0] <= x <= best[1] else min(abs(x - best[0]), abs(x - best[1]))
    return best[2] if dist < 0.02 else None
ep_rows = []
for a, b in zip(edges[:-1], edges[1:]):
    if b - a < 1e-6:
        continue
    m = (a + b) / 2
    p, o = lookup(percept, m), lookup(onoff, m)
    assert p is not None and o is not None, (a, b, p, o)
    ep_rows.append([r4(xax_a(a)), r4(xax_a(b)), f"{p}_{o}", "state1" if p == "conscious" else "state2", p, o])
# merge consecutive identical states (edges of the two tilings that coincide split nothing)
merged = []
for r in ep_rows:
    if merged and merged[-1][2] == r[2] and abs(merged[-1][1] - r[0]) < 2e-4:  # same state, contiguous (sub-0.01-pt seams)
        merged[-1][1] = r[1]
    else:
        merged.append(list(r))
n_zero = sum(1 for r in merged if r[1] <= r[0])
merged = [r for r in merged if r[1] > r[0]]  # seams between the two tilings shorter than the 0.1-ms rounding step
print(f"[a] dropped {n_zero} zero-duration (<0.1 ms) seam intervals")
pp.write_csv(os.path.join(OUT, "edfig9a_state_epochs.csv"),
             ["t_start_s", "t_end_s", "state", "llr_state", "percept", "on_off"], merged,
             [PROV, "Panel a: background shading = four inferred states per time bin, drawn as two overlaid tilings of 20 %-opacity "
              "rectangles: orange (#fcae34) = conscious (state 1) / purple (#543379) = suppressed (state 2), and white = On / black = Off.",
              f"The two tilings have {len(percept)} and {len(onoff)} rectangles; this file lists the {len(merged)} intervals of the "
              "combined four-state sequence (consecutive identical states merged; seams between the two tilings shorter than the 0.1-ms "
              "rounding step dropped, so a few consecutive rows may share a boundary time while differing by < 0.1 ms). Edge precision about 0.1 ms (0.01 pt).",
              f"Same x calibration as edfig9a_spikes.csv (resid {xax_a.resid:.2e}). Shading spans t = {merged[0][0]} to {merged[-1][1]} s.",
              "Rendered colours: conscious_On = pale orange, conscious_Off = dark tan, suppressed_On = pale lavender, suppressed_Off = dark grey-purple."])
print(f"[a] epochs {len(merged)}; first {merged[0]}, last {merged[-1]}")
pp.render(page, pp.R(5, 14, 262, 142), 300, os.path.join(ORIG_DIR, "edfig9a_orig.png"))

# ======================================================================================= panel b: faces
ims = pp.images(page, pp.R(265, 30, 515, 310))
colnames = {274: "gt_conscious", 334: "recon_state1", 393: "gt_suppressed", 453: "recon_state2"}
rowsy = sorted(set(round(i["bbox"][1] / 50) for i in ims))
assert len(ims) == 20, len(ims)
for im in ims:
    r = rowsy.index(round(im["bbox"][1] / 50)) + 1
    cname = colnames[min(colnames, key=lambda k: abs(k - im["bbox"][0]))]
    fn = os.path.join(OUT, f"edfig9b_r{r}_{cname}.png")
    w, h = pp.extract_image(page, im["xref"], fn)
    print(f"[b] row {r} {cname}: xref {im['xref']} {w}x{h} px at {[round(v, 1) for v in im['bbox']]}")
pp.render(page, pp.R(265, 12, 515, 308), 300, os.path.join(ORIG_DIR, "edfig9b_orig.png"))


# ======================================================================================= dashed-line recovery
def dash_centrelines(d, width=1.0):
    """Centre-line pieces (x0,y0,x1,y1) of a dashed line that was exported as filled dash outlines."""
    pieces = []
    for sp in d["subpaths"]:
        pts = list(sp)
        if math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) > 1e-6:
            pts.append(pts[0])
        E0 = []
        for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
            L = math.hypot(bx - ax, by - ay)
            if L >= 1e-6:
                E0.append((ax, ay, bx, by, L, (bx - ax) / L, (by - ay) / L))
        E = []
        for i, e in enumerate(E0):
            if e[4] < 0.6:  # notches / tiny split pieces (end caps are exactly `width` long, sides are longer)
                continue
            prv, nxt = E0[i - 1], E0[(i + 1) % len(E0)]
            is_cap = abs(e[4] - width) < 0.04 and abs(prv[5] * e[5] + prv[6] * e[6]) < 0.25 and abs(nxt[5] * e[5] + nxt[6] * e[6]) < 0.25
            if not is_cap:
                E.append(e)
        for i, e1 in enumerate(E):
            for e2 in E[i + 1:]:
                if e1[5] * e2[5] + e1[6] * e2[6] > -0.9995:  # must be antiparallel (opposite sides of the outline)
                    continue
                nx, ny = -e1[6], e1[5]
                mx, my = (e2[0] + e2[2]) / 2, (e2[1] + e2[3]) / 2
                dist = (mx - e1[0]) * nx + (my - e1[1]) * ny
                if abs(abs(dist) - width) > 0.12:
                    continue
                ux, uy = e1[5], e1[6]
                t2 = sorted([(e2[0] - e1[0]) * ux + (e2[1] - e1[1]) * uy, (e2[2] - e1[0]) * ux + (e2[3] - e1[1]) * uy])
                lo, hi = max(0.0, t2[0]), min(e1[4], t2[1])
                if hi - lo < 0.15:
                    continue
                sx0, sy0 = e1[0] + nx * dist / 2, e1[1] + ny * dist / 2
                pieces.append((sx0 + ux * lo, sy0 + uy * lo, sx0 + ux * hi, sy0 + uy * hi))
    return pieces


def dashed_vertices(pieces, xv):
    """y (PDF) of a polyline with vertices at x positions xv, from dash centre-line pieces; NaN where no dash
    touches either adjacent segment. Also returns the disagreement between the two adjacent-segment estimates."""
    n = len(xv)
    seg = [[] for _ in range(n - 1)]
    for x0, y0, x1, y1 in pieces:
        if x1 < x0:
            x0, y0, x1, y1 = x1, y1, x0, y0
        if x1 - x0 < 1e-4:
            continue
        k = int(np.searchsorted(xv, (x0 + x1) / 2)) - 1
        if 0 <= k < n - 1:
            m = (y1 - y0) / (x1 - x0)
            seg[k].append((m, y0 - m * x0, math.hypot(x1 - x0, y1 - y0)))
    y, spread = np.full(n, np.nan), np.full(n, np.nan)
    for k in range(n):
        ests = []
        for s in [k - 1, k]:
            if 0 <= s < n - 1 and seg[s]:
                w = np.array([l[2] for l in seg[s]])
                v = np.array([l[0] * xv[k] + l[1] for l in seg[s]])
                ests.append(float((w * v).sum() / w.sum()))
        if ests:
            y[k], spread[k] = np.mean(ests), (max(ests) - min(ests) if len(ests) > 1 else 0.0)
    return y, spread


def snap_polyline(points, xax, yax, nmax, x_of_index):
    """Map stroke points to (index -> value); points at clip boundaries (x not on the index grid) are dropped."""
    out = {}
    for x, y in points:
        k = int(round(xax(x)))
        if 1 <= k <= nmax and abs(x - x_of_index(k)) < 0.03:
            if k not in out or abs(x - x_of_index(k)) < abs(out[k][0] - x_of_index(k)):
                out[k] = (x, yax(y))
    return {k: v for k, (x, v) in out.items()}


# ======================================================================================= panel c
C = region(5, 145, 130, 290)
xax_c = axis_pairs(C, "x", [10, 20, 30, 40, 50], pp.R(40, 267.6, 130, 271))
yax_c = axis_pairs(C, "y", [-100, -50, 0, 50, 100], pp.R(28, 150, 31.6, 270))
xc = lambda k: xax_c.inv(k)
XV_C = np.array([xc(k) for k in range(1, 51)])
series_c = {}
# solid strokes
for d in C:
    if d["kind"] == "stroke" and d["width"] and abs(d["width"] - 1.0) < 1e-3 and hx(d) in ("#1c0f29", "#fcae34", "#543379"):
        name = {"#1c0f29": "priming_average", "#fcae34": "binocular_conscious_state1", "#543379": "binocular_conscious_state2"}[hx(d)]
        series_c.setdefault(name, {}).update(snap_polyline(d["points"], xax_c, yax_c, 50, xc))
# dashed fills
for d in C:
    if d["kind"] == "fill" and hx(d) in ("#fcae34", "#543379") and d["n_items"] > 100:
        name = {"#fcae34": "binocular_suppressed_state1", "#543379": "binocular_suppressed_state2"}[hx(d)]
        pcs = dash_centrelines(d)
        yv, spr = dashed_vertices(pcs, XV_C)
        series_c[name] = {k + 1: yax_c(yv[k]) for k in range(50) if not np.isnan(yv[k])}
        series_c[name + "__spread"] = spr
        print(f"[c] {name}: {len(pcs)} dash pieces, {np.isnan(yv).sum()} vertices without dash info, "
              f"max adjacent-segment disagreement {np.nanmax(spr) * abs(yax_c.slope):.2f} %")
hdr_c = ["feature_index", "feature_group", "priming_average", "binocular_conscious_state1", "binocular_conscious_state2",
         "binocular_suppressed_state1", "binocular_suppressed_state2"]
rows_c = []
for k in range(1, 51):
    rows_c.append([k, "shape" if k <= 20 else "appearance"] + [r4(series_c[n].get(k, float("nan"))) for n in hdr_c[2:]])
n_clip = sum(1 for k in range(1, 51) if k not in series_c["binocular_conscious_state2"])
pp.write_csv(os.path.join(OUT, "edfig9c.csv"), hdr_c, rows_c,
             [PROV, "Panel c: explained variance of features (%) vs feature index (1-50; 1-20 shape, 21-50 appearance), 5 series.",
              f"x axis from tick marks at 10..50 (resid {xax_c.resid:.2e}); y axis from tick marks at -100..100 (resid {yax_c.resid:.2e}).",
              "Solid series (priming_average black #1c0f29, binocular_conscious_state1 orange #fcae34, binocular_conscious_state2 purple #543379) "
              "are 1-pt stroke polylines with one vertex per feature; precision about 0.1 % (0.01 pt).",
              f"binocular_conscious_state2 is clipped at the lower axis limit: {n_clip} features have values below -100 % and are left empty "
              "(the drawn line leaves the axes there).",
              "Dashed series (binocular_suppressed_state1 orange dashed, binocular_suppressed_state2 purple dashed) were exported as filled "
              "dash outlines; the centre line of each dash was reconstructed from its two long parallel edges and the polyline vertex values "
              "were read where the dashes cover the vertex or by extending the adjacent dash segments; precision about 0.5-1 % "
              "(worse on steep segments). Empty cells = vertex not covered by any dash (none expected)."])
pp.render(page, pp.R(2, 143, 131, 290), 300, os.path.join(ORIG_DIR, "edfig9c_orig.png"))

def band_section(points, x, tol=0.02):
    """[min y, max y] of a closed polygon's intersection with the vertical line at x (None if no intersection)."""
    pts = list(points)
    if math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) > 1e-6:
        pts.append(pts[0])
    ys = []
    for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
        if abs(ax - x) <= tol:
            ys.append(ay)
        if abs(bx - x) <= tol:
            ys.append(by)
        if (ax - x) * (bx - x) < 0 and abs(bx - ax) > 1e-9:
            ys.append(ay + (by - ay) * (x - ax) / (bx - ax))
    return (min(ys), max(ys)) if ys else None


# ======================================================================================= panel d
D = region(130, 145, 262, 290)
xax_d = axis_pairs(D, "x", [0, 20, 40, 60], pp.R(150, 267, 262, 271))
yax_d = axis_pairs(D, "y", [0, 20, 40, 60, 80, 100], pp.R(153, 150, 156.4, 270))
xd = lambda n: xax_d.inv(n)
XV_D = np.array([xd(n) for n in range(1, 61)])
series_d = {}
cols_d = {"#1c0f29": "priming_average", "#fcae34": "state1", "#543379": "state2"}
for d in D:
    c = hx(d)
    if c not in cols_d:
        continue
    op = d["raw"].get("fill_opacity")
    if d["kind"] == "stroke" and d["n_items"] == 59:
        name = "priming_average" if c == "#1c0f29" else f"binocular_conscious_{cols_d[c]}"
        series_d[name] = snap_polyline(d["points"], xax_d, yax_d, 60, xd)
    elif d["kind"] == "fill" and op is not None and abs(op - 0.2) < 0.01:
        # band polygon (clipped by the axes at 0 and 100 %): take its vertical cross-section at every face position
        env = {}
        for n in range(1, 61):
            sec = band_section(d["points"], xd(n))
            if sec:  # y is downwards in PDF: max y -> lower value; clamp the axes-box clip (-0.01 / 100.01) to 0 / 100
                env[n] = (min(max(yax_d(sec[1]), 0.0), 100.0), min(max(yax_d(sec[0]), 0.0), 100.0))
        series_d.setdefault("_bands", []).append((c, d["n_items"], env))
    elif d["kind"] == "fill" and op is not None and abs(op - 1.0) < 0.01 and d["n_items"] > 100:
        name = f"binocular_suppressed_{cols_d[c]}"
        pcs = dash_centrelines(d)
        yv, spr = dashed_vertices(pcs, XV_D)
        series_d[name] = {n + 1: yax_d(yv[n]) for n in range(60) if not np.isnan(yv[n])}
        print(f"[d] {name}: {len(pcs)} dash pieces, {np.isnan(yv).sum()} vertices without dash info, "
              f"max adjacent-segment disagreement {np.nanmax(spr) * abs(yax_d.slope):.2f} %")
# assign bands to series: a band belongs to the series whose line lies inside it (mean of |line - band mid| smallest)
names_d = ["priming_average", "binocular_conscious_state1", "binocular_conscious_state2",
           "binocular_suppressed_state1", "binocular_suppressed_state2"]
band_of = {}
for c, nit, env in series_d["_bands"]:
    cands = [n for n in names_d if (c == "#1c0f29" and n == "priming_average") or (c != "#1c0f29" and n.endswith(cols_d[c]))]
    best = min(cands, key=lambda n: np.mean([abs(series_d[n][k] - (lo + hi) / 2) for k, (lo, hi) in env.items() if k in series_d[n] and k > 5]))
    assert best not in band_of, (best, c, nit)
    band_of[best] = env
    print(f"[d] band {c} ({nit} items) -> {best}; faces covered {min(env)}..{max(env)} ({len(env)})")
hdr_d = ["n_faces"]
for n in names_d:
    hdr_d += [n, n + "_lo", n + "_hi"]
rows_d = []
for k in range(1, 61):
    row = [k]
    for n in names_d:
        lo, hi = band_of[n].get(k, (float("nan"), float("nan")))
        row += [r4(series_d[n].get(k, float("nan"))), r4(lo), r4(hi)]
    rows_d.append(row)
pp.write_csv(os.path.join(OUT, "edfig9d.csv"), hdr_d, rows_d,
             [PROV, "Panel d: decoding accuracy (%) vs number of faces (1-60), 5 series with shaded bands (20 %-opacity filled polygons).",
              f"x axis from tick marks at 0,20,40,60 (resid {xax_d.resid:.2e}); y axis from tick marks at 0..100 (resid {yax_d.resid:.2e}).",
              "Solid series (priming_average black #1c0f29, binocular_conscious_state1 orange #fcae34, binocular_conscious_state2 purple #543379): "
              "1-pt stroke polylines, one vertex per face count; precision about 0.1 %.",
              "Dashed series (binocular_suppressed_state1 orange dashed, binocular_suppressed_state2 purple dashed): exported as filled dash "
              "outlines; centre lines reconstructed from the dash edges (see README); precision about 0.5 %.",
              "_lo/_hi: lower/upper edge of the shaded band at each face count, measured as the vertical cross-section of the band "
              "polygon at that x (precision about 0.1 %), clamped to [0, 100]. Bands are clipped by the axes at 0 and 100 %, so _lo = 0 or _hi = 100 may stand "
              "for values beyond the axis; empty _lo/_hi cells = the band polygon has zero area there (binocular_conscious_state2 beyond "
              "14 faces, where line and band both sit at 0 %). Empty value cells in the dashed series = polyline vertex inside a dash gap "
              "(dash pattern 4 pt on / 4 pt off vs 1.57 pt per face), not recoverable."])
pp.render(page, pp.R(130, 143, 262, 290), 300, os.path.join(ORIG_DIR, "edfig9d_orig.png"))
pp.render(page, pp.R(2, 143, 262, 306), 300, os.path.join(ORIG_DIR, "edfig9cd_orig.png"))

# ======================================================================================= panel e: histograms
E = region(5, 306, 145, 400)
xax_e = axis_pairs(E, "x", [0, 2], pp.R(45, 377.5, 100, 380))  # bottom row ticks (all rows identical x)
row_base = [331.395, 354.395, 377.395]
yt = pp.tick_marks(E, "y", max_len=4.0, min_len=1.0, region=pp.R(41, 310, 43.7, 380))
ytp = [t["pos"] for t in yt]
assert len(ytp) == 6, ytp
yax_rows = [pp.Axis([(ytp[1], 0), (ytp[0], 100)]), pp.Axis([(ytp[3], 0), (ytp[2], 100)]), pp.Axis([(ytp[5], 0), (ytp[4], 100)])]
leg_e = {"#fcae34": "state1_conscious", "#ffd28a": "state1_suppressed", "#b56cc7": "state2_conscious", "#543379": "state2_suppressed"}
hist_rows = []
max_frac = 0.0
for d in E:
    op = d["raw"].get("fill_opacity")
    if d["kind"] != "fill" or hx(d) not in leg_e or op is None or abs(op - 0.302) > 0.01:
        continue
    r = min(range(3), key=lambda i: abs(d["rect"][3] - row_base[i]))
    yax = yax_rows[r]
    tops = {}
    for it in d["raw"]["items"]:
        if it[0] == "l" and abs(it[1].y - it[2].y) < 1e-3:
            key = tuple(sorted([round(it[1].x, 3), round(it[2].x, 3)]))
            tops[key] = min(tops.get(key, 1e9), it[1].y)
        elif it[0] == "re":
            rr = it[1]
            key = (round(rr.x0, 3), round(rr.x1, 3))
            tops[key] = min(tops.get(key, 1e9), rr.y0)
    for (x0, x1), ytop in sorted(tops.items()):
        if x1 - x0 < 0.5:
            continue
        cnt = yax(ytop)
        max_frac = max(max_frac, abs(cnt - round(cnt)))
        hist_rows.append([r + 1, leg_e[hx(d)], r4(xax_e(x0)), r4(xax_e(x1)), int(round(cnt))])
tot = {}
for r, s, lo, hi, cnt in hist_rows:
    tot[(r, s)] = tot.get((r, s), 0) + cnt
print("[e] totals per (row, series):", tot, "max |count - integer| before rounding", round(max_frac, 4))
pp.write_csv(os.path.join(OUT, "edfig9e.csv"), ["panel_row", "series", "gain_bin_lo", "gain_bin_hi", "count"], hist_rows,
             [PROV, "Panel e: three stacked histograms of single-cell tuning gain; each row overlays two series (filled at 30 % opacity "
              "plus a step outline). Row 1: state1_conscious (orange #fcae34, 0.2-wide bins) and state1_suppressed (pale orange #ffd28a, "
              "0.1-wide bins); row 2: state2_conscious (pale purple #b56cc7, 0.1-wide bins) and state2_suppressed (purple #543379, 0.2-wide bins); "
              "row 3: state1_conscious and state2_suppressed (0.2-wide bins).",
              f"x axis from tick marks at 0 and 2 (resid {xax_e.resid:.2e}); y axis of each row from its two tick marks at 0 and 100 counts "
              "(the three rows have different count scales). Counts come from the bar heights of the 30 %-opacity filled rectangles; "
              "the measured heights were all within 0.005 counts of an integer and were rounded to integers.",
              "Colours: state1_conscious #fcae34, state1_suppressed #ffd28a, state2_conscious #b56cc7, state2_suppressed #543379.",
              "The right-most bin of the 0.2-wide series is cut by the axis limit at gain 2.5 (bin 2.4-2.5 as drawn). "
              "Totals per series are listed in README.md."])
pp.render(page, pp.R(2, 306, 148, 400), 300, os.path.join(ORIG_DIR, "edfig9e_orig.png"))


# ======================================================================================= scatter helpers
def scatter(draws, xax, yax, size):
    mk = [d for d in draws if d["kind"] == "fill" and d["has_curves"] and d["n_items"] == 4 and hx(d) == "#000000"
          and abs((d["rect"][2] - d["rect"][0]) - size) < 0.05]
    pts = [(xax((d["rect"][0] + d["rect"][2]) / 2), yax((d["rect"][1] + d["rect"][3]) / 2)) for d in mk]
    return sorted(pts)


# ======================================================================================= panel f
F = region(145, 306, 262, 400)
xax_f = axis_pairs(F, "x", [0, 2], pp.R(170, 377.3, 235, 380))
yax_f = axis_pairs(F, "y", [0, 2], pp.R(166, 310, 169.1, 376))
pts_f = scatter(F, xax_f, yax_f, 0.5)
pp.write_csv(os.path.join(OUT, "edfig9f.csv"), ["gain_conscious_state1", "gain_suppressed_state2"], [[r4(x), r4(y)] for x, y in pts_f],
             [PROV, f"Panel f: scatter of {len(pts_f)} cells (0.5-pt black filled circles; centre of each marker path).",
              f"x axis from tick marks at 0 and 2 (resid {xax_f.resid:.2e}); y axis from tick marks at 0 and 2 (resid {yax_f.resid:.2e}); "
              "precision about 0.001 gain units.",
              "Reference lines in the panel (not data): dashed identity line y = x, dashed vertical line at x = 0, dashed horizontal line at y = 0.",
              "The Fig. 4d legend quotes n = 543 cells; 539 markers are drawn here (markers may coincide or lie outside the axes)."])
pp.render(page, pp.R(145, 306, 262, 400), 300, os.path.join(ORIG_DIR, "edfig9f_orig.png"))

# ======================================================================================= panel g
G = region(5, 400, 125, 486)
xax_g = axis_pairs(G, "x", [0, 3], pp.R(40, 464.7, 110, 468))
yax_g = axis_pairs(G, "y", [0, 3], pp.R(41, 400, 43.7, 466))
pts_g = scatter(G, xax_g, yax_g, 0.5)
pp.write_csv(os.path.join(OUT, "edfig9g.csv"), ["mean_state1_norm", "mean_state2_norm"], [[r4(x), r4(y)] for x, y in pts_g],
             [PROV, f"Panel g: scatter of {len(pts_g)} cells (0.5-pt black filled circles; centre of each marker path).",
              f"x axis from tick marks at 0 and 3 (resid {xax_g.resid:.2e}); y axis from tick marks at 0 and 3 (resid {yax_g.resid:.2e}); "
              "precision about 0.001 units.",
              "Reference lines in the panel (not data): dashed identity line y = x, dashed vertical line at x = 0, dashed horizontal line at y = 0.",
              "The Fig. 4e legend quotes n = 543 cells; 446 markers are drawn here (markers may coincide or lie outside the axes)."])
pp.render(page, pp.R(2, 400, 125, 486), 300, os.path.join(ORIG_DIR, "edfig9g_orig.png"))

# ======================================================================================= panel h (first): decoding vs cells
H1 = region(140, 400, 262, 486)
xax_h1 = axis_pairs(H1, "x", [0, 1000], pp.R(160, 465, 235, 468))
yax_h1 = axis_pairs(H1, "y", [0, 50, 100], pp.R(166, 400, 168.5, 466))
line = [d for d in H1 if d["kind"] == "stroke" and d["n_items"] == 23][0]
band = [d for d in H1 if d["kind"] == "fill" and d["n_items"] == 48][0]
cells = [int(round(xax_h1(x))) for x, y in line["points"]]
acc = [yax_h1(y) for x, y in line["points"]]
benv = {}
for x, y in band["points"]:
    benv.setdefault(int(round(xax_h1(x))), []).append(yax_h1(y))
rows_h1 = [[c, r4(a), r4(min(benv[c])), r4(max(benv[c]))] for c, a in zip(cells, acc)]
pp.write_csv(os.path.join(OUT, "edfig9h_decoding_vs_cells.csv"), ["n_cells", "decoding_accuracy_pct", "band_lo_pct", "band_hi_pct"], rows_h1,
             [PROV, "Panel h (first of two panels labelled h): decoding accuracy (%) for state 1 vs state 2 vs number of cells; black 1-pt line "
              "with a 20 %-opacity grey band (standard deviation across decoding iterations per the Fig. 4f legend).",
              f"x axis from tick marks at 0 and 1000 (resid {xax_h1.resid:.2e}); y axis from tick marks at 0,50,100 (resid {yax_h1.resid:.2e}).",
              "n_cells values are the line vertices snapped to integers (1-10, 20-100 by 10, 200-500 by 100, 1000); precision of accuracy about 0.1 %.",
              "Dashed horizontal reference line at 50 % (chance) is not data."])
pp.render(page, pp.R(140, 400, 262, 486), 300, os.path.join(ORIG_DIR, "edfig9h_decoding_vs_cells_orig.png"))

# ======================================================================================= panel h (second): modulation index scatters
sub = {"all_states": (295, 306, 395, 395), "state1": (420, 306, 520, 395), "state2": (295, 395, 395, 486), "slope_equalized": (420, 395, 520, 486)}
rows_h2 = []
for name, (x0, y0, x1, y1) in sub.items():
    S = region(x0, y0, x1, y1)
    xt = pp.tick_marks(S, "x", max_len=4.0, min_len=1.0)
    yt = pp.tick_marks(S, "y", max_len=4.0, min_len=1.0)
    xt = [t["pos"] for t in xt if t["cy"] > y1 - 25]
    yt = [t["pos"] for t in yt if t["cx"] < x0 + 12]
    assert len(xt) == 3 and len(yt) == 3, (name, xt, yt)
    xax = pp.Axis(list(zip(xt, [-1, 0, 1])))
    yax = pp.Axis(list(zip(sorted(yt, reverse=True), [-1, 0, 1])))
    pts = scatter(S, xax, yax, 0.72)
    print(f"[h2] {name}: {len(pts)} markers; x in {min(p[0] for p in pts):.3f}..{max(p[0] for p in pts):.3f}, "
          f"y in {min(p[1] for p in pts):.3f}..{max(p[1] for p in pts):.3f}")
    rows_h2 += [[name, r4(x), r4(y)] for x, y in pts]
pp.write_csv(os.path.join(OUT, "edfig9h_modulation_index.csv"), ["subpanel", "modulation_index_unambiguous", "modulation_index_binocular"], rows_h2,
             [PROV, "Panel h (second of two panels labelled h): four scatter plots of modulation index during binocular rivalry (y) vs during "
              "unambiguous presentation (x); subpanel = all_states (top left), state1 (top right, orange title), state2 (bottom left, purple "
              "title), slope_equalized (bottom right). 0.72-pt black filled circles; centre of each marker path.",
              "Each subpanel calibrated from its own tick marks at -1, 0, 1 on both axes (linear, resid < 1e-6); precision about 0.001.",
              "Reference lines (not data): dashed identity line (y = x; y = -x in the state2 subpanel), dashed vertical line at x = 0, dashed horizontal line at y = 0.",
              "Marker counts: all_states 2906, state1 2906, state2 2906, slope_equalized 1256 (the Fig. 4g legend quotes n = 2885 cell-stimulus pairs)."])
pp.render(page, pp.R(265, 304, 520, 486), 300, os.path.join(ORIG_DIR, "edfig9h_modulation_index_orig.png"))
print("done")
