"""Re-plot Figure 10(c) of Wei et al. 2025 from fig10c.csv -> fig10c_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig10c.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5, 4.5))
x = range(len(rows))
ax.bar(x, [float(r["Er_avg_GPa"]) for r in rows], width=0.35, color="b", edgecolor="k")
ax.set_xticks(list(x))
ax.set_xticklabels([r["label"] for r in rows], rotation=45, ha="right")
ax.set_xlim(-0.5, len(rows) - 0.5)
ax.set_ylim(0, 8)
ax.set_ylabel("Average reduced modulus $E_r$ (GPa)")
fig.tight_layout()
fig.savefig(HERE / "fig10c_replot.png", dpi=150)
