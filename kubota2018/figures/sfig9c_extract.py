"""Supplementary Fig. 9c (kubota2018 SI p. 19): trace the 11 Monte Carlo curves in both panels
('Backscattered electrons' and 'Primary (absorbed) electrons'), tier 3 with gaps.

Source: the embedded figure image of SI page 19 (987 x 1225 px JPEG, 167 ppi), native resolution.
Each panel plots number of electrons (top x axis) against depth (y axis, nm). The 11 series come in
colour pairs, solid = lower energy, dashed = the next 0.5 keV: red 1 / 1.5 keV, blue 2 / 2.5,
orange 3 / 3.5, purple 4 / 4.5, magenta 5 / 5.5, black 6 keV (legend right of the panels).

Method: pixels are classified by colour (HSV). Within one colour, connected components of 40 px or
more are the solid curve, components of 4-39 px are the dashes (dots) of the dashed curve. The solid
curve is traced row by row (one row = one depth): x_lo, x_hi are the ends of the run in that row (a
near-horizontal stretch covers many columns), x their mean. Each dash gives one point (its
centroid; x_lo/x_hi = its horizontal extent). Where curves cross, pieces of a solid curve can be cut
below 40 px and then count as dashes, and dashes touching a solid curve join it; the overlays show
where. Writes sfig9c.csv and ../work/supp_sfig9c_overlay_*.png.
"""
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig45_common import WORK, fit_axis, si_image, write_csv  # noqa: E402

img = si_image(19)
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(int)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
CLS = {
    "red": ((H <= 6) | (H >= 170)) & (S > 90) & (V > 100),
    "blue": (H >= 106) & (H <= 122) & (S > 80),
    "orange": (H >= 12) & (H <= 28) & (S > 60) & (V > 150),
    "purple": (H >= 124) & (H <= 140) & (S > 80),
    "magenta": (H >= 148) & (H <= 168) & (S > 70),
    "black": (V < 90) | ((V < 120) & (S < 60)),  # JPEG chroma bleed gives dark pixels high S
}
PAIRS = [("red", "1 keV", "1.5 keV"), ("blue", "2 keV", "2.5 keV"), ("orange", "3 keV", "3.5 keV"),
         ("purple", "4 keV", "4.5 keV"), ("magenta", "5 keV", "5.5 keV"), ("black", "6 keV", None)]

# Panel geometry in the embedded image (axis lines and ticks located in the image; tick labels read off it)
PANELS = {
    "Backscattered electrons": dict(
        axis_row=752, axis_col=242, rows=(754, 945), cols=(243, 404),
        yt=[752.0, 788.0, 824.0, 860.5, 897.0, 932.5], yv=[0, -100, -200, -300, -400, -500],
        xt=[244, 276, 308, 340, 373], xv=[0, 50, 100, 150, 200], x_break=390),
    "Primary (absorbed) electrons": dict(
        axis_row=751, axis_col=549, rows=(753, 950), cols=(550, 716),
        yt=[751.0, 778.0, 806.0, 833.0, 860.0, 887.0, 915.0, 942.0],
        yv=[0, -200, -400, -600, -800, -1000, -1200, -1400],
        xt=[552, 579.5, 605.5, 632, 658.5, 685.5, 712.5], xv=[0, 500, 1000, 1500, 2000, 2500, 3000], x_break=None),
}


def runs_of(row_mask, c0):
    cols = np.where(row_mask)[0]
    if not len(cols):
        return []
    groups = np.split(cols, np.where(np.diff(cols) > 2)[0] + 1)
    return [(c0 + g[0], c0 + g[-1]) for g in groups]


def split_pair(mask, rows, cols, min_solid=40, min_dot=4):
    """Split one colour into the solid curve (large connected components) and the dashes/dots of the
    dashed curve (small components). Returns (solid mask, list of dots (cx, cy, x0, x1, y0, y1))."""
    r0, r1 = rows
    c0, c1 = cols
    m = np.zeros(mask.shape, np.uint8)
    m[r0:r1, c0:c1] = mask[r0:r1, c0:c1]
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
    solid = np.zeros(mask.shape, bool)
    dots = []
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area >= min_solid:
            solid |= lab == i
        elif area >= min_dot:
            dots.append((cen[i][0], cen[i][1], x, x + w - 1, y, y + h - 1))
    return solid, dots


def main():
    rows_out = []
    from PIL import Image
    for pname, P in PANELS.items():
        fy, ry, my = fit_axis(P["yt"], P["yv"])
        fx, rx, mx = fit_axis(P["xt"], P["xv"])
        ov = img.copy()
        for colour, solid_name, dashed_name in PAIRS:
            solid, dots = split_pair(CLS[colour], P["rows"], P["cols"])
            if dashed_name is None:      # black: one solid series; keep its small pieces too
                for cx, cy, x0, x1, y0, y1 in dots:
                    solid[y0:y1 + 1, x0:x1 + 1] |= CLS[colour][y0:y1 + 1, x0:x1 + 1]
                dots = []
            for r in range(*P["rows"]):
                for lo, hi in runs_of(solid[r, P["cols"][0]:P["cols"][1]], P["cols"][0]):
                    flag = "solid trace"
                    if P["x_break"] is not None and hi >= P["x_break"] - 12:
                        flag += "; reaches the axis break (x beyond about 230 not calibrated)"
                    rows_out.append((pname, solid_name, "solid", float(fy(r)), float(fx(lo)), float(fx(hi)),
                                     float(fx((lo + hi) / 2)), flag, r, lo, hi))
                    ov[r, lo:hi + 1] = (0, 200, 0)
            for cx, cy, x0, x1, y0, y1 in sorted(dots, key=lambda d: -d[1]):
                flag = "dash centroid"
                if P["x_break"] is not None and x1 >= P["x_break"] - 12:
                    flag += "; reaches the axis break (x beyond about 230 not calibrated)"
                rows_out.append((pname, dashed_name, "dashed", float(fy(cy)), float(fx(x0)), float(fx(x1)),
                                 float(fx(cx)), flag, round(cy, 1), x0, x1))
                ov[int(round(cy)), int(round(cx))] = (0, 255, 255)
                ov[y0:y1 + 1, x0] = (0, 160, 255)
        tag = "bse" if pname.startswith("Back") else "pe"
        c0, c1 = P["cols"]
        r0, r1 = P["rows"]
        Image.fromarray(ov[r0 - 12:r1 + 3, c0 - 12:c1 + 12]).resize(((c1 - c0 + 24) * 4, (r1 - r0 + 15) * 4),
                                                                     Image.NEAREST).save(
            os.path.join(WORK, f"supp_sfig9c_overlay_{tag}.png"))
        print(pname, "res_y", round(ry, 2), "res_x", round(rx, 2), "1px y", round(abs(my), 2), "1px x", round(abs(mx), 2))
    write_csv(os.path.join(HERE, "sfig9c.csv"), [
        "Supplementary Figure 9c (kubota2018 SI): 'Estimated numbers of the electrons found at different depths by the"
        " Monte Carlo simulation'; two panels, 'Backscattered electrons' and 'Primary (absorbed) electrons'",
        "columns: panel, series (legend text), style (solid/dashed as drawn), depth_nm (y axis 'depth (nm)'),"
        " x_lo, x_hi, x (number of electrons, top x axis; ends and mean of the colour run in that pixel row),"
        " flag, pixel_row, pixel_col_lo, pixel_col_hi (embedded image)",
        "provenance: tier 3, digitized from the embedded raster image of SI page 19 (987 x 1225 px"
        " JPEG, 167 ppi) at native resolution, script sfig9c_extract.py; colour classes in HSV, curves traced row by row"
        " (solid curve = large connected components of the colour, dashed curve = its small components, the dashes)",
        "axis fits: BSE panel y on 6 ticks 0..-500 nm (1 px = 2.8 nm), x on 5 ticks 0..200 (1 px = 1.55 electrons);"
        " PE panel y on 8 ticks 0..-1400 nm (1 px = 7.3 nm), x on 7 ticks 0..3000 (1 px = 18.6 electrons)",
        "uncertainty: about 1-2 px (BSE: 3-6 nm, 2-3 electrons; PE: 7-15 nm, 20-40 electrons) where the curve is"
        " steep; where it is nearly horizontal the run x_lo..x_hi is the honest range",
        "BSE panel: the top x axis is broken ('//') after 200 and ends at '3000'; values in the break region are not"
        " calibrated (flagged). A grey horizontal line at -50 nm is labelled '50 nm' (not data)",
        "limits: near depth 0 all curves converge and cross; there pieces of curves are missing or attributed to the"
        " wrong member of a colour pair (a solid fragment < 40 px counted as a dash, a dash touching the solid"
        " curve merged into it). The pale dashed curves (especially 3.5 keV) are partly lost in the colour"
        " classification, and where solid and dashed curves of one colour touch, both are traced as one."
        " Treat this as an approximate trace; check the overlays (work/supp_sfig9c_overlay_*.png)",
        "known misassignments (checked on the overlays): single stray points of another curve with a similar hue"
        " (BSE '2.5 keV' at -267 nm, PE '2.5 keV' at -443 nm); near the y axis, where a solid curve and the dashes"
        " of its partner run down the axis together, the dashes merge into the solid trace (PE '3 keV' below about"
        " -400 nm and BSE '5 keV' below about -480 nm are probably the 3.5 keV and 5.5 keV curves)",
    ], ["panel", "series", "style", "depth_nm", "x_lo", "x_hi", "x", "flag", "pixel_row", "pixel_col_lo",
        "pixel_col_hi"], rows_out,
        fmt=["{}", "{}", "{}", "{:.1f}", "{:.1f}", "{:.1f}", "{:.1f}", "{}", "{}", "{}", "{}"])
    from collections import Counter
    print(Counter((r[0][:3], r[1]) for r in rows_out))


if __name__ == "__main__":
    main()
