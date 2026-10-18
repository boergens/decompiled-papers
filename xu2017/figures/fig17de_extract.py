"""Digitize Figure 17(d) and 17(e) of Xu et al. 2017 (PDF p. 28): Monte Carlo 'X Step Edge' and 'Z Step Edge'.

Source: the embedded raster image of Figure 17 (2880 x 2160 px, ~403 ppi); panels d and e in its lower part.
    python3 -I -B figures/fig17de_extract.py  -> figures/fig17d.csv, figures/fig17e.csv (+ work/fig17de_overlay.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from digitize_common import write_csv, overlay  # noqa: E402
from xu_helpers import load, lin, split_disks, work_path  # noqa: E402

a = load(28).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
band = np.zeros(R.shape, bool)
band[1400:2010, :] = True
MASKS = {"800 V": (B - R > 80) & (B > 150) & band,        # blue (91,155,213)
         "1200 V": (R - B > 120) & (R > 180) & band}      # orange (237,125,49)

# Grid lines found with work/explore.py (light grey, 3 px wide; centre rows/cols):
#   y (both panels): 12.0 at row 1424 (d) / 1423 (e) ... 8.0 at row 1985 (d) / 1984 (e), every 0.5 = 70.1 px
#   d, x: -4, -2, 0, 2, 4 at cols 391, 611, 832, 1052, 1273
#   e, x: 0, 5, ..., 35 at cols 1731, 1857, 1983, 2109, 2235, 2361, 2486, 2612
PANELS = {
    "d": dict(x=(391, 1273), xv=(-4, 4), y=(1985, 1424), xlim=(300, 1450),
              legend=[(530, 1515, 570, 1630)], title="X Step Edge"),
    "e": dict(x=(1731, 2612), xv=(0, 35), y=(1984, 1423), xlim=(1650, 2880),
              legend=[(2290, 1515, 2330, 1630)], title="Z Step Edge"),
}
R0 = np.sqrt(372 / np.pi)   # radius of one marker from the area of isolated markers (~372 px)

pts_all = []
for key, P in PANELS.items():
    fx = lin(P["x"][0], P["xv"][0], P["x"][1], P["xv"][1])
    fy = lin(P["y"][0], 8.0, P["y"][1], 12.0)
    rows = []
    for series, m in MASKS.items():
        m = m.copy()
        m[:, :P["xlim"][0]] = False
        m[:, P["xlim"][1]:] = False
        for (x0, y0, x1, y1) in P["legend"]:
            m[y0:y1, x0:x1] = False                      # legend symbols
        lab, n = ndimage.label(m)
        for i, sl in enumerate(ndimage.find_objects(lab), 1):
            sub = lab[sl] == i
            if sub.sum() < 100:
                continue
            pad = 3
            subp = np.pad(sub, pad)
            centres, err = split_disks(subp, R0)
            for cx, cy in centres:
                X, Y = sl[1].start + cx - pad, sl[0].start + cy - pad
                rows.append((series, float(fx(X)), float(fy(Y)), len(centres), round(err / (np.pi * R0 * R0), 2)))
                pts_all.append((X, Y))
    rows.sort(key=lambda r: (r[0] != "800 V", r[1]))
    write_csv(str(HERE / f"fig17{key}.csv"), [
        f"Xu et al. 2017 eLife 6:e25916, Figure 17({key}): '{P['title']}', Monte Carlo backscatter fraction vs step-edge position.",
        "Columns: series (legend '800 V' = blue circles, '1200 V' = orange circles; the caption calls these landing energies 800 eV and 1.2 keV),",
        "  x_nm = 'Nanometers' (edge position), backscatter_percent = 'Backscatter %',",
        "  n_in_cluster = number of circles fitted to the blob this marker belongs to (1 = isolated marker),",
        "  fit_mismatch = mismatched pixels of that blob's circle fit, in units of one marker's area (0 = perfect).",
        "Provenance: tier 3, digitized from the embedded raster image (~403 ppi, no vector data in the PDF) by fig17de_extract.py.",
        "  Axes calibrated on the light grey grid lines (y 8.0-12.0 every 0.5; x every 2 nm in d, every 5 nm in e); the grid is",
        "  evenly spaced to within 1 px. Markers: colour masks; touching markers are split by fitting equal circles of radius",
        f"  {R0:.1f} px (from isolated markers) to each blob.",
        f"Uncertainty: about +-{abs(fx(1) - fx(0)):.3f} nm in x and +-{abs(fy(1) - fy(0)):.4f} % in y per pixel; isolated markers ~1 px;",
        "  markers inside clusters (n_in_cluster > 1) ~2-3 px.",
    ], ["series", "x_nm", "backscatter_percent", "n_in_cluster", "fit_mismatch"], rows,
        fmt=["{}", "{:.3f}", "{:.3f}", "{}", "{}"])
    print(key, len(rows), [(r[0], round(r[1], 2), round(r[2], 2), r[3]) for r in rows])
overlay(a.astype(np.uint8), pts_all, work_path("fig17de_overlay.png"))
