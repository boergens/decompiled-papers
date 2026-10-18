"""Digitize Fig. 4a of Kubota et al. 2018 (main PDF p. 6): emission spectra of the three tapes at four
excitation wavelengths (four sub-panels "Excitation 405/488/561/633 nm").

Source: the four embedded 300 ppi raster images (~342 x 341 px each); tick labels are PDF text (y labels only
on the first sub-panel; all four images have identical y tick rows, so the same values are used).
    python3 -I fig4a_extract.py  -> fig4a.csv (+ ../work/fig4a_<exc>_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from kubota_main_common import Img, calib, WORK  # noqa: E402
from digitize_common import tick_positions, tick_positions_v, trace_envelope, fit_axis, write_csv, overlay  # noqa: E402

PANELS = {405: (107.1, 68.9, 189.2, 150.7), 488: (202.5, 68.8, 284.6, 150.7),
          561: (300.3, 68.7, 382.4, 150.6), 633: (396.3, 68.8, 478.9, 150.7)}
XAX = (331, 332)                  # bottom axis line rows (same in all four images)
HW = 2                            # half the ~5 px line width
rows, notes = [], []

# y calibration from the first sub-panel: labels 0..25 (x10^3); 0 sits on the axis line
im0 = Img(6, PANELS[405])
k0 = (im0.g < 110) & (np.ptp(im0.a.astype(int), axis=2) < 60)
yt0 = tick_positions_v(k0, (9, 10), -1, 4, 40, XAX[0]) + [(XAX[0] + XAX[1]) / 2]
yl = [l for l in im0.labels((70, 55, 110, 160)) if l[0] <= 25 and l[1] < 0]
fy, ry, sy, yp, yv = calib(yt0, yl, 2)

for exc, bb in PANELS.items():
    im = Img(6, bb)
    a = im.a.astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    c0 = 11 if exc == 633 else 9          # y axis line column
    k = (im.g < 110) & (np.ptp(a, axis=2) < 60)
    # check that this sub-panel's y ticks sit where sub-panel 405's do
    yt = tick_positions_v(k, (c0, c0 + 1), -1, 4, 40, XAX[0])
    assert max(abs(p - q) for p, q in zip(sorted(yt), sorted(yt0[:-1]))) <= 1.5, (exc, yt, yt0)
    xt = tick_positions(k, XAX, +1, 4, c0 + 2, k.shape[1]) + [c0 + 0.5]      # the 400 nm tick is the y axis
    xl = [l for l in im.labels((bb[0] - 5, bb[3], bb[2] + 5, bb[3] + 12)) if -5 < l[1] < k.shape[1] + 5]
    fx, rx, sx, xp, xv = calib(xt, xl, 1)
    notes.append(f"  {exc} nm: x on {len(xp)} ticks {xv} (400 = the y-axis line), max residual {rx:.2f} nm")
    masks = {
        "CNT-PET": (R > 150) & (G < 110) & (B < 110),
        "Kapton": (B > 150) & (R < 120) & (G < 170),
        "cc-Kapton": k.copy(),
    }
    masks["cc-Kapton"][XAX[0]:, :] = False        # the axis line and ticks
    for m in masks.values():
        m[:, :c0 + 3] = False
        m[:36, :c0 + 12] = False                  # the axis-break marks
    pts = []
    for name, m in masks.items():
        env = trace_envelope(m, c0 + 3, m.shape[1], 30, XAX[1] + 3, HW, min_px=2)
        for c, ym, yu, ylo in env:
            if ym != ym:
                continue
            flag = ""
            col = np.where(m[30:XAX[1] + 3, int(c)])[0] + 30
            if name == "cc-Kapton" and col.max() >= XAX[0] - 1:
                # merged with the axis line: take the line's top edge + half width
                yu = ylo = ym = col.min() + HW
                flag = "touches the axis line; centre = top edge + half width"
            rows.append((exc, name, float(fx(c)), float(fy(ym)), float(fy(yu)), float(fy(ylo)), flag))
            pts += [(c, yu), (c, ylo)]
    overlay(im.a, pts, os.path.join(WORK, f"fig4a_{exc}_overlay.png"), colour=(0, 255, 0))

write_csv(os.path.join(HERE, "fig4a.csv"), [
    "Kubota et al. 2018 Nat Commun 9:437, Fig. 4a: 'Emission spectra' of the tapes, four sub-panels 'Excitation 405 nm',",
    "  '488 nm', '561 nm', '633 nm' (main PDF p. 6). Series per the colour key of Fig. 4c: red = CNT-PET, blue = Kapton,",
    "  black = cc-Kapton.",
    "Columns: excitation_nm (sub-panel); series; wavelength_nm (x axis 'Wavelength (nm)'); intensity_x1e3_mid = y axis",
    "  'Intensity gradations (16 bit)' in units of 10^3 (axis label 'x10^3'); _upper/_lower = the top and bottom of the",
    "  plotted line within this pixel column (they differ on steep flanks). One row per pixel column where the line's",
    "  colour is visible; columns where another series is drawn on top of it are missing.",
    "Provenance: tier 3, digitized from the four embedded 300 ppi raster images (no vector plot paths in the PDF) by",
    "  fig4a_extract.py: colour masks (red, blue, near-black), per-column line envelope (tools trace_envelope, half",
    "  line width 2 px of the ~5 px line). y calibrated on the tick marks of sub-panel 405 paired with its PDF-text",
    f"  labels 0-25, max residual {ry:.3f} x10^3 (0 = the axis line); the other sub-panels have the same tick rows",
    "  (checked to 1.5 px) and no labels of their own. x calibration per sub-panel:",
] + notes + [
    f"Uncertainty: about +-{2 * abs(sy):.2f} x10^3 in y (2 px) and +-2 nm in x; near 0 the three lines overlap each",
    "  other and the axis line, so values below ~0.5 x10^3 are rough.",
    "The y axis is broken: above 25 x10^3 (tick at ~27.6 by spacing) there is a break mark and a top tick labelled 65.5",
    "  (x10^3, the 16-bit maximum 65535). No line reaches the break.",
], ["excitation_nm", "series", "wavelength_nm", "intensity_x1e3_mid", "intensity_x1e3_upper", "intensity_x1e3_lower",
    "flag"], rows, fmt=["{}", "{}", "{:.1f}", "{:.3f}", "{:.3f}", "{:.3f}", "{}"])
print(len(rows), "rows; y", yp, yv, ry)
print("\n".join(notes))
