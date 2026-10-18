"""Re-plot Fig. 17 a-d from fig17.csv -> fig17_replot.png (grouped bars with error bars)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
with open(HERE / "fig17.csv") as fh:
    rows = list(csv.DictReader(line for line in fh if not line.startswith("#")))

COL = {"Fx": "blue", "Fy": "red", "Fz": "magenta"}
VEL = ["0.1", "0.5", "1.0", "1.5", "2.0"]
fig, axs = plt.subplots(2, 2, figsize=(9, 7.2))
for ax, (letter, hc) in zip(axs.flat, [("a", 5), ("b", 10), ("c", 15), ("d", 20)]):
    for j, comp in enumerate(("Fx", "Fy", "Fz")):
        r = [x for x in rows if x["panel"] == letter and x["component"] == comp]
        r.sort(key=lambda x: float(x["velocity_A_per_ps"]))
        xs = np.arange(5) + (j - 1) * 0.2
        v = np.array([float(x["force_nN"]) for x in r])
        lo = np.array([float(x["err_low_nN"]) for x in r])
        hi = np.array([float(x["err_high_nN"]) for x in r])
        ax.bar(xs, v, 0.18, color=COL[comp], label=comp)
        ax.vlines(xs, lo, hi, color="0.3", lw=0.8)
        ax.hlines(np.r_[lo, hi], np.r_[xs, xs] - 0.05, np.r_[xs, xs] + 0.05, color="0.3", lw=0.8)
    ax.axhline(0, color="k", lw=1)
    ax.set_ylim(-10, 6)
    ax.set_yticks(range(-10, 7, 2))
    ax.set_xticks(range(5))
    ax.set_xticklabels(VEL)
    ax.set_xlabel("Sliding velocity (Å/ps)")
    ax.set_ylabel("Force (nN)")
    ax.set_title(f"({letter}) $h_c$ = {hc} Å")
    ax.legend(loc="lower left", fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig17_replot.png", dpi=110)
