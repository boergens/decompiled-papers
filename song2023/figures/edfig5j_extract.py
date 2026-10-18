"""Extended Data Fig. 5j (Raman spectra of Os(vi) + FeCN and Os(vi), two wavenumber windows) -> edfig5j.csv

Tier 1: Edmond 'Extended Data Fig.6/Extended Data Fig.6j,k/' (the folder name says Extended Data Fig. 6, but the
data are the Raman spectra of Extended Data Fig. 5j,k; same in the code folder 'Extended Data Fig.6jk'):
data_batch2.mat (data2.osvi = Os(vi) in CaC), data_batch3.mat (data3.osvi_FeCNii_400 = Os(vi) + FeCN(ii)),
peak_calibration_allrounds.mat (x2_c, x3_c = calibrated Raman shift, cm-1). data2/data3 hold MATLAB 'table'
objects, decoded with song_common.mat_tables (column Var2 = counts). The processing is that of the authors'
Extended_data_Fig6jk.m, figure 41: in each window a straight baseline (linspace between the two constants written
in the script) is subtracted, and in the 750-1010 cm-1 window Os(vi)+FeCN is scaled by 0.9 and Os(vi) by 2.7.
Not shown in the paper: the 'os viii' and 'rO' curves that the script also plots.
Check: the processed points are drawn onto the raster figure (PDF p. 18; x fitted separately on the ticks of the
two x-axis segments, y on ticks 0..2 x10^4) and the printed red/blue traces are compared with them.
Run: python3 -I edfig5j_extract.py
"""
import os
import sys

import numpy as np
import scipy.io as sio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, SRC, WORK, fit, hue_mask, mat_tables, overlay, page_image, write_csv  # noqa: E402

P = os.path.join(SRC, "Extended Data Fig.6/Extended Data Fig.6j,k")
cal = sio.loadmat(os.path.join(P, "peak_calibration_allrounds.mat"), squeeze_me=True)
x2c, x3c = cal["x2_c"], cal["x3_c"]
d2 = mat_tables(os.path.join(P, "data_batch2.mat"), "data2")
d3 = mat_tables(os.path.join(P, "data_batch3.mat"), "data3")


def win(x, y, lo, hi, b0, b1, scale=1.0):
    idx = np.where((x > lo) & (x < hi))[0]
    return x[idx], scale * (y[idx] - np.linspace(b0, b1, len(idx))), y[idx]


curves = [  # (series, window, x, processed y, raw y, provenance string)
    ("Os vi+FeCN", "750-1010", *win(x3c, d3["osvi_FeCNii_400"]["Var2"], 750, 1010, 3.007e4, 2.674e4, 0.9),
     "data3.osvi_FeCNii_400, x3_c; 0.9*(y - linspace(3.007e4, 2.674e4))"),
    ("Os vi", "750-1010", *win(x2c, d2["osvi"]["Var2"], 750, 1010, 1.057e4, 9524, 2.7),
     "data2.osvi, x2_c; 2.7*(y - linspace(1.057e4, 9524))"),
    ("Os vi+FeCN", "1900-2300", *win(x3c, d3["osvi_FeCNii_400"]["Var2"], 1900, 2300, 4.823e4 + 5564, 5.528e4 + 7704),
     "data3.osvi_FeCNii_400, x3_c; y - linspace(4.823e4+5564, 5.528e4+7704)"),
    ("Os vi", "1900-2300", *win(x2c, d2["osvi"]["Var2"], 1900, 2300, 1.1918e4 + 7161, 2.374e4 + 392),
     "data2.osvi, x2_c; y - linspace(1.1918e4+7161, 2.374e4+392)"),
]
a = page_image(18)
xl = fit([815, 879, 942, 1005, 1068], [800, 850, 900, 950, 1000])
xr = fit([1147, 1229, 1310, 1392, 1474], [1900, 2000, 2100, 2200, 2300])
py2y, y2py, ry = fit([1725, 1664, 1602, 1543, 1483], [0, 0.5e4, 1e4, 1.5e4, 2e4])
masks = {"Os vi+FeCN": hue_mask(a, 170, 8, 100, 100), "Os vi": hue_mask(a, 105, 125, 100, 60)}
import cv2  # noqa: E402
dist = {k: cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 3) for k, m in masks.items()}
rows, ov, notes = [], [], []
for name, w, x, y, raw, how in curves:
    x2p = xl[1] if w == "750-1010" else xr[1]
    xp, yp = x2p(x), y2py(y)
    ok = (yp > 1480) & (yp < 1728)
    dd = dist[name][np.round(yp[ok]).astype(int), np.round(xp[ok]).astype(int)]
    notes.append(f"{name} {w} cm-1: {len(x)} points, {100 * np.mean(dd <= 2):.0f}% within 2 px of the printed {name} trace "
                 f"(median {np.median(dd):.1f} px)")
    for xi, yi, ri in zip(x, y, raw):
        rows.append([name, w, f"{xi:.3f}", f"{yi:.1f}", f"{ri:g}", how])
    ov += list(zip(xp, yp))
write_csv(os.path.join(HERE, "edfig5j.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 5j: Raman spectra, Intensity (a.u., x10^4 on the axis) vs",
    "  'Wavelength (cm-1)' (Raman shift), Os vi+FeCN (red) and Os vi (blue), windows 750-1010 and 1900-2300 cm-1.",
    "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU, folder 'Extended Data Fig.6/Extended Data Fig.6j,k'",
    "  (mislabelled: these are the ED Fig. 5j,k Raman data), MATLAB tables decoded by song_common.mat_tables;",
    "  processed exactly as in the authors' Extended_data_Fig6jk.m (baseline + scale, column 'processing').",
    "Check against the printed figure (raster p. 18, tier-3 calibration of both x-axis segments and y):",
] + ["  " + n for n in notes] + [
    "  Red curves: on the printed trace in both windows. Os vi, 750-1010: a least-squares fit of the printed blue trace",
    "  to 'scale*raw + linear baseline' gives scale 2.73 (script: 2.7), rms 41 counts, i.e. it matches (the low hit rate",
    "  comes from overlap with red). Os vi, 1900-2300: the printed blue trace lies ~600 counts above the script's",
    "  processing; the best fit is 1.96*raw + another linear baseline (rms 250 counts, the noise level). The red FeCN",
    "  peaks there are printed at ~1.48 and ~1.8 x10^4, the script gives 2.25 x10^4 for the higher one. So the paper",
    "  used a different baseline/scale in the 1900-2300 window than the deposited script; the values follow the script.",
    "  750-1010 window: peak maxima Os vi+FeCN 1.59e4 at 882 cm-1, Os vi 1.07e4 at 916 cm-1 (printed ~1.6 and ~1.15).",
    "Columns: series; window_cm1; raman_shift_cm1 (calibrated); intensity (processed, as plotted); raw_counts; processing.",
], ["series", "window_cm1", "raman_shift_cm1", "intensity", "raw_counts", "processing"], rows)
overlay(a, ov, os.path.join(WORK, "edfig5j_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig5j_overlay_full.png")).crop((600, 1380, 1500, 1800)).save(os.path.join(WORK, "edfig5j_overlay.png"))
print("\n".join(notes))
