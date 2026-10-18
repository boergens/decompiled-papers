"""Re-plot Figure 12(b) of Xu et al. 2017 from fig12b.csv -> fig12b_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig12b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(9, 1.6))
for b in sorted({r["sample_bias_V"] for r in rows}, key=float):
    seg = [r for r in rows if r["sample_bias_V"] == b]
    xs = [float(r["x_frac"]) for r in seg]
    ys = [float(r["counts_mid"]) if r["counts_mid"] else 0.0 for r in seg]
    ax.plot([xs[0]] + xs + [xs[-1]], [0] + ys + [0], color="0.15", lw=1.5)
for y in (1000, 2000, 3000):
    ax.axhline(y, color="0.75", lw=0.8)
ax.set_xlim(0, 1)
ax.set_ylim(0, 4000)
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylabel("Electron Counts")
fig.tight_layout()
fig.savefig(HERE / "fig12b_replot.png", dpi=150)
