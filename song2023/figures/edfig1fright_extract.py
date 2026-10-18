"""Extended Data Fig. 1f, right plot (EDS wt.% of Os, Fe, U for 1-mm samples with TCH, without TCH, with PG)
-> edfig1fright.csv

Tier 1: Edmond 'Extended Data Fig.1/Extended Data Fig. 1f/EDX/TCH.doc', 'no TCH.doc', 'PG.doc' (.docx files with EDAX
'Analysis Report' tables, 20 kV, 30 s live time; 3, 2 and 3 point measurements). All reports are in the CSV.
Which ones are plotted: each printed point and error bar matches the second report of its file (1-1-2,
8withou_TCH-4-2, 5with_PG-5-2) with error bar = +- Error (2-sig); the means of the reports do not match (e.g. TCH Os
mean 31.6 vs printed ~40). The digitized printed centre/half-bar (tier 3, raster PDF p. 12, y fitted on 7 ticks
0..60) is given for the visible points.
Run: python3 -I edfig1fright_extract.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, SRC, WORK, docx_eds_reports, fit, hue_mask, overlay, page_image, write_csv  # noqa: E402

a = page_image(12)
py2y, y2py, ry = fit([1276, 1321, 1366, 1411.5, 1456.5, 1501.5, 1546.5], [60, 50, 40, 30, 20, 10, 0])
XC = {"Os": 972, "Fe": 1065, "U": 1158}
files = {"TCH": ("TCH.doc", (105, 130, 80, 40)), "no TCH": ("no TCH.doc", (12, 25, 120, 120)), "PG": ("PG.doc", (170, 8, 90, 80))}
LW = 1.5
rows, ov = [], []
for cond, (fn, hh) in files.items():
    reps = docx_eds_reports(os.path.join(SRC, "Extended Data Fig.1/Extended Data Fig. 1f/EDX", fn))
    mask = hue_mask(a, *hh)
    for k, (title, kv, lt, els) in enumerate(reps):
        for el, line, inten, conc, err, mdl in els:
            if el not in XC:
                continue
            plotted = k == 1
            pc = ph = ""
            if plotted:
                xc = XC[el]
                r = np.where(mask[1270:1545, xc - 1:xc + 2].any(1))[0] + 1270
                if len(r) >= 6:
                    lo, hi = py2y(r.max() - LW), py2y(r.min() + LW)
                    pc, ph = f"{(lo + hi) / 2:.2f}", f"{(hi - lo) / 2:.2f}"
                ov += [(XC[el], y2py(conc)), (XC[el], y2py(conc + err)), (XC[el], y2py(conc - err))]
            rows.append([cond, el, title, line, f"{conc:.3f}", f"{err:.3f}", "yes" if plotted else "no", pc, ph])
write_csv(os.path.join(HERE, "edfig1fright.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 1f (right plot): wt.% of Os, Fe and U (EDS) in 1-mm samples",
    "  stained with TCH (blue), without TCH ('no TCH', orange) and with pyrogallol ('PG', red).",
    "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU, 'Extended Data Fig.1/Extended Data Fig. 1f/EDX/*.doc'",
    "  (EDAX reports, 20 kV, live time 30 s): conc_wt = Conc, error_2sig = Error (2-sig).",
    "plotted = yes: the report that matches the printed point (centre and +-error_2sig bar); see extract script.",
    "plotted_center, plotted_halfbar: digitized from the printed figure (tier 3, +-0.5 wt.%; part of the TCH bars is",
    "  hidden under PG, so its digitized values cover only the visible part; Fe points overlap, values unreliable).",
    "Note: Methods give 18 keV for EDS; these reports say 20 kV (ED Fig. 1b reports: 10 kV).",
], ["condition", "element", "report", "line", "conc_wt", "error_2sig", "plotted", "plotted_center", "plotted_halfbar"], rows)
overlay(a, ov, os.path.join(WORK, "edfig1fright_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig1fright_overlay_full.png")).crop((880, 1250, 1240, 1620)).save(os.path.join(WORK, "edfig1fright_overlay.png"))
for r in rows:
    if r[6] == "yes":
        print(r)
