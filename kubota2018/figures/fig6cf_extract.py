"""Digitize Fig. 6c and 6f of Kubota et al. 2018 (main PDF p. 10): intensity histograms (filled black) of the
images in Fig. 6a (BSD, 2-7 keV) and Fig. 6d (In-lens SE, 1-5 keV), six sub-panels each.

Source: one embedded 300 ppi raster image per row of six sub-panels; tick labels are PDF text (y labels only on
the first sub-panel of each row; the other sub-panels' y tick rows are checked to be the same).
    python3 -I fig6cf_extract.py  -> fig6c.csv, fig6f.csv (+ ../work/fig6c_overlay.png, fig6f_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from kubota_main_common import Img, calib, WORK  # noqa: E402
from digitize_common import tick_positions, tick_positions_v, frame_lines, fit_axis, write_csv, overlay  # noqa: E402

PANELS = {
    "c": dict(bb=(69.0, 214.8, 542.1, 267.0), xax=(204, 205), kev=["2", "3", "4", "5", "6", "7"],
              src="Fig. 6a (BSD, 3 nm pixel^-1, 7646 x 7793 pixel images)"),
    "f": dict(bb=(69.4, 438.6, 543.7, 511.9), xax=(295, 297), kev=["1", "1.5", "2", "3", "4", "5"],
              src="Fig. 6d (In-lens SE, 3 nm pixel^-1, 7354 x 7494 pixel images)"),
}

for panel, P in PANELS.items():
    im = Img(10, P["bb"])
    k = im.g < 128
    H, W = k.shape
    XAX = P["xax"]
    yaxes = [g for g in frame_lines(k[:XAX[0]], 0, 0.6) if g[1] - g[0] <= 2]   # the six thin y-axis lines (columns)
    assert len(yaxes) == 6, yaxes
    labs = im.labels((P["bb"][0] - 25, P["bb"][1] - 5, P["bb"][2] + 5, P["bb"][3] + 12))
    ylabs = [l for l in labs if l[1] < 0]
    rows, pts, notes = [], [], []
    yv0 = None
    for i, ya in enumerate(yaxes):
        # the scanned row of sub-panels is slightly tilted (axis rows drift by ~3 px over the image width),
        # so each sub-panel gets its own axis rows and y calibration
        c_blank = ya[1] + 15
        ax_rows = [r for r in range(XAX[0] - 6, XAX[1] + 6) if k[r, c_blank]]
        xax = (min(ax_rows), max(ax_rows))
        yt = tick_positions_v(k, ya, -1, 4, 0, xax[0] - 2) + [(xax[0] + xax[1]) / 2]
        if yv0 is None:
            fy, ry, sy, yp, yv0 = calib(yt, ylabs, 2)
        else:
            # same tick values in the same order as the labelled first sub-panel
            assert len(yt) == len(yv0), (panel, i, yt, yv0)
            fy, ry, sy = fit_axis(yt, sorted(yv0, reverse=True))
        x_end = yaxes[i + 1][0] - 25 if i < 5 else W
        line = np.where(k[xax[0]:xax[1] + 1, ya[1]:x_end].any(0))[0] + ya[1]
        brk = np.where(np.diff(line) > 4)[0]                 # end of the axis line (allow small gaps)
        x_last = int(line[brk[0]] if len(brk) else line[-1])
        xt = tick_positions(k, xax, +1, 3, ya[1] + 1, x_last + 3)
        xl = [l for l in labs if l[2] > xax[1] and ya[0] - 8 < l[1] < x_last + 12]
        fx, rx, sx, xp, xv = calib(xt, xl, 1)
        notes.append(f"  sub-panel {i + 1} ({P['kev'][i]} keV): axis rows {xax[0]}-{xax[1]}; y on {len(yt)} ticks, max residual "
                     f"{ry:.3f}; x on {len(xp)} labelled ticks {min(xv):g}-{max(xv):g}, max residual {rx:.2f}; axis line ends at "
                     f"gray value {float(fx(x_last)):.1f}")
        XAXi = xax
        for c in range(ya[1] + 2, x_last + 1):
            col = np.where(k[:XAXi[0] - 1, c])[0]
            top = float(col.min()) if len(col) else (XAXi[0] + XAXi[1]) / 2
            rows.append((P["kev"][i], float(fx(c)), max(0.0, float(fy(top))), "" if len(col) else "no fill above the axis line"))
            pts.append((c, top))
    overlay(im.a, pts, os.path.join(WORK, f"fig6{panel}_overlay.png"), colour=(255, 0, 255))
    write_csv(os.path.join(HERE, f"fig6{panel}.csv"), [
        f"Kubota et al. 2018 Nat Commun 9:437, Fig. 6{panel}: intensity histograms of the images in {P['src']},",
        "  one sub-panel per acceleration voltage (main PDF p. 10). The sub-panels carry no keV labels of their own;",
        f"  the kev column gives the voltage of the image above each, i.e. the column order of Fig. 6{'a' if panel == 'c' else 'd'}.",
        "Columns: kev; gray_value (x axis 'Gray scale', 0-255); counts = top of the filled histogram in this pixel column,",
        "  in the units of the y axis 'Counts' as labelled (0-2.5 / 0-3.0; no multiplier is printed, so the absolute",
        "  scale of the counts is not known). One row per pixel column (~2 per gray value).",
        "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector plot paths in the PDF) by",
        "  fig6cf_extract.py: top edge of the black fill per pixel column. y calibrated per sub-panel on its own tick",
        f"  marks and axis line (the image row is tilted by ~3 px over its width), with the values of the PDF-text labels",
        f"  of the first sub-panel ({min(yv0):g}-{max(yv0):g}; 0 = the axis line) in the same order. Per sub-panel:",
    ] + notes + [
        f"Uncertainty: about +-{2 * abs(sy):.3f} in counts and +-{2 * abs(float(fx(1)) - float(fx(0))):.1f} gray values (2 px).",
        "The authors' histogram data are named in the paper (ref. 70, Kubota, 'Electron micrographs and raw data for the",
        "  signal intensity histograms', figshare) but were not available here.",
    ], ["kev", "gray_value", "counts", "flag"], rows, fmt=["{}", "{:.2f}", "{:.4f}", "{}"])
    print(panel, len(rows), "rows; y values", yv0)
    print("\n".join(notes))
