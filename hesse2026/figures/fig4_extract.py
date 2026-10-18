"""Extraction script for Figure 4 (PDF page 38) of Hesse et al. 2026 (bioRxiv 10.64898/2026.10.15.759299v1).

Reads the PDF with tools/pdfplot.py and writes the per-panel CSVs in this folder. Run from anywhere:
    python3 fig4_extract.py
It is kept here for provenance; the fig4<p>.py redraw scripts read only the CSVs.

Coordinates in the comments are PDF points, origin top-left of the page (page is 518.76 x 362.88 pt).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "tools"))
import pdfplot as pp  # noqa: E402

PDF = os.path.join(ROOT, "source", "2026.10.15.759299v1.full.pdf")
PAGE_NO = 38
page = pp.open_page(PDF, PAGE_NO)
R = pp.R


def out(name):
    return os.path.join(HERE, name)


def is_marker(d, n_items=4):
    return d["kind"] == "fill" and d["has_curves"] and d["n_items"] == n_items


def centre(d):
    x0, y0, x1, y1 = d["rect"]
    return (x0 + x1) / 2, (y0 + y1) / 2


def dash_path_extent(d):
    """Endpoints (in PDF pt) of a dashed line drawn as a filled path of several dash polygons (each dash is a thin
    rectangle). For horizontal / vertical lines the centre line is used; for diagonals the mid-points of the two end
    dashes' short edges are approximated by the extreme points averaged over the dash thickness."""
    pts = np.array(d["points"])
    x0, y0, x1, y1 = d["rect"]
    w, h = x1 - x0, y1 - y0
    if h < 1.0:      # horizontal
        yc = pts[:, 1].mean()
        return (x0, yc), (x1, yc)
    if w < 1.0:      # vertical
        xc = pts[:, 0].mean()
        return (xc, y0), (xc, y1)
    # diagonal: take the two points with extreme x and average with their dash partner (same subpath) to get the centre
    subs = [np.array(sp[:4]) for sp in d["subpaths"]]
    subs.sort(key=lambda a: a[:, 0].mean())
    first, last = subs[0], subs[-1]
    # the short edge of a dash rectangle: the two points nearest the extreme x
    def short_edge_mid(a, side):
        idx = np.argsort(a[:, 0])[:2] if side == "min" else np.argsort(a[:, 0])[-2:]
        return tuple(a[idx].mean(axis=0))
    return short_edge_mid(first, "min"), short_edge_mid(last, "max")


# --------------------------------------------------------------------------- colour map (panels a, b)
# The colourbar is an embedded 13 x 89 px image (xref 250): a linear blue -> white -> red ramp, pure red
# (255,0,0) in the top row (label "6"), white at the middle row, pure blue (0,0,255) in the bottom row
# (label "-3"). White is therefore at z = 1.5 (the midpoint of -3..6). We invert colours with the continuous
# model  u = (R - B)/255,  z = 1.5 + 4.5 u  (exact for colours on the ramp, mean-z for blended pixels).
Z_MIN, Z_MAX = -3.0, 6.0
Z_MID = (Z_MIN + Z_MAX) / 2


def rgb_to_z(r, g, b):
    """Invert a colour on the blue-white-red ramp to a z-score.

    Along the ramp R - B = 255*u (red half: R = 255, B = 255(1-u); blue half: B = 255, R = 255(1+u)), so
    z = 1.5 + 4.5*(R - B)/255. This is linear in u over the WHOLE ramp, so for a pixel that is a blend of several ramp
    colours (downsampled heatmap) it returns the mean z of the blended values (assuming linear blending of RGB).
    Also returns the RGB distance of the colour from the ramp (0 = exactly on the ramp; on the ramp max(R,B) = 255 and
    G = min(R,B))."""
    r, g, b = float(r), float(g), float(b)
    u = (r - b) / 255
    dist = max(255 - max(r, b), abs(g - min(r, b)))
    return Z_MID + (Z_MAX - Z_MID) * u, dist


def hex_to_rgb(h):
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


# verify the model against the colourbar image
cb_xref = 250
pp.extract_image(page, cb_xref, out("fig4_colourbar_raw.png"))
cb = np.array(Image.open(out("fig4_colourbar_raw.png")).convert("RGB"))
cb_rows = cb[:, cb.shape[1] // 2, :].astype(int)
n_cb = cb_rows.shape[0]
cb_csv = []
worst = 0.0
for i, (r, g, b) in enumerate(cb_rows):
    z_pos = Z_MAX - (Z_MAX - Z_MIN) * i / (n_cb - 1)       # row i -> value if rows span the ends exactly
    z_inv, dist = rgb_to_z(r, g, b)
    worst = max(worst, abs(z_inv - z_pos))
    cb_csv.append([i, int(r), int(g), int(b), round(z_pos, 4), round(z_inv, 4)])
pp.write_csv(out("fig4_colourbar.csv"), ["row_from_top", "R", "G", "B", "z_by_row_position", "z_by_colour_model"], cb_csv, [
    "Figure 4, page 38: colourbar shared by panels a and b (embedded raster image xref 250, 13 x 89 px, placed at",
    "x 119.8-124.5 / 374.4-379.1 pt, y 25.63-57.99 pt). Each row is uniform; labels: '6' at the top, '-3' at the bottom.",
    "z_by_row_position assumes row 0 = 6 and row 88 = -3 (endpoints exactly at the pixel rows); z_by_colour_model is the",
    "inversion of the row's colour with the continuous model used for panels a/b (white = 1.5). Max |difference| = %.3f." % worst,
    "The mapping is only as accurate as the assumption that the colour axis is exactly [-3, 6]: the tick labels are text spans",
    "centred ~1 pt inside the image ends, which is within the label-placement jitter seen on other axes of this figure.",
])
print("colourbar: rows", n_cb, "max |z_model - z_row| =", round(worst, 3))

# --------------------------------------------------------------------------- panel a: four scatter plots
clip_a = R(5, 14, 250, 177)
draws_a = pp.drawings(page, clip_a)
markers_a = [d for d in draws_a if is_marker(d) and abs((d["rect"][2] - d["rect"][0]) - 2.24) < 0.05]
print("panel a scatter markers:", len(markers_a))

# tick marks: x ticks are 0.5 x 1.78 pt fills below the x axis lines (y 159.5 bottom row, 86.68 top row);
# y ticks are 1.78 x 0.5 fills left of the y axes (x 50.66 left column, 176.76 right column).
sub_a = {
    ("conscious", "state1"): dict(x=R(45, 85, 118, 90), y=R(45, 20, 52, 92)),
    ("conscious", "state2"): dict(x=R(45, 158, 118, 163), y=R(45, 95, 52, 162)),
    ("suppressed", "state1"): dict(x=R(170, 85, 245, 90), y=R(170, 20, 178, 92)),
    ("suppressed", "state2"): dict(x=R(170, 158, 245, 163), y=R(170, 95, 178, 162)),
}
rows_a = []
axes_a = {}
for (face, state), reg in sub_a.items():
    xax = pp.axis_from_ticks(draws_a, "x", [-1, 1], region=reg["x"])
    yax = pp.axis_from_ticks(draws_a, "y", [-1, 1], region=reg["y"])
    axes_a[(face, state)] = (xax, yax)
    # plot box: between the two ticks on each axis (markers may stick out by their radius)
    xr = sorted(p for p, v in xax.pairs)
    yr = sorted(p for p, v in yax.pairs)
    sel = [d for d in markers_a if xr[0] - 2 <= centre(d)[0] <= xr[1] + 2 and yr[0] - 2 <= centre(d)[1] <= yr[1] + 2]
    print(f"  {face} {state}: {len(sel)} markers; xax resid {xax.resid:.2g}, yax resid {yax.resid:.2g}; "
          f"x ticks at {[round(p,2) for p in xr]}, y ticks at {[round(p,2) for p in yr]}")
    for k, d in enumerate(sel):
        cx, cy = centre(d)
        r, g, b = hex_to_rgb(pp.hexcolor(d["fill"]))
        z, dist = rgb_to_z(r, g, b)
        sat = "high" if (r, g, b) == (255, 0, 0) else ("low" if (r, g, b) == (0, 0, 255) else "")
        rows_a.append([face, state, k + 1, round(xax(cx), 4), round(yax(cy), 4), round(z, 3), pp.hexcolor(d["fill"]).lstrip("#"), sat])
assert len(rows_a) == 6000, len(rows_a)
pp.write_csv(out("fig4a.csv"),
             ["face", "state", "draw_order", "projection_preferred_axis_au", "projection_orthogonal_axis_au",
              "response_zscored", "marker_colour_rgb_hex", "colour_saturated"], rows_a, [
    "marker_colour_rgb_hex is the marker fill colour as rrggbb (no leading #, so that CSV readers with comment='#' work).",
    "Figure 4a, page 38: four scatter plots (face = conscious | suppressed; state = state1 | state2), 1500 points each.",
    "Points are filled circles (2.24 pt wide, 4 Bezier items) read from the vector paths; x = centre of the marker bbox mapped",
    "with the x axis (tick marks at -1 and 1, the only ticks; residual ~1e-7), y likewise (ticks -1 and 1).",
    "draw_order = order in which the markers appear in the PDF content stream within that subplot (1..1500); it is probably",
    "the stimulus index but that is not verifiable from the PDF.",
    "response_zscored = inversion of the marker fill colour through the colourbar (fig4_colourbar.csv): linear blue-white-red",
    "ramp, blue = -3, white = 1.5, red = 6; z = 1.5 + 4.5*(R - B)/255 (R - B is linear in z along the whole ramp).",
    "Marker colours are quantised in steps of 2/255, i.e. ~0.035 z units; colour_saturated = 'high' for pure red (z >= 6,",
    "true value unknown), 'low' for pure blue (z <= -3). The most common colour #6a6aff (z = -1.13, 648 points) is",
    "presumably the floor value for stimuli with zero spikes.",
    "Position precision: marker centres are exact to the PDF's 2-decimal coordinates (~0.0004 axis units).",
])

# inset: line plot with error bars, x in -1..1, y in 0..9
clip_in = R(118, 70, 172, 128)
draws_in = pp.drawings(page, clip_in, how="inside")
xax_i = pp.axis_from_ticks(draws_in, "x", [-1, 1], region=R(128, 120.5, 170, 123))
yax_i = pp.axis_from_ticks(draws_in, "y", [0, 9], region=R(129, 78, 132, 123))
print("inset axes:", xax_i, yax_i)
rows_in = []
for col, name in [("#fcae34", "state1_conscious"), ("#543379", "state2_suppressed")]:
    line = [d for d in draws_in if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == col and d["n_items"] == 5][0]
    pts = line["points"]
    # vertical error-bar segments: strokes of width 0.5, one point x == point x
    vsegs = [d for d in draws_in if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == col and d["n_items"] == 1
             and abs(d["points"][0][0] - d["points"][1][0]) < 1e-3]
    for k, (px, py) in enumerate(pts):
        ys = [p[1] for d in vsegs if abs(d["points"][0][0] - px) < 1e-3 for p in d["points"]]
        lo_pt, hi_pt = max(ys), min(ys)   # larger PDF y = lower value
        rows_in.append([name, k + 1, round(xax_i(px), 4), round(yax_i(py), 4), round(yax_i(lo_pt), 4), round(yax_i(hi_pt), 4)])
pp.write_csv(out("fig4a_inset.csv"), ["series", "bin_index", "projection_preferred_axis_au", "response", "errorbar_lo", "errorbar_hi"], rows_in, [
    "Figure 4a inset, page 38: response vs projection onto the preferred axis, binned (6 bins), for the conscious face in",
    "state 1 (orange #fcae34) and the suppressed face in state 2 (purple #543379). Values from the vector paths: the series",
    "line (stroke, 6 vertices) gives the points; errorbar_lo/hi are the ends of the vertical error-bar strokes (the legend does",
    "not say whether they are s.e.m. or s.d.). x axis calibrated on the tick marks at -1 and 1 (resid %.1e), y axis on the" % xax_i.resid,
    "ticks at 0 and 9 (resid %.1e). The y axis is labelled 'Response' without units (ticks 0 and 9)." % yax_i.resid,
])

# --------------------------------------------------------------------------- panel b: heatmaps (embedded rasters)
# The four heatmaps are embedded 169 x 169 px RGB images placed in 61.0 x 61.0 pt boxes; each represents 554 cells (rows)
# x 1500 stimuli (columns), so the pixel grid is a ~3.3 x 8.9-fold downsampled version of the data (done by whoever
# exported the figure). get_image_rects reports a second placement of each image directly below the visible one; that copy
# lies outside the Form XObject clip rectangle and is not visible (the strip between the panels renders pure white).
panels_b = {
    "state1_conscious": 248, "state1_suppressed": 246,
    "state2_conscious": 247, "state2_suppressed": 249,
}
for name, xref in panels_b.items():
    png = out(f"fig4b_{name}_raw.png")
    w, h = pp.extract_image(page, xref, png)
    im = np.array(Image.open(png).convert("RGB")).astype(int)
    Z = np.zeros(im.shape[:2]); D = np.zeros(im.shape[:2])
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            Z[i, j], D[i, j] = rgb_to_z(*im[i, j])
    rects = page.get_image_rects(xref)
    vis = min(rects, key=lambda r: r.y0)
    hdr = ["cell_row_px_%d" % 0] if False else [f"stim_col_{j+1}" for j in range(im.shape[1])]
    rows = [[f"{i+1}"] + [f"{v:.2f}" for v in Z[i]] for i in range(im.shape[0])]
    pp.write_csv(out(f"fig4b_{name}.csv"), ["cell_row_px"] + hdr, rows, [
        f"Figure 4b, page 38, '{name.replace('_', ' ')}' heatmap: response (z-scored) matrix recovered PER PIXEL from the embedded",
        f"raster image (PDF xref {xref}, {w} x {h} px RGB, placed at x {vis.x0:.2f}-{vis.x1:.2f}, y {vis.y0:.2f}-{vis.y1:.2f} pt).",
        "The figure states 554 cells x 1500 stimuli, but the embedded image is only 169 x 169 px: rows are ~3.3 cells and",
        "columns ~8.9 stimuli each, averaged by the exporter. Rows top to bottom and columns left to right as displayed",
        "(cells sorted by tuning gain, stimuli sorted by projection onto each cell's preferred axis).",
        "Values = colour inverted through the colourbar (fig4_colourbar.csv; blue -3, white 1.5, red 6; see fig4a.csv comments).",
        "Because pixels are averages of several cells/stimuli, their colours are blends of ramp colours (purple-ish), i.e.",
        f"off the ramp: max RGB distance from the ramp = {D.max():.0f}/255, mean = {D.mean():.1f}/255. The inversion uses",
        "z = 1.5 + 4.5*(R-B)/255, which is linear along the whole ramp and therefore returns the MEAN z of the blended",
        "cells/stimuli in that pixel (assuming the exporter averaged RGB linearly); it cannot recover individual cells.",
        f"Value range in this matrix: {Z.min():.2f} to {Z.max():.2f}; pure-red/blue pixels are saturated (>= 6 / <= -3).",
    ])
    print(f"panel b {name}: {w}x{h}, z range {Z.min():.2f}..{Z.max():.2f}, mean {Z.mean():.2f}, off-ramp dist mean {D.mean():.1f} max {D.max():.0f}")

# --------------------------------------------------------------------------- panel c: three stacked histograms
clip_c = R(5, 178, 152, 272)
draws_c = pp.drawings(page, clip_c, how="intersects")
# x axis (shared, drawn under the bottom subplot): ticks at 0 and 2; y axes: ticks at 0 and 100 per subplot
xax_c = pp.axis_from_ticks(draws_c, "x", [0, 2], region=R(55, 251.3, 105, 253.5))
print("panel c x axis:", xax_c)
subplots_c = [  # (y tick region, series: colour -> name)
    (R(48, 190, 51, 206), {"#fcae34": "state1_conscious", "#ffd28a": "state1_suppressed"}),
    (R(48, 213, 51, 229), {"#543379": "state2_suppressed", "#b56cc7": "state2_conscious"}),
    (R(48, 236, 51, 252), {"#fcae34": "state1_conscious", "#543379": "state2_suppressed"}),
]
rows_c = []
XLIM_C = (-0.5, 2.5)   # axis limits (axis line spans xax_c(50.42) = -0.500 to xax_c(111.67) = 2.512 incl. line caps); bars are clipped at 2.5
for si, (yreg, series) in enumerate(subplots_c):
    yax = pp.axis_from_ticks(draws_c, "y", [0, 100], region=yreg)
    for col, name in series.items():
        # the bars: a fill with opacity 0.30 made of one 4-point subpath per bar, in the subplot's y range
        cands = [d for d in draws_c if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == col
                 and d["raw"].get("fill_opacity", 1) < 0.5 and yreg.y0 - 3 < d["rect"][3] < yreg.y1 + 3]
        assert len(cands) == 1, (si, col, len(cands))
        bars = []
        for sp in cands[0]["subpaths"]:
            xs = [p[0] for p in sp]; ys = [p[1] for p in sp]
            bars.append((xax_c(min(xs)), xax_c(max(xs)), yax(min(ys)), yax(max(ys))))
        bars.sort()
        # bin width of this series = smallest bar width not touching the axis ends (MATLAB merges adjacent bars of equal
        # height into one rectangle, and clips the first/last bin at the axis limits)
        inner = [hi - lo for lo, hi, c, b in bars if lo > XLIM_C[0] + 0.02 and hi < XLIM_C[1] - 0.02]
        w = round(min(inner), 2)
        for lo, hi, cnt, base in bars:
            at_left = lo < XLIM_C[0] + 0.02
            at_right = hi > XLIM_C[1] - 0.02
            n = max(1, int(round((hi - lo) / w - 0.49 + 0.5)))        # number of whole bins in this rectangle
            if at_left and not at_right:
                n = int(np.ceil((hi - lo) / w - 1e-6)); edges = [round(hi - (n - k) * w, 4) for k in range(n + 1)]
            elif at_right:
                n = int(np.ceil((hi - lo) / w - 1e-6)); edges = [round(lo + k * w, 4) for k in range(n + 1)]
            else:
                n = int(round((hi - lo) / w)); edges = [round(lo + k * w, 4) for k in range(n + 1)]
            for k in range(n):
                clipped = (at_left and k == 0 and edges[0] < XLIM_C[0] - 0.01) or (at_right and k == n - 1 and edges[-1] > XLIM_C[1] + 0.01)
                rows_c.append([si + 1, name, col.lstrip("#"), edges[k], edges[k + 1], round(cnt, 3), int(round(cnt)), round(base, 3),
                               int(clipped), round(lo, 4), round(hi, 4)])
    print(f"  subplot {si+1}: y axis {yax}; bins: " + ", ".join(f"{n}={sum(1 for r in rows_c if r[0]==si+1 and r[1]==n)}" for n in series.values()))
pp.write_csv(out("fig4c.csv"), ["subplot", "series", "colour_rgb_hex", "gain_bin_lo", "gain_bin_hi", "count_measured", "count_rounded",
                                "bar_base", "bin_clipped_at_axis", "drawn_rect_lo", "drawn_rect_hi"], rows_c, [
    "Figure 4c, page 38: histograms of single-cell tuning gain, three stacked subplots (top to bottom: subplot 1 = state 1",
    "conscious (#fcae34) with state 1 suppressed (#ffd28a); subplot 2 = state 2 suppressed (#543379) with state 2 conscious",
    "(#b56cc7); subplot 3 = state 1 conscious vs state 2 suppressed). Each series is drawn as translucent bars (fill opacity",
    "0.30) plus an opaque stair-step outline of the same colour; the bars give bin edges (x) and counts (y). Shared x axis",
    "calibrated on the tick marks at 0 and 2 (resid %.1e); each subplot's y axis on its ticks at 0 and 100 (resid ~1e-7)." % xax_c.resid,
    "MATLAB merged adjacent bars of equal height into one rectangle (drawn_rect_lo/hi); these were split into bins of the",
    "series' bin width (0.2 for state1_conscious, state1_suppressed and state2_suppressed; 0.1 for state2_conscious).",
    "Bins at the axis ends are clipped by the axis limits -0.5..2.5 (bin_clipped_at_axis = 1): their drawn rectangle is",
    "narrower than a bin and the listed edge beyond the limit is inferred from the bin width.",
    "count_measured is the bar top mapped through the y axis; count_rounded the nearest integer (all within 0.01 of an",
    "integer). bar_base should be 0. Empty bins are not drawn and are absent here. colour_rgb_hex is rrggbb without #.",
])
# sanity: integer-ness of counts
dev = max(abs(r[5] - r[6]) for r in rows_c)
print("panel c: max deviation of counts from integers:", round(dev, 3))

# --------------------------------------------------------------------------- panels d, e, g: dot scatters
def scatter_panel(clip, xvals, xreg, yvals, yreg, marker_w, tag):
    draws = pp.drawings(page, clip, how="intersects")
    xax = pp.axis_from_ticks(draws, "x", xvals, region=xreg)
    yax = pp.axis_from_ticks(draws, "y", yvals, region=yreg)
    xr = sorted(p for p, v in xax.pairs); yr = sorted(p for p, v in yax.pairs)
    mk = [d for d in draws if is_marker(d) and abs((d["rect"][2] - d["rect"][0]) - marker_w) < 0.05]
    pts = [(xax(centre(d)[0]), yax(centre(d)[1])) for d in mk]
    dashes = [d for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#000000" and d["n_items"] in (32, 44)]
    lines = []
    for d in dashes:
        (ax0, ay0), (ax1, ay1) = dash_path_extent(d)
        lines.append((d["n_items"], round(xax(ax0), 3), round(yax(ay0), 3), round(xax(ax1), 3), round(yax(ay1), 3)))
    print(f"{tag}: {len(mk)} markers; xax {xax}; yax {yax}; dashed lines (items, x0,y0,x1,y1): {lines}")
    return pts, xax, yax, lines, mk

# d: gain suppressed state 2 vs gain conscious state 1
pts_d, xax_d, yax_d, lines_d, mk_d = scatter_panel(R(150, 180, 250, 272), [0, 2], R(180, 251, 235, 253.5),
                                                   [0, 2], R(174, 195, 177.5, 245), 0.5, "panel d")
pp.write_csv(out("fig4d.csv"), ["draw_order", "gain_conscious_state1", "gain_suppressed_state2"],
             [[k + 1, round(x, 4), round(y, 4)] for k, (x, y) in enumerate(pts_d)], [
    "Figure 4d, page 38: one dot per cell, x = tuning gain for the conscious face in state 1, y = gain for the suppressed face",
    "in state 2. Dots are 0.5-pt filled circles (vector paths); %d dots found (the legend says n = 543 cells; the missing" % len(pts_d),
    "12 are presumably outside the plotted range -0.5..2.5 and were culled on export, or exact duplicates; not recoverable).",
    "x axis calibrated on tick marks at 0 and 2 (resid %.1e), y axis on ticks at 0 and 2 (resid %.1e)." % (xax_d.resid, yax_d.resid),
    "Reference lines drawn in the panel (dashed black): identity x = y from (%.2f, %.2f) to (%.2f, %.2f); x = 0; y = 0." % tuple(lines_d[0][1:]) if lines_d[0][0] == 44 else "",
    "Precision ~0.001 gain units (marker centre from PDF coordinates).",
])

# e: mean state 2 vs mean state 1 (norm.)
pts_e, xax_e, yax_e, lines_e, mk_e = scatter_panel(R(5, 266, 150, 362), [0, 3], R(45, 338.4, 115, 341),
                                                   [0, 3], R(48, 276, 51, 340), 0.5, "panel e")
pp.write_csv(out("fig4e.csv"), ["draw_order", "mean_response_state1_norm", "mean_response_state2_norm"],
             [[k + 1, round(x, 4), round(y, 4)] for k, (x, y) in enumerate(pts_e)], [
    "Figure 4e, page 38: one dot per cell, x = mean response across stimuli in state 1 (normalised), y = same in state 2.",
    "Dots are 0.5-pt filled circles (vector paths); %d dots found (legend: n = 543 cells; 12 presumably outside the plotted" % len(pts_e),
    "range 0..3 and culled on export, or exact duplicates). x axis: ticks at 0 and 3 (resid %.1e); y axis: ticks at 0 and 3" % xax_e.resid,
    "(resid %.1e). Dashed identity line drawn from (%.2f, %.2f) to (%.2f, %.2f)." % ((yax_e.resid,) + tuple(lines_e[0][1:])),
    "Precision ~0.001 units.",
])

# g: four scatters of modulation index binocular vs unambiguous
sub_g = [
    ("all_states", R(262, 178, 390, 265), R(300, 251.3, 372, 253.5), R(303, 186, 306, 254)),
    ("state1", R(390, 178, 518, 265), R(428, 251.3, 498, 253.5), R(430, 186, 432.6, 254)),
    ("state2", R(262, 265, 390, 362), R(300, 338.5, 372, 341), R(303, 274, 306, 341)),
    ("slope_equalized", R(390, 265, 518, 362), R(428, 338.5, 498, 341), R(430, 274, 432.6, 341)),
]
rows_g = []
lines_g = {}
for name, clip, xreg, yreg in sub_g:
    # dots are 0.72 pt wide (a few 0.71 from rounding); the 0.05 tolerance in scatter_panel catches both
    pts, xax, yax, lines, mk = scatter_panel(clip, [-1, 0, 1], xreg, [-1, 0, 1], yreg, 0.72, f"panel g {name}")
    lines_g[name] = lines
    for k, (x, y) in enumerate(pts):
        rows_g.append([name, k + 1, round(x, 4), round(y, 4)])
pp.write_csv(out("fig4g.csv"), ["subplot", "draw_order", "modulation_index_unambiguous", "modulation_index_binocular"], rows_g, [
    "Figure 4g, page 38: four scatter plots (subplot = all_states | state1 | state2 | slope_equalized), one dot per",
    "cell-stimulus pair: x = modulation index for unambiguous (monocular) presentation, y = modulation index for binocular",
    "presentation. Dots are ~0.72-pt filled circles (vector paths). Counts per subplot: " +
    ", ".join(f"{n}={sum(1 for r in rows_g if r[0]==n)}" for n, *_ in sub_g) + " (legend: n = 2885 pairs each;",
    "the missing dots are presumably outside the -1..1 plotted range, culled on export, or exactly overlapping).",
    "Axes calibrated on tick marks at -1, 0, 1 (residuals < 1e-6). Precision ~0.001.",
    "Dashed reference lines per subplot (from the dashed paths): x = 0, y = 0, and a diagonal: " +
    "; ".join(f"{n}: ({l[0][1]},{l[0][2]})-({l[0][3]},{l[0][4]})" for n, l in ((n, [x for x in lines_g[n] if x[0] == 44]) for n, *_ in sub_g)) + ".",
])

# --------------------------------------------------------------------------- panel f: decoding accuracy vs number of cells
clip_f = R(150, 266, 250, 362)
draws_f = pp.drawings(page, clip_f, how="intersects")
xax_f = pp.axis_from_ticks(draws_f, "x", [0, 1000], region=R(170, 338.8, 245, 341))
yax_f = pp.axis_from_ticks(draws_f, "y", [0, 50, 100], region=R(174.5, 276, 177.5, 340))
print("panel f axes:", xax_f, yax_f)
line_f = [d for d in draws_f if d["kind"] == "stroke" and d["width"] == 1.0][0]
band_f = [d for d in draws_f if d["kind"] == "fill" and d["n_items"] == 48][0]
lx, ly = pp.polyline_to_xy(line_f["points"], xax_f, yax_f)
bx, lo, hi = pp.band_envelope([(xax_f(x), yax_f(y)) for x, y in band_f["points"]], 2)
dash_f = [d for d in draws_f if d["kind"] == "fill" and d["n_items"] == 32][0]
(dx0, dy0), (dx1, dy1) = dash_path_extent(dash_f)
print("panel f: line pts", len(lx), "band xs", len(bx), "dashed line y =", round(yax_f(dy0), 2), round(yax_f(dy1), 2))
rows_f = []
for k, (x, y) in enumerate(zip(lx, ly)):
    j = min(range(len(bx)), key=lambda j: abs(bx[j] - x))
    assert abs(bx[j] - x) < 0.5, (x, bx[j])
    rows_f.append([round(x, 2), round(y, 3), round(lo[j], 3), round(hi[j], 3)])
pp.write_csv(out("fig4f.csv"), ["n_cells", "decoding_accuracy_pct", "band_lo_pct", "band_hi_pct"], rows_f, [
    "Figure 4f, page 38: decoding accuracy (state 1 vs state 2, %) as a function of the number of cells. Mean = black",
    "stroke (1 pt, %d vertices); band_lo/hi = lower/upper edge of the grey band (black fill, opacity 0.2) at the same x" % len(lx),
    "(legend: s.d. across 100 decoding iterations). x axis: ticks at 0 and 1000 (resid %.1e); y axis: ticks at 0, 50, 100" % xax_f.resid,
    "(resid %.1e). Dashed chance line at y = %.1f%%." % (yax_f.resid, yax_f(dy0)),
])
print("done")
