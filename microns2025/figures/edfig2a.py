#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 2A from edfig2a.csv -> edfig2a_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

rows = mc.read_csv(Path(__file__).with_suffix(".csv"))
fig, ax = plt.subplots(figsize=(4.2, 4))
bars = [r for r in rows if r["series"] == "All Cells"]
ax.bar([float(r["bin_left"]) for r in bars], [float(r["count"]) - 1 for r in bars], bottom=1,
       width=[float(r["bin_right"]) - float(r["bin_left"]) for r in bars], align="edge", color="#c6c8ca", label="All Cells")
for name, col in [("Dendrite Proofreading Complete", "#0073b1"), ("Cleaned Axons", "#ee7e31")]:
    s = sorted((r for r in rows if r["series"] == name), key=lambda r: int(r["bin"]))
    xs, ys = [], []
    for r in s:
        xs += [float(r["bin_left"]), float(r["bin_right"])]
        ys += [float(r["count"])] * 2
    ax.plot(xs, ys, color=col, lw=0.8, label=name)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(10 ** -0.175, 10 ** 3.675)  # axis frame, from the extraction (74.03..292.47 pt)
ax.set_ylim(1, 10 ** 4.768)  # frame top at 58.59 pt
ax.set_xlabel("Number of edits")
ax.set_ylabel("Number of cells")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(Path(__file__).with_name("edfig2a_replot.png"), dpi=150)
