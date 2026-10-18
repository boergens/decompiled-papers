"""Re-plot Figure 2B of Tegethoff & Briggman 2024 from fig2b.csv -> fig2b_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig2b.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
cats = ["1.34", "1.57", "1.83", "2.11", "2.44"]
fig, ax = plt.subplots(figsize=(5, 2.8))
x = [cats.index(r["nma_ddsa_ratio"]) + 1 + float(r["x_offset"]) for r in rows]
ax.plot(x, [float(r["hardness_HV"]) for r in rows], "o", ms=1.8, color="k")
ax.set_xlim(0, 5.75)
ax.set_xticks(range(1, 6))
ax.set_xticklabels(cats)
ax.set_ylim(9.5, 15)
ax.set_yticks(range(10, 16))
ax.set_yticks([9.5 + 0.5 * i for i in range(12)], minor=True)
ax.grid(axis="y", which="both", color="0.92")
ax.set_xlabel("NMA:DDSA ratio")
ax.set_ylabel("Hardness (HV)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2b_replot.png"), dpi=150)
