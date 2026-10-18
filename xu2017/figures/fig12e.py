"""Re-plot Figure 12(e) of Xu et al. 2017 from fig12e.csv and fig12e_markers.csv -> fig12e_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def read(name):
    with open(HERE / name) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


h, m = read("fig12e.csv"), read("fig12e_markers.csv")
biases = sorted({r["sample_bias_V"] for r in h}, key=float)
fig, axs = plt.subplots(1, 9, figsize=(13, 1.9), sharey=True)
for ax, b in zip(axs, biases):
    rr = [r for r in h if r["sample_bias_V"] == b]
    ax.plot([float(r["counts_per_pixel"]) for r in rr], [float(r["height_frac"]) for r in rr], "k", lw=0.8)
    for r in m:
        if r["sample_bias_V"] == b:
            ax.plot([float(r["counts_per_pixel"])] * 2, [0, float(r["height_frac"])], "k", lw=0.6)
    ax.set_xscale("log")
    ax.set_xlim(400, 4000)
    ax.set_ylim(0, 1)
    ax.set_xticks([500, 1000, 2000])
    ax.set_xticklabels(["500", "1000", "2000"], fontsize=6)
    ax.minorticks_off()
    ax.set_yticks([])
    ax.set_title(f"{b} V", fontsize=7)
fig.tight_layout()
fig.savefig(HERE / "fig12e_replot.png", dpi=150)
