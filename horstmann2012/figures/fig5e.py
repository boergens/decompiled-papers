"""Re-plot Figure 5E of Horstmann et al. 2012 from fig5e.csv -> fig5e_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig5e.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
x = [float(r["bin_centre_nm"]) for r in rows]
y = [float(r["count_digitized"]) for r in rows]

fig, ax = plt.subplots(figsize=(4.2, 3.2))
ax.bar(x, y, width=15, facecolor="white", edgecolor="black", linewidth=2)
ax.set_xlim(-12, 350)
ax.set_ylim(0, 13)
ax.set_xticks(range(0, 321, 40))
ax.set_yticks([0, 5, 10])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlabel("Distance SV to AZ [nm]", fontweight="bold")
ax.set_ylabel("No. SVs", fontweight="bold")
fig.tight_layout()
fig.savefig(HERE / "fig5e_replot.png", dpi=150)
