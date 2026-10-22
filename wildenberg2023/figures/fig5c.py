"""Re-plot Figure 5C of Wildenberg et al. 2023 from fig5c.csv -> fig5c_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig5c.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
x = [float(r["kerf_slices"]) for r in rows]
y = [float(r["accuracy_pct"]) for r in rows]
fig, ax = plt.subplots(figsize=(4.2, 2.0), facecolor="black")
ax.set_facecolor("black")
ax.plot(x, y, "-", color="#ed7d31", lw=2, zorder=2)
ax.plot(x, y, "o", mfc="white", mec="black", ms=5, zorder=3)
for r in rows:
    if r["printed_annotation"]:
        ax.annotate(r["printed_annotation"], (float(r["kerf_slices"]), float(r["accuracy_pct"])),
                    textcoords="offset points", xytext=(0, 6), ha="center", color="white", fontsize=7)
for v in (40, 60, 80, 100):
    ax.axhline(v, color="0.85", lw=0.6, ls=(0, (1, 2)), zorder=1)
ax.set_xlim(-10, 120)
ax.set_ylim(35, 108)
ax.set_xticks([0, 50, 100])
ax.set_xticklabels(["0", "50\n1.5 um", "100\n3 um"])
ax.set_yticks([40, 60, 80, 100])
ax.set_xlabel("Kerf size (slices/microns)", color="white")
ax.set_ylabel("Accuracy (%)", color="white")
ax.tick_params(colors="white")
for sp in ax.spines.values():
    sp.set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig5c_replot.png"), dpi=200, facecolor="black")
