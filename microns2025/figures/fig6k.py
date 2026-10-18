#!/usr/bin/env python3
"""Re-plot Fig. 6k from fig6k.csv -> fig6k_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("fig6k.csv"))
post = np.zeros((6, 80, 63)); pre = np.zeros((6, 1, 63))
for a in r:
    k, b = int(a["clip"]) - 1, int(a["time_bin"]) - 1
    if a["map"] == "presyn":
        pre[k, 0, b] = float(a["normalized_activity"])
    else:
        post[k, int(a["row"]) - 1, b] = float(a["normalized_activity"])
fig = plt.figure(figsize=(7, 2))
gs = fig.add_gridspec(2, 7, height_ratios=[1, 8], width_ratios=[1] * 6 + [0.08], wspace=0.08, hspace=0.05)
for k in range(6):
    a1 = fig.add_subplot(gs[0, k]); a1.imshow(pre[k], cmap="Greys", vmin=0, vmax=1, aspect="auto"); a1.axis("off")
    a1.set_title(f"Clip {k + 1}", fontsize=7)
    a2 = fig.add_subplot(gs[1, k]); im = a2.imshow(post[k], cmap="Greys", vmin=0, vmax=1, aspect="auto", interpolation="nearest")
    a2.set_xticks([]); a2.set_yticks([])
    if k == 0:
        a2.set_ylabel("Postsyn neurons", fontsize=7)
fig.colorbar(im, cax=fig.add_subplot(gs[1, 6]), label="Normalized activity")
fig.savefig(Path(__file__).with_name("fig6k_replot.png"), dpi=150, bbox_inches="tight")
