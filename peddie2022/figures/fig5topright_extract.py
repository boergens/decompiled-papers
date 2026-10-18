#!/usr/bin/env python3
"""Digitize the histogram of Figure 5 (top right, "Mitochondria volume (10^3 pixels)" vs "Count")
from the embedded raster image on p. 49 -> fig5topright.csv (tier 3, digitized).

Axis lines and tick marks are located in the native-resolution image (2096 x 923 px), a linear
pixel->data map is fitted on the labelled ticks of each axis, and the blue bars are found with a
colour mask: bar edges from the mask along a row just above the x axis, bar tops from the mask
in each bar's central columns. Run from anywhere: python3 -I fig5topright_extract.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, fit_axis, frame_lines, overlay, tick_positions, tick_positions_v, write_csv  # noqa: E402

PDF = ROOT / "source" / "peddie2022_vEM_primer_AAM.pdf"
X0, Y0, X1, Y1 = 1450, 0, 2096, 420  # histogram region in the embedded image (px)


def main():
    a = embedded_image(PDF, 49)
    sub = a[Y0:Y1, X0:X1].astype(int)
    g = sub.mean(2)
    dark = g < 100
    xrow = frame_lines(dark[:, 50:], 1, 0.4)[0]  # x-axis line (rows)
    ycol = frame_lines(dark[:380], 0, 0.5)[0]  # y-axis line (columns)
    # x ticks hang below the axis line; y ticks stick out to the left of the axis line
    xt = tick_positions(dark, xrow, +1, 3, ycol[1] + 3, sub.shape[1] - 5)
    yt = tick_positions_v(dark, ycol, -1, 5, 5, xrow[1] + 1)
    xvals = [0, 20, 40, 60, 80, 100]
    yvals = [25, 20, 15, 10, 5, 0]  # top to bottom
    assert len(xt) == len(xvals), xt
    assert len(yt) == len(yvals), yt
    fx, rx, mx = fit_axis(xt, xvals)
    fy, ry, my = fit_axis(yt, yvals)
    # blue bars: R low, B high
    r, gg, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    blue = (b > 120) & (r < 90) & (b - r > 60)
    row = xrow[0] - 3
    on = blue[row]
    cols = np.where(on)[0]
    # split into contiguous runs; a 1-2 px light seam separates adjacent bars of different height,
    # so also split where the bar top changes
    tops = np.array([np.where(blue[:row + 1, c])[0].min() if blue[:row + 1, c].any() else -1 for c in range(sub.shape[1])])
    edges = []
    start = cols[0]
    for c0, c1 in zip(cols, cols[1:]):
        if c1 != c0 + 1 or abs(tops[c1] - tops[c0]) > 2:
            edges.append((start, c0))
            start = c1
    edges.append((start, cols[-1]))
    rows, pts = [], []
    for e0, e1 in edges:
        mid = slice(e0 + 3, e1 - 2)
        top = float(np.median(tops[mid]))
        left, right = float(fx(e0 - 0.5)), float(fx(e1 + 0.5))
        count = float(fy(top - 0.5))  # outer edge of the top row of bar pixels
        rows.append([round(left, 2), round(right, 2), round(count, 2), int(round(count))])
        pts += [(X0 + e0, Y0 + top), (X0 + e1, Y0 + top), (X0 + (e0 + e1) / 2, Y0 + top)]
    hdr = [
        "Peddie et al. 2022 (Nat Rev Methods Primers, Europe PMC author manuscript), Figure 5, top-right panel:",
        "histogram of mitochondria volumes, x 'Mitochondria volume (10^3 pixels)', y 'Count'. Both axes linear.",
        "Provenance: tier 3, digitized from the embedded raster image on PDF p. 49 (2096 x 923 px, ~4.16 px per pt),",
        f"region x {X0}-{X1}, y {Y0}-{Y1} px. Axis fits on the labelled tick marks: x {len(xt)} ticks (0-100), "
        f"max residual {rx:.3f} units, {abs(1 / mx):.3f} px per unit; y {len(yt)} ticks (0-25), max residual {ry:.3f}, {abs(1 / my):.3f} px per count.",
        "Bars found with a blue colour mask; bin edges = outer edges of each bar's pixel run along a row just above the x axis;",
        "count = top of the bar. Uncertainty: about +-0.3 units on the bin edges (1 px), +-0.1 on the counts (1 px).",
        "count_rounded is the nearest integer (counts are integers). Empty bins between the bars are not drawn and not listed;",
        "the bars have about equal widths, so the bins between ~40 and ~78 have count 0.",
        "Columns: bin_left, bin_right (10^3 pixels), count (as read), count_rounded.",
    ]
    write_csv(HERE / "fig5topright.csv", hdr, ["bin_left", "bin_right", "count", "count_rounded"], rows,
              fmt=["{:.2f}", "{:.2f}", "{:.2f}", "{}"])
    (ROOT / "work").mkdir(exist_ok=True)
    big = a.copy()
    overlay(big[Y0:Y1, X0:X1], [(x - X0, y - Y0) for x, y in pts], str(ROOT / "work" / "fig5topright_overlay.png"))
    for row_ in rows:
        print(row_)


if __name__ == "__main__":
    main()
