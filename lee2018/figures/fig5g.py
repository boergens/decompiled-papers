"""Re-plot Fig 5(g) of Lee et al. 2018 from fig5g.csv -> fig5g_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig5g.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5, 3.6))
for name, ls in (("Section pickup time", "--"), ("Section pickup and placement time", "-")):
    for r in rows:
        if r["series"] != name or not r["count"] or float(r["count"]) <= 0:
            continue
        x0, x1, h = float(r["bin_left_s"]), float(r["bin_right_s"]), float(r["count"])
        ax.bar(x0, h, width=x1 - x0, align="edge", color="0.6", alpha=0.5, edgecolor="0.3", linestyle=ls, linewidth=0.8)
    ax.plot([], [], color="0.3", ls=ls, label=name)
ax.set_xlim(0, 100)
ax.set_ylim(0, 250)
ax.set_xticks([0, 50, 100])
ax.set_yticks([0, 250])
ax.set_xlabel("Single section cycle time [s]")
ax.set_ylabel("Section count")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig5g_replot.png", dpi=150)
