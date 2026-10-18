"""edfig2_extract.py -- recover Extended Data Figure 2 (PDF page 42) panels a-c.
Run from this folder: python3 edfig2_extract.py
Writes: edfig2a_r{1-5}_{gt_conscious,recon_average,gt_suppressed}.png, edfig2b.csv, edfig2c.csv,
        edfig2b_orig.png / edfig2c_orig.png (300-dpi crops), edfig2b_overlay.png / edfig2c_overlay.png (QA).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edfig_extract_lib as L  # noqa: E402
from edfig_extract_lib import pp, fitz, fmt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
PAGE = 42
page = pp.open_page(L.PDF, PAGE)

# ---------------------------------------------------------------- panel a: face grid (5 rows x 3 visible columns)
print("== panel a")
ims = pp.images(page, pp.R(40, 40, 285, 316))
cols = {46.3: "gt_conscious", 106.3: "recon_average", 165.8: "gt_suppressed", 225.8: "hidden_col4"}
rows = sorted(set(round(im["bbox"][1]) for im in ims))
print("  image rows (y):", rows, " columns (x):", sorted(set(round(im["bbox"][0], 1) for im in ims)))
hidden = {}
for im in ims:
    x0, y0 = im["bbox"][0], im["bbox"][1]
    col = min(cols, key=lambda c: abs(c - x0))
    r = min(range(len(rows)), key=lambda i: abs(rows[i] - y0)) + 1
    name = cols[col]
    if name == "hidden_col4":
        hidden[r] = im["xref"]
        continue
    out = f"edfig2a_r{r}_{name}.png"
    w, h = pp.extract_image(page, im["xref"], out)
    print(f"  row {r} {name:14s} xref {im['xref']} -> {out} ({w}x{h} px, placed {im['bbox'][2]-x0:.1f} pt wide)")
# the 4th image column is clipped away by the form XObject's clip rectangle (not visible in the figure);
# check whether it merely duplicates the reconstruction column
from PIL import Image  # noqa: E402
for r, xref in sorted(hidden.items()):
    tmp = f"/tmp/claude-1000/hidden_{xref}.png"
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    pp.extract_image(page, xref, tmp)
    A = np.asarray(Image.open(tmp).convert("L"), float)
    B = np.asarray(Image.open(f"edfig2a_r{r}_recon_average.png").convert("L"), float)
    C = np.asarray(Image.open(f"edfig2a_r{r}_gt_suppressed.png").convert("L").resize(A.shape[::-1]), float)
    print(f"  hidden 4th-column image row {r} (xref {xref}): mean|diff| vs recon_average {np.abs(A-B).mean():.2f}, vs gt_suppressed {np.abs(A-C).mean():.2f}")
    os.remove(tmp)
pp.render(page, pp.R(40, 20, 285, 316), 300, "edfig2a_orig.png")

# ---------------------------------------------------------------- panel b: explained variance vs feature #
print("== panel b")
clip_b = pp.R(284, 25, 390, 148)
series_b = [
    dict(name="priming_average", color="#1c0f29", style="solid"),
    dict(name="priming_average_predicting_flashed", color="#1c0f29", style="dashed"),
    dict(name="binocular_conscious_average", color="#808080", style="solid"),
    dict(name="binocular_suppressed_average", color="#808080", style="dashed"),
]
rb = L.extract_panel(page, clip_b, [10, 20, 30, 40, 50], pp.R(280, 141, 390, 146),
                     [-100, -50, 0, 50, 100], pp.R(284, 25, 289.5, 145), series_b, 50)
L.overlay_png(page, clip_b, rb, series_b, "edfig2b_overlay.png")
pp.render(page, pp.R(258, 12, 390, 195), 300, "edfig2b_orig.png")
d = rb["data"]
hdr = ["feature_index", "feature_set", "priming_average", "priming_average_predicting_flashed",
       "priming_average_predicting_flashed_qc", "binocular_conscious_average", "binocular_suppressed_average",
       "binocular_suppressed_average_qc"]
rows = []
for k in range(50):
    rows.append([k + 1, "shape" if k < 20 else "appearance",
                 fmt(d["priming_average"]["y"][k]),
                 fmt(d["priming_average_predicting_flashed"]["y"][k]), d["priming_average_predicting_flashed"]["code"][k],
                 fmt(d["binocular_conscious_average"]["y"][k]),
                 fmt(d["binocular_suppressed_average"]["y"][k]), d["binocular_suppressed_average"]["code"][k]])
comments = [
    "Extended Data Figure 2b (PDF page 42): explained variance of face features (%) predicted from average neural activity, vs feature index.",
    "Source: vector paths in the PDF. Clip region (PDF pt, origin top-left) x 284-390, y 25-148.",
    f"x axis: tick marks at features 10,20,30,40,50 -> Axis slope {rb['xax'].slope:.6f} pt^-1, max residual {rb['xax'].resid:.2e}; vertices of every series sit on x = feature 1..50 (checked against the solid strokes, max dev <0.01 pt).",
    f"y axis: tick marks at -100,-50,0,50,100 % -> slope {rb['yax'].slope:.6f}, max residual {rb['yax'].resid:.2e}. 1 pt = {abs(rb['yax'].slope):.3f} %.",
    "feature_set: features 1-20 are the 20 principal shape features, 21-50 the 30 principal appearance features (bracket labels 'Shape'/'Appearance' in the figure).",
    "priming_average (black solid, #1c0f29) and binocular_conscious_average (grey solid, #808080): stroke path vertices, precision ~0.01 pt (~0.02 %).",
    "priming_average_predicting_flashed (black dashed) and binocular_suppressed_average (grey dashed): the PDF stores these as filled dash outlines (4 pt dash / 4 pt gap, 1 pt wide); the centreline was recovered from the dash polygons (see README). Quality code per value in the *_qc column:",
    "  direct = vertex inside a dash (precision ~0.05 pt = 0.1 %); extrap = vertex in a gap, extrapolated along the adjacent straight segment (~0.1-0.4 pt);",
    "  extrap_offscale = same but the value is outside the -100..100 axis range (the line is clipped by the axes box there; precision ~1-2 pt); interp = both adjacent segments fall in one dash gap, value is the linear interpolation of the neighbours (bound: within ~1.2 pt = 2.2 % of the truth);",
    "  clipped = the line is below -100 % here (not drawn, value unknown: empty); gap = not recoverable (empty).",
    "Values are rounded to 0.01 %.",
]
pp.write_csv("edfig2b.csv", hdr, rows, comments)
print("  wrote edfig2b.csv")

# ---------------------------------------------------------------- panel c: decoding accuracy vs number of faces
print("== panel c")
clip_c = pp.R(409, 25, 512, 147)
series_c = [
    dict(name="priming_average", color="#1c0f29", style="solid", band=True),
    dict(name="priming_average_predicting_flashed", color="#1c0f29", style="dashed", band=True),
    dict(name="binocular_conscious_average", color="#808080", style="solid", band=True),
    dict(name="binocular_suppressed_average", color="#808080", style="dashed", band=True),
]
rc = L.extract_panel(page, clip_c, [0, 20, 40, 60], pp.R(405, 140.5, 512, 145),
                     [0, 20, 40, 60, 80, 100], pp.R(409, 28, 414, 143), series_c, 60)
L.overlay_png(page, clip_c, rc, series_c, "edfig2c_overlay.png")
pp.render(page, pp.R(385, 12, 519, 195), 300, "edfig2c_orig.png")
d = rc["data"]
hdr = ["n_faces"]
for s in series_c:
    hdr += [s["name"], s["name"] + "_lo", s["name"] + "_hi"]
    if s["style"] == "dashed":
        hdr.append(s["name"] + "_qc")
rows = []
band_notes = []
for s in series_c:
    dd = d[s["name"]]
    # absent band (entirely clipped away / zero height at the boundary): lo = hi = line value
    for k in range(60):
        if dd["bflag"][k] == "absent":
            dd["lo"][k] = dd["hi"][k] = dd["y"][k]
    for key, label in (("hi_clipped", "upper edge clipped at 100 (true value above 100)"),
                       ("lo_clipped", "lower edge clipped at 0 (true value below 0)"),
                       ("degenerate", "band has zero height (upper = lower = line)"),
                       ("absent", "band not drawn (entirely at/below the 0 boundary): lo = hi = line value")):
        ks = [k + 1 for k in range(60) if key in dd["bflag"][k]]
        if ks:
            band_notes.append(f"{s['name']} band, n_faces {ks}: {label}.")
for k in range(60):
    row = [k + 1]
    for s in series_c:
        dd = d[s["name"]]
        row += [fmt(dd["y"][k]), fmt(dd["lo"][k]), fmt(dd["hi"][k])]
        if s["style"] == "dashed":
            row.append(dd["code"][k])
    rows.append(row)
comments = [
    "Extended Data Figure 2c (PDF page 42): Euclidean-distance decoding accuracy (%) vs number of faces (target + distractors), from average activity.",
    "Source: vector paths in the PDF. Clip region (PDF pt, origin top-left) x 409-512, y 25-147.",
    f"x axis: tick marks at 0,20,40,60 faces -> slope {rc['xax'].slope:.6f}, max residual {rc['xax'].resid:.2e}; all series have one vertex per n_faces = 1..60 (checked against the solid strokes).",
    f"y axis: tick marks at 0,20,...,100 % -> slope {rc['yax'].slope:.6f}, max residual {rc['yax'].resid:.2e}. 1 pt = {abs(rc['yax'].slope):.3f} %.",
    "Columns: <series> = plotted line; <series>_lo / <series>_hi = lower / upper edge of the shaded band (filled polygon, alpha 0.2; the legend does not say what the band is - the related main-figure panels use SD across sessions/pairs).",
    "priming_average (black solid, #1c0f29), binocular_conscious_average (grey solid, #808080): stroke vertices, precision ~0.01 pt (~0.01 %).",
    "priming_average_predicting_flashed (black dashed), binocular_suppressed_average (grey dashed): the PDF stores these as filled dash outlines (4 pt dash / 4 pt gap). *_qc codes: band_mid = value is the midpoint of the shaded band, which is exactly symmetric about the line (precision ~0.01 pt; used wherever both band edges are unclipped);",
    "  the independent recovery of the dashed line's centreline from the dash polygons agreed with the band midpoints as follows (dash-recovery code: n vertices, max |difference| in pt): " + "; ".join(f"{s['name']}: " + (", ".join(f"{c} ({n}, {m:.2f})" for c, (n, m) in sorted(d[s['name']]['agree'].items())) or "n/a (its band is clipped or absent everywhere)") for s in series_c if s['style'] == 'dashed') + ".",
    "  Other codes (band edge clipped there, value from the dash polygons): direct = vertex inside a dash (~0.05 pt); extrap = extrapolated along the adjacent straight segment (~0.1-0.4 pt); interp = linear interpolation of the neighbours (bound ~1.2 pt); band = band collapses onto the line / lies entirely at the 0 boundary; gap/clipped = empty.",
    "Bands are clipped by the axes box (0..100 %); clipped edges are written as the clip value:",
] + ["  " + n for n in band_notes] + ["Values are rounded to 0.01 %."]
pp.write_csv("edfig2c.csv", hdr, rows, comments)
print("  wrote edfig2c.csv")
print("done")
