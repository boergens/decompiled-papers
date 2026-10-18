"""Extended Data Fig. 5d (UV-vis absorption of potassium osmate(vi) in 0.15 M cacodylate buffer: fresh, 2 h, 24 h)
-> edfig5d.csv

Tier 1: Edmond 'Extended Data Fig.5/Extended Data Fig.5d/data.mat', struct data4, fields os_vi_cac, os_vi_cac_2h,
os_vi_cac_20h (two columns: wavelength nm, absorbance), as plotted by the authors' Extended_Data_Fig5d.m (legend
'fresh', '2h', '20h'; the paper's legend says '24 h'). All points 190-1380 nm are written; the panel shows 300-1000 nm.
Check: the three curves are traced in the raster figure (PDF p. 18; x fitted on ticks 400/600/800/1000 nm, y on ticks
0..0.3) by colour (blue, red-orange, yellow) and compared with the source data at the same wavelengths.
Run: python3 -I edfig5d_extract.py
"""
import os
import sys

import numpy as np
import scipy.io as sio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, SRC, WORK, fit, hue_mask, overlay, page_image, trace, write_csv  # noqa: E402

m = sio.loadmat(os.path.join(SRC, "Extended Data Fig.5/Extended Data Fig.5d/data.mat"), squeeze_me=True, struct_as_record=False)
d4 = m["data4"]
series = [("fresh", "os_vi_cac", (100, 112)), ("2 h", "os_vi_cac_2h", (2, 12)), ("24 h", "os_vi_cac_20h", (18, 28))]
a = page_image(18)
px2x, x2px, rx = fit([213, 279, 344, 410], [400, 600, 800, 1000])
py2y, y2py, ry = fit([737, 695.5, 654, 612, 569, 528, 486.5], [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3])
rows, ov, notes = [], [], []
for name, field, (h0, h1) in series:
    v = getattr(d4, field)
    wl, ab = v[:, 0], v[:, 1]
    o = np.argsort(wl)
    wl, ab = wl[o], ab[o]
    for w_, b_ in zip(wl, ab):
        rows.append([name, field, f"{w_:g}", f"{b_:.6g}"])
        if 300 <= w_ <= 1000:
            ov.append((x2px(w_), y2py(b_)))
    mask = hue_mask(a, h0, h1, 120, 120)
    xs, ys = trace(mask, 185, 408, 490, 735)
    ok = np.isfinite(ys)
    dif = py2y(ys[ok]) - np.interp(px2x(xs[ok]), wl, ab)
    notes.append(f"{name}: traced {ok.sum()} columns, median(printed - source) = {np.median(dif):+.4f}, "
                 f"median |diff| = {np.median(np.abs(dif)):.4f} absorbance units")
write_csv(os.path.join(HERE, "edfig5d.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 5d: UV-vis absorption (a.u.) of potassium osmate (vi) in sodium",
    "  cacodylate buffer, fresh (blue), after 2 h (red) and after 24 h (yellow); x = wavelength (nm), panel shows 300-1000 nm.",
    "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU, 'Extended Data Fig.5/Extended Data Fig.5d/data.mat',",
    "  data4.os_vi_cac, data4.os_vi_cac_2h, data4.os_vi_cac_20h (all 2381 points per curve, 190-1380 nm, 0.5-nm steps).",
    "  NB: the source field and the authors' plotting script call the third curve '20h'; the paper's legend says '24 h'",
    "  and Methods say time points 2 min, 2 h and 24 h.",
    "Check against the printed figure (traced curve centres, raster p. 18; overlaps make the traces partly mixed):",
] + ["  " + n for n in notes] + [
    "Columns: series (paper legend); source_field; wavelength_nm; absorbance.",
], ["series", "source_field", "wavelength_nm", "absorbance"], rows)
overlay(a, ov, os.path.join(WORK, "edfig5d_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig5d_overlay_full.png")).crop((100, 450, 470, 800)).save(os.path.join(WORK, "edfig5d_overlay.png"))
print(notes)
