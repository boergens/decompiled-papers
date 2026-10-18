"""Extraction shared by fig3, fig3inset, fig4a, fig4b (bond-length distributions, Origin raster).

Method (tier 3, digitized):
- axis calibration on inward major tick marks (black mask), linear fit;
- series separated by colour (fukplot.classify: white-blend of black / red / blue);
- text labels, dotted circles/ellipses and other small marks in a series colour are removed by
  dropping connected components whose bounding box is smaller than `min_extent` px in both
  directions (per series: larger for black, which carries the text labels); legend and inset areas are blanked by hand-given pixel boxes;
- per pixel column, the run of series pixels nearest the previous column's value is taken
  (digitize_common.trace_envelope). Because peaks are steep, a column can hold a long vertical
  run: y_upper/y_lower are the run's ends moved inward by half the line width, so the curve
  passes between them in that column; y_mid is their mean. Peak heights: use y_upper.
- columns where a series is not visible (drawn over by another curve) are left out.
"""
import numpy as np

import digitize_common as dc
import fukplot as fp


def clean_mask(mask, min_extent):
    out = np.zeros_like(mask)
    for r, c in fp.components(mask, 1):
        if (r.max() - r.min() + 1) >= min_extent or (c.max() - c.min() + 1) >= min_extent:
            out[r, c] = True
    return out


def calibrate(a, frame, xt_vals, yt_vals, tick_len=6):
    """frame = (left_col, right_col, top_row, bottom_row) of the axis box lines."""
    dark = a.max(2) < 100
    L, R, T, B = frame
    xt = fp.inward_ticks_x(dark, B, -1, tick_len, L + 2, R - 1)
    yt = sorted(fp.inward_ticks_y(dark, L, 1, tick_len, T + 2, B - 1), reverse=True)
    assert len(xt) == len(xt_vals), (xt, xt_vals)
    assert len(yt) == len(yt_vals), (yt, yt_vals)
    fx, rx, mx = fp.fit(xt, xt_vals)
    fy, ry, my = fp.fit(yt, yt_vals)
    return dict(fx=fx, fy=fy, rx=rx, ry=ry, mx=mx, my=my, xt=xt, yt=yt,
                x_left=float(fx(L)), x_right=float(fx(R)), y_bot=float(fy(B)), y_top=float(fy(T)))


def traces(a, cal, frame, palette, names, blank_boxes, min_extent=18, half_width=1.0, masks=None):
    L, R, T, B = frame
    lab, _ = fp.classify(a, palette)
    out = []
    used = {}
    for k, name in enumerate(names):
        m = (lab == k) if masks is None or masks.get(name) is None else masks[name]
        m = m.copy()
        m[: T + 2, :] = False
        m[B - 1:, :] = False
        m[:, : L + 2] = False
        m[:, R - 1:] = False
        for x0, y0, x1, y1 in blank_boxes:
            m[y0:y1, x0:x1] = False
        m = clean_mask(m, min_extent[name] if isinstance(min_extent, dict) else min_extent)
        used[name] = m
        env = dc.trace_envelope(m, L + 2, R - 1, T + 2, B - 1, half_width=half_width, min_px=1)
        for c, ym, yu, yl in env:
            if ym == ym:
                out.append((name, float(cal["fx"](c)), float(cal["fy"](ym)), float(cal["fy"](yu)), float(cal["fy"](yl)), int(c), ym))
    return out, used
