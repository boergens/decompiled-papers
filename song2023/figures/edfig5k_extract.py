"""Extended Data Fig. 5k (Raman, 750-1010 cm-1: Os(vi) + FeCN in vitro vs brain staining solution after FeCN)
-> edfig5k.csv

Tier 1: Edmond 'Extended Data Fig.6/Extended Data Fig.6j,k/data_round4.mat' (data4.y.brain_fecnii, data4.y.osvi_fecnii,
counts) with x4 from peak_calibration_allrounds.mat (Raman shift, cm-1), processed as in the authors'
Extended_data_Fig6jk.m, figure 51: in 750-1010 cm-1 a straight baseline is subtracted
(brain: linspace(1141, 1048-22); Os(vi)+FeCN: linspace(1479, 1389-22)). The printed y axis (0, 1, 2) carries no
multiplier, and the printed curves are NOT the script's output: they are rescaled. A least-squares fit of each printed
trace (raster PDF p. 18, axes fitted on the tick marks, curve centres traced by colour) to
'scale * raw counts + linear baseline' gives the mapping used for column intensity_axis (tier-3 calibration of a
tier-1 spectrum, like a y-scale fitted to the figure).
Run: python3 -I edfig5k_extract.py
"""
import os
import sys

import cv2
import numpy as np
import scipy.io as sio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, SRC, WORK, fit, hue_mask, overlay, page_image, trace, write_csv  # noqa: E402

P = os.path.join(SRC, "Extended Data Fig.6/Extended Data Fig.6j,k")
cal = sio.loadmat(os.path.join(P, "peak_calibration_allrounds.mat"), squeeze_me=True)
d4 = sio.loadmat(os.path.join(P, "data_round4.mat"), squeeze_me=True, struct_as_record=False)["data4"]
x4 = cal["x4"]
idx = np.where((x4 > 750) & (x4 < 1010))[0]
curves = [("Osvi + FeCN", "data4.y.osvi_fecnii - linspace(1479, 1389-22)", d4.y.osvi_fecnii[idx].astype(float), 1479, 1389 - 22, (170, 8)),
          ("Brain FeCN", "data4.y.brain_fecnii - linspace(1141, 1048-22)", d4.y.brain_fecnii[idx].astype(float), 1141, 1048 - 22, (50, 85))]
a = page_image(18)
px2x, x2px, rx = fit([1552, 1615, 1679, 1742, 1805, 1868.5], [750, 800, 850, 900, 950, 1000])
YT = [1725, 1664, 1602, 1541, 1480]
rows, ov, notes = [], [], []
py2y, y2py, ry = fit(YT, [0, 0.5, 1, 1.5, 2])
xs_all = x4[idx]
for name, how, raw, b0, b1, (h0, h1) in curves:
    y = raw - np.linspace(b0, b1, len(idx))
    mask = hue_mask(a, h0, h1, 100, 80)
    tx, ty = trace(mask, 1556, 1866, 1478, 1723)
    ok = np.isfinite(ty)
    xc, yc = px2x(tx[ok]), py2y(ty[ok])
    r_ = np.interp(xc, xs_all, raw)
    A = np.vstack([r_, xc, np.ones_like(xc)]).T
    (sc, c1, c0), *_ = np.linalg.lstsq(A, yc, rcond=None)
    rms = float(np.sqrt(np.mean((yc - A @ [sc, c1, c0]) ** 2)))
    ya = sc * raw + c1 * xs_all + c0
    notes.append(f"{name}: printed = {sc:.6f} * raw {c1:+.6f} * x {c0:+.4f} (1 printed unit = {1 / sc:.0f} counts); "
                 f"rms {rms:.3f} printed units over {ok.sum()} traced columns")
    ov += list(zip(x2px(xs_all), y2py(ya)))
    for xi, yi, yai, ri in zip(xs_all, y, ya, raw):
        rows.append([name, f"{xi:.3f}", f"{yi:.1f}", f"{yai:.4f}", f"{ri:g}", how])
write_csv(os.path.join(HERE, "edfig5k.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 5k: Raman spectra 750-1010 cm-1, 'Osvi + FeCN' (red, in vitro)",
    "  and 'Brain FeCN' (green, brain staining solution after the FeCN step); dashed line at the Os(vi) peak (~880 cm-1).",
    "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU, 'Extended Data Fig.6/Extended Data Fig.6j,k/data_round4.mat'",
    "  and peak_calibration_allrounds.mat (x4), processed as in Extended_data_Fig6jk.m (figure 51), see script.",
] + ["  " + n for n in notes] + [
    "  The printed curves are also smoother than the deposited spectra (the raw points scatter by about +-0.1 printed",
    "  units around them): some smoothing was applied for the figure that is not in the deposited script.",
    "Columns: series; raman_shift_cm1; intensity (baseline-subtracted counts as in the script); intensity_axis (raw counts",
    "  mapped to the printed axis with the fitted scale and baseline above);",
    "  raw_counts; processing.",
], ["series", "raman_shift_cm1", "intensity", "intensity_axis", "raw_counts", "processing"], rows)
overlay(a, ov, os.path.join(WORK, "edfig5k_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig5k_overlay_full.png")).crop((1480, 1380, 1924, 1800)).save(os.path.join(WORK, "edfig5k_overlay.png"))
print(notes)
