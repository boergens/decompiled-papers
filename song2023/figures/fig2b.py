"""Re-plot Fig. 2b (bottom) of Song et al. 2023 from fig2b.csv -> fig2b_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(l for l in open(os.path.join(HERE, "fig2b.csv")) if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(2.6, 2.2))
for name, col in (("Control", "k"), ("Hemisphere", "#28aae1")):
    r = [x for x in rows if x["series"] == name]
    edges = [float(x["bin_lo_um"]) for x in r] + [float(r[-1]["bin_hi_um"])]
    c = np.array([float(x["count"]) for x in r])
    ax.stairs(c, edges, color=col, lw=1, label=name, baseline=None)
ax.set_yscale("log")
ax.set_xlim(0, 100)
ax.set_ylim(1, 1e6)
ax.set_yticks([1e1, 1e3, 1e5])
ax.set_xticks([0, 50, 100])
ax.set_xlabel("Axon path length (µm)")
ax.set_ylabel("Automatically\nreconstructed axons")
ax.legend(frameon=False, fontsize=7)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2b_replot.png"), dpi=200)
