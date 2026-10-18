"""Re-plot Extended Data Fig. 5j from edfig5j.csv -> edfig5j_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "edfig5j.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
names = [r["category"] for r in rows]
vals = [float(r["sections"]) for r in rows]
fig, ax = plt.subplots(figsize=(2.2, 3))
ax.bar(range(3), vals, color="0.85", edgecolor="k", width=0.6)
ax.set_xticks(range(3), names, rotation=20)
ax.set_ylim(0, 90)
ax.set_yticks([0, 30, 60, 90])
ax.set_yticks(range(0, 91, 10), minor=True)
ax.set_ylabel("sections")
ax.text(2.4, 88, f"{sum(vals):.0f} total", ha="right", va="top")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(HERE / "edfig5j_replot.png", dpi=150)
