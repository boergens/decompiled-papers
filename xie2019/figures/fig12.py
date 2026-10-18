"""Re-plot Figure 12 (a) and (b) of Xie & Fang 2019 from fig12a.csv and fig12b.csv -> fig12_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def load(p):
    with open(HERE / f"fig12{p}.csv") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
for ax, p, ylim, step in ((axs[0], "a", (10, 170), 20), (axs[1], "b", (22, 46), 4)):
    rows = load(p)
    for s, c in (("Ft", "#4472c4"), ("Fn", "#ed7d31")):
        x = [float(r["tool_edge_radius_nm"]) for r in rows if r["series"] == s]
        y = [float(r["cutting_force_nN"]) for r in rows if r["series"] == s]
        if x:
            ax.plot(x, y, "o-", color=c, label=s, ms=6)
    ax.set_xlim(0, 10)
    ax.set_xticks(range(11))
    ax.set_ylim(*ylim)
    ax.set_yticks(range(ylim[0], ylim[1] + 1, step))
    ax.grid(color="0.85")
    ax.set_xlabel("Tool edge radius R(nm)")
    ax.set_ylabel("Cutting forces(nN)")
    ax.text(0.08, 0.92, p + ")", transform=ax.transAxes, style="italic")
    ax.legend(loc="center right")
fig.tight_layout()
fig.savefig(HERE / "fig12_replot.png", dpi=150)
