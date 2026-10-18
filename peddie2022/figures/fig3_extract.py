#!/usr/bin/env python3
"""Digitize the region outlines of Figure 3 (resolution vs target volume) from the embedded raster
image on p. 47 -> fig3.csv (tier 3, digitized).

The regions are blurred, semi-transparent colour shapes. Each pixel's displacement from white (255 - RGB) is
unmixed into non-negative strengths of the five region colours (the core colour of each region as printed),
allowing at most two regions per pixel (least squares over every single colour and every pair, best fit
wins, small penalty for pairs). A region's mask is where its strength is >= 0.5 (half the colour strength, the
middle of the blurred edge). The largest connected part of each mask is closed, its holes (the black labels)
are filled, and its outer contour is simplified to a polygon (cv2.approxPolyDP, 3 px).

Axes: x ticks 100 nm, 1 um, 10 um, 100 um, 1 mm are evenly spaced -> one decade per tick; x is given as
log10(length in nm) from a linear fit on the five ticks. y ticks 1, 5, 10, 50, 100, 1000 nm are evenly
spaced although their values are not (category-style axis): y is given as the tick position
(0 = tick "1", 1 = "5", 2 = "10", 3 = "50", 4 = "100", 5 = "1000"), and, as an interpretation only, as nm
interpolated log-linearly between the two neighbouring tick labels.
Run from anywhere: python3 -I fig3_extract.py
"""
import itertools
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, fit_axis, frame_lines, tick_positions, tick_positions_v, write_csv  # noqa: E402

PDF = ROOT / "source" / "peddie2022_vEM_primer_AAM.pdf"

COLOURS = {  # region name as printed -> core colour (RGB), from a k-means of the saturated pixels of the plot
    "ET, ssET": (103, 148, 194),
    "FIB-SEM": (106, 193, 185),
    "SBF-SEM, AT, ssTEM": (203, 226, 181),
    "X-ray microscopy": (253, 242, 105),
    "Emerging vEM technologies": (228, 139, 138),
}
THRESH = 0.5
X_TICKS = [2, 3, 4, 5, 6]  # log10 nm: 100 nm, 1 um, 10 um, 100 um, 1 mm
Y_LABELS = [1, 5, 10, 50, 100, 1000]


def y_nm(pos):
    """Log-linear interpolation between neighbouring tick labels (interpretation of the uneven axis)."""
    lg = np.log10(Y_LABELS)
    i = int(np.clip(np.floor(pos), 0, len(lg) - 2))
    return float(10 ** (lg[i] + (pos - i) * (lg[i + 1] - lg[i])))


def main():
    a = embedded_image(PDF, 47)
    g = a.astype(float).mean(2)
    dark = g < 80
    xrow = frame_lines(dark, 1, 0.5)[0]
    ycol = frame_lines(dark, 0, 0.4)[0]
    xt = tick_positions(dark, xrow, +1, 14, ycol[1] + 5, 1900)
    yt = tick_positions_v(dark, ycol, -1, 14, 40, xrow[0])
    assert len(xt) == 5 and len(yt) == 6, (xt, yt)
    fx, rx, mx = fit_axis(xt, X_TICKS)
    yt_sorted = sorted(yt, reverse=True)  # bottom (label 1) first
    fy, ry, my = fit_axis(yt_sorted, list(range(6)))
    # plot area: right of the y axis, above the x axis
    x0, y0, x1, y1 = ycol[1] + 3, 0, a.shape[1], xrow[0] - 2
    sub = a[y0:y1, x0:x1].astype(np.float32)
    names = list(COLOURS)
    D = np.array([[255 - v for v in COLOURS[n]] for n in names], np.float32)
    Y = (255 - sub).reshape(-1, 3)
    best = np.full(len(Y), np.inf, np.float32)
    beta = np.zeros((len(Y), len(names)), np.float32)
    for k in range(len(names)):
        d = D[k]
        b = np.clip(Y @ d / (d @ d), 0, None)
        r = ((Y - b[:, None] * d) ** 2).sum(1)
        m = r < best
        best[m] = r[m]
        beta[m] = 0
        beta[m, k] = b[m]
    for i, j in itertools.combinations(range(len(names)), 2):
        A = np.stack([D[i], D[j]], 1)
        sol = np.linalg.lstsq(A, Y.T, rcond=None)[0].T
        r = ((Y - sol @ A.T) ** 2).sum(1) + 50
        m = (sol >= 0).all(1) & (r < best)
        best[m] = r[m]
        beta[m] = 0
        beta[m, i] = sol[m, 0]
        beta[m, j] = sol[m, 1]
    beta = beta.reshape(sub.shape[0], sub.shape[1], len(names))
    rows, summary, contours_px = [], [], {}
    for k, reg in enumerate(names):
        m = (beta[:, :, k] >= THRESH).astype(np.uint8)
        n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
        big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        m = (lab == big).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(cs, key=cv2.contourArea)
        filled = np.zeros_like(m)
        cv2.drawContours(filled, [c], -1, 1, -1)  # fills the holes left by the black labels
        poly = cv2.approxPolyDP(c, 3.0, True)[:, 0, :].astype(float)
        poly[:, 0] += x0
        poly[:, 1] += y0
        contours_px[reg] = poly
        for i, (px, py) in enumerate(poly):
            xp = float(fx(px))
            yp = float(fy(py))
            rows.append([reg, i, round(px, 1), round(py, 1), round(xp, 3), round(10 ** xp, 1), round(yp, 3), round(y_nm(yp), 2)])
        xs, ys = poly[:, 0], poly[:, 1]
        summary.append(f"{reg}: x from {10 ** fx(xs.min()):.3g} to {10 ** fx(xs.max()):.3g} nm (log10 {fx(xs.min()):.2f} to {fx(xs.max()):.2f}); "
                       f"y tick position {fy(ys.max()):.2f} to {fy(ys.min()):.2f} (~{y_nm(fy(ys.max())):.3g} to {y_nm(fy(ys.min())):.3g} nm); "
                       f"area {int(filled.sum())} px")
    hdr = [
        "Peddie et al. 2022 (Nat Rev Methods Primers, Europe PMC author manuscript), Figure 3 (single panel): outlines of the",
        "five coloured regions, 'Resolution (nm)' (vertical) vs 'Target volume' (horizontal).",
        "Provenance: tier 3, digitized from the embedded raster image on PDF p. 47 (2096 x 1482 px, ~4.16 px per pt).",
        "The regions are drawn blurred (soft edges about 30-60 px wide): each outline is where the region colour is at about half",
        "strength (colour unmixing, strength >= 0.5, see fig3_extract.py). Where regions overlap, the overlap is counted for both;",
        "an edge that lies under another region (e.g. the right end of FIB-SEM and SBF-SEM bands under the red ellipse) is uncertain.",
        "Uncertainty: about +-0.1 decade in x and +-0.15 tick positions in y at the soft edges; the regions are qualitative.",
        f"x: ticks 100 nm, 1 um, 10 um, 100 um, 1 mm evenly spaced (one decade per tick); linear fit of log10(nm) on {len(xt)} ticks,",
        f"max residual {rx:.4f} decade, {abs(1 / mx):.1f} px per decade. The x label is 'Target volume' but the ticks are lengths.",
        "y: ticks 1, 5, 10, 50, 100, 1000 evenly spaced although the values are not (category-style axis); y_tickpos = position in",
        f"tick spacings above the '1' tick (fit on 6 ticks, max residual {ry:.4f}, {abs(1 / my):.1f} px per tick spacing).",
        "y_nm_interp is NOT read from the figure: log-linear interpolation between the two neighbouring tick labels (an interpretation).",
        "Columns: region (as labelled), vertex (polygon order), x_px, y_px (embedded-image pixels), x_log10_nm, x_nm, y_tickpos, y_nm_interp.",
        "Extents (from the polygons):",
    ] + ["  " + s for s in summary]
    write_csv(HERE / "fig3.csv", hdr,
              ["region", "vertex", "x_px", "y_px", "x_log10_nm", "x_nm", "y_tickpos", "y_nm_interp"], rows,
              fmt=["{}", "{}", "{:.1f}", "{:.1f}", "{:.3f}", "{:.4g}", "{:.3f}", "{:.4g}"])
    # overlay: outlines on the source image
    (ROOT / "work").mkdir(exist_ok=True)
    im = a.copy()
    for reg, poly in contours_px.items():
        cv2.polylines(im, [poly.astype(np.int32).reshape(-1, 1, 2)], True, (255, 0, 255), 3)
    for x in xt:
        cv2.line(im, (int(x), xrow[1]), (int(x), xrow[1] + 25), (0, 160, 0), 3)
    for y in yt:
        cv2.line(im, (ycol[0] - 25, int(y)), (ycol[0], int(y)), (0, 160, 0), 3)
    cv2.imwrite(str(ROOT / "work" / "fig3_overlay.png"), cv2.cvtColor(im, cv2.COLOR_RGB2BGR)[::2, ::2])
    print("\n".join(summary))


if __name__ == "__main__":
    main()
