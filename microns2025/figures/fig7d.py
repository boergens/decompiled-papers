#!/usr/bin/env python3
"""Re-plot Fig. 7d from fig7d.csv -> fig7d_replot.png (values, re-coloured with matplotlib maps)."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("fig7d.csv"))
ROWS7 = ["L2P", "L3P", "L4P", "L5ET", "L5NP", "L5IT", "L6P"]
left = np.zeros((7, 7)); top = np.zeros((7, 78)); depth = np.zeros((1, 78)); bot = {g: np.full((7, 78), np.nan) for g in ["DTC", "PTC", "ITC", "STC"]}
for a in r:
    v = float(a["value"]); c = int(a["column"]) - 1
    if a["submap"] == "left":
        left[ROWS7.index(a["row"]), c] = v
    elif a["submap"] == "top":
        top[int(a["row"].split()[-1]) - 1, c] = v
    elif a["submap"] == "depth":
        depth[0, c] = v
    else:
        bot[a["group"]][ROWS7.index(a["row"]), c] = v
fig = plt.figure(figsize=(10, 3.6))
gs = fig.add_gridspec(3, 2, width_ratios=[1, 11], height_ratios=[2.2, 0.6, 7], wspace=0.15, hspace=0.08)
ax = fig.add_subplot(gs[0, 1]); ax.imshow(top, cmap="Greys", vmin=0, vmax=8, aspect="auto", interpolation="nearest"); ax.axis("off")
ax = fig.add_subplot(gs[1, 1]); ax.imshow(depth, cmap="viridis", vmin=0, vmax=1, aspect="auto"); ax.axis("off")
ax = fig.add_subplot(gs[2, 1])
for g, cm, vmax in [("DTC", "Reds", 4000), ("PTC", "Blues", 4000), ("ITC", "Greens", 200), ("STC", "Oranges", 200)]:
    ax.imshow(np.ma.masked_invalid(bot[g]), cmap=cm, vmin=0, vmax=vmax, aspect="auto", interpolation="nearest")
ax.set_yticks(range(7), ROWS7); ax.set_xticks([16, 48.5, 70.5, 76], ["DTC", "PTC", "ITC", "STC"])
ax.set_xlabel("Number of order 1 inhibitory partner→order 2 excitatory partners synapses", fontsize=7)
ax = fig.add_subplot(gs[2, 0]); ax.imshow(left, cmap="Greys", vmin=0, vmax=250, aspect="auto", interpolation="nearest")
ax.set_xticks([]); ax.set_yticks([]); ax.set_ylabel("Number of L3a→order 1 excitatory\npartner synapses", fontsize=6)
fig.savefig(Path(__file__).with_name("fig7d_replot.png"), dpi=150, bbox_inches="tight")
