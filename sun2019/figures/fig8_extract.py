"""Digitize Figure 8 of Sun & Gamstedt 2019 (PDF p. 5): AFM surface height profiles along the cutting
direction for five cutting speeds (five coloured lines, offset vertically by the authors).

Source: the embedded 300 ppi RGB raster of Fig. 8 (969 x 744 px, lossless); no vector paths in the PDF.
    python3 -I -B figures/fig8_extract.py   -> figures/fig8.csv (+ work/fig8_overlay.png)
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
a = embedded_image(PDF, 5, bbox_near=(309, 58, 541, 236))
r, g, b = (a[:, :, i].astype(int) for i in range(3))
dark = gray(a) < 120
rows = frame_lines(dark, 1, 0.5)
cols = frame_lines(dark, 0, 0.5)
TOP, BOT = rows[0], rows[-1]
LEFT, RIGHT = cols[0], cols[-1]
yb, yt = (BOT[0] + BOT[1]) / 2, (TOP[0] + TOP[1]) / 2

# x: inward ticks every 50 nm from 0 to 500 (labels on 0, 100, ..., 500)
xt = tick_positions(dark, BOT, -1, 6, LEFT[1] + 2, RIGHT[0] - 1)
assert len(xt) == 11, xt
fx, resx, sx = fit_axis(xt, [50 * i for i in range(11)])
# y: inward ticks every 0.5 nm from 0.5 to 9.5; bottom frame 0, top frame 10 (both labelled)
lt = tick_positions_v(dark, LEFT, 1, 5, TOP[1] + 2, BOT[0] - 1)
assert len(lt) == 19, lt
fy, resy, sy = fit_axis(lt + [yb, yt], [9.5 - 0.5 * i for i in range(19)] + [0, 10])

SERIES = {   # paper's label -> colour mask
    "v0=0.25 mm s-1": (gray(a) < 110) & (a.max(2).astype(int) - a.min(2).astype(int) < 40),
    "v0=0.5 mm s-1": (r > 150) & (g < 120) & (b < 120),
    "v0=1.0 mm s-1": (b > 150) & (r < 130) & (g < 130),
    "v0=3.0 mm s-1": (g > 80) & (r < 110) & (b < 110) & (g - r > 40),
    "v0=10.0 mm s-1": (r > 150) & (b > 150) & (g < 150),
}
NAN = float('nan')
# pixel boxes (col0, row0, col1, row1) of the series labels, read off the image and checked by drawing them on it
# (work/fig8_boxes.png); the lines of v0=1.0, 3.0 and 10.0 cross their own labels
LABEL_BOX = {"v0=0.25 mm s-1": (160, 55, 445, 112), "v0=0.5 mm s-1": (270, 140, 525, 195),
             "v0=1.0 mm s-1": (415, 222, 655, 278), "v0=3.0 mm s-1": (540, 368, 775, 435),
             "v0=10.0 mm s-1": (690, 472, 965, 537)}
x0, x1 = LEFT[1] + 3, RIGHT[0] - 2
y0, y1 = TOP[1] + 3, BOT[0] - 8
out, pts = [], []
for name, mask in SERIES.items():
    m = mask.copy()
    m[:, :x0] = False
    m[:, x1:] = False
    m[:y0] = False
    m[y1:] = False
    # drop components that are not the line: the letters of the labels that do not touch it
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_WIDTH] > 80
    m = keep[lab]
    bx0, by0, bx1, by1 = LABEL_BOX[name]
    cs = np.where(m.any(0))[0]
    hist = []              # accepted (column, centre row)
    for c in range(cs.min(), cs.max() + 1):
        rr = np.where(m[:, c])[0]
        if len(rr) == 0:
            continue
        runs = np.split(rr, np.where(np.diff(rr) > 2)[0] + 1)
        flag = "other mark of same colour in column" if len(runs) > 1 else ""
        if not hist:
            run = max(runs, key=len)
        elif not (bx0 <= c < bx1):
            # outside the label: the run nearest to the previous column's centre
            prev = hist[-1][1]
            run = min(runs, key=lambda q: 0 if q[0] - 3 <= prev <= q[-1] + 3 else min(abs(q[0] - prev), abs(q[-1] - prev)))
        else:
            # inside the label's box: extrapolate the line over the last accepted columns and take the run on that
            # path; where the line touches a letter (run too thick) or no run is near the path, leave the value empty
            hc, hy = np.array(hist[-5:]).T
            gap = c - hc[-1]
            slope = float(np.polyfit(hc, hy, 1)[0]) if len(hc) >= 3 and np.ptp(hc) > 0 else 0.0
            if gap > 3:          # after a few empty columns, search around the last value
                slope = 0.0
            pred = hy[-1] + slope * gap

            def dist(q):
                return 0 if q[0] - 2 <= pred <= q[-1] + 2 else min(abs(q[0] - pred), abs(q[-1] - pred))
            run = min(runs, key=dist)
            if dist(run) > 6 + abs(slope) + 1.0 * gap:
                out.append((name, float(fx(c)), NAN, NAN, NAN, "line crosses its label: no line pixel on its path"))
                continue
            if by0 <= run[0] and run[-1] <= by1 and len(run) > 8 + 1.5 * abs(slope):
                out.append((name, float(fx(c)), NAN, NAN, NAN, "line crosses its label: merges with a letter"))
                continue
            if by0 <= (run[0] + run[-1]) / 2 <= by1:
                flag = "inside the label box"
        top, bot = run[0], run[-1]
        mid = (top + bot) / 2
        hist.append((c, mid))
        out.append((name, float(fx(c)), float(fy(mid)), float(fy(top + 2)), float(fy(bot - 2)), flag))
        pts += [(c, mid)]
overlay(a, pts, str(HERE.parent / "work" / "fig8_overlay.png"), colour=(0, 230, 230))
write_csv(str(HERE / "fig8.csv"), [
    "Sun & Gamstedt 2019, Nanomanuf Metrol 2:45-55, Fig. 8: experimental surface heights along the cutting direction",
    "  (AFM), one line per cutting speed v0 as labelled in the panel (t_u = 85 nm per Sect. 3.2.1).",
    "Columns: series = the panel's label; distance_nm; height_nm = 'Relative height (nm)' of the line centre in this",
    "  pixel column; height_upper/height_lower = top and bottom of the line in the column, each moved inward by half",
    "  the ~4 px line width (they differ on steep flanks); flag = column needs care (see below).",
    "The curves are offset vertically by the authors (they are stacked 0.25 at the top, 10.0 at the bottom); the",
    "  offsets are not stated, so only height differences within one curve are meaningful.",
    "Provenance: tier 3, digitized from the embedded 300 ppi RGB raster (lossless, no vector data in the PDF) by",
    f"  fig8_extract.py: linear fits on the 11 x ticks (residual {resx:.2f} nm) and 19 y ticks + frames",
    f"  (residual {resy:.3f} nm); each line traced with a colour mask per pixel column, following the run nearest to",
    "  the previous column; the labels' letters that do not touch the line were removed as separate components.",
    f"Uncertainty: about +-{2 * abs(sx):.1f} nm in distance and +-{2 * abs(sy):.2f} nm in height (2 px), more in flagged",
    "  columns. Flags: 'other mark of same colour in column' = a letter of the series label is in the same column",
    "  (the run on the line's path was used); 'inside the label box' = traced between the letters of its own label",
    "  (v0=1.0, 3.0 and 10.0 cross their labels), check against the image; 'line crosses its label: ...' = the line",
    "  touches a letter there and its height cannot be read: values left empty.",
], ["series", "distance_nm", "height_nm", "height_upper", "height_lower", "flag"], out,
    fmt=["{}", "{:.2f}", "{:.3f}", "{:.3f}", "{:.3f}", "{}"])
print("wrote fig8.csv", len(out), "rows; residuals", resx, resy)
from collections import Counter
print(Counter((o[0], o[5]) for o in out))
