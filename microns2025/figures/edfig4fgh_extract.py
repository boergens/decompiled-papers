#!/usr/bin/env python3
"""Extended Data Fig. 4f, g, h (p. 27): scatter plots of signal correlation (matched vs matched, y) against signal
correlation (matched vs nearest non-matched, x), coloured by oracle score. Each panel is one embedded raster image
(810 x 590 px, 600 ppi, seaborn style) including axes and colour bar -> edfig4f.csv, edfig4g.csv, edfig4h.csv.

The thousands of small markers (about 7 px wide, white edges) overlap heavily and cannot be separated into single
points, so the CSV is a pixel table: every pixel of the plot area that belongs to a marker (not background, not white
grid line or marker edge), with its data coordinates and the oracle score read from its colour on the colour bar.
Axes: white grid lines found in the image: x 0.0, 0.5, 1.0 (0.0 hidden by markers in f, extrapolated with the
0.5 spacing); y -0.2 ... 1.0 step 0.2. Colour bar: column centre of the bar, tick marks 0.0 ... 0.4 found as dark
ticks to its right. Pixels within 3 px of the black diagonal line (y = x, drawn from -0.3 to 1.0) are flagged,
since black is also the colour of oracle ~0.22 in this colour map."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import digitize_common as dc  # noqa: E402

BG = np.array([225, 225, 233])
TITLES = {"f": "all matched", "g": "matched oracle > 0.2", "h": "matched and nearest oracle > 0.2"}
BBOX = {"f": (111, 262, 209, 333), "g": (249, 262, 347, 333), "h": (394, 262, 491, 333)}


def groups(v):
    g = []
    for i in v:
        if g and i - g[-1][-1] <= 1:
            g[-1].append(i)
        else:
            g.append([i])
    return [float(np.mean(x)) for x in g]


for p in "fgh":
    a = dc.embedded_image(str(mc.PDF), 27, bbox_near=BBOX[p]).astype(int)
    H, W, _ = a.shape
    bg = np.abs(a - BG).sum(2) < 10
    r = np.where(bg.sum(1) > 0.3 * W)[0]
    c = np.where(bg.sum(0) > 0.3 * H)[0]
    y0, y1, x0, x1 = r.min(), r.max(), c.min(), c.max()
    white = a.min(2) > 248
    sub = white[y0:y1 + 1, x0:x1 + 1]
    gx = [g + x0 for g in groups(np.where(sub.mean(0) > 0.6)[0])]
    gy = [g + y0 for g in groups(np.where(sub.mean(1) > 0.6)[0])]
    assert len(gy) == 7, gy
    if len(gx) == 2:  # 0.0 line hidden
        gx = [gx[0] - (gx[1] - gx[0])] + gx
    X = mc.LinAxis(list(zip(gx, [0.0, 0.5, 1.0])))
    Y = mc.LinAxis(list(zip(gy, [1.0, 0.8, 0.6, 0.4, 0.2, 0.0, -0.2])))
    sat = (a.max(2) - a.min(2)) > 25
    cc = np.where(sat[:, x1 + 5:].mean(0) > 0.5)[0] + x1 + 5
    cb0, cb1 = cc.min(), cc.max()
    rr = np.where(sat[:, cb0 + 3:cb1 - 3].mean(1) > 0.5)[0]
    dark = a.max(2) < 90
    tk = groups(np.where(dark[:, cb1 + 2:cb1 + 8].mean(1) > 0.6)[0])
    assert len(tk) == 5, tk
    C = mc.LinAxis(list(zip(tk, [0.4, 0.3, 0.2, 0.1, 0.0])))
    lut_rows = np.arange(rr.min() + 2, rr.max() - 1)
    lut = a[lut_rows, (cb0 + cb1) // 2 - 5:(cb0 + cb1) // 2 + 5].mean(1)
    lut_val = C(lut_rows)
    # diagonal line endpoints in pixels
    d0 = np.array([X.inv(-0.3), Y.inv(-0.3)])
    d1 = np.array([X.inv(1.0), Y.inv(1.0)])
    rows, qa = [], []
    for yy in range(y0 + 1, y1):
        for xx in range(x0 + 1, x1):
            px = a[yy, xx]
            if np.abs(px - BG).sum() < 20 or px.min() > 235:
                continue
            dist = np.sqrt(((lut - px) ** 2).sum(1))
            i = int(dist.argmin())
            if dist[i] > 40:
                continue
            t = np.clip(np.dot([xx, yy] - d0, d1 - d0) / np.dot(d1 - d0, d1 - d0), 0, 1)
            near = np.hypot(*([xx, yy] - (d0 + t * (d1 - d0)))) <= 3
            rows.append([xx, yy, f"{X(xx):.4f}", f"{Y(yy):.4f}", f"{lut_val[i]:.3f}", f"{dist[i]:.1f}",
                         "%02x%02x%02x" % tuple(px), int(near)])
            qa.append((xx, yy))
    comments = [
        f"Extended Data Fig. 4{p} (p. 27 of microns2025.pdf), panel title '{TITLES[p]}': y 'signal corr matched vs matched',",
        "x 'signal corr matched vs nearest non-matched', colour 'oracle score'.",
        "Provenance: tier 3, digitized from the embedded raster (600 ppi); PIXEL TABLE, not individual points: the markers",
        "overlap and cannot be separated. One row per marker pixel (colour within RGB distance 40 of the colour bar).",
        f"Uncertainty: one pixel = {abs(X.a):.4f} (x) and {abs(Y.a):.4f} (y) correlation units; oracle score from colour,",
        "+-0.01 for saturated colours, worse where the colour map is dark (0.18-0.26 all near-black).",
        "Columns: px, py (pixel column/row in the embedded image, origin top left); x, y (data units); oracle_score (from colour);",
        "colour_dist (RGB distance to the nearest colour-bar entry); rgb (pixel colour); near_diagonal (1 = within 3 px of the",
        "black y = x line; such dark pixels may be line, not marker).",
        X.describe("x"), Y.describe("y"), C.describe("colour bar (pixel row -> oracle score)"),
        f"Plot area pixels x {x0}..{x1}, y {y0}..{y1}; colour bar pixels x {cb0}..{cb1}, y {rr.min()}..{rr.max()}.",
    ]
    out = Path(__file__).with_name(f"edfig4{p}.csv")
    mc.write_csv(out, comments, ["px", "py", "x", "y", "oracle_score", "colour_dist", "rgb", "near_diagonal"], rows)
    im = a.copy().astype(np.uint8)
    for xx, yy in qa:
        im[yy, xx] = (0, 255, 0)
    from PIL import Image
    Image.fromarray(np.hstack([a.astype(np.uint8), im])).save(mc.K / "work" / f"overlay_edfig4{p}.png")
