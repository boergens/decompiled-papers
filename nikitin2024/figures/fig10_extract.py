"""Digitize Figure 10 of Nikitin et al. 2024 (J. Synchrotron Rad. 31, 851-866; PDF p. 11): Fourier ring correlation.

Three series on one panel: FRC (black, noisy), smoothed FRC (red), 1/2-bit threshold (blue); x = Spatial/Nyquist
frequency 0..1, y = Correlation 0..1. Source: the embedded 1385 x 711 px raster (no vector paths in the PDF:
tools/vector_dump.py reports 0 paths in the figure region), tier 3 "digitized".
Run from anywhere:  python3 -I -B fig10_extract.py   -> fig10.csv next to this script, work/fig10_overlay.png
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for up in range(1, 6):                                   # walk up to the collection's tools/
    cand = os.path.abspath(os.path.join(HERE, *([".."] * up), "tools"))
    if os.path.exists(os.path.join(cand, "digitize_common.py")):
        sys.path.insert(0, cand)
        break
import numpy as np  # noqa: E402
from digitize_common import embedded_image, gray, frame_lines, fit_axis, trace, trace_envelope, write_csv, overlay  # noqa: E402

PDF = os.path.join(HERE, "..", "source", "nikitin2024.pdf")
a = embedded_image(PDF, 11, bbox_near=(45.7, 348.7, 295.0, 476.6))
g = gray(a)
H, W = g.shape

# --- axes box and grid lines ---
dark = g < 160
rows = frame_lines(dark, 1, 0.4)
cols = frame_lines(dark, 0, 0.4)
top, bot = rows[0][0], rows[-1][1]
left, right = cols[0][1], cols[-1][0]
inner = g[top + 3:bot - 2, left + 3:right - 2]
light = (inner > 150) & (inner < 238)                     # the light-grey grid lines


def groups(idx):
    out = []
    for i in idx:
        if out and i - out[-1][-1] <= 1:
            out[-1].append(i)
        else:
            out.append([i])
    return [float(np.mean(gp)) for gp in out]


gx = groups(np.where(light.mean(0) > 0.5)[0] + left + 3)   # grid columns at x = 0, 0.2, ..., 1.0
gy = groups(np.where(light.mean(1) > 0.5)[0] + top + 3)    # grid rows at y = 1.0, 0.8, ..., 0
assert len(gx) == 6 and len(gy) == 6, (gx, gy)
fx, resx, mx = fit_axis(gx, [0, 0.2, 0.4, 0.6, 0.8, 1.0])
fy, resy, my = fit_axis(gy, [1.0, 0.8, 0.6, 0.4, 0.2, 0.0])
# check: the outward x tick at 0 below the bottom frame
tick0 = np.where(g[bot + 3, left - 20:left + 40] < 120)[0] + left - 20
assert abs(np.mean(tick0) - gx[0]) < 2.5, (tick0, gx[0])

# --- blank the legend box, the "1.69 um" text and the arrow shaft ---
work = a.astype(float).copy()
work[14:176, 905:1378] = 255                               # legend (upper right)
work[318:372, 885:1065] = 255                              # "1.69 um"
p0, p1 = np.array([905.0, 378.0]), np.array([818.0, 462.0])   # arrow shaft (tail -> before the head)
yy, xx = np.mgrid[0:H, 0:W]
d = p1 - p0
t = np.clip(((xx - p0[0]) * d[0] + (yy - p0[1]) * d[1]) / (d @ d), 0, 1)
dist = np.hypot(xx - (p0[0] + t * d[0]), yy - (p0[1] + t * d[1]))
work[dist < 11] = 255
gw = work.mean(2)

red = np.sqrt(((work - np.array((211, 21, 31))) ** 2).sum(2)) < 80
blue = np.sqrt(((work - np.array((67, 124, 158))) ** 2).sum(2)) < 70
black = (gw < 110) & ~red & ~blue
x0, x1 = left + 2, right - 1
y0, y1 = top + 2, bot - 1

# FRC: the red line is drawn over the black one, so the black line's full extent per column is the union
env = trace_envelope(black | red, x0, x1, y0, y1, half_width=1.5, min_px=1)
sm_x, sm_y = trace(red, x0, x1, y0, y1, min_px=1)
th = trace_envelope(blue, x0, x1, y0, y1, half_width=1.0, min_px=1)

rows_out, pts = [], {"FRC": [], "smoothed FRC": [], "1/2-bit threshold": []}
for k in range(0, x1 - x0, 2):
    c, mid, hi, lo = env[k]
    if mid == mid:
        rows_out.append(("FRC", float(fx(c)), float(fy(mid)), float(fy(lo)), float(fy(hi))))
        pts["FRC"].append((c, mid))
    if sm_y[k] == sm_y[k]:
        rows_out.append(("smoothed FRC", float(fx(sm_x[k])), float(fy(sm_y[k])), np.nan, np.nan))
        pts["smoothed FRC"].append((sm_x[k], sm_y[k]))
    c, mid, hi, lo = th[k]
    if mid == mid:
        rows_out.append(("1/2-bit threshold", float(fx(c)), float(fy(mid)), float(fy(lo)), float(fy(hi))))
        pts["1/2-bit threshold"].append((c, mid))

# crossing of the smoothed FRC and the threshold (the arrow's target), from the traces
sm = {int(x): y for x, y in zip(sm_x, sm_y) if y == y}
thr = {int(th[i][0]): th[i][1] for i in range(len(th)) if th[i][1] == th[i][1]}
cross, prev = None, None
for c in range(x0 + 300, x1):
    if c in sm and c in thr:
        diff = sm[c] - thr[c]                                 # pixel rows grow downwards: red goes below blue
        if prev is not None and prev[1] < 0 <= diff:
            cp, dp = prev
            xc = cp + (c - cp) * (-dp) / (diff - dp)           # linear interpolation between the two columns
            cross = (float(fx(xc)), float(fy(thr[c])))
            break
        prev = (c, diff)
tip = (float(fx(803)), float(fy(477)))

ov = a.copy()
for name, colour in [("FRC", (0, 255, 255)), ("smoothed FRC", (255, 0, 255)), ("1/2-bit threshold", (255, 200, 0))]:
    overlay(ov, pts[name], os.path.join(HERE, "..", "work", "fig10_overlay.png"), colour=colour)
    from PIL import Image
    ov = np.asarray(Image.open(os.path.join(HERE, "..", "work", "fig10_overlay.png")).convert("RGB")).copy()

px_x, px_y = abs(mx), abs(my)
write_csv(os.path.join(HERE, "fig10.csv"), [
    "Nikitin et al. 2024, J. Synchrotron Rad. 31, 851-866, Figure 10 (p. 861): resolution estimation by Fourier ring",
    "  correlation with the 1/2-bit criterion. x = Spatial/Nyquist frequency (0..1, linear), y = Correlation (0..1, linear).",
    "Columns: series (the legend's names: FRC, smoothed FRC, 1/2-bit threshold), x, y (line centre), y_lo, y_hi (vertical",
    "  extent of the line in that pixel column, for the noisy FRC trace and the steep start of the threshold; empty for the",
    "  smoothed FRC).",
    "Provenance: tier 3, digitized from the embedded 1385 x 711 px raster image (no vector paths in the PDF) by fig10_extract.py;",
    f"  axes calibrated on the six grid lines per axis at the labelled ticks (max residual {resx:.4f} in x, {resy:.4f} in y);",
    f"  one pixel = {px_x:.4f} in x and {px_y:.4f} in y; sampled every 2nd pixel column.",
    f"Uncertainty: about +-{2 * px_x:.4f} in x and +-{2 * px_y:.4f} in y (2 px) for the smoothed FRC and the threshold; the raw",
    "  FRC is a 3 px line that oscillates by up to +-0.05, so its per-column centre is uncertain by that much where it is",
    "  hidden under the red smoothed curve (y_lo/y_hi give the extent). Legend box, the '1.69 um' label and the arrow shaft were",
    "  blanked before tracing; the arrowhead touches the curve near x = 0.54.",
    f"Annotation: the arrow labelled '1.69 um' points at ({tip[0]:.3f}, {tip[1]:.3f}) (arrow tip, data units); the smoothed FRC",
    f"  crosses the 1/2-bit threshold at x = {cross[0]:.3f}, y = {cross[1]:.3f} in these traces." if cross else
    f"Annotation: the arrow labelled '1.69 um' points at ({tip[0]:.3f}, {tip[1]:.3f}) (data units).",
], ["series", "spatial_over_nyquist_frequency", "correlation", "correlation_lo", "correlation_hi"], rows_out,
    fmt=["{}", "{:.4f}", "{:.4f}", "{:.4f}", "{:.4f}"])
print("wrote fig10.csv", len(rows_out), "rows; grid x", gx, "grid y", gy, "res", resx, resy, "cross", cross, "tip", tip)
