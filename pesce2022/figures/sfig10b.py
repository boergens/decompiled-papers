"""Re-plot Supplementary Fig. 10b of Pesce et al. 2022 from sfig10b.csv -> sfig10b_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "sfig10b.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(3.4, 3.2))
for r in rows:
    a, b = float(r["post_clearing"]), float(r["stripping"])
    ax.plot([0, 1], [a, b], "-", color="k", lw=1, zorder=1)
    ax.plot(0, a, "s", color="#515151", ms=6, zorder=2)
    ax.plot(1, b, "s", color="#f14040", ms=6, zorder=2)
ax.plot([0, 0, 1, 1], [1.235, 1.245, 1.245, 1.235], color="k", lw=2)
ax.text(0.5, 1.247, "N.S.", ha="center", va="bottom", fontweight="bold", fontsize=8)
ax.set_xlim(-0.5, 1.5)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Post-clearing", "Stripping"])
ax.set_ylim(1.0, 1.25)
ax.set_yticks([1.0, 1.05, 1.1, 1.15, 1.2, 1.25])
ax.set_yticklabels(["1,00", "1,05", "1,10", "1,15", "1,20", "1,25"])
ax.set_ylabel("Tortuosity")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig10b_replot.png"), dpi=150)
