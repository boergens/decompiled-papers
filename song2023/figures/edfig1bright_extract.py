"""Extended Data Fig. 1b, right plot (EDS wt.% of Os, Fe, U, Pb at periphery / middle / center) -> edfig1bright.csv

Tier 1: Edmond data/Extended Data Fig.1/Extended Data Fig. 1a-b/EDX/'EDS raw data.doc' (a .docx file): three EDAX
'Analysis Report' tables Image1-1, Image1-2, Image1-3 (10 kV, 60 s live time) with Conc (wt.%) and Error (2-sig) per
element (C, O, Fe, Os, Pb, U). Image1-1/1-2/1-3 = Periphery/Middle/Center (the only order consistent with the plot).
Check: the plotted points and error bars are digitized from the raster figure (PDF p. 12, embedded 300-ppi image;
y axis fitted on the 0/10/20/30 ticks) and written next to the source values.
Run: python3 -I edfig1bright_extract.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, SRC, WORK, docx_eds_reports, fit, hue_mask, hsv, overlay, page_image, write_csv  # noqa: E402

a = page_image(12)
py2y, y2py, ry = fit([102, 186, 270, 354], [30, 20, 10, 0])
XC = {"Periphery": 1631, "Middle": 1735, "Center": 1836}
reports = docx_eds_reports(os.path.join(SRC, "Extended Data Fig.1/Extended Data Fig. 1a-b/EDX/EDS raw data.doc"))
loc_of = {"Image1-1": "Periphery", "Image1-2": "Middle", "Image1-3": "Center"}
h = hsv(a)
masks = {"Os": hue_mask(a, 170, 8, 90, 80), "U": hue_mask(a, 105, 130, 80, 40), "Pb": hue_mask(a, 55, 85, 90, 80),
         "Fe": (h[..., 1] < 60) & (h[..., 2] > 60) & (h[..., 2] < 170)}
LW = 1.5  # half line width in px
rows, ov = [], []
for title, kv, lt, els in reports:
    loc = loc_of[title]
    for el, line, inten, conc, err, mdl in els:
        if el not in masks:
            continue
        xc = XC[loc]
        r = np.where(masks[el][60:352, xc - 1:xc + 2].any(1))[0] + 60
        if len(r) >= 6:
            lo, hi = py2y(r.max() - LW), py2y(r.min() + LW)
            pc, ph = f"{(lo + hi) / 2:.2f}", f"{(hi - lo) / 2:.2f}"
        else:
            pc = ph = ""
        rows.append([el, loc, title, line, f"{conc:.3f}", f"{err:.3f}", pc, ph])
        ov.append((xc, y2py(conc)))
write_csv(os.path.join(HERE, "edfig1bright.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 1b (right plot): EDS element concentration (WT.%) of Os, Fe, U, Pb",
    "  at Periphery, Middle and Center of the 2-mm sample of panel a (1-mm Hua protocol).",
    "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU, 'Extended Data Fig. 1a-b/EDX/EDS raw data.doc' (EDAX",
    "  reports Image1-1..1-3, 10 kV, live time 60 s); conc_wt = Conc, error_2sig = Error (2-sig) of the report.",
    "plotted_center, plotted_halfbar: digitized from the printed figure (tier 3; raster p. 12, y fitted on 4 ticks,",
    "  +-0.3 wt.%; empty where the point is hidden under another series or the axis).",
    "Agreement: the printed points lie 0.2-0.5 wt.% (2-4 px) above the report values, and the printed error bars are",
    "  about half the 2-sigma error (Os periphery: +-0.43 printed vs 0.868 2-sig). The plot was therefore made either",
    "  with +-1 sigma bars or from slightly different numbers than this file; the offset is larger than the reading error.",
    "Columns: element; location; report; line (X-ray line); conc_wt; error_2sig; plotted_center; plotted_halfbar (wt.%).",
], ["element", "location", "report", "line", "conc_wt", "error_2sig", "plotted_center", "plotted_halfbar"], rows)
overlay(a, ov, os.path.join(WORK, "edfig1bright_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig1bright_overlay_full.png")).crop((1540, 40, 1986, 400)).save(os.path.join(WORK, "edfig1bright_overlay.png"))
for r in rows:
    print(r)
