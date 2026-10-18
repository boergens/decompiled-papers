"""Re-plot Figure 1b of Nguyen et al. 2016 from fig1b.csv -> fig1b_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig1b.csv")) as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
x = [float(r["concentration_wt_pct"]) for r in rows]
y = [float(r["resistance_ohm_per_cm"]) for r in rows]

fig, ax = plt.subplots(figsize=(3.4, 2.2))
ax.plot(x, y, "o", color="k", ms=6)
ax.set_yscale("log")
ax.set_ylim(1, 1e4)
ax.set_xlim(3.4, 20)          # the x axis line starts left of the 5 tick in the figure
ax.set_xticks([5, 10, 15, 20])
ax.set_xlabel("Concentration (wt%)")
ax.set_ylabel("Resistance\n(Ω/cm)")
ax.spines[["top", "right"]].set_visible(False)
ax.minorticks_off()
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1b_replot.png"), dpi=150)
