"""Extended Data Fig. 5j: bar chart (sections per partial-section category), digitized (tier 3).

Reads the embedded raster image (150 ppi) of PDF page 37 straight from the source PDF, calibrates
the y axis on its ten tick marks (0..90 every 10; labels 0, 30, 60, 90 printed), and takes each bar's
value from the centre of its dark top outline (intensity-weighted). Writes edfig5j.csv and an overlay
in work/.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, fit_axis, overlay, write_csv  # noqa: E402

PDF = ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"
a = embedded_image(str(PDF), 37)
g = a.astype(float).mean(2)
ink = np.clip(200 - g, 0, None)  # darkness weight

# y-axis line is image column 804 (rows 622..849); ticks point left (cols 800-803)
tick_col = 801
col = ink[600:860, tick_col]
rows = np.where(col > 60)[0]
groups = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
tick_rows = [600 + float((g_ * col[g_]).sum() / col[g_].sum()) for g_ in groups]
assert len(tick_rows) == 10, tick_rows
vals = [90 - 10 * i for i in range(10)]
fy, res, _ = fit_axis(tick_rows, vals)

bars = [("minor", 826, 853), ("moderate", 876, 903), ("severe", 926, 952)]
out, pts = [], []
for name, c0, c1 in bars:
    cs = range(c0 + 4, c1 - 3)
    tops = []
    for c in cs:
        # walk up from just above the baseline through the light-grey bar fill to the dark top outline
        r = 840
        while ink[r, c] < 60:
            r -= 1
        run = np.arange(r - 2, r + 2)
        w = ink[run, c]
        tops.append(float((run * w).sum() / w.sum()))
    yt = float(np.median(tops))
    out.append((name, float(fy(yt)), round(abs(float(fy(yt)) - float(fy(yt + 1))), 2)))
    pts += [(c, yt) for c in cs]

hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Extended Data Fig. 5j: number of sections in each partial-section category",
    "(minor / moderate / severe) for the 208 partial sections within the 16000 sections imaged at 56.4x56.4x60 nm3/vx.",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster image on PDF page 37 (figures/edfig5j_extract.py).",
    f"y calibrated on 10 tick marks (0..90 step 10), linear fit, max residual {res:.2f} sections.",
    "value = centre of the bar's dark top outline (found by walking up from the baseline through the grey fill); uncertainty ~ one source pixel (column u_px, sections per pixel).",
    "Bar values are counts, so the true values are integers; the three digitized values sum to "
    + f"{sum(v for _, v, _ in out):.1f} (the panel prints '208 total').",
    "columns: category; sections (digitized bar height); u_px (sections per source pixel)",
]
write_csv(HERE / "edfig5j.csv", hdr, ["category", "sections", "u_px"], out, fmt=["{}", "{:.2f}", "{:.2f}"])
(ROOT / "work").mkdir(exist_ok=True)
overlay(a, pts + [(tick_col, r) for r in tick_rows], str(ROOT / "work" / "edfig5j_overlay.png"))
print(out, res)
