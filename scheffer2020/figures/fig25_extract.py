"""Fig. 25 (p. 47): digitize the delay-amplitude scatter plots (a) and (b) from the embedded raster (2141 x 803 px).

Tier 3 (digitized). The authors' Figure 25-source data 1-4 are not available locally.
Calibration on the white gridlines: (a) x = 0.5 ... 3.5 ms, y = 0.2 ... 1.4 mV; (b) x = 2 ... 10 ms, y = 0.05 ... 0.15 mV.
(a) GA->GA: blue '+' markers (16 x 16 px, 2 px strokes) in a narrow overlapping cloud: cluster summary plus the
    cloud's centre and ink extent per 4-px row step. GA->EB (pink x) and GA->PB (green asterisks) are solid bands of hundreds of
    overlapping markers: given as a cluster summary (marker-centre extent = ink extent minus half a marker) and as the
    band's centre line (mean ink row) per 4-px column step.
(b) nine compact clusters of blue '+' markers (3 R_a x 3 R_m cases); the markers in a cluster overlap almost
    completely, so each cluster is given as a summary (ink centroid, marker-centre extent).
Writes figures/fig25a.csv, figures/fig25b.csv and work/fig25a_overlay.png, work/fig25b_overlay.png.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from scipy import ndimage

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import fc_dig as fd  # noqa: E402

a = fd.embedded(47)
BLUE, PINK, GREEN = (7, 115, 180), (204, 121, 168), (24, 159, 116)

# ---- (a)
fxa, rxa = fd.fit([182.5, 303.0, 423.5, 544.5, 664.5, 785.5, 905.5], [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
ya = fd.white_lines(a, 65, 1025, 100, 720, "h")          # 1.4 ... 0.2
fya, rya = fd.fit(ya, [1.4 - 0.2 * i for i in range(len(ya))])
# check gridline pixel positions found by code
xa = fd.white_lines(a, 70, 1020, 90, 730, "v")
assert np.allclose(xa, [182.5, 303.0, 423.5, 544.5, 664.5, 785.5, 905.5], atol=1.5), xa
BOXA = (63, 82, 1025, 734)
LEGA = (780, 85, 1025, 185)
rows, ov = [], {}
m = fd.blank(fd.colour_mask(a, BLUE, 45), [LEGA])
m[:, :BOXA[0]] = False; m[:, 300:] = False   # the GA->GA cloud lies left of 1 ms
m[:BOXA[1]] = False; m[BOXA[3]:] = False
ys, xs = np.where(m)
half = 8
rows.append(["GA->GA", "cluster_summary", float(fxa(xs.mean())), float(fya(ys.mean())),
             float(fxa(xs.min() + half)), float(fxa(xs.max() - half)), float(fya(ys.max() - half)), float(fya(ys.min() + half))])
ov["GA->GA"] = []
for y in range(ys.min(), ys.max() + 1, 4):        # the cloud is tall and narrow: centre per row step
    xr = np.where(m[y])[0]
    if len(xr):
        rows.append(["GA->GA", "cloud_row", float(fxa(xr.mean())), float(fya(y)), float(fxa(xr.min())), float(fxa(xr.max())), "", ""])
        ov["GA->GA"].append((xr.mean(), y))
for name, col, half in (("GA->EB", PINK, 8), ("GA->PB", GREEN, 8)):
    m = fd.blank(fd.colour_mask(a, col, 60), [LEGA])
    m[:, :BOXA[0]] = False; m[:, BOXA[2]:] = False; m[:BOXA[1]] = False; m[BOXA[3]:] = False
    lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=3))
    big = np.argmax(ndimage.sum(m, lab, range(1, n + 1))) + 1
    m &= lab == big
    ys, xs = np.where(m)
    cx0, cx1 = xs.min() + half, xs.max() - half
    cy0, cy1 = ys.min() + half, ys.max() - half
    rows.append([name, "cluster_summary", float(fxa(xs.mean())), float(fya(ys.mean())),
                 float(fxa(cx0)), float(fxa(cx1)), float(fya(cy1)), float(fya(cy0))])
    tr = fd.trace(m, xs.min(), xs.max() + 1, BOXA[1], BOXA[3], min_px=3, longest=False)
    for t in tr[::4]:
        rows.append([name, "band_centre", float(fxa(t[0])), float(fya(t[1])), "", "", float(fya(t[3])), float(fya(t[2]))])
    ov[name] = [(t[0], t[1]) for t in tr[::4]]
fd.write_csv(HERE / "fig25a.csv", [
    "Fig. 25(a) of Scheffer et al. 2020 (eLife 9:e57443), p. 47: 'Delay and Amplitude of Response' for inputs in the gall (GA) of an EPG neuron.",
    "x = Delay in millisec (linear, 0 to 4.0); y = Amplitude in millivolts (linear, 0 to 1.5).",
    "Provenance: tier 3, digitized from the embedded raster (2141 x 803 px); the authors' Figure 25-source data 1-3 were not available locally.",
    f"Calibration on white gridlines: x 0.5..3.5 (max residual {rxa:.4f} ms), y 0.2..1.4 (max residual {rya:.4f} mV).",
    "GA->GA (blue +, 16 px markers) forms a narrow overlapping cloud in which single markers cannot be separated reliably:",
    "kind cloud_row: every 4 px row of the cloud, x = mean ink column, x_min/x_max = ink extent in that row (incl. marker arms), y = row.",
    "kind cluster_summary: x, y = ink centroid; x_min/x_max, y_min/y_max = extent of marker centres (ink extent minus 8 px, half a marker).",
    "kind band_centre: centre (mean ink row) of the band every 4 px column; y_min/y_max = lower/upper ink edge in that column (includes marker size).",
    "Uncertainty: about +-0.01 ms and +-0.003 mV per pixel; band contents (hundreds of overlapping markers) cannot be separated into points.",
    "Columns: series, kind, x, y, x_min, x_max, y_min, y_max."],
    ["series", "kind", "x", "y", "x_min", "x_max", "y_min", "y_max"], rows)
fd.overlay(a[:, :1070], ov, HERE.parent / "work" / "fig25a_overlay.png", r=3)

# ---- (b)
xb = fd.white_lines(a, 1190, 2125, 40, 735, "v")        # 2 ... 10
fxb, rxb = fd.fit(xb, [2, 4, 6, 8, 10][:len(xb)])
yb = [y for y in fd.white_lines(a, 1185, 2125, 40, 740, "h") if y > 100]   # 0.15, 0.10, 0.05
fyb, ryb = fd.fit(yb, [0.15, 0.10, 0.05][:len(yb)])
m = fd.colour_mask(a, BLUE, 70)
m[:, :1182] = False; m[:36] = False; m[745:] = False
lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=4))
rows, ovb = [], {"clusters": []}
cl = []
for i in range(1, n + 1):
    ys, xs = np.where(m & (lab == i))
    if len(ys) < 30:
        continue
    cl.append((xs.mean(), ys.mean(), xs.min(), xs.max(), ys.min(), ys.max(), len(ys)))
for c in sorted(cl):
    half = 6.5
    x0c, x1c = (c[2] + half, c[3] - half) if c[3] - c[2] >= 2 * half else (c[0], c[0])
    y0c, y1c = (c[4] + half, c[5] - half) if c[5] - c[4] >= 2 * half else (c[1], c[1])
    rows.append(["GA->PB", "cluster_summary", float(fxb(c[0])), float(fyb(c[1])), float(fxb(x0c)),
                 float(fxb(x1c)), float(fyb(y1c)), float(fyb(y0c)), c[6]])
    ovb["clusters"].append((c[0], c[1]))
fd.write_csv(HERE / "fig25b.csv", [
    "Fig. 25(b) of Scheffer et al. 2020 (eLife 9:e57443), p. 47: 'Delay and Amplitude of Response', gall to PB, for 3 x 3 values of R_a and R_m.",
    "x = Delay in millisec (linear, 0 to 12); y = Amplitude in millivolts (linear, 0 to 0.2).",
    "Provenance: tier 3, digitized from the embedded raster (2141 x 803 px); the authors' Figure 25-source data 4 was not available locally.",
    f"Calibration on white gridlines: x 2..10 (max residual {rxb:.4f} ms), y 0.05..0.15 (max residual {ryb:.5f} mV).",
    "One row per cluster of blue '+' markers (the markers within a cluster overlap almost completely and cannot be separated):",
    "x, y = ink centroid; x_min/x_max, y_min/y_max = extent of the marker centres (ink extent minus 6.5 px, half a marker; = centroid for a single-marker cluster); ink_px = blue pixels.",
    "The printed arrows 'Decreasing Rm' and 'Increasing Ra' (black) are not data. The caption does not say which cluster is which R_a/R_m combination.",
    "Uncertainty: about +-0.04 ms and +-0.0003 mV per pixel.",
    "Columns: series, kind, x, y, x_min, x_max, y_min, y_max, ink_px."],
    ["series", "kind", "x", "y", "x_min", "x_max", "y_min", "y_max", "ink_px"], rows)
fd.overlay(a[:, 1070:], {"clusters": [(x - 1070, y) for x, y in ovb["clusters"]]}, HERE.parent / "work" / "fig25b_overlay.png", r=6)
print("a", rxa, rya, "b", rxb, ryb, len(rows))
