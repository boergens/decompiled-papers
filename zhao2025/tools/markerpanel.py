"""Shared extraction for zhao2025's vector scatter panels with error bars (Figs. 4a, 4b, 5a, 5b).

A panel = filled square markers (one colour), error bars (stroked lines or thin filled rectangles) and a dash-dot
fit line drawn as filled dash polygons. Writes one CSV and an overlay PNG.
"""
import numpy as np
import pymupdf
from PIL import Image, ImageDraw

import vecplot as vp


def extract(pdf, pno, box, X, Y, marker_color, fit_index, csv_path, overlay_path, head, xname, yname,
            tearing_last=True, marker_size=(3.5, 5.5), legend_box=None):
    pg = vp.page(pdf, pno)
    ds = vp.drawings_in(pg, box)
    segs = [s for s in vp.segments(ds) if s["color"] == marker_color]   # bars in the marker colour only
    marks = []
    for d in ds:
        its = d["items"]
        if d["type"] == "f" and d["fillc"] == marker_color and len(its) == 1 and its[0][0] == "re":
            r = its[0][1]
            if marker_size[0] <= r.width <= marker_size[1] and marker_size[0] <= r.height <= marker_size[1]:
                if legend_box and legend_box[0] <= r.x0 and r.x1 <= legend_box[2] and legend_box[1] <= r.y0 and r.y1 <= legend_box[3]:
                    continue   # legend sample marker
                marks.append(d)
    marks.sort(key=lambda d: d["rect"].x0)
    rows, ov = [], []
    for n, d in enumerate(marks):
        cx, cy = vp.bbox_centre(d)
        eb = vp.error_bars(cx, cy, segs)
        # data point: x from a vertical bar line or the junction of two horizontal half-bars, else the square's centre
        if eb["x_bar"] is not None:
            px, sx = eb["x_bar"], "vbar"
        elif eb.get("x_junction") is not None:
            px, sx = eb["x_junction"], "hjunction"
        else:
            px, sx = cx, "marker"
        if eb["y_bar"] is not None:
            py, sy = eb["y_bar"], "hbar"
        elif eb.get("y_junction") is not None:
            py, sy = eb["y_junction"], "vjunction"
        else:
            py, sy = cy, "marker"
        if abs(px - cx) > 0.3 or abs(py - cy) > 0.3:
            px, py, sx, sy = cx, cy, "marker", "marker"   # bars not centred on this square: use the square
        yl = yh = xl = xh = ""
        if eb["y_caps"]:
            c = [Y(v) for v in eb["y_caps"]]
            yl, yh = round(float(min(c)), 5), round(float(max(c)), 5)
        if eb["x_caps"]:
            c = [X(v) for v in eb["x_caps"]]
            xl, xh = round(float(min(c)), 5), round(float(max(c)), 5)
        series = "Tearing-induced" if (tearing_last and n == len(marks) - 1) else "Cutting-induced"
        centre_src = sx + "/" + sy
        rows.append([series, round(float(X(px)), 5), round(float(Y(py)), 5), xl, xh, yl, yh,
                     round(float(X(cx)), 5), round(float(Y(cy)), 5), centre_src])
        ov.append((px, py, (0, 200, 0), 3))
        for v in eb["y_caps"]:
            ov.append((px, v, (255, 0, 255), 2))
        for v in eb["x_caps"]:
            ov.append((v, py, (255, 0, 255), 2))
    m, c, xa, xb, res = vp.fit_line_vertices(pg.get_drawings()[fit_index])
    fx = [xa, xb]
    fy = [m * xa + c, m * xb + c]
    dx = X(fx); dy = Y(fy)
    slope = (dy[1] - dy[0]) / (dx[1] - dx[0])
    icpt = dy[0] - slope * dx[0]
    for xx, yy in zip(fx, fy):
        ov.append((xx, yy, (0, 120, 255), 4))
    tail = [
        "Fit line (red dash-dot, drawn as filled dash polygons; least-squares line through all their vertices, max",
        f"  vertex offset {res:.2f} pt = line half-width): from {xname} = {dx[0]:.4g} to {dx[1]:.4g}, i.e. {yname} = {slope:.5g} * {xname} + ({icpt:.5g}).",
        "  The paper prints no equation for this line; these numbers are read off the drawing.",
    ]
    vp.write_csv(csv_path, head + tail, ["series", "x", "y", "x_err_low", "x_err_high", "y_err_low", "y_err_high",
                                         "marker_box_centre_x", "marker_box_centre_y", "centre_from"], rows)
    z = 6
    clip = pymupdf.Rect(*box)
    pix = pg.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    for x, y, col, rad in ov:
        u, v = (x - clip.x0) * z, (y - clip.y0) * z
        dr.ellipse((u - rad, v - rad, u + rad, v + rad), outline=col, width=2)
    im.save(overlay_path)
    return rows, (slope, icpt, dx)
