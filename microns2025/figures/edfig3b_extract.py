#!/usr/bin/env python3
"""Extended Data Fig. 3B (p. 26): soma centres of multi-soma IDs as of 9/30/20 (left, n = 17,753) and 4/4/23
(right, n = 98), y vs x, colour = z (depth). Vector paths -> edfig3b_left.csv, edfig3b_right.csv.

Each soma centre is a filled circle path (4 Bezier items, 1.65 pt wide); the centre is its bbox centre.
Axes (plotly; tick labels are outlined glyphs, read from the render): x gridlines at 200, 400, ..., 1600 um,
y gridlines at 200, 400, ..., 1200 um; calibrated on the gridline positions (exact).
Colour: the colour bar (right panel only; an 11 x 126 px inline raster, i.e. ~1 px per pt) is sampled at 8x render
along its centre; tick labels 600 ... 1100 (glyph centres at 447.83 ... 325.69 pt) calibrate z. Each marker's fill colour
is matched to the nearest colour-bar colour (RGB distance, reported). The left panel has no colour bar of its own;
the same colour scale is assumed (same plotting code, same colour range of the markers)."""
import sys
from pathlib import Path

import numpy as np
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[25]
# colour bar LUT
z8 = 8
pix = page.get_pixmap(clip=pymupdf.Rect(536.75, 324.22, 546.64, 449.23), matrix=pymupdf.Matrix(z8, z8))
a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(float)
col = a[3:-3, a.shape[1] // 2 - 4:a.shape[1] // 2 + 4].mean(1)
ypt = 324.22 + (np.arange(3, a.shape[0] - 3) + 0.5) / z8
Z = mc.LinAxis([(447.83, 600), (423.41, 700), (398.99, 800), (374.55, 900), (350.12, 1000), (325.69, 1100)])
zlut = Z(ypt)

for side, clip, xg, yg, n_expected in [
        ("left", (41, 272, 300, 470), [75.39, 101.22, 127.06, 152.89, 178.72, 204.55, 230.38, 256.22],
         [451.84, 427.64, 403.44, 379.24, 355.04, 330.84], 17753),
        ("right", (300, 272, 535, 470), [330.48, 355.35, 380.22, 405.09, 429.96, 454.82, 479.69, 504.56],
         [451.62, 427.5, 403.37, 379.24, 355.11, 330.99], 98)]:
    X = mc.LinAxis(list(zip(xg, range(200, 1601, 200))))
    Y = mc.LinAxis(list(zip(yg, range(200, 1201, 200))))
    dr = pp.drawings(page, pp.R(*clip), how="inside")
    m = [d for d in dr if d["kind"] == "fill" and d["n_items"] == 4 and d["has_curves"] and d["rect"][2] - d["rect"][0] < 2]
    assert len(m) == n_expected, len(m)
    rows, qa = [], []
    for d in m:
        x0, y0, x1, y1 = d["rect"]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rgb = np.array(d["fill"][:3]) * 255
        dist = np.sqrt(((col - rgb) ** 2).sum(1))
        i = int(dist.argmin())
        rows.append([f"{X(cx):.2f}", f"{Y(cy):.2f}", f"{zlut[i]:.0f}", f"{dist[i]:.1f}", pp.hexcolor(d["fill"])])
        qa.append((cx, cy))
    title = "Soma Centers of Multi-Soma IDs as of 9/30/20" if side == "left" else "Soma Centers of Multi-Soma IDs as of 4/4/23"
    mc.write_csv(Path(__file__).with_name(f"edfig3b_{side}.csv"), [
        f"Extended Data Fig. 3B {side} panel (p. 26 of microns2025.pdf): '{title}', n = {len(rows)} markers.",
        "Provenance: tier 2, vector paths (marker centres exact to ~0.01 pt = ~0.08 um); z from the marker colour via the",
        "colour bar: tier 3 (colour bar is a ~1 px/pt raster; z resolution ~4 um, plus label-centre calibration +-1 um).",
        "Columns: x_um, y_um (plot axes 'x (um)', 'y (um)'; y increases downwards in the plot = pia (top) to white matter);",
        "z_um (depth from the colour, nearest colour-bar entry); colour_dist (RGB distance of the marker fill to that entry, 0-441);",
        "fill (marker colour as drawn). Rows in drawing order.",
        "The left panel has no colour bar; the right panel's colour bar (600-1100 um) is assumed to apply to both." if side == "left" else
        "Colour bar 'z (um)' printed on this panel, labels 600-1100.",
        X.describe("x"), Y.describe("y"), Z.describe("colour bar z"),
    ], ["x_um", "y_um", "z_um", "colour_dist", "fill"], rows)
    mc.overlay_pts(25, clip, qa, f"overlay_edfig3b_{side}.png", r=1)
