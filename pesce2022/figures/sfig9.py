"""Re-plot Supplementary Fig. 9 of Pesce et al. 2022 from sfig9.csv -> sfig9_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "sfig9.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
bars = [r for r in rows if r["row_type"] == "bar"]
pts = [r for r in rows if r["row_type"] == "point"]
labels = [r["condition"] for r in bars]
fig, ax = plt.subplots(figsize=(6, 4.4))
for i, r in enumerate(bars):
    m, sd = float(r["mean"]), float(r["sd"])
    ax.bar(i, m, width=0.64, fill=False, edgecolor="0.25", lw=2)
    ax.plot([i, i], [m, m + sd], color="0.25", lw=2)
    ax.plot([i - 0.16, i + 0.16], [m + sd, m + sd], color="0.25", lw=2)
for r in pts:
    i = labels.index(r["condition"])
    ax.plot(i, float(r["value"]), "o", color="0.3", alpha=0.45, ms=7, mec="none")
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontweight="bold")
ax.set_xlim(-0.6, len(labels) - 0.4)
ax.set_ylim(0, 3600)
ax.set_yticks(range(0, 3501, 500))
ax.set_yticklabels(["0,0", "5,0x10$^2$", "1,0x10$^3$", "1,5x10$^3$", "2,0x10$^3$", "2,5x10$^3$", "3,0x10$^3$", "3,5x10$^3$"])
ax.set_ylabel("Intensity", fontweight="bold")
ax.set_title("Stripping efficiency", loc="right", fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig9_replot.png"), dpi=150)
