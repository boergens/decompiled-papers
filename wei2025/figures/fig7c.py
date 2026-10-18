"""Re-plot Figure 7(c) of Wei et al. 2025 from fig7c.csv -> fig7c_replot.png"""
import csv
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig7c.csv") as f:
    lines = f.read().splitlines()
rows = list(csv.DictReader(l for l in lines if not l.startswith("#")))
COL = {"x-direction": "k", "y-direction": "#eb4352", "z-direction": "#f847d6", "overall": "#322ff7"}
fig, ax = plt.subplots(figsize=(5, 4))
if 0:   # stage bands (not data), x extents from the CSV header
    hdr = " ".join(l for l in lines if l.startswith("#"))
    for name, colour in (("blue", "#eaeef9"), ("orange", "#fbe5d7"), ("green", "#f3f8f1")):
        mt = re.search(name + r" (-?[0-9.]+)-([0-9.]+)", hdr)
        if mt:
            ax.axvspan(float(mt.group(1)), float(mt.group(2)), color=colour, lw=0)
for s, c in COL.items():
    ln = [r for r in rows if r["series"] == s and r["kind"] == "line"]
    x = np.array([float(r["t_ps"]) for r in ln])
    y = np.array([float(r["force_nN"]) for r in ln])
    gap = np.where(np.diff(x) > 0.6)[0] + 1        # leave gaps where the line is hidden
    yu = np.array([float(r["force_nN_upper"]) for r in ln])
    yl = np.array([float(r["force_nN_lower"]) for r in ln])
    ax.fill_between(np.insert(x, gap, np.nan), np.insert(yl, gap, np.nan), np.insert(yu, gap, np.nan), color=c, lw=0, alpha=0.8)
    ax.plot(np.insert(x, gap, np.nan), np.insert(y, gap, np.nan), color=c, lw=1.0, label=s)
    mk = [r for r in rows if r["series"] == s and r["kind"] == "marker"]
    if mk:
        ax.plot([float(r["t_ps"]) for r in mk], [float(r["force_nN"]) for r in mk], "o", color=c, ms=3)
ax.set_xlim(-10, 150)
ax.set_xticks(range(0, 141, 20))
ax.set_ylim(-5, 13)
ax.set_yticks(list(range(-4, 13, 2)))
ax.set_xlabel("Time (ps)")
ax.set_ylabel("Pairwise interaction force (nN)")
ax.legend(fontsize=7, frameon=False, ncol=2 if len(COL) == 6 and "c" == "a" else 1)
fig.tight_layout()
fig.savefig(HERE / "fig7c_replot.png", dpi=150)
