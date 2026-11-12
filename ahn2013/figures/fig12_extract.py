"""Digitize Fig. 12 (p. 8 of the PDF, journal p. 031104-7): FDTD results for a WGP with an opaque defect (the text,
p. 9, says a 250 nm x 250 nm opaque defect is modelled and "These results are shown in Fig. 12"). Two plotted panels
in one embedded Flate image (2087 x 775 px, 300 ppi; no vector paths on the page):
  left:  TM transmission (left axis, black solid) and TE transmission (right axis, blue dashed) vs wavelength,
         annotation box "Minimal change in transmission";
  right: extinction ratio vs wavelength (black solid), annotation box "Minimal change in extinction ratio".
Calibration and line following as in figures/fig11_extract.py: x from the major tick marks (400 ... 800 nm), y
from the tick marks of each axis (darkness centroids), lines as the smooth path of most ink (dynamic
programming), legend / annotation boxes and the circles with arrows masked; TE only where a dash is.
Writes figures/fig12left.csv, figures/fig12right.csv and work/fig12_overlay.png.

    python3 -I -B figures/fig12_extract.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "work"))
import digi  # noqa: E402

a = digi.image(8, (63.4, 59.8, 564.3, 245.8))
g = digi.gray(a)
hsv = digi.hsv(a)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
black_ink = np.where(S < 80, np.clip((200.0 - V) / 150.0, 0, 1), 0)
blue_ink = np.where((H >= 100) & (H <= 130) & (V < 245), np.clip((S - 30.0) / 150.0, 0, 1), 0)

X = [400, 500, 600, 700, 800]
PANELS = [
    dict(name="left", title=None, xt=((672, 676), 100, 910), cols=(116, 898), rows=(28, 659),
         left=dict(t=((103, 107), 30, 660), v=[0.9 - 0.1 * k for k in range(9)], label="TM transmission"),
         right=dict(t=((907, 911), 30, 660), v=[1.6e-3 - 4.0e-4 * k for k in range(4)], label="TE transmission"),
         axis_row=660.5, boxes=[(690, 15, 890, 113), (440, 220, 845, 350)],
         te_boxes=[(670, 505, 870, 570), (670, 596, 800, 625)]),
    dict(name="right", title=None, xt=((671, 675), 1250, 2087), cols=(1264, 2062), rows=(26, 658),
         left=dict(t=((1251, 1255), 30, 660), v=[3500 - 500 * k for k in range(7)], label="Extinction Ratio"),
         right=None, axis_row=660.0, boxes=[(1285, 78, 1700, 210)]),
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
    panel = "%s panel" % P["name"]
    hdr = [
        "Fig. 12, %s (ahn2013, PDF p. 8)%s: FDTD model, opaque 250 nm x 250 nm defect (text p. 9), %s." % (
            panel, ", title '%s'" % P["title"] if P["title"] else "",
            "transmission vs wavelength" if P["right"] else "extinction ratio vs wavelength"),
        "Columns: series (legend names; ER has no legend), axis (the y axis the series belongs to, by its label),",
        "wavelength_nm, value (centre of the line in that pixel column), value_min / value_max (edges of the line's",
        "ink in that column, i.e. the line width).",
        "Provenance: tier 3, digitized from the embedded Flate image (2087 x 775 px) with figures/fig12_extract.py;",
        "line followed as the smooth path of most ink (dynamic programming), one row per source pixel column",
        "(%.2f nm). x from the 5 major tick marks (max residual %.2f nm); %s." % (dx, rx, hdr_axes),
        "Uncertainty: about 1 px: +-%.1f nm in x, +-%.3g on the left axis%s." % (
            dx, abs(myl), (", +-%.2g on the right axis" % abs(digi.fit(yr, P["right"]["v"])[3])) if P["right"] else ""),
    ]
    if P["right"]:
        hdr.append("The left axis has tick labels 0.0 ... 1.0, the right axis 0.0 ... 2.0E-3; the ticks used are the")
        hdr.append("inner ones (the 1.0 / 2.0E-3 tick at the top and the 0 tick on the x-axis line are checks only).")
        hdr.append("Points more than 2.5 px off the local median (where an ellipse crosses the curve) are dropped.")
        hdr.append("TE is a dashed line: rows only where a dash is. The circles with arrows are annotations pointing")
        hdr.append("each curve to its axis (black: TM -> left axis, blue: TE -> right axis), not data; for TE the blue")
        hdr.append("circle above and below the curve and its arrow are masked (pixel boxes %s)." % P["te_boxes"])
    if P["boxes"]:
        hdr.append("Masked (no data read there): legend box and/or annotation text box, pixel boxes %s." % P["boxes"])
    digi.write_csv(os.path.join(HERE, "fig12%s.csv" % P["name"]), hdr,
                   ["series", "axis", "wavelength_nm", "value", "value_min", "value_max"], rows,
                   ["{}", "{}", "{:.1f}", "{:.5g}", "{:.5g}", "{:.5g}"])
digi.overlay(a, [((255, 0, 255), pts_k), ((0, 200, 0), pts_b)], os.path.join(ROOT, "work", "fig12_overlay.png"))
