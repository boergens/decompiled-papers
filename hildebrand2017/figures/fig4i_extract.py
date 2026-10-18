"""Fig. 4i: sum of all normalized a and d per slice, 'original' (black) and 'swapped right MeLc and Mauthner'
(pink), digitized from the 150 ppi raster on PDF page 29 (tier 3). Writes fig4i.csv + work/fig4i_overlay.png.

x: ticks every 1000 slices (labels 2013, 5013, 8013, 11013) on the axis row 778; y: ticks every 2 (labels 0, 10).
Each series is traced per pixel column (centre of the colour-mask run nearest the previous column's value).
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, fit_axis, overlay, write_csv  # noqa: E402
from histo_common import tick_centres  # noqa: E402

a = embedded_image(str(ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"), 29)
g = a.astype(float).mean(2)
ink = 255 - g
R, G, B = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)

xt = [262 + t for t in tick_centres(ink[780, 262:940], 60)]
xt = [t for t in xt if abs(t - 520) > 3]          # drop the red slice marker (cols 519-521)
assert len(xt) == 10, xt
fx, resx, mx = fit_axis(xt, [2013 + 1000 * k for k in range(10)])
yt = [700 + t for t in tick_centres(ink[700:781, 267], 80)]
assert len(yt) == 6, yt
fy, resy, my = fit_axis(yt, [10, 8, 6, 4, 2, 0])

Y0, Y1 = 704, 777                  # plot rows above the x-axis line (row 778)
X0, X1 = 270, 936
legend = (800, 940, 712, 746)      # legend box (cols, rows) excluded
black = (a.max(2) < 100)
pink = (R > 200) & (G > 120) & (G < 225) & (np.abs(G - B) < 35)
redline = range(518, 523)


def run_trace(mask):
    xs, ys, prev = [], [], None
    for c in range(X0, X1):
        m = mask[Y0:Y1, c].copy()
        if legend[0] <= c < legend[1]:
            m[legend[2] - Y0:legend[3] - Y0] = False
        r = np.where(m)[0]
        if c in redline or not len(r):
            xs.append(c)
            ys.append(np.nan)
            continue
        runs = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
        if prev is None:
            run = max(runs, key=len)
        else:
            run = min(runs, key=lambda q: abs(Y0 + q.mean() - prev))
        prev = Y0 + run.mean()
        xs.append(c)
        ys.append(prev)
    return np.array(xs, float), np.array(ys, float)


rows, pts = [], []
for name, mask in (("original", black), ("swapped", pink)):
    xs, ys = run_trace(mask)
    for x, y in zip(xs, ys):
        if y != y:
            continue
        note = "near x axis (line may merge with the axis)" if y > 775 else ""
        rows.append((name, float(fx(x)), float(fy(y)), int(x), round(float(y), 1), note))
        pts.append((x, y))
hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Fig. 4i: sum of all normalized a and d (angle and distance differences) per",
    "slice for the 6-pair subset; series 'original' (black) and 'swapped' (pink: identities of the right MeLc and Mauthner",
    "axons swapped, legend 'swapped right [green dot] and [purple dot]').",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster on PDF page 29 (figures/fig4i_extract.py), one value per",
    f"image pixel column ({abs(mx):.1f} slices per column). x calibrated on 10 ticks 2013..11013 step 1000, max residual",
    f"{resx:.1f} slices; y on 6 ticks 0..10 step 2, max residual {resy:.3f}. Uncertainty about +-1 px = +-{abs(my):.2f} in y.",
    "Columns 518-522 (the red slice-5560 marker) and the legend box are skipped; where both lines overlap only the one",
    "drawn on top is visible and the other is traced from its visible pixels.",
    "columns: series; slice; sum (sum of normalized a and d, axis units); px_x; px_y (image pixel); note",
]
write_csv(HERE / "fig4i.csv", hdr, ["series", "slice", "sum", "px_x", "px_y", "note"], rows,
          fmt=["{}", "{:.0f}", "{:.3f}", "{}", "{}", "{}"])
(ROOT / "work").mkdir(exist_ok=True)
overlay(a, pts, str(ROOT / "work" / "fig4i_overlay.png"))
print(len(rows), resx, resy)
