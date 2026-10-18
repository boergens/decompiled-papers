"""Re-plot Figure 3e of He et al. 2018 from fig3e.csv -> fig3e_replot.png (six histograms, 3 x 2)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig3e.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
titles = ["cuboid 1 top sub-slice", "cuboid 1 bottom sub-slice", "cuboid 2 top sub-slice",
          "cuboid 2 bottom sub-slice", "cuboid 3 top sub-slice", "cuboid 3 bottom sub-slice"]
fig, axs = plt.subplots(3, 2, figsize=(7, 6.5), sharex=True, sharey=True)
for ax, t in zip(axs.flat, titles):
    for series, col in (("red", "red"), ("green", "tab:green")):
        r = [q for q in rows if q["subplot"] == t and q["series"] == series]
        x = [float(q["x_1e3_atoms_per_voxel"]) for q in r]
        y = [float(q["frequency"]) if q["frequency"] else float("nan") for q in r]   # 'hidden' dots: no y
        ax.plot(x, y, "-o", color=col, ms=3, lw=1.2)
    ax.set_title(t, fontsize=9)
    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 200)
    ax.set_xticks([-10, -5, 0, 5, 10])
    ax.set_yticks([0, 50, 100, 150, 200])
    ax.grid(color="0.85")
fig.supxlabel("Number of lead atoms (10$^3$ /voxel)")
fig.supylabel("Frequency")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3e_replot.png"), dpi=150)
