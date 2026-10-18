"""Re-plot Figure 10(d) of Wei et al. 2025 from fig10d.csv -> fig10d_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig10d.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5, 4.5))
x = range(len(rows))
ax.bar(x, [float(r["H_avg_GPa"]) for r in rows], width=0.35, color="r", edgecolor="k")
ax.set_xticks(list(x))
ax.set_xticklabels([r["label"] for r in rows], rotation=45, ha="right")
ax.set_xlim(-0.5, len(rows) - 0.5)
ax.set_ylim(0, 2.5)
ax.set_ylabel("Average hardness (GPa)")
fig.tight_layout()
fig.savefig(HERE / "fig10d_replot.png", dpi=150)
