"""Re-plot Fig. 1b of Kubota et al. 2018 from fig1b.csv -> fig1b_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig1b.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
x = [float(r["length_m"]) for r in rows]
y = [float(r["surface_resistance_ohm_per_sq"]) for r in rows]
fig, ax = plt.subplots(figsize=(4, 2.8))
ax.plot(x, y, "o-", color="k", ms=5, lw=1.2)
ax.set_xlim(-0.3, 10.2)
ax.set_ylim(213, 322)          # the paper's axis is broken below 220 (a '0' sits under the break)
ax.set_xticks(range(0, 11, 2))
ax.set_xticks(range(0, 11), minor=True)
ax.set_yticks(range(220, 321, 20))
ax.set_xlabel("Length (meter)")
ax.set_ylabel("Surface resistance (Ω □$^{-1}$)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1b_replot.png"), dpi=150)
