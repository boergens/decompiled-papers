"""Re-plot Fig. 6c and 6f of Kubota et al. 2018 from fig6c.csv / fig6f.csv -> fig6c_replot.png, fig6f_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
for panel, ymax, yt in (("c", 2.5, [0, 0.5, 1.0, 1.5, 2.0, 2.5]), ("f", 3.0, [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])):
    with open(os.path.join(HERE, f"fig6{panel}.csv")) as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    kevs = list(dict.fromkeys(r["kev"] for r in rows))
    fig, axs = plt.subplots(1, 6, figsize=(13, 1.9), sharey=True)
    for ax, kv in zip(axs, kevs):
        r = [q for q in rows if q["kev"] == kv]
        x = [float(q["gray_value"]) for q in r]
        y = [float(q["counts"]) for q in r]
        ax.fill_between(x, 0, y, color="black", lw=0)
        ax.set_xlim(0, 255)
        ax.set_xticks(range(0, 241, 40))
        ax.set_xticks(range(0, 241, 20), minor=True)
        ax.tick_params(labelsize=6)
        ax.set_xlabel("Gray scale", fontsize=7)
        ax.set_title(f"({kv} keV image)", fontsize=7)
    top = max(float(q["counts"]) for q in rows)
    axs[0].set_ylim(0, max(ymax, top) * 1.03)   # the 5 keV peak of 6f rises above the top tick (3.0)
    axs[0].set_yticks(yt)
    axs[0].set_ylabel("Counts", fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"fig6{panel}_replot.png"), dpi=150)
