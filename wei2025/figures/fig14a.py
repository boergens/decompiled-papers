"""Re-plot Figure 14(a) of Wei et al. 2025 from fig14a.csv -> fig14a_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig14a.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5, 4.5))
x = range(len(rows))
ax.plot(x, [float(r["abs_avg_sliding_force_nN"]) for r in rows], "o--", color="b")
ax.set_xticks(list(x))
ax.set_xticklabels([r["label"] for r in rows], rotation=45, ha="right", fontweight="bold")
ax.set_xlim(-0.5, len(rows) - 0.5)
ax.set_ylim(0.5, 4.5)
ax.set_ylabel("Absolute value of average sliding force (nN)")
fig.tight_layout()
fig.savefig(HERE / "fig14a_replot.png", dpi=150)
