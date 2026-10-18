#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 3B (both panels) from edfig3b_left.csv / edfig3b_right.csv -> edfig3b_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

fig, axs = plt.subplots(1, 2, figsize=(9, 3.4))
for ax, side, title in [(axs[0], "left", "Soma Centers of Multi-Soma IDs as of 9/30/20"),
                        (axs[1], "right", "Soma Centers of Multi-Soma IDs as of 4/4/23")]:
    r = mc.read_csv(Path(__file__).with_name(f"edfig3b_{side}.csv"))
    sc = ax.scatter([float(a["x_um"]) for a in r], [float(a["y_um"]) for a in r], c=[float(a["z_um"]) for a in r],
                    cmap="plasma_r", vmin=600, vmax=1100, s=1.5, alpha=0.8)
    ax.set_xlim(200 - (75.39 - 70.37) / 25.83 * 200, 1800)
    ax.set_ylim(200 - (452.75 - 451.84) / 24.2 * 200, 1200 + (330.84 - 313.79) / 24.2 * 200)
    ax.invert_yaxis() if False else None
    ax.set_xlabel("x (µm)")
    ax.set_ylabel("y (µm)")
    ax.set_title(f"{title}\nn = {len(r)}", fontsize=8, loc="left")
fig.colorbar(sc, ax=axs[1], label="z (µm)")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("edfig3b_replot.png"), dpi=150)
