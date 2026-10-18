#!/usr/bin/env python3
"""Re-plot Fig. 3d from fig3d.csv (depth grid, nm) -> fig3d_replot.png."""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(HERE, "fig3d.csv")) as f:
    r = csv.reader(l for l in f if not l.startswith("#"))
    next(r)
    for row in r:
        rows.append([float(v) if v else np.nan for v in row])
g = np.array(rows)
# approximation of the printed bar: black - blue - cyan - green - yellow - orange
cmap = LinearSegmentedColormap.from_list("scm", [(0, "black"), (0.12, "black"), (0.3, "#0055ff"), (0.5, "#00f0ff"),
                                                 (0.62, "#30ff00"), (0.75, "#fff000"), (1, "#ff7000")])
cmap.set_bad("#d8c8a8")
fig, ax = plt.subplots(figsize=(8.4, 3.6))
im = ax.imshow(g, cmap=cmap, vmin=-550, vmax=0, interpolation="nearest")
ax.set_title("3D laser SCM (digitized depth, nm; grey-beige = not mapped)")
ax.set_xticks([]); ax.set_yticks([])
cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.06, pad=0.04, ticks=[-550, -400, -200, 0])
cb.set_label("Depth (nm)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3d_replot.png"), dpi=120)
