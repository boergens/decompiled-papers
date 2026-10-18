#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 5a from edfig5a.csv -> edfig5a_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("edfig5a.csv"))
COL = {"fiducial-based automatch": "#f0af99", "vessel-based automatch": "#e96852", "fiducial-vessel agreements": "#cd1d30"}
fig, axs = plt.subplots(1, 2, figsize=(8, 3.4), sharey=True)
for ax, panel, title in [(axs[0], "residual percentile", "residual percentile"), (axs[1], "separation percentile", "seperation percentile")]:
    for s, c in COL.items():
        pts = sorted(((int(a["vertex"]), float(a["recall"]), float(a["precision"])) for a in r if a["panel"] == panel and a["series"] == s))
        ax.plot([p[1] for p in pts], [p[2] for p in pts], color=c, label=s)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.8, 1.0)
    ax.grid(True, color="k", lw=0.3)
    ax.set_title(title, fontsize=8)
    ax.set_xlabel("recall")
axs[0].set_ylabel("precision")
axs[0].legend(fontsize=6, loc="center right")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("edfig5a_replot.png"), dpi=150)
