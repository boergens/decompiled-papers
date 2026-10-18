"""Re-plot Fig. 11 from fig11.csv -> fig11_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig11.csv", newline="") as f:
    rows = list(csv.DictReader(r for r in f if not r.startswith("#")))
x = [int(r["order"]) for r in rows]
y = [float(r["n_types"]) for r in rows]
fig, ax = plt.subplots(figsize=(10, 6.2))
ax.bar(x, y, width=1.0, color="#3a78b0", edgecolor="white", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels([r["region"] for r in rows], rotation=-90)
ax.set_xlim(0.5, len(x) + 0.5)
ax.set_ylim(0, 1925)
ax.set_yticks([0, 500, 1000, 1500])
ax.yaxis.grid(True, color="#e5e5e5")
ax.set_axisbelow(True)
ax.set_ylabel("#types", style="italic")
ax.set_xlabel("brain regions", style="italic")
fig.tight_layout()
fig.savefig(HERE / "fig11_replot.png", dpi=100)
