"""Extract Supplementary Figure 6 of Wildenberg et al. 2023 (bioRxiv 2023.10.23.563679v1, PDF p. 37): number of
myelinated axons traced (log scale) against distance (mm), for success rates 0.50/0.75/0.90/0.99 and pillar
diameters 1 mm (solid) and 2 mm (dotted). Tier 2: the plot is pure vector (no raster image on the page).

    python3 -I sfig6_extract.py   -> sfig6.csv (+ ../work/sfig6_overlay.png for checking)

The tick labels are glyph outlines (no text spans), so the axes are calibrated from the tick marks:
x: 10 major ticks at 0..90 mm (31.62 pt apart) with the axis end at 100 mm; y: major ticks at 10^1..10^4
(51.57 pt per decade) and the x axis line at 10^0, checked against the log minor ticks (2..9 x 10^n).
The series are stroked polylines: 4 solid (dash pattern none) and 4 dotted (dash pattern [1.85 1.85] or
[4.03 4.03]); their vertices are taken as they are. Values below 10^0 are clipped by the axes box in the PDF.
"""
import csv
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = "/home/admin/ephemeral/oct_17_papers/tools"
PDF = os.path.join(HERE, "../source/wildenberg2023.pdf")
WORK = os.path.join(HERE, "../work")
PAGE = 37
CLIP = (100, 185, 520, 545)

dump = os.path.join(WORK, "vd_sfig6.json")
subprocess.run([sys.executable, "-I", "-B", os.path.join(TOOLS, "vector_dump.py"), PDF, str(PAGE),
                *map(str, CLIP), "--out", dump], check=True)
d = json.load(open(dump))
paths = d["paths"]


def seg(p):
    return p["items"][0]


# --- axes: thin black strokes (width 0.50)
thin = [p for p in paths if p["stroke"] == [0.0, 0.0, 0.0] and p["width"] and abs(p["width"] - 0.5007) < 0.01 and len(p["items"]) == 1 and p["items"][0][0] == "l"]
horiz = [p for p in thin if abs(seg(p)[1][1] - seg(p)[2][1]) < 0.01]
vert = [p for p in thin if abs(seg(p)[1][0] - seg(p)[2][0]) < 0.01]
xaxis = max(horiz, key=lambda p: abs(seg(p)[1][0] - seg(p)[2][0]))
yaxis = max(vert, key=lambda p: abs(seg(p)[1][1] - seg(p)[2][1]))
x_axis_y = seg(xaxis)[1][1]
x0_pt, x1_pt = sorted((seg(xaxis)[1][0], seg(xaxis)[2][0]))
y_axis_x = seg(yaxis)[1][0]
ytop_pt, ybot_pt = sorted((seg(yaxis)[1][1], seg(yaxis)[2][1]))
print(f"x axis: y={x_axis_y:.3f}, from x={x0_pt:.3f} to {x1_pt:.3f};  y axis: x={y_axis_x:.3f}, from y={ytop_pt:.3f} to {ybot_pt:.3f}")

# x major ticks: short vertical strokes (3.1 pt) just above the x axis
xt = sorted(seg(p)[1][0] for p in vert if min(abs(seg(p)[1][1] - x_axis_y), abs(seg(p)[2][1] - x_axis_y)) < 0.1 and 2.5 < abs(seg(p)[1][1] - seg(p)[2][1]) < 5)
print("x ticks (pt):", [round(v, 2) for v in xt], "n =", len(xt))
assert len(xt) == 10
xvals = list(range(0, 100, 10))
(kx, bx), *_ = np.linalg.lstsq(np.vstack([xt, np.ones(10)]).T, xvals, rcond=None)
print("x fit residuals (mm):", np.round(np.array(xvals) - (kx * np.array(xt) + bx), 4), " axis end ->", round(kx * x1_pt + bx, 3), "mm")

# y major ticks: 3.2 pt long horizontal strokes to the right of the y axis (minor ticks are 1.6 pt)
yt = sorted(seg(p)[1][1] for p in horiz if min(abs(seg(p)[1][0] - y_axis_x), abs(seg(p)[2][0] - y_axis_x)) < 0.1 and 2.5 < abs(seg(p)[2][0] - seg(p)[1][0]) < 5 and seg(p)[1][1] < ybot_pt - 1)
print("y major ticks (pt):", [round(v, 2) for v in yt], "n =", len(yt))
assert len(yt) == 4
yvals = [4, 3, 2, 1]                                       # log10 N, top to bottom
pts = yt + [ybot_pt]
vals = yvals + [0]
(ky, by), *_ = np.linalg.lstsq(np.vstack([pts, np.ones(5)]).T, vals, rcond=None)
print("y fit residuals (log10):", np.round(np.array(vals) - (ky * np.array(pts) + by), 4))
# check the minor ticks (2..9 x 10^n) against the fit
minor = sorted(seg(p)[1][1] for p in horiz if min(abs(seg(p)[1][0] - y_axis_x), abs(seg(p)[2][0] - y_axis_x)) < 0.1 and 1 < abs(seg(p)[2][0] - seg(p)[1][0]) < 2.5 and seg(p)[1][1] < ybot_pt - 1)
mres = []
for y in minor:
    v = ky * y + by
    frac = v - np.floor(v)
    cand = np.log10(np.arange(1, 11))   # decade ticks are drawn twice (major and minor length)
    mres.append(min(abs(frac - cand)))
print("y minor ticks: n =", len(minor), " max |residual| (log10) =", round(max(mres), 4))
print("axes box top (pt)", round(ytop_pt, 2), "-> log10 N =", round(ky * ytop_pt + by, 3))

# --- series
COLORS = {"0.99": [0.0784, 0.4392, 1.0], "0.90": [0.8785, 0.1294, 0.0], "0.75": [0.4706, 1.0, 0.0], "0.50": [0.3411, 0.0, 0.9215]}


def colour_name(c):
    for k, v in COLORS.items():
        if c and max(abs(a - b) for a, b in zip(c, v)) < 0.01:
            return k
    return None


rows = []
overlay = []
for p in paths:
    name = colour_name(p["stroke"])
    if not name or len(p["items"]) < 5:
        continue                                   # legend swatches are fills; legend line samples have 1 item
    dashed = bool(p.get("dashes") and p["dashes"] not in ("[] 0", "", None))
    diam = "2 mm" if dashed else "1 mm"
    verts = [p["items"][0][1]] + [it[2] for it in p["items"]]
    for vx, vy in verts:
        x = kx * vx + bx
        logn = ky * vy + by
        clipped = "clipped" if vy > ybot_pt - 0.05 else ""
        rows.append([name, diam, "dotted" if dashed else "solid", round(x, 3), round(logn, 4), round(10 ** logn, 1), clipped])
        overlay.append((vx, vy, name, dashed))
    print(f"series success {name}, pillar {diam} ({'dotted' if dashed else 'solid'}): {len(verts)} vertices, "
          f"x {kx * verts[0][0] + bx:.2f}..{kx * verts[-1][0] + bx:.2f} mm, log10 N {ky * verts[0][1] + by:.3f}..{ky * verts[-1][1] + by:.3f}")

rows.sort(key=lambda r: (-float(r[0]), r[1], r[3]))
with open(os.path.join(HERE, "sfig6.csv"), "w", newline="") as f:
    for c in [
        "Wildenberg et al. 2023, bioRxiv 2023.10.23.563679v1, Supplementary Figure 6 (PDF p. 37): estimated number of",
        "  myelinated axons traced (log10 scale) against distance (mm), for four success rates per pillar crossing and two",
        "  pillar diameters. One row per vertex of the plotted polylines (the paper's own line vertices).",
        "Columns: success_rate = legend value (0.50 purple, 0.75 green, 0.90 red-orange, 0.99 blue); pillar_diameter_mm = 1 mm",
        "  (solid line) or 2 mm (dotted line); line_style; distance_mm = x; log10_n_traced = y in log10 units;",
        "  n_traced = 10**log10_n_traced; flag 'clipped' where the vertex lies on the bottom of the axes box (10^0):",
        "  there the PDF line is cut by the axes and the true value is below 1.",
        "Provenance: tier 2, vector paths of the PDF (sfig6_extract.py). x calibrated on the 10 major tick marks at",
        f"  0..90 mm (residuals < {max(abs(np.array(xvals) - (kx * np.array(xt) + bx))):.3f} mm; the axis end maps to {kx * x1_pt + bx:.2f} mm);",
        f"  y on the 4 major ticks 10^1..10^4 and the x axis line at 10^0 (residuals < {max(abs(np.array(vals) - (ky * np.array(pts) + by))):.4f} decades),",
        f"  checked against {len(minor)} minor ticks (max residual {max(mres):.4f} decades). The tick labels are glyph outlines.",
        "Uncertainty: about 0.003 mm in x and 0.0002 decades in y (0.01 pt coordinate precision); exact up to the PDF's precision.",
        "The y axis has no label with units: 'No. MAs traced'. The axes box top is at log10 N = %.3f (N about %.0f)." % (ky * ytop_pt + by, 10 ** (ky * ytop_pt + by)),
    ]:
        f.write("# " + c + "\n")
    w = csv.writer(f)
    w.writerow(["success_rate", "pillar_diameter_mm", "line_style", "distance_mm", "log10_n_traced", "n_traced", "flag"])
    for r in rows:
        w.writerow([r[0], r[1].split()[0], r[2], r[3], r[4], r[5], r[6]])
print("wrote sfig6.csv:", len(rows), "rows")

# --- overlay: the vertices (mapped back through the calibration) on a 4x render
import pymupdf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
page = pymupdf.open(PDF)[PAGE - 1]
S = 4
pix = page.get_pixmap(matrix=pymupdf.Matrix(S, S), clip=pymupdf.Rect(*CLIP))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
for r in rows:
    px = ((r[3] - bx) / kx - CLIP[0]) * S
    py = ((r[4] - by) / ky - CLIP[1]) * S
    dr.ellipse([px - 2, py - 2, px + 2, py + 2], outline=(0, 0, 0) if r[2] == "solid" else (255, 0, 255))
for v in range(0, 101, 10):
    px = ((v - bx) / kx - CLIP[0]) * S
    dr.line([px, im.height - 60, px, im.height - 40], fill=(255, 0, 0), width=1)
for v in range(0, 5):
    py = ((v - by) / ky - CLIP[1]) * S
    dr.line([0, py, 30, py], fill=(255, 0, 0), width=1)
im.save(os.path.join(WORK, "sfig6_overlay.png"))
print("wrote work/sfig6_overlay.png")
