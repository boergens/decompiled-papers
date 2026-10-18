"""Fig. 11 (p. 25): bar chart, number of cell types per brain region. Tier 3, digitized from the embedded
JPEG (2734 x 1706 px) at native resolution.

Calibration: y-axis major tick marks (labels 0, 500, 1000, 1500) located in the image; linear fit.
Bars: one per x tick (43 ticks = 43 printed labels). For each bar the median green channel of two 7-px strips beside the tick centre (the tick mark
itself is dark) is followed upwards from the axis while it is bar-coloured; the partially covered top row adds
its coverage fraction, so the bar top is found to sub-pixel precision. Bar bottom = centre of the
x-axis line (value 0).
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import rasterfig as rf  # noqa: E402

LABELS = ["SLP(R)", "SMP(R)", "PLP(R)", "AVLP(R)", "SCL(R)", "SIP(R)", "ICL(R)", "LH(R)", "SPS(R)", "PVLP(R)",
          "WED(R)", "LAL(R)", "CRE(R)", "IB", "VES(R)", "AL(R)", "IPS(R)", "GNG", "SAD", "FB", "LO(R)", "EPA(R)",
          "AOTU(R)", "ATL(R)", "GOR(R)", "CA(R)", "gL(R)", "EB", "AME(R)", "NO", "BU(R)", "PB", "b'L(R)", "LOP(R)",
          "a'L(R)", "aL(R)", "bL(R)", "PED(R)", "FLA(R)", "AB(R)", "CAN(R)", "ME(R)", "PRW"]

a = rf.load(25).astype(float)
g = a.mean(2)
H, W = g.shape

# --- y calibration from major tick marks left of the y axis (x 225..243)
rows = [r for r in range(H - 300) if (g[r, 225:243] < 120).sum() >= 15]
groups = np.split(np.array(rows), np.where(np.diff(rows) > 1)[0] + 1)
tick_px = [grp.mean() for grp in groups]
tick_val = [1500, 1000, 500, 0]
assert len(tick_px) == 4, tick_px
k, b = np.polyfit(tick_px, tick_val, 1)          # value = k*px + b
res = np.array(tick_val) - (k * np.array(tick_px) + b)
y0 = -b / k                                       # pixel row of value 0

# --- x tick centres below the axis
row = g[int(y0) + 11]
xs = np.where(row < 120)[0]
runs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1)
ticks = [r.mean() for r in runs if r.mean() > 240]
assert len(ticks) == len(LABELS), len(ticks)

axis_top = int(np.argmax(a[int(y0) - 30:, int(ticks[-1]) - 14, 1] < 200)) + int(y0) - 30  # first row of the axis line (beside the empty PRW bar)
out = []
for lab, xc in zip(LABELS, ticks):
    cols = list(range(int(xc) - 16, int(xc) - 9)) + list(range(int(xc) + 10, int(xc) + 17))
    strip = np.median(a[:axis_top, cols, 1], axis=1)   # green channel: 255 white, 120 bar
    r = axis_top - 1
    while r > 0 and strip[r] < 200:                # contiguous bar run upwards from the axis
        r -= 1
    full = axis_top - 1 - r                          # fully covered rows
    part = np.clip((255 - strip[r]) / (255 - 120), 0, 1) if full > 0 else 0.0  # partial top row
    height_px = (full + part + (y0 - axis_top)) if full > 0 else 0.0
    out.append((lab, round(xc, 1), round(height_px * -k, 1)))

out_csv = HERE / "fig11.csv"
with open(out_csv, "w", newline="") as f:
    f.write("# Figure 11 (p. 25 of elife-57443-v4.pdf): number of cell types in each major brain region (bar chart).\n")
    f.write("# Provenance: tier 3, digitized from the embedded raster image (JPEG, 2734 x 1706 px) by fig11_extract.py.\n")
    f.write("# Tier 1 not available: the caption names 'Figure 11-source data 1' (eLife online), not in papers/scheffer2020/.\n")
    f.write(f"# y calibration: linear fit to the 4 labelled major ticks (0, 500, 1000, 1500); {-1/k:.3f} px per type; residuals {np.round(res, 2).tolist()} types.\n")
    f.write("# Columns: region = x-axis label as printed (Greek letters are printed as Latin: gL = gammaL, b'L = beta'L, a'L = alpha'L, aL = alphaL, bL = betaL);\n")
    f.write("#   order = bar position from the left (1-based); n_types = bar height in number of cell types (y axis '#types').\n")
    f.write("# Uncertainty: about +-2 types (1 px = 1.46 types; JPEG edges). Bars below about 3 types are hard to tell from the axis line;\n")
    f.write("#   PRW shows no visible bar (0 here, could be 1-2).\n")
    w = csv.writer(f)
    w.writerow(["order", "region", "n_types"])
    for i, (lab, xc, v) in enumerate(out, 1):
        w.writerow([i, lab, v])

# overlay
from PIL import Image, ImageDraw  # noqa: E402
im = Image.fromarray(a.astype(np.uint8))
d = ImageDraw.Draw(im)
for lab, xc, v in out:
    yy = y0 + v / k
    d.line([(xc - 28, yy), (xc + 28, yy)], fill=(255, 0, 0), width=3)
(HERE.parent / "work").mkdir(exist_ok=True)
im.save(HERE.parent / "work" / "fig11_overlay.png")
print(out_csv, len(out), "bars; px/type", -1 / k, "res", res, "y0", y0, "axis_top", axis_top)
