"""Digitize Figure 3 of Sun & Gamstedt 2019 (PDF p. 3): chip thickness (circles, left axis) and shear
plane angle (squares, right axis) versus cutting thickness (category axis).

Source: the embedded 300 ppi greyscale raster of Fig. 3 (969 x 601 px); no vector paths in the PDF.
    python3 -I -B figures/fig3_extract.py   -> figures/fig3.csv (+ work/fig3_overlay.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from digitize_common import (embedded_image, gray, frame_lines, tick_positions, tick_positions_v,  # noqa: E402
                             fit_axis, write_csv, overlay)

PDF = str(HERE.parent / "source" / "sun2019.pdf")
a = embedded_image(PDF, 3, bbox_near=(54, 295, 286, 440))
dark = gray(a) < 120
rows = frame_lines(dark, 1, 0.5)
cols = frame_lines(dark, 0, 0.5)
TOP, BOT = rows[0], rows[-1]
LEFT, RIGHT = cols[0], cols[-1]

# x: category axis. 11 inward ticks at equal spacing; the six categories sit on every second one.
xt = tick_positions(dark, BOT, -1, 6, LEFT[1] + 2, RIGHT[0] - 1)
assert len(xt) == 11, xt
cat_x = xt[0::2]
labels = [60, 85, 110, 140, 170, 200]
# left y: inward ticks at 250, 200, ..., 50; bottom frame = 0, top frame = 300
lt = tick_positions_v(dark, LEFT, 1, 5, TOP[1] + 2, BOT[0] - 1)
assert len(lt) == 5, lt
yb, yt = (BOT[0] + BOT[1]) / 2, (TOP[0] + TOP[1]) / 2
fl, resl, sl = fit_axis(lt + [yb, yt], [250, 200, 150, 100, 50, 0, 300])
# right y: inward ticks at 55, 50, 45; bottom frame = 40, top frame = 60
rt = tick_positions_v(dark, RIGHT, -1, 5, TOP[1] + 2, BOT[0] - 1)
assert len(rt) == 3, rt
fr, resr, sr = fit_axis(rt + [yb, yt], [55, 50, 45, 40, 60])

# markers: open away the lines and text (strokes ~3 px), keep the solid markers (~15-18 px)
m = dark.astype(np.uint8)
m[:, :LEFT[1] + 4] = 0
m[:, RIGHT[0] - 3:] = 0
m[:TOP[1] + 4] = 0
m[BOT[0] - 8:] = 0
o = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(o)
pts = []   # (series, category index, x_px, y_px, note)
for i in range(1, n):
    x, y, w, h, area = st[i]
    k = int(np.argmin([abs(cen[i][0] - c) for c in cat_x]))
    assert abs(cen[i][0] - cat_x[k]) < 4
    if h <= 19:
        kind = "shear plane angle" if area > 260 else "chip thickness"
        pts.append((kind, k, cen[i][0], cen[i][1], ""))
    else:
        # circle overlapping square at 140 nm: circle on top, square below (seen in the image);
        # centres from the outer edges: circle diameter 15 px, square side 18 px (isolated markers)
        pts.append(("chip thickness", k, cen[i][0], y + 7.5, "marker partly covered by the square; centre from its top edge"))
        pts.append(("shear plane angle", k, cen[i][0], y + h - 1 - 8.5, "overlaps the circle; centre from its bottom edge"))
pts.sort(key=lambda p: (p[0], p[1]))
assert [p[1] for p in pts] == [0, 1, 2, 3, 4, 5] * 2, pts

rows_out = []
for s, k, xp, yp, note in pts:
    val = float(fl(yp)) if s == "chip thickness" else float(fr(yp))
    rows_out.append((s, labels[k], k, val, note))
overlay(a, [(p[2], p[3]) for p in pts], str(HERE.parent / "work" / "fig3_overlay.png"))
write_csv(str(HERE / "fig3.csv"), [
    "Sun & Gamstedt 2019, Nanomanuf Metrol 2:45-55, Fig. 3: chip thickness and shear plane angle as a function of",
    "  the cutting thickness.",
    "Columns: series (paper's labels: 'chip thickness' = filled circles, solid line, left axis; 'shear plane angle' =",
    "  filled squares, dashed line, right axis); cutting_thickness_nm = printed category label of the x axis;",
    "  category_index = position on the x axis (0..5, evenly spaced; the axis is a category axis, NOT to scale);",
    "  value = chip thickness in nm or shear plane angle in degrees.",
    "Provenance: tier 3, digitized from the embedded 300 ppi greyscale raster (no vector data in the PDF) by",
    "  fig3_extract.py: frame and tick marks located in the image, linear fit per y axis on the ticks and frame",
    f"  (left axis residual {resl:.2f} nm, right axis {resr:.3f} deg); marker centres from connected components",
    "  after a 9 px morphological opening that removes lines and text.",
    f"Uncertainty: about +-{2 * abs(sl):.1f} nm (left) and +-{2 * abs(sr):.2f} deg (right), i.e. 2 px; +-1.5 px more for",
    "  the two overlapping markers at 140 nm (centres from their outer edges, see note).",
], ["series", "cutting_thickness_nm", "category_index", "value", "note"], rows_out,
    fmt=["{}", "{}", "{}", "{:.2f}", "{}"])
print("wrote fig3.csv", len(rows_out), "rows; residuals", resl, resr)
for r in rows_out:
    print(r)
