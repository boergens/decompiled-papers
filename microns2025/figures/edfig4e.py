#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 4e from edfig4e.csv -> edfig4e_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("edfig4e.csv"))
fig, ax = plt.subplots(figsize=(3.4, 3))
for name, col in [("control units", "#da8054"), ("matched units", "#4470ae")]:
    s = [a for a in r if a["series"] == name]
    ax.bar([float(a["bin_left"]) for a in s], [float(a["count"]) for a in s],
           width=[float(a["bin_right"]) - float(a["bin_left"]) for a in s], align="edge", color=col,
           edgecolor="white", lw=0.3, alpha=0.8, label=name)
ax.set_xlim((404.25 - 413.90) / 94.275, (484.84 - 413.90) / 94.275)
ax.set_ylim(0, (234.45 - 165.01) / 0.21825)
ax.set_xlabel("oracle score")
ax.set_ylabel("count")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(Path(__file__).with_name("edfig4e_replot.png"), dpi=150)
