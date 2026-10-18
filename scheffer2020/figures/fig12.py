"""Re-plot Fig. 12 from fig12.csv -> fig12_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig12.csv", newline="") as f:
    rows = list(csv.DictReader(r for r in f if not r.startswith("#")))
x = list(range(1, len(rows) + 1))
fig, ax = plt.subplots(figsize=(9, 6))
ax.bar(x, [float(r["n_types"]) for r in rows], width=0.95, color="#3a78b0")
ax.set_xticks(x)
ax.set_xticklabels([r["neurons_in_type"] for r in rows])
ax.set_xlim(0.5, len(x) + 0.5)
ax.set_ylim(0, 2145)
ax.set_yticks([0, 500, 1000, 1500, 2000])
ax.yaxis.grid(True, color="#e5e5e5")
ax.set_axisbelow(True)
ax.set_ylabel("#types", style="italic")
ax.set_xlabel("#neurons in a type", style="italic")
fig.tight_layout()
fig.savefig(HERE / "fig12_replot.png", dpi=100)
