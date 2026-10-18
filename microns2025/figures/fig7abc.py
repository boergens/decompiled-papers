#!/usr/bin/env python3
"""Re-plot Fig. 7a-c from fig7{a,b,c}.csv.gz (density maps) -> fig7abc_replot.png."""
import csv
import gzip
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

fig, axs = plt.subplots(1, 3, figsize=(10, 3.4))
for ax, p, cmap in zip(axs, "abc", ["Reds", "Reds", "Blues"]):
    with gzip.open(Path(__file__).with_name(f"fig7{p}.csv.gz"), "rt") as f:
        r = list(csv.DictReader(l for l in f if not l.startswith("#")))
    ax.scatter([float(a["postsyn_depth_um"]) for a in r], [float(a["presyn_depth_um"]) for a in r],
               c=[float(a["ink"]) for a in r], cmap=cmap, vmin=0, vmax=0.8, s=0.05, marker="s", lw=0, rasterized=True)
    ax.set_xlim(-10, 750)
    ax.set_ylim(750, 0)
    ax.set_xticks(range(0, 701, 100))
    ax.set_yticks(range(0, 701, 100))
    ax.set_xlabel("Postsynaptic soma depth (µm)")
    ax.set_ylabel("Presynaptic soma depth (µm)")
    ax.set_title(p, loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("fig7abc_replot.png"), dpi=150)
