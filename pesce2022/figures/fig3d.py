"""Re-plot Fig. 3d of Pesce et al. 2022 from fig3d.csv -> fig3d_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig3d.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
bars = [r for r in rows if r["row_type"] == "bar"]
pts = [r for r in rows if r["row_type"] == "point"]
labels = [r["round"] for r in bars]
fig, ax = plt.subplots(figsize=(4.4, 3.6))
for i, r in enumerate(bars):
    m, sd = float(r["mean"]), float(r["sd"])
    ax.bar(i, m, width=0.68, fill=False, edgecolor="0.25", lw=2)
    ax.plot([i, i], [m, m + sd], color="0.25", lw=2)
    ax.plot([i - 0.2, i + 0.2], [m + sd, m + sd], color="0.25", lw=2)
for r in pts:
    ax.plot(labels.index(r["round"]), float(r["value"]), "o", color="0.45", alpha=0.6, ms=6, mec="none")
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontweight="bold")
ax.set_xlabel("SST label", fontweight="bold")
ax.set_xlim(-0.6, len(labels) - 0.4)
ax.set_ylim(0, 5.5)
ax.set_yticks(range(0, 6))
ax.set_ylabel("Signal to noise", fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3d_replot.png"), dpi=150)
