#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 1 (both plots) from edfig1a.csv / edfig1b.csv -> edfig1_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

fig, axs = plt.subplots(2, 1, figsize=(6, 7.5))
for ax, p, yk, ylim in [(axs[0], "a", "y_um", (200, 1300)), (axs[1], "b", "z_um", (590, 1130))]:
    r = mc.read_csv(Path(__file__).with_name(f"edfig1{p}.csv"))
    sc = ax.scatter([float(a["x_um"]) for a in r], [float(a[yk]) for a in r], c=[float(a["F1"]) for a in r],
                    cmap="magma_r", vmin=0.5, vmax=1, marker="s", s=12)
    ax.set_xlim(200 - 0.5 * 75, 1800)
    ax.set_ylim(*ylim)
    ax.set_xlabel("x (µm)")
    ax.set_ylabel(yk.replace("_um", " (µm)"))
    ax.set_title("Location of Synapse Test Volumes", fontsize=9)
    fig.colorbar(sc, ax=ax, label="F$_1$")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("edfig1_replot.png"), dpi=150)
