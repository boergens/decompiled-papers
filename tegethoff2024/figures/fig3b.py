"""Re-plot Figure 3B of Tegethoff & Briggman 2024 from fig3b.csv -> fig3b_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig3b.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5, 2.8))
x = [float(r["humidity_percent"]) for r in rows]
y = [float(r["hardness_HV"]) for r in rows]
ax.plot(x, y, "o", ms=1.8, color="k")
for seq in sorted({r["sequence"] for r in rows}):
    xs = [float(r["humidity_percent"]) for r in rows if r["sequence"] == seq]
    ax.text(sum(xs) / len(xs), 13.6, seq, ha="center", fontsize=8)
ax.set_xlim(0, 100)
ax.set_ylim(0, 14)
ax.set_yticks(range(0, 15, 2))
ax.grid(axis="y", color="0.92")
ax.set_xlabel("Relative humidity (%)")
ax.set_ylabel("Hardness (HV)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3b_replot.png"), dpi=150)
