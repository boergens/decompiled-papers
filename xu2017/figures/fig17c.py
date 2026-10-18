"""Re-plot Figure 17(c) of Xu et al. 2017 from fig17c.csv.gz -> fig17c_replot.png"""
import csv
import gzip
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

HERE = Path(__file__).resolve().parent
with gzip.open(HERE / "fig17c.csv.gz", "rt") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
# node positions read off the printed colour bar (fraction of its height from the bottom)
cmap = LinearSegmentedColormap.from_list("bar", [(0, "black"), (0.07, "black"), (0.17, "#560099"), (0.29, "#0a00ff"), (0.45, "#00ffed"),
                                                 (0.60, "#00ff09"), (0.77, "#fffa00"), (0.92, "#ff0000"), (1, "#ff0000")])
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.set_facecolor("black")
sc = ax.scatter([float(r["x_nm"]) for r in rows], [float(r["z_nm"]) for r in rows],
                c=[float(r["bar_fraction"]) for r in rows], cmap=cmap, vmin=0, vmax=1, s=0.15, marker="s", lw=0)
ax.set_xlim((-11.6, 11.8))
ax.set_ylim((-11, 0.5))
ax.set_aspect("equal")
ax.grid(color="w", lw=0.5)
ax.set_xticks([-10, -5, 0, 5, 10])
ax.set_yticks([0, -5, -10])
ax.set_xlabel("nm")
fig.colorbar(sc, ax=ax, label="position on colour bar (0 = '0 eV', 1 = '1.2 KeV')", shrink=0.7)
fig.tight_layout()
fig.savefig(HERE / "fig17c_replot.png", dpi=150)
