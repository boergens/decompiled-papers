"""Extract Fig. 9 (p. 6 of the PDF, journal p. 031104-5) from its vector paths: GSolver model of WGPs with 100 nm
pitch ((a), (c)) and 130 nm pitch ((b), (d)) for four Al thicknesses; (a), (b) transmission, (c), (d) extinction
ratio (log axis). Tier 2 (vector): the plot is drawn as filled outlines in the PDF; every line, dash, tick mark
and glyph is a filled path (no stroked paths, no text), so tick values are read off the rendered figure.

How:
- axes: the tick marks are grey filled rectangles (one path per axis, one subpath per tick); x = 400 ... 800 nm
  (5 ticks), y = 0 ... 1 by 0.1 ((a), (b), 11 ticks) or 1.E+00 ... 1.E+09 ((c), (d), 10 ticks, log10).
  Linear fits through all ticks (residuals printed and written to the CSVs).
- series: four black filled paths per panel, one per Al thickness; a dashed series is one path with one closed
  subpath per dash. Which path is which thickness: by the number of dashes and the dash length, matched to the
  legend samples of (a) / (b) (100nmAl long dashes, 150nmAl short dashes, 200nmAl medium dashes, 250nmAl solid);
  the PDF draws them in that order in every panel.
- values: each outline (Bezier pieces flattened) is cut with vertical lines at every 10 nm (the outlines have a
  vertex every 3.1 pt = 10 nm, i.e. the data points); the centre of the stroke there is the midpoint between the
  lowest and highest crossing. Where a dash gap falls on a 10-nm position there is no value (dashed lines).
- the series outlines run far beyond the axes box (about 200 ... 1200 nm) and are hidden there by the PDF's clip
  path (the axes box); those values are kept with in_plot = 0 (not printed in the paper's figure), the printed
  part has in_plot = 1. Values outside the y range are left as computed (none occur inside the axes box).
Writes figures/fig9a.csv ... fig9d.csv and work/fig9_overlay.png (points over a 300-dpi render).

    python3 -I -B figures/fig9_extract.py
"""
import os
import sys

import numpy as np
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "tools"))
import digitize_common as dc  # noqa: E402

PDF = os.path.join(ROOT, "source", "ahn2013_jm3_12_3_031104.pdf")
page = pymupdf.open(PDF)[5]
draws = page.get_drawings()

# axes boxes = the clip rectangles the PDF sets for the series (PyMuPDF extended drawings)
PANELS = {
    "a": dict(clip=(169.13, 453.47, 302.13, 549.13), log=False, yv=[round(1.0 - 0.1 * k, 1) for k in range(11)]),
    "b": dict(clip=(347.44, 453.93, 477.26, 549.60), log=False, yv=[round(1.0 - 0.1 * k, 1) for k in range(11)]),
    "c": dict(clip=(179.48, 611.37, 303.70, 688.58), log=True, yv=[10.0 ** (9 - k) for k in range(10)]),
    "d": dict(clip=(349.39, 610.22, 478.87, 688.67), log=True, yv=[10.0 ** (9 - k) for k in range(10)]),
}
NAMES = ["100nmAl", "150nmAl", "200nmAl", "250nmAl"]
DASH = {"100nmAl": "long dashes", "150nmAl": "short dashes", "200nmAl": "medium dashes", "250nmAl": "solid"}


def subpaths(d, nb=10):
    """Closed polygons of a filled path, Bezier pieces flattened to nb segments."""
    polys, cur, last = [], [], None
    for it in d["items"]:
        op = it[0]
        if op == "l":
            p1, p2 = it[1], it[2]
            if last is None or abs(p1.x - last.x) > 1e-6 or abs(p1.y - last.y) > 1e-6:
                if cur:
                    polys.append(cur)
                cur = [(p1.x, p1.y)]
            cur.append((p2.x, p2.y))
            last = p2
        elif op == "c":
            p0, c1, c2, p3 = it[1], it[2], it[3], it[4]
            if last is None or abs(p0.x - last.x) > 1e-6 or abs(p0.y - last.y) > 1e-6:
                if cur:
                    polys.append(cur)
                cur = [(p0.x, p0.y)]
            for t in np.linspace(0, 1, nb + 1)[1:]:
                x = (1 - t) ** 3 * p0.x + 3 * (1 - t) ** 2 * t * c1.x + 3 * (1 - t) * t ** 2 * c2.x + t ** 3 * p3.x
                y = (1 - t) ** 3 * p0.y + 3 * (1 - t) ** 2 * t * c1.y + 3 * (1 - t) * t ** 2 * c2.y + t ** 3 * p3.y
                cur.append((x, y))
            last = p3
        elif op == "re":
            r = it[1]
            if cur:
                polys.append(cur)
            polys.append([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)])
            cur, last = [], None
    if cur:
        polys.append(cur)
    return polys


def slice_y(poly, x):
    """y of all crossings of the closed polygon with the vertical line at x."""
    ys = []
    n = len(poly)
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if (x0 - x) * (x1 - x) < 0 or (x0 == x and x1 != x):
            t = (x - x0) / (x1 - x0)
            ys.append(y0 + t * (y1 - y0))
    return ys


def fit(pix, vals, log):
    v = np.log10(vals) if log else np.asarray(vals, float)
    m, b = np.polyfit(pix, v, 1)
    res = float(np.max(np.abs(np.polyval([m, b], pix) - v)))
    return m, b, res


def grey(d):
    f = d.get("fill")
    return f is not None and abs(f[0] - f[1]) < 0.01 and 0.45 < f[0] < 0.6


summary = []
overlay_pts = []
for key, P in PANELS.items():
    x0, y0, x1, y1 = P["clip"]
    box = pymupdf.Rect(x0 - 4, y0 - 4, x1 + 4, y1 + 4)
    # tick paths: grey fills with one subpath per tick, just outside the left / bottom edge of the axes box
    ticks_y = [d for d in draws if grey(d) and box.intersects(d["rect"]) and d["rect"].x1 <= x0 + 0.5
               and d["rect"].width < 3 and len(d["items"]) >= 5]
    ticks_x = [d for d in draws if grey(d) and box.intersects(d["rect"]) and d["rect"].y0 >= y1 - 0.5
               and d["rect"].height < 3 and len(d["items"]) == 5]
    assert len(ticks_y) == 1 and len(ticks_x) == 1, (key, len(ticks_y), len(ticks_x))
    ty = sorted((r[1].y0 + r[1].y1) / 2 for r in ticks_y[0]["items"])
    tx = sorted((r[1].x0 + r[1].x1) / 2 for r in ticks_x[0]["items"])
    assert len(ty) == len(P["yv"]) and len(tx) == 5, (key, ty, tx)
    mx, bx, rx = fit(tx, [400, 500, 600, 700, 800], False)
    my, by, ry = fit(ty, P["yv"], P["log"])

    def X(px):
        return mx * px + bx

    def Y(py):
        v = my * py + by
        return 10 ** v if P["log"] else v

    def PX(nm):
        return (nm - bx) / mx

    # series: the four big black filled paths overlapping this axes box, in drawing order
    cx = (x0 + x1) / 2
    # the grey up-arrow ("Increasing Al thickness") of (c) / (d) is drawn over the series (#bfbfbf fill)
    arrows = [d["rect"] for d in draws if d.get("fill") is not None and abs(d["fill"][0] - 0.749) < 0.01
              and d["rect"].intersects(pymupdf.Rect(x0, y0, x1, y1))]
    ser = [d for d in draws if d.get("fill") is not None and max(d["fill"]) < 0.05 and d["rect"].width > 100
           and d["rect"].x0 < cx < d["rect"].x1 and d["rect"].y1 > y0 and d["rect"].y0 < y1
           and abs(d["rect"].x0 - (x0 - 65)) < 10]   # every panel's outlines start about 65 pt left of its box
    assert len(ser) == 4, (key, len(ser))
    nsub = [len(subpaths(d)) for d in ser]
    # median dash length (pt, along x) of each path, to match against the legend samples
    dlen = [round(float(np.median([max(q[0] for q in poly) - min(q[0] for q in poly) for poly in subpaths(d)])), 2)
            if len(subpaths(d)) > 1 else None for d in ser]
    rows = []
    for name, d in zip(NAMES, ser):
        polys = subpaths(d)
        xs_all = [p[0] for poly in polys for p in poly]
        lo_nm, hi_nm = X(min(xs_all)), X(max(xs_all))
        for nm in range(int(np.ceil(lo_nm / 10.0)) * 10, int(hi_nm) + 1, 10):
            px = PX(nm)
            ys = []
            for poly in polys:
                c = slice_y(poly, px)
                if len(c) >= 2:
                    ys.append((min(c), max(c)))
            if not ys:
                continue
            if len(ys) > 1:       # overlapping dashes / pieces: take the piece spanning the most
                ys.sort(key=lambda t: t[1] - t[0])
            top, bot = ys[-1]
            mid = (top + bot) / 2
            inside = (x0 - 1e-6 <= px <= x1 + 1e-6) and (y0 <= mid <= y1)
            under = any(r.x0 <= px <= r.x1 and r.y0 <= mid <= r.y1 for r in arrows)
            rows.append([name, nm, Y(mid), (bot - top), 1 if inside else 0, px, mid,
                         "under the grey arrow" if (inside and under) else ""])
            if inside:
                overlay_pts.append((px, mid))
    # stroke width (pt) from the solid series inside the box
    wid = np.median([r[3] for r in rows if r[0] == "250nmAl" and r[4] == 1])
    summary.append((key, rx, ry, nsub, wid))
    print(key, "median dash length per path (pt):", dlen)
    hdr = [
        "Fig. 9(%s) (ahn2013, PDF p. 6): GSolver model, %s pitch WGP (panel label '%s' in (c) / (d); caption: (a) 100-nm," % (
            key, "100-nm" if key in "ac" else "130-nm", "100nm pitch" if key in "ac" else "130nm pitch"),
        "(b) 130-nm pitch), %s vs wavelength for Al thicknesses 100, 150, 200, 250 nm (legend: 100nmAl ... 250nmAl)." % (
            "transmission (axis label 'Transmission (%)', ticks 0 ... 1)" if not P["log"] else "extinction ratio (log axis)"),
        "Columns: series (legend name), wavelength_nm, value (%s), in_plot (1 = inside the axes box, printed;" % (
            "transmission as plotted, 0 ... 1" if not P["log"] else "extinction ratio"),
        "0 = part of the vector outline outside the axes box, hidden by the PDF's clip path, not visible in the paper),",
        "x_pt, y_pt (stroke centre on the PDF page, points, origin top left).",
        "Provenance: tier 2, vector paths in the PDF (filled stroke outlines), figures/fig9_extract.py: outlines cut at",
        "every 10 nm, centre between the outline edges; exact up to the PDF's precision (0.001 pt) and the flattening",
        "of the curved joins. Axes: linear fits through the grey tick marks, x 5 ticks (max residual %.3f nm), y %d" % (
            rx, len(ty)),
        "ticks (max residual %.2g %s). Tick values read off the figure (the labels are outlines too)." % (
            ry, "decades" if P["log"] else ""),
        "Series by dash pattern, in drawing order: subpaths per path %s, median dash length %s pt; legend" % (nsub, dlen),
        "samples: 100nmAl 9.3 pt dashes (with a short piece), 150nmAl 3.5 pt, 200nmAl 4.7 pt, 250nmAl solid. Dashed",
        "series have no value where a 10-nm position falls into a dash gap.",
        "Stroke width about %.2f pt = %.2g %s; values at overlaps of two lines are still exact (each line is its own" % (
            wid, (wid * abs(my)), "decades" if P["log"] else ""),
        "path).",
    ]
    if P["log"]:
        hdr.append("The y axis is log10, labels 1.E+00 ... 1.E+09. note = 'under the grey arrow': inside the bounding box of")
        hdr.append("the grey arrow 'Increasing Al thickness', which is drawn over the lines (hidden in print, value from the path).")
    dc.write_csv(os.path.join(HERE, "fig9%s.csv" % key), hdr,
                 ["series", "wavelength_nm", "value", "in_plot", "x_pt", "y_pt", "note"],
                 [[r[0], r[1], r[2], r[4], r[5], r[6], r[7]] for r in rows],
                 ["{}", "{}", "{:.5g}", "{}", "{:.3f}", "{:.3f}", "{}"])
    print(key, "x res %.4f nm, y res %.3g" % (rx, ry), "subpaths", nsub, "width %.2f pt" % wid,
          "rows", len(rows), "in plot", sum(r[4] for r in rows))

# legend samples of (a) and (b): dash lengths, to confirm the series order
for lx0, lx1 in ((250, 271), (428, 449)):
    for d in draws:
        r = d["rect"]
        if d.get("fill") is not None and max(d["fill"]) < 0.05 and lx0 <= r.x0 and r.x1 <= lx1 + 1 and 495 < r.y0 < 545 \
                and r.height < 2:
            ps = subpaths(d)
            print("legend sample y %.1f: %d pieces, lengths %s pt" % (
                r.y0, len(ps), [round(max(p[0] for p in q) - min(p[0] for p in q), 2) for q in ps]))
# overlay on a 300-dpi render of the figure
clip = pymupdf.Rect(100, 449, 486, 726)
zoom = 300 / 72
pix = page.get_pixmap(dpi=300, clip=clip)
img = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()
dc.overlay(img, [((x - clip.x0) * zoom, (y - clip.y0) * zoom) for x, y in overlay_pts],
           os.path.join(ROOT, "work", "fig9_overlay.png"))
