#!/usr/bin/env python3
"""Re-plot Fig. 6h from fig6h.csv (as plain stacked bars; flow bands drawn as their left-end bars) -> fig6h_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("fig6h.csv"))
cols = ["Connects to target", "Target cell class", "Target cell type", "Functionally matched"]
fig, ax = plt.subplots(figsize=(3, 3.2))
for a in r:
    i = cols.index(a["column"])
    x, w = i, 0.8
    if a["column"] == "Functionally matched":
        x, w = (i - 0.2, 0.4) if a["segment"] == "Manual" else (i + 0.2, 0.4)
    ax.bar(x, float(a["height_pt"]), bottom=float(a["bottom_pt"]), width=w, color=a["colour"])
    if float(a["height_pt"]) > 8:
        ax.text(x, float(a["bottom_pt"]) + float(a["height_pt"]) / 2, a["segment"].split(" (")[0], ha="center", va="center",
                fontsize=5, color="white")
ax.set_xticks(range(4), cols, rotation=45, ha="right", fontsize=7)
ax.set_yticks([16.82 * k for k in range(7)], ["0"] + [""] * 6)
ax.set_ylim(0, 120)
ax.set_ylabel("Output synapses")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("fig6h_replot.png"), dpi=150)
