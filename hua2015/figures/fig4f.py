"""Re-plot Fig. 4f of Hua et al. 2015 from fig4f.csv (tier 1, authors' .mat data) -> fig4f_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
x, y = [], []
with open(os.path.join(HERE, "fig4f.csv")) as f:
    for r in csv.DictReader(l for l in f if not l.startswith("#")):
        x.append(float(r["p_e"]))
        y.append(float(r["p_pe_plotted"]))
fig, ax = plt.subplots(figsize=(3.2, 1.8))
ax.plot(x, y, color="b", lw=0.8)
ax.set_yscale("log")
ax.set_ylim(1e-1, 1e3)
ax.set_xlim(-0.1, 1.1)
ax.set_xticks([0, 1])
ax.set_yticks([1e-1, 1e1, 1e3])
ax.set_xlabel("$p_e$")
ax.set_ylabel("$p(p_e)$")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4f_replot.png"), dpi=150)
