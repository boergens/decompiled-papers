"""Fig. 21 (p. 43): digitize the log-log scatter ('observed', blue +) and the 'rough fit' line (orange).

Tier 3 (digitized) from the embedded raster (2200 x 1674 px, native). The authors' Figure 21-source data 1 is not
available locally. Calibration on the white decade gridlines: x = 1, 10, 100 (and 1000 at the right frame),
y = 1e6 ... 1 (log fits). Markers: '+' template matched on a blue colour mask (13 x 13 px cross, 3 px strokes),
peaks kept by non-maximum suppression; overlapping markers (strengths above ~40, where neighbouring integers are
closer than a marker width) cannot all be separated: the detected crosses are given with status 'overlap'.
Fit line: line centre per pixel column on an orange mask (columns hidden under markers are skipped).
Writes figures/fig21.csv and work/fig21_overlay.png.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import fc_dig as fd  # noqa: E402

a = fd.embedded(43)
X0, Y0, X1, Y1 = 232, 66, 2144, 1520         # inside the plot frame
LEG = (1680, 80, 2144, 220)                  # legend box (blanked)
xs = fd.white_lines(a, 240, 2150, 80, 1500, "v")
xs = [x for x in xs if x > 250]              # 1, 10, 100, 1000 (right frame)
fx, rx = fd.fit(xs, [1, 10, 100, 1000][:len(xs)], log=True)
ys = [y for y in fd.white_lines(a, 240, 2140, 60, 1520, "h") if y > 200]   # 1e6 ... 1
fy, ry = fd.fit(ys, [10.0 ** (6 - i) for i in range(len(ys))], log=True)

blue = fd.blank(fd.colour_mask(a, (7, 115, 180), 60), [LEG]).astype(np.float32)
blue[:, :X0] = 0; blue[:, X1:] = 0; blue[:Y0] = 0; blue[Y1:] = 0
orng = fd.colour_mask(a, (213, 97, 40), 60).astype(np.float32)   # the fit line is drawn over the markers
T = np.zeros((13, 13), np.float32); T[5:8, :] = 1; T[:, 5:8] = 1
cc = cv2.matchTemplate(np.maximum(blue, orng), T, cv2.TM_CCORR)   # template pixels covered by blue or orange
cb = cv2.matchTemplate(blue, np.ones((13, 13), np.float32), cv2.TM_CCORR)   # blue pixels in the window
peak = (cc >= 0.85 * T.sum()) & (cb >= 15) & (cc == cv2.dilate(cc, np.ones((5, 5), np.uint8)))
py, px = np.where(peak)
pts = []
for x, y in sorted(zip(px + 6, py + 6)):
    if pts and abs(pts[-1][0] - x) <= 2 and abs(pts[-1][1] - y) <= 2:
        continue
    pts.append((float(x), float(y)))
rows = []
for x, y in pts:
    s = float(fx(x)); n = float(fy(y))
    spacing_px = 616 * np.log10((round(s) + 1) / max(round(s), 1))   # px between this integer and the next
    status = "ok" if spacing_px >= 13 else "overlap"
    rows.append(["observed", s, n, int(round(s)) if spacing_px >= 6 else "", int(round(n)) if n < 6.5 else "", status])

orange = fd.blank(fd.colour_mask(a, (213, 97, 40), 45), [LEG])
tr = fd.trace(orange, X0 + 2, X1, Y0 + 2, Y1 - 2, min_px=2)
for t in tr:
    rows.append(["rough fit", float(fx(t[0])), float(fy(t[1])), "", "", ""])

# check the fit line against the caption: N(s) = A s^-1.67 exp(-s/42)
f = np.array([(float(fx(t[0])), float(fy(t[1]))) for t in tr])
A = np.exp(np.median(np.log(f[:, 1]) + 1.67 * np.log(f[:, 0]) + f[:, 0] / 42))
M = np.c_[np.ones(len(f)), np.log(f[:, 0]), f[:, 0]]
coef, *_ = np.linalg.lstsq(M, np.log(f[:, 1]), rcond=None)
note = (f"Free fit of the digitized line to log N = c + k log s - s/s0: k = {coef[1]:.3f}, s0 = {-1 / coef[2]:.1f}"
        f" (caption: exponent -1.67, cutoff 42); A = {np.exp(coef[0]):.4g}.")
print(note, "rx", rx, "ry", ry, "markers", len(pts))
fd.write_csv(HERE / "fig21.csv", [
    "Fig. 21 of Scheffer et al. 2020 (eLife 9:e57443), p. 43: 'Number of connections vs strength of connection'.",
    "x = Strength of connection (log axis, ~0.8 to 1000); y = Number of links with specified strength (log axis, ~0.6 to 1e7).",
    "Provenance: tier 3, digitized from the embedded raster image (2200 x 1674 px); the authors' Figure 21-source data 1 was not available locally.",
    f"Calibration: white decade gridlines, x at 1, 10, 100, 1000 (log fit, max residual {rx:.4f} decades), y at 1e6..1 (max residual {ry:.4f} decades).",
    "series 'observed': one row per detected '+' marker centre (template match on a blue mask); x_int = nearest integer strength where",
    "neighbouring integers are >= 6 px apart (strength < ~100); status ok = marker separable (integers >= 13 px apart, strength <~ 4..20 where isolated),",
    "overlap = in the dense cloud (strength above ~20-40) where crosses overlap: some markers are hidden and positions are uncertain by a few px.",
    "Uncertainty: about +-0.002 decades (1 px) for isolated markers; y values are counts, so isolated ones should be near integers (bottom rows 1..6).",
    "series 'rough fit': orange line centre per pixel column. " + note,
    "y_int = nearest integer count for the bottom rows (y < 6.5, rows >= 13 px apart). In dense rows a cross can be found twice a few px apart.",
    "Columns: series, x, y, x_int, y_int, status."], ["series", "x", "y", "x_int", "y_int", "status"], rows)
fd.overlay(a, {"observed": pts, "rough fit": [(t[0], t[1]) for t in tr[::4]]}, HERE.parent / "work" / "fig21_overlay.png", r=3)
