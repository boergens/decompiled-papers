"""Extended Data Fig. 1l (membrane contrast vs location in the sample, three protocols) -> edfig1l.csv

Tier 1: Edmond 'Extended Data Fig.1/Extended Data Fig. 1l/3. Calculated contrast values/contrast_data.mat'
(contrast_all, 9 cells: per-subimage median intensity difference membrane vs non-membrane, from
membrane_contrast_calculating.m). Cell order = alphabetical folder order of '1. Fiji processed raw images'
(Fig.1c/1d/1e x core/intermediate/peripheral) as the image counts show: cells 1-3 = Fig.1c peripheral (10 images),
intermediate (7), core (5); 4-6 = Fig.1d; 7-9 = Fig.1e (folder names use an older figure numbering).
EDF_Fig1l.m plots mean +- std (MATLAB std, n-1) of cells 1-3 (legend 'Hua'), 4-6 ('This protocol (d)'), 7-9
('This protocol (e)') at x = Peripheral, Intermediate, Core. Matching to the printed colours by value: 1-3 = black
'Hua (FIg.1b upper row)', 4-6 = magenta 'm' (Extended Data Fig. 1m, Os3), 7-9 = blue 'FIg.1b bottom row' (Os24).
Check: circle-marker centres digitized from the raster figure (PDF p. 12; y fitted on 11 ticks 0..100).
Run: python3 -I edfig1l_extract.py
"""
import os
import sys

import numpy as np
import scipy.io as sio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, SRC, WORK, dark_mask, fit, hue_mask, overlay, page_image, write_csv  # noqa: E402

m = sio.loadmat(os.path.join(SRC, "Extended Data Fig.1/Extended Data Fig. 1l/3. Calculated contrast values/contrast_data.mat"),
               squeeze_me=True)
cells = [np.atleast_1d(c).astype(float) for c in m["contrast_all"]]
a = page_image(12)
py2y, y2py, ry = fit([2300, 2331.5, 2363, 2394, 2425.5, 2456.5, 2488, 2519, 2550.5, 2582, 2613], range(100, -1, -10))
XC = [717.5, 820.0, 929.0]
locs = ["Periphery", "Intermediate", "Core"]
groups = [("Hua (Fig.1b upper row)", "black", 0, dark_mask(a, 90, 50)),
          ("This protocol (m, Os3)", "magenta", 3, hue_mask(a, 140, 165, 80, 120)),
          ("This protocol (Fig.1b bottom row, Os24)", "blue", 6, hue_mask(a, 110, 130, 120, 80))]
rows, ov = [], []
for name, col, k0, mask in groups:
    for j in range(3):
        c = cells[k0 + j]
        mean, sd = c.mean(), c.std(ddof=1)
        xc = int(XC[j])
        y0 = int(y2py(mean)) - 20
        win = mask[y0:y0 + 40, xc - 14:xc + 15]
        # marker ring: rows that contain >= 4 mask pixels spread over > 6 columns
        r, cc = np.where(win)
        pc = f"{float(py2y(y0 + np.median(r))):.1f}" if len(r) > 10 else ""
        rows.append([name, col, locs[j], k0 + j + 1, len(c), f"{mean:.3f}", f"{sd:.3f}", pc,
                     " ".join(f"{v:g}" for v in c)])
        ov += [(XC[j], y2py(mean)), (XC[j], y2py(mean + sd)), (XC[j], y2py(mean - sd))]
write_csv(os.path.join(HERE, "edfig1l.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 1l: 'Intensity difference membrane vs. background' (grey levels",
    "  after imadjust) at Periphery / Intermediate / Core of 2-mm samples, mean +- s.d. over subimages.",
    "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU, 'Extended Data Fig. 1l/3. Calculated contrast",
    "  values/contrast_data.mat' (contrast_all), read by edfig1l_extract.py; mean and sd (n-1) as in EDF_Fig1l.m.",
    "  Mapping of cells to series and locations: see the script docstring.",
    "plotted_center: median row of the series colour near the marker in the printed figure (tier 3 check, +-1.5 units;",
    "  markers of different series overlap at Periphery). The asterisks above Intermediate and Core are not data.",
    "Columns: series; colour; location; cell (1-based index in contrast_all); n_images; mean; sd; plotted_center;",
    "  values (all per-image values, space separated).",
], ["series", "colour", "location", "cell", "n_images", "mean", "sd", "plotted_center", "values"], rows)
overlay(a, ov, os.path.join(WORK, "edfig1l_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig1l_overlay_full.png")).crop((560, 2250, 1200, 2711)).save(os.path.join(WORK, "edfig1l_overlay.png"))
for r in rows:
    print(r[:8])
