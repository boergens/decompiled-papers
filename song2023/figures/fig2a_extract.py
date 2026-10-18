"""Fig. 2a (bar chart, mean inter-error distance along axons) of Song et al. 2023 -> fig2a.csv.

Tier 1 (source data): ../source/edmond_RG58DU/extracted/data/Fig.2/Fig.2a/data.mat
(the authors' MATLAB workspace behind Fig2a_MIED.m: per-axon path length (um) and number of c2+c3
discontinuities for 20 H6 axons ('data') and 21 control axons ('data2'), plus the saved 100 resamples).
Bar = total path length / total discontinuities (mIED_H6, mIED_AMK in the .mat, um -> mm).
Whiskers as coded in Fig2a_MIED.m: bar +- 0.5 * (75th - 25th percentile) of the resampled IEDs.

Check against the printed figure: the bars and whiskers are vector paths on PDF p. 3; the y axis is
calibrated on its eight tick marks (0 ... 0.7 mm). The as-plotted values are written next to the source values.
Run: python3 -I fig2a_extract.py
"""
import csv
import os

import numpy as np
import pymupdf
import scipy.io as sio

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../source/edmond_RG58DU/extracted/data/Fig.2/Fig.2a/data.mat")
PDF = os.path.join(HERE, "../source/41592_2023_Article_1866.pdf")


def mprctile(x, p):
    """MATLAB prctile (midpoint rule, Inf kept)."""
    x = np.sort(np.asarray(x, float)); n = len(x)
    q = (np.arange(1, n + 1) - 0.5) / n * 100
    return np.interp(p, q, x)


m = sio.loadmat(SRC, squeeze_me=True)
src = {}
for name, key, ied in (("Hemisphere", "data", "IED_H6"), ("Control", "data2", "IED_AMK")):
    d = m[key]
    mied = d[:, 0].sum() / d[:, 1].sum() / 1000  # mm
    lo, hi = mprctile(m[ied], [25, 75]) / 1000
    src[name] = dict(n_axons=len(d), path_mm=d[:, 0].sum() / 1000, n_err=int(d[:, 1].sum()), mied=mied,
                     p25=lo, p75=hi, half=0.5 * (hi - lo),
                     mied_saved=float(m["mIED_H6" if key == "data" else "mIED_AMK"]) / 1000)

# --- vector paths (as printed) ---
page = pymupdf.open(PDF)[2]
clip = pymupdf.Rect(270, 195, 345, 290)
ticks, rects = [], []
for dr in page.get_drawings():
    r = dr["rect"]
    if not (clip.x0 <= r.x0 and r.x1 <= clip.x1 and clip.y0 <= r.y0 and r.y1 <= clip.y1):
        continue
    if dr.get("color") is not None and abs(r.y1 - r.y0) < 0.01 and r.x1 < 287.2 and r.x0 > 283:
        ticks.append(r.y0)
    for it in dr["items"]:
        if it[0] == "re":
            rects.append((dr.get("fill"), it[1]))
ticks = sorted(ticks)[::-1]  # bottom (0) to top (0.7)
assert len(ticks) == 8, ticks
vals = np.arange(8) * 0.1
A = np.vstack([ticks, np.ones(8)]).T
(a, b), res, *_ = np.linalg.lstsq(A, vals, rcond=None)
resid = np.max(np.abs(A @ [a, b] - vals))
y2v = lambda y: a * y + b  # noqa: E731
plotted = {}
for name, col, x0, x1 in (("Hemisphere", (0.157, 0.667, 0.882), 292, 309), ("Control", (0.369, 0.369, 0.369), 316, 333)):
    fill = [r for f, r in rects if f and abs(f[0] - col[0]) < 0.01 and x0 < r.x0 < x1][0]
    caps = [r for f, r in rects if f == (0.0, 0.0, 0.0) and x0 < r.x0 < x1 and 9 < (r.x1 - r.x0) < 11 and (r.y1 - r.y0) < 1]
    caps = sorted((c.y0 + c.y1) / 2 for c in caps)
    plotted[name] = dict(bar=y2v(fill.y0), cap_hi=y2v(caps[0]), cap_lo=y2v(caps[-1]))

rows = []
for name in ("Hemisphere", "Control"):
    s, p = src[name], plotted[name]
    rows.append([name, s["n_axons"], f"{s['path_mm']:.6f}", s["n_err"], f"{s['mied']:.6f}", f"{s['mied_saved']:.6f}",
                 f"{s['p25']:.6f}", f"{s['p75']:.6f}", f"{s['mied_saved'] - s['half']:.6f}", f"{s['mied_saved'] + s['half']:.6f}",
                 f"{p['bar']:.4f}", f"{p['cap_lo']:.4f}", f"{p['cap_hi']:.4f}"])
with open(os.path.join(HERE, "fig2a.csv"), "w", newline="") as f:
    for h in [
        "Song et al. 2023 Nat Methods, Fig. 2a (bar chart): mean inter-error distance along manually traced axons (mm),",
        "  striatum of hemisphere H6 ('Hemisphere', blue bar) vs control SBEM dataset ('Control', gray bar).",
        "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU, data/Fig.2/Fig.2a/data.mat (= Fig2a_data.mat for the",
        "  per-axon table), read by fig2a_extract.py. Columns n_axons..whisker_high_mm are computed from it:",
        "  mean_IED_mm = total path length / total number of c2+c3 discontinuities (as in Fig2a_MIED.m);",
        "  mean_IED_saved_mm = the scalar mIED_H6 / mIED_AMK saved in data.mat. For the hemisphere it differs from the",
        "  value recomputed from the saved per-axon table (total path 1405.75 um saved vs 1423.82 um in the table, same",
        "  3 discontinuities); the printed bar (0.470) matches the saved scalar (0.469), not the table (0.475).",
        "  p25_mm, p75_mm = 25th/75th percentiles (MATLAB prctile) of the 100 saved resampled IEDs (IED_H6, IED_AMK);",
        "  whisker_low/high_mm = mean_IED_saved -+ 0.5*(p75-p25), which is how Fig2a_MIED.m draws the error bar.",
        "Columns plotted_*: read from the vector paths of the printed figure (PDF p. 3), y axis fitted on 8 tick marks",
        f"  (0..0.7 mm; the ticks are unevenly spaced, max fit residual {resid:.4f} mm), so plotted values are good to ~0.003 mm.",
        "Agreement: the printed bar heights agree with the saved mean IEDs within 0.002 mm. The printed whiskers do NOT match the",
        "  saved resamples (printed half-lengths ~0.19 mm for both groups; saved: 0.186 and 0.176 mm): the figure was",
        "  evidently drawn from a different random resampling (randi) than the one saved in data.mat. The KS test on",
        "  the saved resamples (dc23 vs dc23_2) gives P = 0.26 (asymptotic), not the P = 0.4814 of the caption.",
        "  (The printed hemisphere whiskers are centred at 0.475 mm, the table-recomputed mean, while its bar is at 0.470.)",
    ]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["group", "n_axons", "total_path_mm", "n_discontinuities", "mean_IED_mm", "mean_IED_saved_mm", "p25_mm", "p75_mm",
                "whisker_low_mm", "whisker_high_mm", "plotted_bar_mm", "plotted_whisker_low_mm", "plotted_whisker_high_mm"])
    w.writerows(rows)
print(rows, resid)

# --- overlay: source-data bar tops (magenta) and saved-resample whiskers (green) on a 4x render of the region ---
from PIL import Image, ImageDraw  # noqa: E402
Z = 4
reg = pymupdf.Rect(270, 195, 345, 290)
pix = page.get_pixmap(clip=reg, matrix=pymupdf.Matrix(Z, Z))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dd = ImageDraw.Draw(im)
v2y = lambda v: (v - b) / a  # noqa: E731
for (name, x0, x1) in (("Hemisphere", 293, 307.5), ("Control", 317.5, 332)):
    s = src[name]
    for v, col in ((s["mied_saved"], (255, 0, 255)), (s["mied_saved"] - s["half"], (0, 200, 0)), (s["mied_saved"] + s["half"], (0, 200, 0))):
        y = (v2y(v) - reg.y0) * Z
        dd.line([((x0 - reg.x0) * Z, y), ((x1 - reg.x0) * Z, y)], fill=col, width=1)
im.save(os.path.join(HERE, "../work/fig2a_overlay.png"))
