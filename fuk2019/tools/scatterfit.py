"""Extraction shared by fig10a/b and fig11a/b: black square markers (optionally with error bars),
two red fitted straight lines and the red dot at their crossing, in an Origin raster export.

Method (tier 3, digitized):
- frame and inward major tick marks located in the black mask; linear pixel->data fit per axis;
- markers: connected components of the black mask (max channel < 110) near the predicted column
  of each temperature 300, 350, ..., 600 K; the marker centre is the centre of the component's
  solid block (rows and columns where the component is at least 60 % of the marker width);
  error bars (fig11): the component's top and bottom rows (the caps), shifted inward by half a
  line width (1 px);
- red: white-blend colour classifier (fukplot.classify). The dot is what survives a morphological
  opening with a disk of `dot_open` px; each line is fitted (least squares, row centre per column)
  on the columns where it is the only red line, and its end points are the extreme columns that
  still have red pixels within 2 px of the fitted line.
"""
import numpy as np

import digitize_common as dc
import fukplot as fp


def calibrate(a, xvals, yvals, tick_len=6):
    dark = a.max(2) < 100
    rows = dc.frame_lines(dark, 1, 0.5)
    cols = dc.frame_lines(dark, 0, 0.5)
    top, bot, left, right = rows[0], rows[-1], cols[0], cols[-1]
    xt = fp.inward_ticks_x(dark, bot[0], -1, tick_len, left[1] + 2, right[0] - 1)
    yt = sorted(fp.inward_ticks_y(dark, left[1], 1, tick_len, top[1] + 2, bot[0] - 1), reverse=True)
    assert len(xt) == len(xvals), (xt, xvals)
    assert len(yt) == len(yvals), (yt, yvals)
    fx, rx, mx = fp.fit(xt, xvals)
    fy, ry, my = fp.fit(yt, yvals)
    return dict(fx=fx, fy=fy, rx=rx, ry=ry, mx=mx, my=my, xt=xt, yt=yt, top=top, bot=bot, left=left,
                right=right, x_left=float(fx(left[0] + 0.5)), x_right=float(fx(right[0] + 0.5)),
                y_bot=float(fy(bot[0] + 0.5)), y_top=float(fy(top[0] + 0.5)))


def markers(a, cal, temps, exclude, size, errorbars=False):
    """One marker per temperature. exclude: list of pixel boxes (x0, y0, x1, y1) to ignore.

    In a window of +-size columns around the predicted column of each temperature, the marker
    is the longest group of rows with >= 60 % of `size` black pixels; its columns are those with
    >= 60 % of that group's height. A marker partly covered by red (fit line or dot) is flagged.
    Error bars: from the marker centre column (+-1 px), black pixels are followed up and
    down from the marker (gaps of up to 3 px bridged); the ends are the caps.
    """
    blk = a.max(2) < 110
    lab, _ = fp.classify(a, [(255, 0, 0), (0, 0, 0)])
    red = lab == 0
    for m in (blk, red):
        m[: cal["top"][1] + 3, :] = False
        m[cal["bot"][0] - 2:, :] = False
        m[:, : cal["left"][1] + 3] = False
        m[:, cal["right"][0] - 2:] = False
        for x0, y0, x1, y1 in exclude:
            m[y0:y1, x0:x1] = False
    inv_x = lambda v: (v - float(cal["fx"](0))) / cal["mx"]
    out = []
    for T in temps:
        cx = int(round(inv_x(T)))
        c0, c1 = cx - size, cx + size + 1
        prof = blk[:, c0:c1].sum(1)
        rows = np.where(prof >= 0.6 * size)[0]
        groups = np.split(rows, np.where(np.diff(rows) > 2)[0] + 1)
        g = max(groups, key=len)
        r0, r1 = int(g.min()), int(g.max())
        colprof = blk[r0:r1 + 1, c0:c1].sum(0)
        cols = c0 + np.where(colprof >= 0.6 * (r1 - r0 + 1))[0]
        px = (cols.min() + cols.max()) / 2
        py = (r0 + r1) / 2
        covered = bool(red[r0 - 1:r1 + 2, cols.min() - 1:cols.max() + 2].sum() > 3)
        h_nom = len(cols)            # markers are square: nominal height = visible width
        note = ""
        if r1 - r0 + 1 < h_nom - 1:
            # partly hidden under red: keep the edge away from the red and use the nominal size
            cs = slice(int(cols.min()), int(cols.max()) + 1)
            red_above = red[max(0, r0 - 4):r0, cs].sum()
            red_below = red[r1 + 1:r1 + 5, cs].sum()
            if red_above > red_below:
                py = r1 - (h_nom - 1) / 2
                note = "top part hidden by red; centre = bottom edge - half the marker width"
            else:
                py = r0 + (h_nom - 1) / 2
                note = "bottom part hidden by red; centre = top edge + half the marker width"
        rec = dict(T_label=T, px=px, py=py, x=float(cal["fx"](px)), y=float(cal["fy"](py)),
                   marker_w_px=int(cols.max() - cols.min() + 1), marker_h_px=r1 - r0 + 1, red_overlap=covered,
                   note=note)
        if errorbars:
            band = blk[:, int(round(px)) - 1:int(round(px)) + 2].any(1)
            top = r0
            while top > 4 and band[top - 4:top].any():   # bridges gaps of up to 3 px (red line on top)
                top -= 1
            while not band[top]:
                top += 1
            bot = r1
            while bot + 5 < len(band) and band[bot + 1:bot + 5].any():
                bot += 1
            while not band[bot]:
                bot -= 1
            top_px, bot_px = float(top), float(bot)   # caps are 1-px lines (no anti-aliasing)
            rec.update(err_top_px=top_px, err_bot_px=bot_px, y_err_high=float(cal["fy"](top_px)),
                       y_err_low=float(cal["fy"](bot_px)))
        out.append(rec)
    return out


def red_parts(a, cal, dot_open, split_px, exclude=()):
    import cv2
    lab, _ = fp.classify(a, [(255, 0, 0), (0, 0, 0)])
    red = lab == 0
    red[: cal["top"][1] + 2, :] = False
    red[cal["bot"][0] - 1:, :] = False
    red[:, : cal["left"][1] + 2] = False
    red[:, cal["right"][0] - 1:] = False
    for x0, y0, x1, y1 in exclude:
        red[y0:y1, x0:x1] = False
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dot_open, dot_open))
    dot = cv2.morphologyEx(red.astype(np.uint8), cv2.MORPH_OPEN, k).astype(bool)
    comps = fp.components(dot, min_size=5)
    r, c = max(comps, key=lambda q: len(q[0]))
    dot_px, dot_py = c.mean(), r.mean()
    lines = red & ~cv2.dilate(dot.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    res = dict(dot_px=dot_px, dot_py=dot_py, dot_x=float(cal["fx"](dot_px)), dot_y=float(cal["fy"](dot_py)))
    for name, cols in (("low", range(cal["left"][1] + 2, int(dot_px - split_px))),
                       ("high", range(int(dot_px + split_px), cal["right"][0] - 1))):
        xs, ys = [], []
        for cc in cols:
            rr = np.where(lines[:, cc])[0]
            if len(rr) == 0:
                continue
            runs = np.split(rr, np.where(np.diff(rr) > 2)[0] + 1)
            if len(runs) != 1 or len(rr) > 8:
                continue
            xs.append(cc)
            ys.append(rr.mean())
        xs, ys = np.array(xs, float), np.array(ys, float)
        m, b = np.polyfit(xs, ys, 1)
        rms = float(np.sqrt(np.mean((m * xs + b - ys) ** 2)))
        # extreme columns with red pixels within 2 px of the line
        rr, cc = np.where(lines)
        near = np.abs(m * cc + b - rr) <= 2.0
        c_lo, c_hi = cc[near].min(), cc[near].max()
        res[name] = dict(slope_px=m, icpt_px=b, rms_px=rms, n_cols=len(xs), c0=float(c_lo), c1=float(c_hi),
                         x0=float(cal["fx"](c_lo)), y0=float(cal["fy"](m * c_lo + b)),
                         x1=float(cal["fx"](c_hi)), y1=float(cal["fy"](m * c_hi + b)))
        L = res[name]
        L["slope"] = (L["y1"] - L["y0"]) / (L["x1"] - L["x0"])
        L["intercept"] = L["y0"] - L["slope"] * L["x0"]
    lo, hi = res["low"], res["high"]
    xi = (hi["intercept"] - lo["intercept"]) / (lo["slope"] - hi["slope"])
    res["crossing_x"] = xi
    res["crossing_y"] = lo["intercept"] + lo["slope"] * xi
    return res
