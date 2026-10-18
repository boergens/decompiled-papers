"""Shared digitizer for the two histograms of Fig. 4f (yin2020, PDF p. 7).

Each histogram is an embedded raster image (300 ppi, ~665 x 334 px) of a solid-blue bar chart with a
light-grey frame; the tick marks are in the image, the tick labels are PDF text next to it. Used by
figures/fig4ftop_extract.py and figures/fig4fbottom_extract.py.
"""
import os
import sys

import numpy as np
import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from digitize_common import embedded_image, gray, fit_axis, write_csv, overlay  # noqa: E402


def groups(idx):
    out = []
    for i in idx:
        if out and i <= out[-1][-1] + 1:
            out[-1].append(i)
        else:
            out.append([i])
    return [float(np.mean(g)) for g in out]


def label_centres(pdf, page, bbox_pt, img_shape, labels, axis):
    """Centres (image px) of the PDF-text tick labels that belong to this image, for a cross-check."""
    p = pymupdf.open(pdf)[page - 1]
    x0, y0, x1, y1 = bbox_pt
    h, w = img_shape[:2]
    out = {}
    for b in p.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for s in ln["spans"]:
                t = s["text"].strip()
                bx = s["bbox"]
                cx, cy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
                if axis == "x" and x0 - 5 < cx < x1 + 5 and y1 < cy < y1 + 12 and t in labels:
                    out[t] = (cx - x0) / (x1 - x0) * w
                if axis == "y" and x0 - 15 < cx < x0 and y0 - 5 < cy < y1 + 5 and t in labels:
                    out[t] = (cy - y0) / (y1 - y0) * h
    return out


def digitize(pdf, page, bbox_pt, xlabels, ylabels, out_csv, overlay_png, title):
    a = embedded_image(pdf, page, bbox_near=bbox_pt)
    g = gray(a)
    h, w = g.shape
    dark = g < 200
    # bottom axis line: the lowest row that is dark across >= 90 % of the width
    axis_row = max(r for r in range(h) if dark[r].mean() > 0.9)
    left_col = min(c for c in range(w) if dark[:, c].mean() > 0.9)
    # x ticks: short marks hanging below the axis line
    xt = groups([c for c in range(w) if dark[axis_row + 1:axis_row + 3, c].any() and c > left_col + 2])
    # y ticks: short marks left of the left frame line
    yt = groups([r for r in range(h) if dark[r, max(0, left_col - 3):left_col].any()])
    assert len(xt) == len(xlabels), (xt, xlabels)
    assert len(yt) == len(ylabels), (yt, ylabels)
    xv = [float(v) for v in xlabels]
    yv = [float(v) for v in ylabels]
    fx, rx, sx = fit_axis(xt, xv)
    fy, ry, sy = fit_axis(yt, yv)
    # cross-check: tick positions vs. centres of the PDF-text labels
    lx = label_centres(pdf, page, bbox_pt, a.shape, set(xlabels), "x")
    ly = label_centres(pdf, page, bbox_pt, a.shape, set(ylabels), "y")
    dx = max(abs(lx[t] - xt[i]) for i, t in enumerate(xlabels) if t in lx)
    dy = max(abs(ly[t] - yt[i]) for i, t in enumerate(ylabels) if t in ly)

    blue = np.clip((a[:, :, 2].astype(float) - a[:, :, 0]) / 104.0, 0, 1)   # bar colour ~ (64, 80, 168)
    barcols = [c for c in range(left_col + 2, w - 3) if blue[:axis_row, c].max() > 0.5]
    c0, c1 = min(barcols), max(barcols)
    # top edge per column, sub-pixel: rows fully blue + the partial coverage of the row above
    tops = {}
    for c in range(c0, c1 + 1):
        col = blue[:axis_row, c]
        full = np.where(col > 0.5)[0]
        if len(full) == 0:
            tops[c] = None
            continue
        t = full.min()
        partial = col[t - 1] if t > 0 else 0
        tops[c] = t - partial            # edge position in pixel-boundary coordinates
    # bin grid: changes of the top edge between neighbouring columns
    ch = [c for c in range(c0 + 1, c1 + 1)
          if (tops[c] is None) != (tops[c - 1] is None) or (tops[c] is not None and tops[c - 1] is not None and abs(tops[c] - tops[c - 1]) > 0.6)]
    ch = [c0] + ch + [c1 + 1]
    seg = np.diff(ch)
    width = float(np.median([s for s in seg if s >= 6]))
    nbin = int(round((c1 + 1 - c0) / width))
    width = (c1 + 1 - c0) / nbin
    rows, pts = [], []
    total = 0
    for k in range(nbin):
        e0, e1 = c0 + k * width, c0 + (k + 1) * width
        inner = [c for c in range(int(np.ceil(e0 + 2)), int(np.floor(e1 - 2)) + 1)]
        tv = [tops[c] for c in inner if tops[c] is not None]
        if not tv:
            top_edge = None
        else:
            top_edge = float(np.median(tv))
        # pixel-boundary coordinate -> centre coordinate: the row index r spans [r, r+1)
        if top_edge is None:
            cnt = 0.0
        else:
            cnt = float(fy(top_edge - 0.5))
        n = int(round(cnt))
        total += n
        xl, xr = float(fx(e0 - 0.5)), float(fx(e1 - 0.5))
        rows.append((xl, xr, (xl + xr) / 2, cnt, n))
        if top_edge is not None:
            for c in inner:
                pts.append((c, top_edge - 0.5))
        pts.append((e0 - 0.5, axis_row - 6))
    os.makedirs(os.path.dirname(overlay_png), exist_ok=True)
    overlay(a, pts, overlay_png)
    write_csv(out_csv, [
        title,
        "Columns: bin_left, bin_right, bin_centre = bin edges and centre in frames per second (fps), from the bar edges;",
        "  count_read = bar height read off the image in Counts (sub-pixel top edge mapped through the y ticks);",
        "  count = count_read rounded to the nearest integer (histogram counts are whole numbers).",
        "Provenance: tier 3, digitized from the embedded 300 ppi raster image of the bars (no vector data in the PDF; the",
        "  tick labels are PDF text) by the matching _extract.py with tools/hist4f.py. Axis calibration: linear fit on the",
        f"  {len(xt)} x tick marks and {len(yt)} y tick marks in the image (max residual {rx:.4f} fps, {ry:.3f} counts); the",
        f"  PDF-text label centres agree with the tick marks to within {dx:.1f} px (x) and {dy:.1f} px (y).",
        f"Bins: {nbin} equal bins of {width:.2f} px = {abs(width * sx):.4f} fps found from the steps of the bar tops; empty bins inside",
        "  the range are listed with count 0. The paper gives no bin settings.",
        f"Uncertainty: bin edges about +-{abs(sx):.3f} fps (1 px); counts about +-{abs(sy):.2f} per px, so +-1 count after rounding.",
        f"Sum of the rounded counts: {total} (caption: 'a sample size of over 1000 sections').",
    ], ["bin_left_fps", "bin_right_fps", "bin_centre_fps", "count_read", "count"], rows,
        fmt=["{:.4f}", "{:.4f}", "{:.4f}", "{:.2f}", "{}"])
    return rows, total
