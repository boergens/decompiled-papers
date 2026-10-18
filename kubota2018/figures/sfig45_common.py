"""Shared digitizing code for Supplementary Figs. 4d-g and 5d-g of kubota2018 (tier 3).

Each panel is a small line plot (about 120 x 110 px in the embedded 150-184 ppi JPEG) with
coloured markers at a few nominal x positions joined by solid or dashed lines. Method:
  1. find the tick marks on the y axis (left of the axis line) and the x axis (below it) in the
     dark mask, and fit a linear pixel -> value map to the tick labels read off the image;
  2. at each nominal x position (from the x calibration), classify the pixels in a narrow
     column window by colour (HSV hue/saturation classes) and take the centroid of the
     largest blob of each series colour as the marker centre;
  3. a series whose marker is hidden under another marker gives no blob (or too few pixels):
     its value is left empty and flagged 'hidden'.
"""
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig_common import WORK, read_csv, si_image  # noqa: E402,F401
from digitize_common import fit_axis, overlay, write_csv  # noqa: E402,F401

COLOURS = {
    # name: (hue ranges in OpenCV 0..180, min saturation, min value, max value)
    "red": ([(0, 7), (170, 180)], 110, 110, 256),
    "orange": ([(11, 26)], 100, 150, 256),
    "blue": ([(104, 126)], 110, 90, 256),
    "magenta": ([(138, 166)], 60, 120, 256),
    "cyan": ([(82, 100)], 60, 150, 256),
    "gray": ([(0, 180)], -1, 95, 175),   # low-saturation mid grey (saturation < 45, checked below)
    "black": ([(0, 180)], -1, 0, 95),    # dark, low saturation
}


def colour_mask(img, name):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(int)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    ranges, smin, vmin, vmax = COLOURS[name]
    m = np.zeros(h.shape, bool)
    for lo, hi in ranges:
        m |= (h >= lo) & (h < hi)
    if smin < 0:
        m &= s < 45
    else:
        m &= s >= smin
    m &= (v >= vmin) & (v < vmax)
    return m


def ticks_left(g, col_axis, r0, r1, length=4, thr=170, frac=0.75):
    """Rows (centres) of tick marks in the `length` columns just left of the y-axis line."""
    band = g[r0:r1, col_axis - length:col_axis] < thr
    rows = np.where(band.mean(1) >= frac)[0]
    if not len(rows):
        return []
    groups = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
    return [r0 + float(np.mean(q)) for q in groups]


def ticks_below(g, row_axis, c0, c1, length=3, thr=170, frac=0.99):
    band = g[row_axis + 1:row_axis + 1 + length, c0:c1] < thr
    cols = np.where(band.mean(0) >= frac)[0]
    if not len(cols):
        return []
    groups = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1)
    return [c0 + float(np.mean(q)) for q in groups]


def marker_centre(mask, xc, r0, r1, half=3, min_px=5):
    """Centroid of the largest blob of `mask` within columns xc +- half and rows r0..r1."""
    c0, c1 = int(round(xc)) - half, int(round(xc)) + half + 1
    sub = mask[r0:r1, c0:c1].astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(sub, 8)
    if n <= 1:
        return np.nan, np.nan, 0
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    area = int(st[i, cv2.CC_STAT_AREA])
    if area < min_px:
        return np.nan, np.nan, area
    return c0 + cen[i][0], r0 + cen[i][1], area


PLOT_COLOURS = {"red": "#e0202a", "orange": "#f0a830", "blue": "#2050d0", "magenta": "#e060c8",
                "cyan": "#40e8e8", "gray": "#808080", "black": "#000000"}


def run_panel(cfg, img=None):
    """Digitize one panel described by cfg (see sfig4_extract.py); returns (rows, overlay points, info)."""
    if img is None:
        img = si_image(cfg["page"])
    g = img.astype(float).mean(2)
    yt = ticks_left(g, cfg["ycol"], cfg["y0"], cfg["row"] + 1)
    xt = ticks_below(g, cfg["row"], cfg["xcol0"], img.shape[1])
    assert len(yt) == len(cfg["yvals"]), (cfg["name"], yt)
    assert len(xt) == len(cfg["xvals"]), (cfg["name"], xt)
    fy, ry, my = fit_axis(yt, cfg["yvals"])
    fx, rx, mx = fit_axis(xt, cfg["xvals"])
    masks = {}
    rows, ov = [], []
    for label, colour, _style in cfg["series"]:
        if colour not in masks:
            masks[colour] = colour_mask(img, colour)
        for x in cfg["xs"]:
            xc = float(np.interp(x, cfg["xvals"], xt))
            r0, r1 = cfg["y0"], cfg.get("rmax", cfg["row"] - 1)
            for lim in cfg.get("limits", []):
                if (lim[0] is None or abs(lim[0] - x) < 1e-6) and (lim[1] is None or lim[1] == colour):
                    r0, r1 = max(r0, lim[2]), min(r1, lim[3])
            cx, cy, area = marker_centre(masks[colour], xc, r0, r1, min_px=3)
            printed = cfg.get("printed", {}).get((label, x), "")
            if cy == cy:
                status = "ok" if area >= 8 else "partly hidden (small blob)"
                rows.append((label, x, float(fx(cx)), float(fy(cy)), area, status, printed, cx, cy))
                ov.append((cx, cy))
            else:
                rows.append((label, x, np.nan, np.nan, area, "hidden under other markers", printed, np.nan, np.nan))
    info = dict(res_y=ry, res_x=rx, unit_y=abs(my), unit_x=abs(mx), yt=yt, xt=xt)
    return rows, ov, info


def write_panel(cfg, rows, info, path, extra_header=()):
    hdr = [
        cfg["title"],
        f"columns: series (legend text), x_nominal ({cfg['xname']}), x_digitized, y ({cfg['yname']}),"
        " marker_px (pixels in the colour blob found), status, printed_panel_c (the depth printed under the"
        " imaged square in panel c of the same figure, where it belongs to this point; empty otherwise),"
        " pixel_x, pixel_y (marker centre in the embedded image)",
        f"provenance: tier 3, digitized from the embedded raster image of SI page {cfg['page']}"
        f" ({cfg['imgdesc']}), native resolution; script {cfg['script']}",
        "method: ticks found in the image and fitted to the printed tick labels; at each nominal x the"
        " pixels of each series colour (HSV class) in a 7-px-wide column window are grouped into blobs and"
        " the centroid of the largest blob is the marker centre",
        f"axis fit: y on {len(info['yt'])} ticks {cfg['yvals'][0]}..{cfg['yvals'][-1]}, max residual"
        f" {info['res_y']:.3g}; x on {len(info['xt'])} ticks {cfg['xvals'][0]}..{cfg['xvals'][-1]},"
        f" max residual {info['res_x']:.3g}",
        f"uncertainty: about 1-2 source pixels = {info['unit_y']:.2g}-{2 * info['unit_y']:.2g} in y"
        f" (1 px = {info['unit_y']:.3g}); markers that overlap other markers are less certain",
        "status 'hidden under other markers': the series colour was not found at that x (the marker is"
        " covered by another series' marker); 'partly hidden': fewer than 8 pixels of its colour visible",
    ] + list(extra_header)
    write_csv(path, hdr, ["series", "x_nominal", "x_digitized", "y", "marker_px", "status", "printed_panel_c",
                          "pixel_x", "pixel_y"], rows,
              fmt=["{}", "{:g}", "{:.3f}", "{:.4g}", "{}", "{}", "{}", "{:.2f}", "{:.2f}"])


def replot(csv_path, out_png, series, xlim, xticks, ylim, yticks, xlabel, ylabel, legend=True, annotate=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = read_csv(csv_path)
    fig, ax = plt.subplots(figsize=(2.6, 2.4))
    for label, colour, style in series:
        r = [q for q in rows if q["series"] == label and q["y"] != ""]
        xs = [float(q["x_nominal"]) for q in r]
        ys = [float(q["y"]) for q in r]
        ax.plot(xs, ys, ls="--" if style == "dashed" else "-", marker="o", ms=3.5, lw=1.2,
                color=PLOT_COLOURS[colour], label=label)
    ax.set_xlim(*xlim)
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{t:g}" for t in xticks])
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(labelsize=7)
    if legend:
        ax.legend(fontsize=6, frameon=False)
    if annotate:
        ax.text(*annotate, transform=ax.transAxes, fontsize=7, ha="right")
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
