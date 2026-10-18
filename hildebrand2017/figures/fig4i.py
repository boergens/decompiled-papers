"""Re-plot Fig. 4i from fig4i.csv -> fig4i_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig4i.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
fig, ax = plt.subplots(figsize=(8, 1.6))
for s, col, lab in (("swapped", "#f4a0a0", "swapped right MeLc and Mauthner"), ("original", "k", "original")):
    xs = [float(r["slice"]) for r in rows if r["series"] == s]
    ys = [float(r["sum"]) for r in rows if r["series"] == s]
    ax.plot(xs, ys, color=col, lw=1, label=lab)
ax.axvline(5560, color="r", lw=2)
ax.set_xlim(2013, 11500)
ax.set_ylim(0, 10)
ax.set_xticks([2013, 5013, 8013, 11013])
ax.set_xticks(range(2013, 11500, 1000), minor=True)
ax.set_yticks([0, 10])
ax.set_xlabel("position in series, slice")
ax.set_ylabel("sum of all\nnormalized a and d", fontsize=7)
ax.legend(frameon=False, fontsize=7)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(HERE / "fig4i_replot.png", dpi=150)
