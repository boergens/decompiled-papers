"""Shared extraction for the precision-recall plots of Appendix 1-figures 1 and 2 (matplotlib plots, embedded as JPEG).

Calibration on the grey gridlines (pixel positions found by code); curves traced per pixel column on tab10 colour
masks (longest run per column, so stray JPEG pixels are ignored; columns where a curve is hidden by another are missing);
the 'manual estimated' point is the centroid of the purple disc outside the legend.
"""
import numpy as np

import fc_dig as fd

TAB = {"initial": (31, 119, 180), "cascade": (255, 127, 14), "hybrid": (214, 39, 40), "synful+": (44, 160, 44)}
PURPLE = (148, 103, 189)


def grid(a, axis):
    g = a.astype(int)
    mx, mn = g.max(axis=2), g.min(axis=2)
    grey = (mx - mn < 20) & (mx > 140) & (mx < 225)
    if axis == "v":
        f = grey[20:500].mean(axis=0)
    else:
        f = grey[:, 80:540].mean(axis=1)
    idx = np.where(f > 0.4)[0]
    return [float(np.mean(r)) for r in fd.runs(list(idx))]


def extract(page, series, xvals, yvals, ygrid_skip, legend, out_csv, out_overlay, title):
    a = fd.embedded(page)
    xs = grid(a, "v")
    ys = [y for y in grid(a, "h") if round(y) not in ygrid_skip]
    assert len(xs) == len(xvals) and len(ys) == len(yvals), (xs, ys)
    fx, rx = fd.fit(xs, xvals)
    fy, ry = fd.fit(ys, yvals)
    rows, ov = [], {}
    for s in series:
        m = fd.blank(fd.colour_mask(a, TAB[s], 60), [legend])
        tr = fd.trace(m, 60, 552, 7, 519, min_px=2)
        ov[s] = [(t[0], t[1]) for t in tr]
        for t in tr:
            rows.append([s, float(fx(t[0])), float(fy(t[1])), float(fy(t[3])), float(fy(t[2]))])
    m = fd.blank(fd.colour_mask(a, PURPLE, 50), [legend])
    bl = [b for b in fd.blobs(m, 60, 7, 552, 519, amin=40, amax=2000)]
    for b in bl:
        rows.append(["manual estimated", float(fx(b[0])), float(fy(b[1])), "", ""])
        ov["manual estimated"] = [(b[0], b[1])]
    hdr = [title,
           "x = recall (linear), y = precision (linear).",
           "Provenance: tier 3, digitized from the embedded raster (563 x 561 px JPEG); the authors' source data file was not available locally.",
           f"Calibration on the grey gridlines: x {xvals[0]}..{xvals[-1]} (max residual {rx:.4f}), y {yvals[0]}..{yvals[-1]} (max residual {ry:.4f}).",
           "One row per pixel column of each curve: y = line centre, y_low/y_high = lower/upper edge of the line ink (lines ~4 px wide).",
           "On near-vertical segments (curve ends) the column centre is the middle of the ink run, so use y_low/y_high there.",
           "Uncertainty: about +-0.002 in recall (1 px) and +-0.0004 (Fig. 1) / +-0.0015 (Fig. 2) in precision per pixel, more where curves overlap.",
           "'manual estimated' = centroid of the purple disc.",
           "Columns: series, x, y, y_low, y_high."]
    fd.write_csv(out_csv, hdr, ["series", "x", "y", "y_low", "y_high"], rows)
    fd.overlay(a, ov, out_overlay, r=1)
    return rx, ry, rows
