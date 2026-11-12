"""Digitize Fig. 11 (p. 7 of the PDF, journal p. 031104-6): FDTD results for a defect-free WGP and a WGP with a
250 nm x 250 nm clear defect. Four plotted panels in one embedded Flate image (2087 x 1609 px, 300 ppi; no vector
paths on the page):
  (a) left  "Defect Free WGP":               TM transmission (left axis, black solid) and TE transmission (right
                                              axis, blue dashed) vs wavelength;
  (a) right "250nm x 250nm Clear Defect":    the same;
  (b) left / right: extinction ratio vs wavelength (black solid), same order (no titles of their own).
Calibration: x from the major tick marks (400 ... 800 nm), each y axis from its tick marks (darkness centroids;
the 0 tick coincides with the x-axis line and is used only as a check). Lines are followed as the smooth path of
most ink (dynamic programming, work/digi.py dp_series), with legend and annotation boxes masked; the circles and
arrows drawn around the curves are not data and are avoided by the smoothness penalty. The blue dashed TE line
is given only where a dash is.
Writes figures/fig11a_left.csv, fig11a_right.csv, fig11b_left.csv, fig11b_right.csv and work/fig11_overlay.png.

    python3 -I -B figures/fig11_extract.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "work"))
import digi  # noqa: E402

a = digi.image(7, (63.4, 329.2, 564.3, 715.3))
g = digi.gray(a)
hsv = digi.hsv(a)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
black_ink = np.where(S < 80, np.clip((200.0 - V) / 150.0, 0, 1), 0)
blue_ink = np.where((H >= 100) & (H <= 130) & (V < 245), np.clip((S - 30.0) / 150.0, 0, 1), 0)

X = [400, 500, 600, 700, 800]
PANELS = [
    dict(name="a_left", title="Defect Free WGP", xt=((711, 715), 100, 900), cols=(116, 879), rows=(118, 699),
         left=dict(t=((102, 106), 50, 690), v=[1.0 - 0.1 * k for k in range(10)], label="TM Transmission"),
         right=dict(t=((884, 888), 50, 690), v=[2.0e-3 - 2.0e-4 * k for k in range(10)], label="TE Transmission"),
         axis_row=700.5, boxes=[(670, 110, 880, 200)], te_boxes=[(640, 570, 880, 618), (640, 642, 800, 690)]),
    dict(name="a_right", title="250nm x 250nm Clear Defect", xt=((706, 710), 1160, 1960), cols=(1176, 1938),
         rows=(114, 694),
         left=dict(t=((1162, 1166), 40, 690), v=[1.0 - 0.1 * k for k in range(10)], label="TM Transmission"),
         right=dict(t=((1944, 1948), 40, 690), v=[1.0e-2 - 1.0e-3 * k for k in range(10)], label="TE Transmission"),
         axis_row=695.5, boxes=[(1730, 108, 1940, 198), (1500, 295, 1905, 420)], te_boxes=[(1725, 555, 1940, 590), (1725, 622, 1870, 665)]),
    dict(name="b_left", title=None, xt=((1476, 1480), 130, 1040), cols=(146, 924), rows=(870, 1463),
         left=dict(t=((132, 136), 850, 1460), v=[4000 - 500 * k for k in range(8)], label="Extinction Ratio"),
         right=None, axis_row=1465.0, boxes=[]),
    dict(name="b_right", title=None, xt=((1479, 1483), 1160, 2087), cols=(1171, 1901), rows=(876, 1466),
         left=dict(t=((1157, 1161), 850, 1460), v=[1000 - 200 * k for k in range(5)], label="Extinction Ratio"),
         right=None, axis_row=1468.0, boxes=[(1200, 970, 1635, 1140)]),
]
pts_k, pts_b = [], []
for P in PANELS:
    xt = digi.ticks_x(g, *P["xt"], thr=30)
    assert len(xt) == 5, (P["name"], xt)
    fx, _, rx, _ = digi.fit(xt, X)
    yl = digi.ticks_y(g, *P["left"]["t"], thr=30)
    yl = [t for t in yl if t < P["axis_row"] - 5]
    assert len(yl) == len(P["left"]["v"]), (P["name"], yl)
    fyl, _, ryl, myl = digi.fit(yl, P["left"]["v"])
    msg = "%s: x res %.2f nm; left y res %.3g, axis -> %.3g" % (P["name"], rx, ryl, fyl(P["axis_row"]))
    c0, c1 = P["cols"]
    r0, r1 = P["rows"]
    rows = []
    k = digi.dp_series(black_ink, c0, c1, r0, r1, P["boxes"], jump=6, lam=0.05)
    lname = "TM" if P["right"] else "ER"
    for c, mid, top, bot in k:
        if mid == mid:
            rows.append([lname, P["left"]["label"], float(fx(c)), float(fyl(mid)), float(fyl(bot)), float(fyl(top))])
            pts_k.append((c, mid))
    hdr_axes = "left y axis from %d tick marks (max residual %.3g; the x-axis line maps to %.3g)" % (
        len(yl), ryl, fyl(P["axis_row"]))
    if P["right"]:
        yr = digi.ticks_y(g, *P["right"]["t"], thr=30)
        yr = [t for t in yr if t < P["axis_row"] - 5]
        assert len(yr) == len(P["right"]["v"]), (P["name"], yr)
        fyr, _, ryr, _ = digi.fit(yr, P["right"]["v"])
        msg += "; right y res %.3g, axis -> %.3g" % (ryr, fyr(P["axis_row"]))
        hdr_axes += ", right y axis from %d tick marks (max residual %.3g)" % (len(yr), ryr)
        # the blue circle's upper arc and the arrow above the TE curve (te_boxes) are masked as well
        b = digi.dp_series(blue_ink, c0, c1, r0, r1, P["boxes"] + P["te_boxes"], jump=5, lam=0.0, quad=0.05)
        b = digi.despike(b, win=15, tol=2.5)   # where an ellipse crosses the curve
        for c, mid, top, bot in b:
            if mid == mid:
                rows.append(["TE", P["right"]["label"], float(fx(c)), float(fyr(mid)), float(fyr(bot)), float(fyr(top))])
                pts_b.append((c, mid))
    print(msg, "rows", len(rows))
    dx = 400.0 / (xt[-1] - xt[0])
    panel = "(%s), %s panel" % (P["name"][0], P["name"].split("_")[1])
    hdr = [
        "Fig. 11 %s (ahn2013, PDF p. 7)%s: FDTD model, %s." % (
            panel, ", title '%s'" % P["title"] if P["title"] else "",
            "transmission vs wavelength" if P["right"] else "extinction ratio vs wavelength"),
        "Columns: series (legend names; ER has no legend), axis (the y axis the series belongs to, by its label),",
        "wavelength_nm, value (centre of the line in that pixel column), value_min / value_max (edges of the line's",
        "ink in that column, i.e. the line width).",
        "Provenance: tier 3, digitized from the embedded Flate image (2087 x 1609 px) with figures/fig11_extract.py;",
        "line followed as the smooth path of most ink (dynamic programming), one row per source pixel column",
        "(%.2f nm). x from the 5 major tick marks (max residual %.2f nm); %s." % (dx, rx, hdr_axes),
        "Uncertainty: about 1 px: +-%.1f nm in x, +-%.3g on the left axis%s." % (
            dx, abs(myl), (", +-%.2g on the right axis" % abs(digi.fit(yr, P["right"]["v"])[3])) if P["right"] else ""),
    ]
    if P["right"]:
        hdr.append("Points more than 2.5 px off the local median (where an ellipse crosses the curve) are dropped.")
        hdr.append("TE is a dashed line: rows only where a dash is. The circles with arrows are annotations pointing")
        hdr.append("each curve to its axis (black: TM -> left axis, blue: TE -> right axis), not data; for TE the blue")
        hdr.append("circle above and below the curve and its arrow are masked (pixel boxes %s)." % P["te_boxes"])
    if P["boxes"]:
        hdr.append("Masked (no data read there): legend box and/or annotation text box, pixel boxes %s." % P["boxes"])
    digi.write_csv(os.path.join(HERE, "fig11%s.csv" % P["name"]), hdr,
                   ["series", "axis", "wavelength_nm", "value", "value_min", "value_max"], rows,
                   ["{}", "{}", "{:.1f}", "{:.5g}", "{:.5g}", "{:.5g}"])
digi.overlay(a, [((255, 0, 255), pts_k), ((0, 200, 0), pts_b)], os.path.join(ROOT, "work", "fig11_overlay.png"))
