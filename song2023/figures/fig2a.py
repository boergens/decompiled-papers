"""Re-plot Fig. 2a of Song et al. 2023 from fig2a.csv -> fig2a_replot.png (bars = saved mean IED, whiskers as printed)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(l for l in open(os.path.join(HERE, "fig2a.csv")) if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(2.2, 3.2))
for i, (r, c) in enumerate(zip(rows, ["#28aae1", "#5e5e5e"])):
    m = float(r["mean_IED_saved_mm"])
    ax.bar(i, m, color=c, edgecolor="k", width=0.6)
    lo, hi = float(r["plotted_whisker_low_mm"]), float(r["plotted_whisker_high_mm"])
    ax.errorbar(i, (lo + hi) / 2, yerr=(hi - lo) / 2, color="k", capsize=8)
    ax.plot([i - 0.25, i + 0.25], [float(r["whisker_low_mm"])] * 2, "r:", lw=1)
    ax.plot([i - 0.25, i + 0.25], [float(r["whisker_high_mm"])] * 2, "r:", lw=1)
ax.set_xticks([0, 1], ["Hemi-\nsphere", "Control"])
ax.set_ylim(0, 0.7)
ax.set_yticks([0, 0.2, 0.4, 0.6])
ax.set_ylabel("Mean inter-error distance\nalong axons (mm)")
ax.set_title("Striatum", fontsize=9)
ax.text(0.5, 0.69, "red dotted: whiskers from saved resamples", fontsize=5, ha="center", color="r")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2a_replot.png"), dpi=200)
