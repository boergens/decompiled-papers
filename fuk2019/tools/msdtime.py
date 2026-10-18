"""Extraction shared by figures/fig9a_extract.py and fig9b_extract.py (MSD-time curves).

Origin raster export, 300 ppi. Frame and inward tick marks located in the black mask; linear
pixel->data fit on the major ticks. The seven curves are separated by colour (white-blend
classifier, fukplot.classify); per pixel column the centre of the curve's run of pixels nearest
the previous column's value is taken (digitize_common.trace_envelope). Columns where the curve
is covered by another curve, by the legend, by a tick mark or by the vertical red dashed line at 15 ps
(red series only) are left empty.
"""
import numpy as np

import digitize_common as dc
import fukplot as fp

SERIES = [("300K", (0, 0, 0)), ("350K", (255, 0, 0)), ("400K", (0, 0, 255)), ("450K", (255, 0, 255)),
          ("500K", (0, 128, 0)), ("550K", (0, 0, 128)), ("600K", (128, 0, 255))]


def extract(page, bbox, yvals):
    a = fp.load(page, bbox)
    dark = a.max(2) < 100
    rows = dc.frame_lines(dark, 1, 0.5)
    cols = dc.frame_lines(dark, 0, 0.5)
    top, bot = rows[0], rows[-1]
    left, right = cols[0], cols[-1]
    # inward major ticks (>= 7 px); interior only, then the frame edges are checked against the fit
    # ticks: low green channel (black ticks; the 15-ps tick is overdrawn by the red dashed line)
    tdark = a[:, :, 1] < 100
    xt = fp.inward_ticks_x(tdark, bot[0], -1, 7, left[1] + 2, right[0] - 1)
    yt = fp.inward_ticks_y(dark, left[1], 1, 7, top[1] + 2, bot[0] - 1)
    xvals = [5, 10, 15, 20]
    assert len(xt) == 4, xt
    yt = sorted(yt, reverse=True)
    assert len(yt) == len(yvals), (yt, yvals)
    fx, rx, mx = fp.fit(xt, xvals)
    fy, ry, my = fp.fit(yt, yvals)
    # legend box: the long vertical dark runs inside the frame, left part of the plot
    g = a.max(2) < 200
    vc = [c for c in range(left[1] + 3, (left[1] + right[0]) // 2) if g[top[1] + 2:bot[0] - 2, c].sum() > 150]
    lc0, lc1 = min(vc), max(vc)
    r = np.where(g[:, lc0])[0]
    runs = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
    run = max(runs, key=len)
    legend = (lc0 - 2, run[0] - 2, lc1 + 2, run[-1] + 2)
    lab, _ = fp.classify(a, [c for _, c in SERIES])
    # the dashed 15-ps marker: red pixel columns with a long vertical extent
    red = lab == 1
    redcount = red[top[1]:bot[0], :].sum(0)
    dashcols = np.where(redcount > 60)[0]
    # tick marks (major and minor, all four sides) are masked out of every series mask
    tickmask = np.zeros(dark.shape, bool)
    # positions of all ticks (major and minor) predicted from the fits: y every 0.5, x every 2.5
    inv_y = lambda v: (v - float(fy(0))) / my
    inv_x = lambda v: (v - float(fx(0))) / mx
    for v in np.arange(0, 50, 0.5):
        r = inv_y(v)
        if top[1] + 2 < r < bot[0] - 1:
            tickmask[int(round(r)) - 2:int(round(r)) + 3, left[1] + 1:left[1] + 12] = True
            tickmask[int(round(r)) - 2:int(round(r)) + 3, right[0] - 11:right[0]] = True
    for v in np.arange(0, 50, 2.5):
        c = inv_x(v)
        if left[1] + 2 < c < right[0] - 1:
            tickmask[bot[0] - 11:bot[0], int(round(c)) - 2:int(round(c)) + 3] = True
            tickmask[top[1] + 1:top[1] + 12, int(round(c)) - 2:int(round(c)) + 3] = True
    x0, x1 = left[1] + 2, right[0] - 1  # skip the anti-aliased column next to each frame line
    y0, y1 = top[1] + 1, bot[0]
    out = []
    for k, (name, _) in enumerate(SERIES):
        m = lab == k
        m[:, : left[1] + 1] = False
        m[:, right[0]:] = False
        m[: top[1] + 1, :] = False
        m[bot[0]:, :] = False
        m[legend[1]:legend[3] + 1, legend[0]:legend[2] + 1] = False
        m[tickmask] = False
        if k == 1:
            for c in dashcols:
                m[:, max(0, c - 3):c + 4] = False
        env = dc.trace_envelope(m, x0, x1, y0, y1, half_width=1.0, min_px=2)
        for c, ym, yu, yl in env:
            if ym == ym:
                out.append((name, float(fx(c)), float(fy(ym)), c, ym))
    info = dict(xt=xt, yt=yt, rx=rx, ry=ry, mx=mx, my=my, frame=(left, right, top, bot), legend=legend,
                dashcols=dashcols.tolist(), x_left=float(fx(left[0] + 0.5)), x_right=float(fx(right[0] + 0.5)),
                y_bot=float(fy(bot[0] + 0.5)), y_top=float(fy(top[0] + 0.5)))
    return a, out, info
