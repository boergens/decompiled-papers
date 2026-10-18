"""Digitize Figure 6 of Sun & Gamstedt 2019 (PDF p. 5): chip thickness (circles, left axis) and shear
plane angle (squares, right axis) versus cutting speed (linear axis).

Source: the embedded 300 ppi greyscale raster of Fig. 6 (969 x 625 px); no vector paths in the PDF.
    python3 -I -B figures/fig6_extract.py   -> figures/fig6.csv (+ work/fig6_overlay.png)
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
a = embedded_image(PDF, 5, bbox_near=(54, 58, 286, 208))
dark = gray(a) < 120
rows = frame_lines(dark, 1, 0.5)
cols = frame_lines(dark, 0, 0.5)
TOP, BOT = rows[0], rows[-1]
LEFT, RIGHT = cols[0], cols[-1]
xl = (LEFT[0] + LEFT[1]) / 2
yb, yt = (BOT[0] + BOT[1]) / 2, (TOP[0] + TOP[1]) / 2

# x: inward ticks at 1..10 mm/s; the left frame is 0
xt = tick_positions(dark, BOT, -1, 6, LEFT[1] + 2, RIGHT[0] - 1)
assert len(xt) == 10, xt
fx, resx, sx = fit_axis(xt + [xl], list(range(1, 11)) + [0])
# left y: inward ticks 98, 96, ..., 88; frames 86 (bottom) and 100 (top)
lt = tick_positions_v(dark, LEFT, 1, 5, TOP[1] + 2, BOT[0] - 1)
assert len(lt) == 6, lt
fl, resl, sl = fit_axis(lt + [yb, yt], [98, 96, 94, 92, 90, 88, 86, 100])
# right y: inward ticks 67, 65, ..., 55; bottom frame 53 (labelled); top frame (68) not labelled, not used
rt = tick_positions_v(dark, RIGHT, -1, 5, TOP[1] + 2, BOT[0] - 1)
assert len(rt) == 7, rt
fr, resr, sr = fit_axis(rt + [yb], [67, 65, 63, 61, 59, 57, 55, 53])

m = dark.astype(np.uint8)
m[:, :LEFT[1] + 4] = 0
m[:, RIGHT[0] - 3:] = 0
m[:TOP[1] + 4] = 0
m[BOT[0] - 8:] = 0
o = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(o)
pts = []
for i in range(1, n):
    x, y, w, h, area = st[i]
    assert h <= 18 and w <= 18, st[i]
    kind = "shear plane angle" if area > 220 else "chip thickness"   # squares ~16 px, circles ~14 px
    pts.append((kind, cen[i][0], cen[i][1]))
pts.sort(key=lambda p: (p[0], p[1]))   # by series, then x
rows_out = []
for s, xp, yp in pts:
    val = float(fl(yp)) if s == "chip thickness" else float(fr(yp))
    rows_out.append((s, float(fx(xp)), val))
assert len(rows_out) == 10, rows_out
overlay(a, [(p[1], p[2]) for p in pts], str(HERE.parent / "work" / "fig6_overlay.png"))
write_csv(str(HERE / "fig6.csv"), [
    "Sun & Gamstedt 2019, Nanomanuf Metrol 2:45-55, Fig. 6: chip thickness and shear plane angle as a function of",
    "  the cutting speed (t_u = 85 nm per Sect. 3.2.1).",
    "Columns: series (paper's labels: 'chip thickness' = filled circles, solid line, left axis; 'shear plane angle' =",
    "  filled squares, dashed line, right axis); cutting_speed_mm_s = marker centre on the linear x axis (the",
    "  nominal speeds of Table 1 are 0.25, 0.5, 1.0, 3.0, 10.0 mm/s); value = chip thickness in nm or shear plane",
    "  angle in degrees.",
    "Provenance: tier 3, digitized from the embedded 300 ppi greyscale raster (no vector data in the PDF) by",
    f"  fig6_extract.py: linear fits on the tick marks and frames (x residual {resx:.3f} mm/s, left {resl:.3f} nm,",
    f"  right {resr:.3f} deg); marker centres from connected components after a 9 px opening.",
    f"Uncertainty: about +-{2 * abs(sx):.3f} mm/s, +-{2 * abs(sl):.2f} nm, +-{2 * abs(sr):.2f} deg (2 px). The circle at",
    "  3 mm/s lies close below the square and is crossed by both lines; its centre may be off by ~1 px more.",
], ["series", "cutting_speed_mm_s", "value"], rows_out, fmt=["{}", "{:.3f}", "{:.2f}"])
print("wrote fig6.csv; residuals", resx, resl, resr)
for r in sorted(rows_out, key=lambda r: (r[0], r[1])):
    print(r)
