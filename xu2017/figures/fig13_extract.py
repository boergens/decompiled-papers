"""Digitize the three Monte Carlo scatter plots of Figure 13 of Xu et al. 2017 (PDF p. 24) as ink-density grids.

Source: the embedded raster image of Figure 13 (2295 x 1164 px, ~321 ppi). Each plot shows one dot per simulated
backscattered electron (energy vs back-scatter angle) for 1.2 keV primary electrons on gold, epoxy and Pt Tetrakis.
The dots overlap far too much to be counted, so each plot is given as the fraction of dark pixels per bin.
    python3 -I -B figures/fig13_extract.py  -> figures/fig13left.csv, fig13middle.csv, fig13right.csv (+ work/fig13_mask.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from digitize_common import write_csv, fit_axis  # noqa: E402
from xu_helpers import load, work_path  # noqa: E402
from PIL import Image  # noqa: E402

a = load(24).astype(int)
g = a.mean(2)
dark = g < 128
ink = 1 - g / 255.0               # 0 = white, 1 = black

# y: the rotated tick labels of the left plot (1.2, 1.0, ..., 0.2, 0) are centred on rows 70, 161.5, 248, 333.5, 412.5, 491, 572.
fy, yres, yslope = fit_axis([70, 161.5, 248, 333.5, 412.5, 491, 572], [1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0])
# x: labels 0, 20, 40, 60, 80 under each plot (centroids of the label text)
PANELS = {
    "left": dict(label="Gold", xl=[271, 416, 554.5, 707.5, 846.5], cols=(271, 905),
                 dashed_cols=[(264, 272), (584, 594)]),
    "middle": dict(label="Epoxy C21H25O5", xl=[931, 1076, 1214.5, 1367.5, 1506.5], cols=(931, 1566),
                   dashed_cols=[(905, 913), (923, 932), (1244, 1254)]),
    "right": dict(label="Pt Tetrakis Pt[(C6H5)3P]4", xl=[1592, 1738, 1876, 2029, 2167.5], cols=(1592, 2226),
                  dashed_cols=[(1566, 1574), (1578, 1587), (1900, 1909)]),
}
valid = np.ones(dark.shape, bool)
for P in PANELS.values():
    for c0, c1 in P["dashed_cols"]:
        valid[:, c0:c1] = False                                 # dashed window lines and the y axis lines
valid[530:539, :] = False                                       # bottom dashed line (0.1 keV)
valid[571:578, :] = False                                       # x axis line
for P in PANELS.values():                                       # top dashed line (1.2 keV), from the y axis to 45 deg
    valid[60:72, P['dashed_cols'][0][0]:P['dashed_cols'][-1][1]] = False
# text labels ('Gold', 'Epoxy C21H25O5', ...): connected dark pieces of >= 60 px in the lower right of each plot
lab, n = ndimage.label(dark)
sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
big = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 60])
text = np.zeros_like(dark)
for P in PANELS.values():
    c0, c1 = P["cols"]
    sub = big[440:580, c1 - 200:c1]
    ys, xs = np.nonzero(sub)
    if len(xs):
        text[440 + ys.min() - 4:440 + ys.max() + 5, c1 - 200 + xs.min() - 4:c1 - 200 + xs.max() + 5] = True
valid &= ~text
Image.fromarray(np.where(valid[..., None], a, [255, 0, 255]).astype(np.uint8)).save(work_path("fig13_mask.png"))

DA, DE = 2.0, 0.025            # bin size: 2 degrees x 0.025 keV
for key, P in PANELS.items():
    fx, xres, xslope = fit_axis(P["xl"], [0, 20, 40, 60, 80])
    c0, c1 = P["cols"]
    cols = np.arange(c0, c1)
    rows = np.arange(56, 577)
    ang = fx(cols)
    en = fy(rows)
    out = []
    for e0 in np.arange(0, 1.2, DE):
        rsel = rows[(en >= e0) & (en < e0 + DE)]
        for a0 in np.arange(0, 90, DA):
            csel = cols[(ang >= a0) & (ang < a0 + DA)]
            if len(rsel) == 0 or len(csel) == 0:
                continue
            v = valid[np.ix_(rsel, csel)]
            if v.sum() < 0.3 * v.size:
                continue
            frac = ink[np.ix_(rsel, csel)][v].mean()
            out.append((a0 + DA / 2, e0 + DE / 2, float(frac), int(v.sum())))
    write_csv(str(HERE / f"fig13{key}.csv"), [
        f"Xu et al. 2017 eLife 6:e25916, Figure 13, {key} scatter plot ('{P['label']}'): Monte Carlo backscattered electrons for",
        "  1.2 keV primary electrons, plotted as one black dot per electron, 'Energy (KeV)' vs 'Back Scatter Angle(degrees)'.",
        "  The dots overlap far too much to count, so this is an INK-DENSITY GRID, not electron counts: ink_fraction = mean darkness",
        "  (1 - grey/255) of the pixels in each bin, an uncalibrated measure of dot density that saturates where the dots merge (near 1.2 keV).",
        f"Columns: angle_deg / energy_keV = bin centre ({DA:g} deg x {DE:g} keV bins); ink_fraction; n_px = number of source pixels used",
        "  (pixels on the dashed 0-45 deg / 0.1-1.2 keV window lines, the axis lines and the printed sample label are left out,"
        "  so bins at 1.2 keV inside the window and bins under the label rely on fewer pixels;",
        "  bins with less than 30 % usable pixels are omitted).",
        "Provenance: tier 3, from the embedded raster image (~321 ppi, no vector data in the PDF) by fig13_extract.py.",
        f"  y: linear fit to the centroids of the rotated tick labels 0-1.2 of the left plot (all three plots share the rows), max residual {yres:.3f} keV;",
        f"  x: linear fit to the centroids of the labels 0-80 under this plot, max residual {xres:.2f} deg. Check: the dashed window lines",
        f"  (nominal 0.1 keV and 45 deg per the table below the plots) come out at {float(fy(534)):.3f} keV and"
        f" {float(fx(np.mean(P['dashed_cols'][-1]))):.1f} deg.",
        f"Uncertainty: calibration about +-0.01 keV and +-1 deg; one source pixel = {abs(yslope):.4f} keV x {abs(xslope):.3f} deg.",
    ], ["angle_deg", "energy_keV", "ink_fraction", "n_px"], out, fmt=["{:.1f}", "{:.4f}", "{:.4f}", "{}"])
    print(key, len(out), "bins; x residual", round(xres, 2), "dashed right line at", [round(float(fx((c0d + c1d) / 2)), 2) for c0d, c1d in P["dashed_cols"][-1:]])
print("y residual", round(yres, 4), "bottom dashed line (row 534) at", round(float(fy(534)), 4), "keV")
