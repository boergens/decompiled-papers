"""Re-plot Fig. 15 from fig15.csv -> fig15_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig15.csv", newline="") as f:
    rows = list(csv.DictReader(r for r in f if not r.startswith("#")))
fig, ax = plt.subplots(figsize=(11, 5.3))
ax.set_facecolor("#e5ecf6")
for s, col, off in (("upstream", "#85d885", -1.25), ("downstream", "#2b802b", 1.25)):
    rr = [r for r in rows if r["series"] == s]
    ax.bar([float(r["bin_centre_pct"]) + off for r in rr], [int(r["count"]) for r in rr], width=2.5, color=col, label=s)
ax.set_xlim(-2.5, 102.5)
ax.set_ylim(0, 418)
ax.set_xticks(range(0, 101, 10))
ax.set_yticks(range(0, 401, 50))
ax.yaxis.grid(True, color="white")
ax.set_axisbelow(True)
ax.set_xlabel("% valid connections")
ax.set_ylabel("Cell Type Count")
ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig15_replot.png", dpi=100)
