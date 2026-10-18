"""Digitize Figure 4A of Denk & Horstmann 2004 (PLoS Biol 2: e329) -> fig4a.csv (tier 3).

Source: the embedded 500 x 852 px JPEG (150 ppi) on PDF page 6 (Figure 4 is a raster image; no vector
data). Panel A occupies the top of that image.

Calibration (pixel -> data), from the tick marks found in the image:
  y: ticks on the left axis line (col 67) at rows 40 (200), 115 (100), 341 (-200), plus the interpolated
     ticks at 0 and -100 (found the same way with a lower threshold); linear fit.
  x: tick marks on the bottom axis line (row 341) at columns ~130 (50), 193 (100), 256 (150), 318 (200),
     381 (250), 444 (300); linear fit.

The five traces (four 256x256 subregions and one 512x512 = black trace) are 1-px lines in a JPEG with
chroma subsampling and overlap almost everywhere, so they cannot all be separated reliably. This script
gives, per pixel column:
  * series 'all_traces': upper and lower envelope of all trace ink and the ink-weighted mean row;
  * series 'pink', 'orange', 'teal', 'lavender', 'black': the median row of the pixels whose colour
    falls in that series' colour class (CIELAB hue angle / lightness), only where at least 1 such
    pixel is in the column. These per-colour values are approximate; colour mixing at crossings
    misassigns pixels (flag 'mixed' where the class pixels in a column span > 6 px).
"""
import csv
import sys
from pathlib import Path

import numpy as np
import cv2

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import digitize_common as dc  # noqa: E402

PDF = HERE.parent / "source" / "denk2004.pdf"
a = dc.embedded_image(str(PDF), 6, bbox_near=(45, 52, 285, 461))
g = a.astype(float).mean(2)

# --- ticks -----------------------------------------------------------------
from scipy import ndimage  # noqa: E402


def centroids(w, thr):
    lab, n = ndimage.label(w > thr)
    out = []
    for i in range(1, n + 1):
        idx = np.where(lab == i)[0]
        out.append(float((w[idx] * idx).sum() / w[idx].sum()))
    return out


wy = (245 - g[:345, 63:66]).clip(0).sum(1)
yt = [r for r in centroids(wy, 15) if 30 < r < 345]
wx = (245 - g[336:340, 100:480]).clip(0).sum(0)
xt = [c + 100 for c in centroids(wx, 30)]
# keep the six labelled ticks (spacing ~63 px), drop trace pixels that touch the axis
xt = [c for c in xt if any(abs(c - (130 + 62.8 * k)) < 4 for k in range(6))]
assert len(yt) == 5, yt
assert len(xt) == 6, xt
fy, ry, _ = dc.fit_axis(yt, [200, 100, 0, -100, -200])
fx, rx, _ = dc.fit_axis(xt, [50, 100, 150, 200, 250, 300])

# --- ink classes -------------------------------------------------------------
Y0, Y1, X0, X1 = 33, 340, 69, 500          # plot interior (axis line at row 341, col 67)
sub = a[Y0:Y1, X0:X1]
lab = cv2.cvtColor(sub, cv2.COLOR_RGB2LAB).astype(float)
L = lab[..., 0] * 100 / 255
A = lab[..., 1] - 128
B = lab[..., 2] - 128
C = np.hypot(A, B)
H = np.degrees(np.arctan2(B, A)) % 360
ink = L < 88
# the x-axis tick marks (rows 336-340, +-2 px around each tick) are not trace ink
for t in xt:
    c0 = int(round(t)) - X0
    ink[336 - Y0:, max(c0 - 2, 0):c0 + 3] = False
classes = {
    "black": ink & (L < 50) & (C < 14),
    "pink": ink & (C > 8) & ((H >= 330) | (H < 35)) & (L >= 50),
    "orange": ink & (C > 8) & (H >= 35) & (H < 110) & (L >= 50),
    "teal": ink & (C > 8) & (H >= 140) & (H < 235),
    "lavender": ink & (C > 8) & (H >= 240) & (H < 330),
}
dark = (88 - L).clip(0) * ink

rows = []
pts_all = []
for c in range(X1 - X0):
    x = float(fx(c + X0))
    col = dark[:, c]
    idx = np.where(col > 0)[0]
    if len(idx):
        top, bot = idx.min() + Y0, idx.max() + Y0
        mean = float((col[idx] * (idx + Y0)).sum() / col[idx].sum())
        rows.append(["all_traces", x, fy(mean), fy(top), fy(bot), len(idx), ""])
        pts_all += [(c + X0, top), (c + X0, bot)]
    for name, m in classes.items():
        idx = np.where(m[:, c])[0]
        if len(idx) == 0:
            continue
        med = float(np.median(idx)) + Y0
        flag = "mixed" if np.ptp(idx) > 6 else ""
        rows.append([name, x, fy(med), fy(idx.min() + Y0), fy(idx.max() + Y0), len(idx), flag])

hdr = [
    "Denk & Horstmann 2004, PLoS Biol 2(11): e329, Figure 4A: peak shift in x-direction (nm) vs slice (#),",
    "  five subregions (four 256x256 px, one 512x512 px = black trace); same dataset as Figures 3A and 3B.",
    "Provenance: tier 3, digitized from the embedded 500x852 px JPEG (150 ppi) on PDF page 6 by fig4a_extract.py.",
    f"Axis calibration: y linear on 5 tick marks (200..-200 nm), max residual {ry:.2f} nm; x linear on 6 tick marks",
    f"  (50..300), max residual {rx:.2f} slices. 1 px = {abs(fy(1)-fy(0)):.2f} nm in y and {fx(1)-fx(0):.3f} slice in x.",
    "Columns: series, slice (x, one row per pixel column, so not integer slice numbers), shift_nm (series value:",
    "  ink-weighted mean row for 'all_traces', median row of the class pixels for a colour series),",
    "  shift_upper_nm / shift_lower_nm (top / bottom of that series' pixels in the column: the envelope for",
    "  'all_traces'), n_px (pixels in the column), flag.",
    "The five lines overlap almost everywhere and are 1 px wide in a chroma-subsampled JPEG, so they cannot be",
    "  separated reliably: 'all_traces' (envelope of all lines) is the robust result. The colour series are",
    "  assigned by CIELAB hue (pink, orange, teal, lavender) or by low lightness (black, the 512x512 trace);",
    "  colour mixing at crossings misassigns pixels; flag 'mixed' where a class spans > 6 px in one column.",
    "  The caption names only the black trace; the colour names are the decompiler's.",
    "The spikes reach the frame (+-200 nm) and are clipped there in the figure. On the tick calibration they come",
    "  out at slice ~58 and ~200.6, while the caption names slices 59 and 202: the plotted x may be offset by",
    "  about 1-1.5 slices from the tick labels (or the slice numbering differs); no correction was applied.",
    "Uncertainty: about +-3 nm (1 px) in y for clean single lines, more where lines overlap; +-1 slice in x.",
]
with open(HERE / "fig4a.csv", "w", newline="") as f:
    for h in hdr:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["series", "slice", "shift_nm", "shift_upper_nm", "shift_lower_nm", "n_px", "flag"])
    for r in rows:
        w.writerow([r[0], f"{r[1]:.2f}", f"{r[2]:.1f}", f"{r[3]:.1f}", f"{r[4]:.1f}", r[5], r[6]])

# overlay: envelope in magenta, class medians in their own colours
ov = a.copy()
colours = {"black": (0, 0, 0), "pink": (255, 0, 160), "orange": (255, 140, 0), "teal": (0, 170, 150),
           "lavender": (90, 60, 255)}
big = cv2.resize(ov, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
inv = lambda v, f: None  # noqa: E731
for r in rows:
    # back to pixels
    c = int(round((r[1] - fx(0)) / (fx(1) - fx(0))))
    yy = (r[2] - fy(0)) / (fy(1) - fy(0))
    if r[0] == "all_traces":
        for v in (r[3], r[4]):
            py = (v - fy(0)) / (fy(1) - fy(0))
            cv2.circle(big, (3 * c + 1, int(3 * py + 1)), 1, (255, 0, 255), -1)
    else:
        cv2.circle(big, (3 * c + 1, int(3 * yy + 1)), 1, colours[r[0]], -1)
(HERE.parent / "work").mkdir(exist_ok=True)
cv2.imwrite(str(HERE.parent / "work" / "fig4a_overlay.png"), cv2.cvtColor(big[: 3 * 360], cv2.COLOR_RGB2BGR))
print("y ticks", [round(v, 1) for v in yt], "res", ry, "x ticks", [round(v, 1) for v in xt], "res", rx)
print(len(rows), "rows")
