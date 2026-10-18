"""Digitize Figure 1 of Xu et al. 2017 (PDF p. 4): regions of 3D EM technologies in resolution vs size/volume.

Source: the embedded raster image of Figure 1 (2735 x 2234 px, ~382 ppi).
    python3 -I -B figures/fig1_extract.py  -> figures/fig1.csv (+ work/fig1_overlay.png)
The figure is a chart of coloured regions with log axes; the data are the corners of the regions, the end points of the
three red constant-time contours and the position of the yellow star.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from digitize_common import write_csv, overlay  # noqa: E402
from xu_helpers import load, logmap, work_path  # noqa: E402

a = load(4).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# Axes (work/explore.py, tick search): y axis line cols 295-300, x axis line rows 1910-1915.
# y (log2): ticks pointing right of the axis at rows 112.5 (64), 412.5 (32), 712.5 (16), 1012.5 (8), 1312.5 (4), 1612.5 (2);
#   1 at the x axis (row 1912.5): exactly 300 px per factor 2.
# x (log10): labelled ticks 0.1 at the y axis (col 297.5), 1 at 860, 10 at 1422.5, 100 at 1985, 1000 at 2547.5 (label centroids
#   309.5, 861.5, 1424, 1987, 2549), with unlabelled ticks every third of a decade (187.5 px): 562.5 px per decade.
fy = logmap(1912.5, 1, 112.5, 64)
fx = logmap(297.5, 0.1, 2547.5, 1000)


def edges(prof, thr):
    """Positions (index of the middle) where the colour changes by more than thr over 3 px."""
    d = np.abs(prof[3:] - prof[:-3]).sum(1)
    out, i = [], 0
    while i < len(d):
        if d[i] > thr:
            j = i
            while j < len(d) and d[j] > thr:
                j += 1
            out.append((i + j) / 2 + 1.5)
            i = j
        i += 1
    return out


teal = (R < 60) & (G > 120) & (B > 100)
green_or_light = (np.abs(a - [255, 255, 255]).sum(2) > 12)         # anything not white

# horizontal band boundaries (column 2600, clear of the band labels): white -> purple -> blue -> light blue -> green
e = edges(a[:, 2600], 25)
y_top, y_b1, y_b2, y_b3 = e[0], e[1], e[2], e[3]                  # ~187, 450, 600, 863
# vertical boundaries along row 1800: orange | yellow | white
e = edges(a[1800, 302:], 60)
x_or, x_ye = 302 + e[0], 302 + e[1]                                # ~672, 1085
x_right = 302 + edges(a[600, 302:], 60)[-1]                         # right end of the bands ~2622
y_or = edges(a[:, 500], 25)[0]                                      # top of the orange box ~787
# teal right (diagonal) edge: last teal pixel in rows 900..1400
rows = np.arange(900, 1420, 20)
tx = np.array([np.nonzero(teal[r, 1085:2000])[0].max() + 1085 + 0.5 for r in rows])
m_t, c_t = np.polyfit(rows, tx, 1)                                  # x = m*y + c
y_teal_bot = float(np.nonzero(teal[:, 1100])[0].max()) + 0.5         # flat bottom of the teal region ~1463
# green region: bottom edge (col 1500) and lower-right diagonal edge (last non-white pixel in rows 1050..1550)
y_gbot = float(np.nonzero(green_or_light[1300:1800, 1500])[0].max() + 1300 + 0.5)
rows2 = np.arange(1060, 1560, 20)
gx = np.array([np.nonzero(green_or_light[r, 1900:2700])[0].max() + 1900 + 0.5 for r in rows2])
m_g, c_g = np.polyfit(rows2, gx, 1)

V = {}
V["teal_top_right"] = (m_t * y_b3 + c_t, y_b3)
V["teal_bottom_right"] = (m_t * y_teal_bot + c_t, y_teal_bot)
V["green_bottom_right"] = (m_g * y_gbot + c_g, y_gbot)
V["green_right_top"] = (x_right, (x_right - c_g) / m_g)

regions = {
    "Diamond Cut Section TEM with Tomography (orange)": [(297.5, 1912.5), (x_or, 1912.5), (x_or, y_or), (297.5, y_or)],
    "Diamond Cut Serial Sections TEM with Tomography (yellow)": [(x_or, 1912.5), (x_ye, 1912.5), (x_ye, y_b3), (x_or, y_b3)],
    "Diamond Cut Serial Sections TEM or SEM (purple band)": [(x_or, y_b1), (x_right, y_b1), (x_right, y_top), (x_or, y_top)],
    "Diamond Cut Block Face (blue band)": [(x_or, y_b2), (x_right, y_b2), (x_right, y_b1), (x_or, y_b1)],
    "Diamond Cut Block Face with SEM Energy Deconvolution (light blue band)": [(x_or, y_b3), (x_right, y_b3), (x_right, y_b2), (x_or, y_b2)],
    "Existing FIB-SEM (teal)": [(x_ye, y_teal_bot), V["teal_bottom_right"], V["teal_top_right"], (x_ye, y_b3)],
    "High Throughput / High Resolution FIB-SEM (green)": [(x_ye, y_gbot), V["green_bottom_right"], V["green_right_top"],
                                                          (x_right, y_b3), V["teal_top_right"], V["teal_bottom_right"],
                                                          (x_ye, y_teal_bot)],
}
out, pts = [], []
for name, poly in regions.items():
    for i, (x, y) in enumerate(poly):
        out.append((name, i + 1, float(fx(x)), float(fy(y)), float(fx(x)) ** 3))
        pts.append((x, y))

# red contour lines: three thick red segments
red = (R > 200) & (G < 80) & (B < 80)
lab, n = ndimage.label(red)
segs = []
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    ys, xs = np.nonzero(lab[sl] == i)
    if len(xs) < 500:
        continue
    xs, ys = xs + sl[1].start, ys + sl[0].start
    p = np.polyfit(xs, ys, 1)
    x0, x1 = xs.min() + 3, xs.max() - 3                              # end caps: the line is ~7 px thick
    segs.append(((x0, np.polyval(p, x0)), (x1, np.polyval(p, x1))))
segs.sort()
for name, (p0, p1) in zip(["3 Days", "3 Months", "8 Years"], segs):
    for k, (x, y) in enumerate((p0, p1)):
        out.append((f"red contour '{name}'", k + 1, float(fx(x)), float(fy(y)), float(fx(x)) ** 3))
        pts.append((x, y))
# yellow star (on the light blue band, right end)
star = (R > 230) & (G > 200) & (B < 80)
star[:, :2300] = False
ys, xs = np.nonzero(star)
out.append(("yellow star", 1, float(fx(xs.mean())), float(fy(ys.mean())), float(fx(xs.mean())) ** 3))
pts.append((xs.mean(), ys.mean()))
overlay(a.astype(np.uint8), [(x + dx, y + dy) for x, y in pts for dx in (-3, 0, 3) for dy in (-3, 0, 3)], work_path("fig1_overlay.png"))

write_csv(str(HERE / "fig1.csv"), [
    "Xu et al. 2017 eLife 6:e25916, Figure 1: regions of 3D imaging technologies in 'Resolution (nm)' vs 'Size (μm) [ Volume (μm3) ]'.",
    "Columns: element (region named by its printed label and colour, red contour line, or star); vertex = corner number (polygon",
    "  corners in order around the region; for contour lines 1 = lower-left end, 2 = upper-right end); size_um = x axis value;",
    "  resolution_nm = y axis value; volume_um3 = size_um**3 (the axis prints both scales: 0.1 [1e-3], 1 [1e0], ... 1000 [1e9]).",
    "Provenance: tier 3, digitized from the embedded raster image (~382 ppi, no vector data in the PDF) by fig1_extract.py.",
    "  Axes: x log10 (562.5 px per decade, labelled ticks 0.1-1000); y log2 (300 px per factor 2, ticks 1-64), both exact to the pixel.",
    "  Region edges from colour transitions along fixed rows/columns; the two diagonal edges are straight-line fits through 26 and",
    f"  25 edge points (teal: {1 / m_t:.4f} rows per column; green: {1 / m_g:.4f}). Both diagonals rise by a factor of 2 in resolution",
    f"  per {abs(300 * m_t / 562.5):.3f} (teal) and {abs(300 * m_g / 562.5):.3f} (green) decades in size. Red lines: straight fits, end points at the visible ends.",
    "  The left ends of the three bands fade to white; their left edge is taken at the orange box's right edge (as drawn).",
    "Uncertainty: about +-1 px = +-0.002 decades in x and +-0.0033 octaves in y; region edges with soft gradients +-3 px.",
    "The figure is a schematic ('in practice there is considerable overlap and only a fuzzy boundary', caption).",
], ["element", "vertex", "size_um", "resolution_nm", "volume_um3"], out, fmt=["{}", "{}", "{:.4g}", "{:.4g}", "{:.4g}"])
for r in out:
    print(r[0][:40], r[1], round(r[2], 3), round(r[3], 2))
