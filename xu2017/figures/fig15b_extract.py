"""Digitize Figure 15(b) of Xu et al. 2017 (PDF p. 26): scattering ratio Os/C vs landing energy.

Source: the embedded raster image of Figure 15 (2880 x 1200 px, ~403 ppi); panel b at its right.
    python3 -I -B figures/fig15b_extract.py  -> figures/fig15b.csv (+ work/fig15b_overlay.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import write_csv, overlay  # noqa: E402
from xu_helpers import load, blobs, lin, logmap, column_centres, work_path  # noqa: E402

a = load(26).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
grey = a.mean(2)

# Frame (found with work/explore.py): left 2274-2281, right 2818-2825, top 423-430, bottom 937-944.
XL, XR = 2277.5, 2821.5
YT, YB = 426.5, 940.5
# x: tick labels 0.6 (centre col 2382.5, tick at 2387.0), 1.0 (label 2602.5, tick 2604.5), 1.4 (label ~2820, right frame).
# Minor ticks every 27.2 px = 0.05; the left frame is 0.4.
fx = lin(2387.0, 0.6, 2604.5, 1.0)
xres = max(abs(fx(XR) - 1.4), abs(fx(XL) - 0.4))
# y: log10, 10 at the bottom frame, 1000 at the top frame; the labelled 100 tick sits at row 683.5 (both sides).
fy = logmap(YB, 10, YT, 1000)
yres = abs(np.log10(fy(683.5)) - 2)

blue = (B - R > 60) & (B - G > 60)
markers = [b for b in blobs(blue, min_area=300) if XL - 40 < b[0] < XR + 40]
markers.sort()
line = (grey < 80) & ~blue
# keep only the curve: the large connected pieces of dark pixels inside the frame (ticks are small separate pieces)
from scipy import ndimage  # noqa: E402
box = np.zeros_like(line)
box[int(YT) + 9:int(YB) - 8, int(XL) + 9:int(XR) - 8] = True
lab, n = ndimage.label(line & box)
sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
line = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 120])
inner = column_centres(line, int(XL) + 9, int(XR) - 8, int(YT) + 9, int(YB) - 8)

rows, pts = [], []
for x, y, area, _ in markers:
    rows.append(("markers", float(fx(x)), float(fy(y))))
    pts.append((x, y))
mx = np.array([fx(m[0]) for m in markers]); my = np.log10([fy(m[1]) for m in markers])
for c, y, top, bot in inner:
    # drop long tick marks: keep pixels within 0.08 decades of the straight-line path between the markers
    if y == y and bot - top < 30 and abs(np.log10(fy(y)) - np.interp(fx(c), mx, my)) < 0.08:
        rows.append(("curve", float(fx(c)), float(fy(y))))
        pts.append((c, y))
overlay(a.astype(np.uint8), pts, work_path("fig15b_overlay.png"))
write_csv(str(HERE / "fig15b.csv"), [
    "Xu et al. 2017 eLife 6:e25916, Figure 15(b): 'Scattering Ratio Os/C' vs 'Landing Energy (eV)'.",
    "The x axis is labelled 'Landing Energy (eV)' with ticks 0.6, 1.0, 1.4; the values are keV (the text speaks of 600 eV); x is given as printed.",
    "Columns: series ('markers' = the 11 blue filled circles; 'curve' = the black line, one row per pixel column of the",
    "  source image, where it is not hidden by a marker), x = landing energy in the printed axis units, y = scattering ratio Os/C.",
    "Provenance: tier 3, digitized from the embedded raster image (~403 ppi, no vector data in the PDF) by fig15b_extract.py.",
    f"  x: linear, calibrated on the 0.6 and 1.0 ticks; the frame edges then come out at 0.4 and 1.4 (max deviation {xres:.4f}).",
    f"  y: log10, calibrated on the bottom (10) and top (1000) frame lines; the labelled 100 tick is off by {yres:.4f} decades.",
    "  Markers: centroid of each blue circle (colour mask). Curve: centre of the black line pixels in each column",
    "  (connected pieces larger than 120 px inside the frame, so short tick marks are excluded,",
    "  and only pixels within 0.08 decades of the marker-to-marker polyline, which drops the three long major ticks).",
    "Uncertainty: about +-0.002 in x (1 px) and +-0.004 decades in y (1 px) for markers; the curve line is ~9 px wide.",
], ["series", "landing_energy", "scattering_ratio_Os_C"], rows, fmt=["{}", "{:.4f}", "{:.4g}"])
print(len(markers), "markers;", [(round(float(fx(m[0])), 3), round(float(fy(m[1])), 1)) for m in markers])
