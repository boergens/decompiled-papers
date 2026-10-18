"""Re-plot Figure 10(a) of Wei et al. 2025 from fig10a.csv -> fig10a_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig10a.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"Pyramid-0°": "k", "Pyramid-45°": "r", "Sphere (R=10 Å)": "lime", "Sphere (R=14.5 Å)": "b",
       "Sphere (R=20 Å)": "c", "Sphere (R=25 Å)": "m"}
fig, ax = plt.subplots(figsize=(5, 4))
for s, c in COL.items():
    ln = [r for r in rows if r["series"] == s and r["kind"] == "line"]
    x = np.array([float(r["hc_A"]) for r in ln])
    y = np.array([float(r["Er_GPa"]) for r in ln])
    gap = np.where(np.diff(x) > 0.2)[0] + 1          # leave gaps where the line is hidden
    ax.plot(np.insert(x, gap, np.nan), np.insert(y, gap, np.nan), color=c, lw=1.5, label=s)
    mk = [r for r in rows if r["series"] == s and r["kind"] == "marker"]
    ax.plot([float(r["hc_A"]) for r in mk], [float(r["Er_GPa"]) for r in mk], "o", mfc="w", mec=c, ms=4)
ax.set_xlim(-2.5, 27.5)
ax.set_ylim(-5, 80)
ax.set_yticks(list(range(0, 81, 10)))
ax.set_xticks(range(0, 26, 5))
ax.set_xlabel("Indentation depth $h_c$ (Å)")
ax.set_ylabel("Reduced modulus $E_r$ (GPa)")
ax.legend(fontsize=8, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig10a_replot.png", dpi=150)
