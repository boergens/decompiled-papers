"""Extract Figure 5C of Wildenberg et al. 2023 (bioRxiv 2023.10.23.563679v1, PDF p. 23): dot plot of tracing
accuracy (%) against computational kerf size (slices). Tier 2: the plot is drawn as vector paths in the PDF.

    python3 -I fig5c_extract.py   -> fig5c.csv (+ ../work/fig5c_overlay.png for checking)

Calibration: y from the four dotted grid lines, which sit at the labelled ticks 100, 80, 60, 40 (text spans
in the PDF); x from the centres of the x tick labels "0", "50", "100" (no tick marks are drawn). The three
white-filled circle markers (radius 1.74 pt) and the orange polyline joining them are the data.
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
PAGE = 23
CLIP = (93, 215, 325, 320)          # panel C box in PDF points (origin top left)

dump = os.path.join(WORK, "vd_fig5c.json")
subprocess.run([sys.executable, "-I", "-B", os.path.join(TOOLS, "vector_dump.py"), PDF, str(PAGE),
                *map(str, CLIP), "--out", dump], check=True)
d = json.load(open(dump))

# --- y axis: dotted grid lines (grey, 4 horizontal segments in one path) at 100, 80, 60, 40
grid = [p for p in d["paths"] if p["stroke"] and abs(p["stroke"][0] - 0.851) < 0.01]
assert len(grid) == 1, len(grid)
ys = sorted(it[1][1] for it in grid[0]["items"])            # top to bottom
yvals = [100, 80, 60, 40]
A = np.vstack([ys, np.ones(4)]).T
(ky, by), res, *_ = np.linalg.lstsq(A, yvals, rcond=None)
yfit = ky * np.array(ys) + by
print("y grid lines (pt):", [round(v, 3) for v in ys], "fit residuals:", np.round(np.array(yvals) - yfit, 4))

# --- x axis: centres of the tick labels 0, 50, 100 (bottom row of labels, y ~ 233-308 bbox because rotated matrix)
labels = {}
for t in d["text"]:
    tx = t["text"].strip()
    if tx in ("0", "50", "100") and t["bbox"][1] > 225:
        labels[int(tx)] = (t["bbox"][0] + t["bbox"][2]) / 2
assert sorted(labels) == [0, 50, 100], labels
xs = [labels[k] for k in (0, 50, 100)]
A = np.vstack([xs, np.ones(3)]).T
(kx, bx), *_ = np.linalg.lstsq(A, [0, 50, 100], rcond=None)
print("x label centres (pt):", [round(v, 2) for v in xs], "fit residuals:", np.round(np.array([0, 50, 100]) - (kx * np.array(xs) + bx), 3))

# --- markers: white-filled circles (4 Bezier arcs each) and the orange line
markers = []
for p in d["paths"]:
    if p["fill"] == [1.0, 1.0, 1.0] and p["stroke"] == [0.0, 0.0, 0.0] and len(p["items"]) == 4 and all(it[0] == "c" for it in p["items"]):
        pts = np.array([q for it in p["items"] for q in it[1:]])
        cx, cy = (pts[:, 0].min() + pts[:, 0].max()) / 2, (pts[:, 1].min() + pts[:, 1].max()) / 2
        markers.append((cx, cy, (pts[:, 0].max() - pts[:, 0].min()) / 2))
markers.sort()
assert len(markers) == 3, markers
line = [p for p in d["paths"] if p["stroke"] and abs(p["stroke"][0] - 0.929) < 0.01]
assert len(line) == 1
verts = [line[0]["items"][0][1]] + [it[2] for it in line[0]["items"]]
print("markers (pt):", [(round(x, 3), round(y, 3), round(r, 2)) for x, y, r in markers])
print("line vertices (pt):", [(round(x, 3), round(y, 3)) for x, y in verts])

annot = {0: "", 50: "(97)", 100: "(60)"}       # the numbers printed next to the 2nd and 3rd marker
rows = []
for (mx, my, r), (lx, ly) in zip(markers, verts):
    x = kx * mx + bx
    y = ky * my + by
    xl = kx * lx + bx
    yl = ky * ly + by
    label = min((0, 50, 100), key=lambda v: abs(v - x))
    rows.append([label, {0: "0", 50: "1.5", 100: "3"}[label], round(x, 2), round(y, 2), round(xl, 2), round(yl, 2), annot[label]])

with open(os.path.join(HERE, "fig5c.csv"), "w", newline="") as f:
    for c in [
        "Wildenberg et al. 2023, bioRxiv 2023.10.23.563679v1, Figure 5C (PDF p. 23): accuracy of human tracing of myelinated",
        "  axons across a computational kerf, against kerf size. One row per plotted marker (3 markers joined by a line).",
        "Columns: kerf_slices_label = the x tick label the marker belongs to (0, 50, 100 slices); kerf_um_label = the",
        "  second row of x labels printed under 50 and 100 ('1.5 um', '3 um'; 30 nm voxels); kerf_slices = marker centre",
        "  mapped through the x calibration; accuracy_pct = marker centre mapped through the y calibration;",
        "  line_x_slices, line_y_pct = the vertex of the orange polyline at that marker (the line joins the marker centres);",
        "  printed_annotation = the number printed above the marker in the figure ('(97)', '(60)').",
        "Provenance: tier 2, vector paths of the PDF (fig5c_extract.py). y calibrated on the four dotted grid lines, which",
        f"  are at the labelled ticks 100/80/60/40 (the grid lines are not exactly equidistant: fit residuals up to {max(abs(np.array(yvals) - yfit)):.2f} %);",
        "  x calibrated on the centres of the tick",
        "  labels 0/50/100 (there are no tick marks; residuals < 0.3 slices).",
        "Uncertainty: y about 0.3 % (the grid-line residual; the coordinate precision itself is 0.01 pt = 0.01 %); x about 1 slice (label centring).",
        "The marker y values are 99.7, 96.8 and 60.1 %: the paper reports 97 % and 60 % (and 100 % for the full stack).",
    ]:
        f.write("# " + c + "\n")
    w = csv.writer(f)
    w.writerow(["kerf_slices_label", "kerf_um_label", "kerf_slices", "accuracy_pct", "line_x_slices", "line_y_pct", "printed_annotation"])
    w.writerows(rows)
print("rows:", rows)

# --- overlay on a 4x render of the panel
import pymupdf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
page = pymupdf.open(PDF)[PAGE - 1]
S = 4
pix = page.get_pixmap(matrix=pymupdf.Matrix(S, S), clip=pymupdf.Rect(*CLIP))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
for (mx, my, r), row in zip(markers, rows):
    # data value -> back to pt through the inverse calibration, drawn as a red cross
    px = ((row[2] - bx) / kx - CLIP[0]) * S
    py = ((row[3] - by) / ky - CLIP[1]) * S
    dr.line([px - 8, py, px + 8, py], fill=(255, 0, 0), width=1)
    dr.line([px, py - 8, px, py + 8], fill=(255, 0, 0), width=1)
for v in (100, 80, 60, 40):
    py = ((v - by) / ky - CLIP[1]) * S
    dr.line([0, py, 20, py], fill=(0, 0, 255), width=1)
for v in (0, 50, 100):
    px = ((v - bx) / kx - CLIP[0]) * S
    dr.line([px, im.height - 20, px, im.height], fill=(0, 0, 255), width=1)
im.save(os.path.join(WORK, "fig5c_overlay.png"))
print("wrote fig5c.csv and work/fig5c_overlay.png")
