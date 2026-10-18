"""Digitize Fig 5(e) of Lee et al. 2018 (PLoS ONE 13:e0206172) -> fig5e.csv (tier 3).

Mean edge spread function across annotated vesicle edges, SiN (red) and Luxel (blue), each a line with a
shaded band. x 'Distance [px]' 0-100, y 'Pixel intensity' 80-220. Embedded 300 ppi image on p. 11 (xref 167).
Per pixel column: the line centre (mean row of the saturated line colour) and the outer rows of the shaded
band (light tint of the same colour), converted with linear fits on the tick marks.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import numpy as np  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(ROOT / "source/lee2018_lasso.pdf"), 11).astype(int)
g = a.mean(2)
d = g < 230
xt = dc.tick_positions(d, (1888, 1889), -1, 5, 330, 810, 0.6)
yt = dc.tick_positions_v(d, (340, 341), +1, 5, 1500, 1895, 0.6)
# x ticks: 0,20,...,100 (the two extra hits at ~494 and ~643 are the dashed region boundaries, not ticks)
xt = [x for x in xt if min(abs(x - 494), abs(x - 643)) > 3]
assert len(xt) == 6 and len(yt) == 8, (xt, yt)
fx, rx, _ = dc.fit_axis(xt, [0, 20, 40, 60, 80, 100])
fy, ry, _ = dc.fit_axis(sorted(yt, reverse=True), [80, 100, 120, 140, 160, 180, 200, 220])
R, G, B = a[..., 0], a[..., 1], a[..., 2]
masks = {
    "SiN (red)": ((R - G > 70) & (G < 165), (R - G > 22) & (R - B > 22)),
    "Luxel (blue)": ((B - R > 70) & (R < 165), (B - R > 22) & (B - G > 22)),
}
# dashed vertical region lines (Interior | Edge | Exterior)
dash_cols = [c for c in range(342, 797) if (g[1530:1880, c] < 128).mean() > 0.3]
dash_x = sorted({round(float(fx(np.mean([c for c in dash_cols if abs(c - k) < 4]))), 2) for k in dash_cols})
rows, over = [], []
for name, (line_m, band_m) in masks.items():
    for c in range(343, 796):
        if any(abs(c - k) <= 3 for k in dash_cols):
            continue
        r = np.where(line_m[1500:1886, c])[0]
        if len(r) == 0:
            continue
        runs = np.split(r, np.where(np.diff(r) > 2)[0] + 1)
        run = max(runs, key=len)
        yc = 1500 + run.mean()
        b = np.where(band_m[1500:1886, c])[0] + 1500
        b = b[np.abs(b - yc) < 25]
        # contiguous band around the line
        top = yc; bot = yc
        bs = set(b.tolist())
        while int(top) - 1 in bs:
            top -= 1
        while int(bot) + 1 in bs:
            bot += 1
        top, bot = int(top), int(bot)
        rows.append([name, float(fx(c)), float(fy(yc)), float(fy(bot + 0.5)), float(fy(top - 0.5))])
        over += [(c, yc), (c, top), (c, bot)]
dc.write_csv(str(HERE / "fig5e.csv"), [
    "Lee et al. 2018, PLoS ONE 13(10):e0206172, Fig 5(e): mean edge spread function across manually annotated vesicle edges,",
    "  SiN (red, n = 60) and Luxel (blue, n = 60). Region labels printed above the plot: Interior | Edge | Exterior,",
    f"  separated by vertical dashed lines at x = {', '.join(str(x) for x in dash_x)} px (digitized).",
    "Columns: series, distance_px (x), intensity (line centre), band_low / band_high = lower and upper edge of the shaded band",
    "  (the caption does not say what the band shows).",
    "Provenance: tier 3, digitized by fig5e_extract.py from the embedded 300 ppi raster (p. 11); no vector or source data.",
    f"  x calibrated on ticks 0-100 every 20 (max residual {rx:.3f}); y on ticks 80-220 every 20 (max residual {ry:.3f}).",
    "  Line = centre of the saturated line colour per pixel column; band = outermost tinted rows touching the line.",
    "  Columns within 3 px of the dashed lines are skipped. One row per source pixel column (0.22 px of x).",
    "Uncertainty: about +-0.4 intensity units (1 source px = 0.39 units) for the line, +-0.8 for the band edges; x +-0.3.",
], ["series", "distance_px", "intensity", "band_low", "band_high"], rows, fmt=["{}", "{:.3f}", "{:.2f}", "{:.2f}", "{:.2f}"])
(ROOT / "work").mkdir(exist_ok=True)
dc.overlay(a.astype(np.uint8), over, str(ROOT / "work/fig5e_overlay.png"), colour=(0, 200, 0))
print("dash", dash_x, rx, ry)
