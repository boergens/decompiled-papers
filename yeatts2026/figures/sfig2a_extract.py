#!/usr/bin/env python3
"""Digitize Supplemental Figure 2, panel a (and, via sfig2b_extract.py, panel b) of Yeatts et al. 2026
(yeatts2026_supplement.pdf p. 3).

Source: the one embedded raster image of the whole figure (768 x 652 px, placed at ~121 ppi; no vector plot
paths in the PDF, only Word's white picture-frame rectangles).  Panel a = two stacked axes boxes on the left
(raw spectral amplitude vs camera pixel number; top: the two raw spectra, bottom: the background-subtracted
interferogram), panel b = two stacked boxes on the right (complex-depth-profile amplitude vs depth, "Intensity
(dB)").  Blue = channel 2, orange = channel 1 (caption).  No axis has numbers, so every coordinate is given as
the fraction of the axis box: x 0 = y-axis line (left), 1 = right end of the x-axis line; y 0 = x-axis line
(bottom), 1 = top end of the y-axis line.  The unlabelled tick marks on both axes are recorded in the header.

    python3 -I sfig2a_extract.py   -> sfig2atop.csv, sfig2abottom.csv (+ ../work/sfig2a_overlay.png)

Method (tier 3, digitized): grey axis lines found as long grey runs; per pixel column, the rows of the blue
(resp. orange) colour mask inside the box give the top, bottom and mean of the trace (envelope, so the
oscillating interferogram and the noisy dB traces keep their full excursions).  Where one trace hides the other
(the later-drawn line wins in the source), the hidden series has no pixels in that column (empty cell).
Uncertainty: ~1 px = 1/300 of the box width in x and 1/100 of the box height in y, plus the line thickness
(~1.5 px) and antialiasing; the source is only 121 ppi, so treat the values as approximate.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * i))) for i in range(1, 6)]:
    if os.path.exists(os.path.join(_d, "tools", "digitize_common.py")):  # the collection's shared tools/, wherever this folder sits
        sys.path.insert(0, os.path.join(_d, "tools")); break   # digitize_common.py
import numpy as np  # noqa: E402
from digitize_common import embedded_image, gray, tick_positions, tick_positions_v, write_csv, overlay  # noqa: E402

PDF = os.path.join(HERE, "../source/yeatts2026_supplement.pdf")


def runs_of(idx, gap=0):
    """Consecutive-index runs of idx as (first, last); runs separated by <= gap missing indices are merged."""
    groups = []
    for i in idx:
        if groups and i <= groups[-1][1] + 1 + gap:
            groups[-1][1] = i
        else:
            groups.append([i, i])
    return [tuple(g) for g in groups]


def find_boxes(a):
    """The four axes boxes of panels a and b: dict (panel, pos) -> (x_left, x_right, y_top, y_bottom) in px.

    Axis lines are grey (r ~ g ~ b, darker than 215).  They are interrupted where the coloured traces cross them,
    so grey runs with gaps up to 15 px (vertical) / 12 px (horizontal) are merged; the plot area is the top 262
    rows.  Each y-axis line (a long vertical grey run) anchors one box: the x-axis rows are the rows that are grey
    just right of it, and the box's right end is where that grey row ends.
    Found: x 70..373 (panel a) and 418..719 (panel b); y 9..110.5 (top boxes, 2-px x-axis line at rows 110-111)
    and 130..231 (bottom boxes).
    """
    rgb = a.astype(int)
    spread = rgb.max(2) - rgb.min(2)
    greyish = (spread < 30) & (gray(a) < 215)
    top = greyish[:262, :]
    boxes = {}
    for c in range(top.shape[1]):
        for r0, r1 in runs_of(np.where(top[:, c])[0], gap=15):
            if r1 - r0 < 50:
                continue
            # x-axis rows: grey in >= 85 % of the 100 px right of the column, within 6 rows of the run's lower end
            rows = [r for r in range(max(0, r1 - 6), min(262, r1 + 7)) if top[r, c + 3:c + 103].mean() >= 0.85]
            if not rows:
                continue
            line = top[rows, :].any(0)
            xr = max(e for s_, e in runs_of(np.where(line[c:])[0], gap=12) if s_ == 0) + c
            panel = 'a' if c < a.shape[1] / 2 else 'b'
            pos = 'top' if r0 < 120 else 'bottom'
            boxes[(panel, pos)] = (float(c), float(xr), float(r0), float(np.mean(rows)))
    assert len(boxes) == 4, boxes
    return boxes, greyish


def series_masks(a):
    rgb = a.astype(int)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    blue = (b - r > 40) & (b > 120)
    orange = (r - b > 40) & (r > 150)
    return {'channel 2 (blue)': blue, 'channel 1 (orange)': orange}


def extract(panel, xlabel, ylabel):
    a = embedded_image(PDF, 3)
    boxes, greyish = find_boxes(a)
    masks = series_masks(a)
    pts_all = []
    for pos in ('top', 'bottom'):
        xl, xr, yt, yb = boxes[(panel, pos)]
        W, H = xr - xl, yb - yt
        # unlabelled tick marks: short grey stubs just inside the x axis (pointing up) and the y axis (pointing right)
        # ticks are 1 px wide / 2 px tall (x axis) and 1-2 px tall / 3 px long (y axis), grey level ~90-210
        xt = tick_positions(greyish, (int(np.floor(yb)), int(np.floor(yb))), -1, 2, int(xl) + 2, int(xr) + 1, frac=0.9)
        yt_ = tick_positions_v(greyish, (int(round(xl)), int(round(xl))), +1, 3, int(yt) - 1, int(yb) - 1, frac=0.9)
        xt = [float(t) for t in xt if t > xl + 3 and t < xr - 1]
        yt_ = [float(t) for t in yt_ if t > yt + 1 and t < yb - 3]
        rows = []
        for name, m in masks.items():
            for c in range(int(xl) + 1, int(xr) + 1):
                rr = np.where(m[int(yt) - 2:int(yb), c])[0]
                if len(rr) == 0:
                    continue
                rr = rr + int(yt) - 2
                top, bot, mid = rr.min(), rr.max(), rr.mean()
                rows.append((name, c, (c - xl) / W, (yb - mid) / H, (yb - top) / H, (yb - bot) / H))
                pts_all.append((c, mid))
        out = os.path.join(HERE, "sfig2%s%s.csv" % (panel, pos))
        write_csv(out, [
            "Yeatts et al. 2026 (bioRxiv 10.64898/2026.06.11.731509), Supplemental Figure 2, panel %s, %s axes box." % (panel, pos),
            "  %s" % ({'a': 'Raw spectral data amplitude for a given camera pixel of one A-line (top: raw spectra; bottom: after background',
                       'b': 'Amplitude of the complex depth profile (the pre-processed A-line) against depth (top: without, bottom: with'}[panel]),
            "  %s" % ({'a': 'subtraction, the oscillating interferogram); x axis "Pixel number", y axis "Intensity" (shared label).',
                       'b': 'background subtraction, following the order of panel c); x axis "Depth", y axis "Intensity (dB)".'}[panel]),
            "Series: 'channel 2 (blue)' and 'channel 1 (orange)' as named in the caption.",
            "Columns: x_px = pixel column of the source image; x_frac = x as the fraction of the axis-box width (0 = y-axis line,",
            "  1 = right end of the x-axis line); y_frac = mean row of the trace in that column as the fraction of the axis-box",
            "  height (0 = x-axis line, 1 = top of the y-axis line); y_frac_top / y_frac_bottom = highest and lowest pixel of the",
            "  trace in that column (envelope; for the oscillating/noisy traces the swing within one column is real).",
            "No axis has numbers. Unlabelled tick marks found: x axis at x_frac = %s;" % ", ".join("%.3f" % ((t - xl) / W) for t in xt),
            "  y axis at y_frac = %s (a tick hidden under the traces where they cross the axis is not listed)." % ", ".join("%.3f" % ((yb - t) / H) for t in sorted(yt_, reverse=True)),
            "  The x ticks are evenly spaced at %.4f of the box width." % (float(np.mean(np.diff(xt))) / W),
        ] + ([
            "  (Decompiler's inference, not printed in the figure: 0.0977 = 1/10.24, i.e. consistent with an x axis of",
            "   0..1024 camera pixels per channel ticked every 100 pixels; the text says each channel has 1024 pixels.",
            "   Treat this as a hypothesis.)",
        ] if panel == 'a' else []) + [
            "Axes box in source pixels: x %.0f..%.0f, y %.0f..%.0f (%.0f x %.0f px)." % (xl, xr, yt, yb, W, H),
            "Provenance: tier 3, digitized from the embedded 768 x 652 px raster image (121 ppi; no vector paths) by",
            "  sfig2a_extract.py (colour masks per pixel column). One row per pixel column and series; a series hidden",
            "  behind the other in a column has no row there.",
            "Uncertainty: about +-%.3f in x_frac and +-%.3f in y_frac (1 px), more where the two traces overlap." % (1 / W, 1 / H),
        ], ["series", "x_px", "x_frac", "y_frac", "y_frac_top", "y_frac_bottom"], rows,
            fmt=["{}", "{:d}", "{:.4f}", "{:.4f}", "{:.4f}", "{:.4f}"])
        print(out, len(rows), "rows; box", boxes[(panel, pos)], "xticks", len(xt), "yticks", len(yt_))
    overlay(a, pts_all, os.path.join(HERE, "../work/sfig2%s_overlay.png" % panel))
    return boxes


if __name__ == "__main__":
    extract('a', 'Pixel number', 'Intensity')
