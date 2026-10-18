#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 4f, g, h from edfig4f/g/h.csv (pixel tables) -> edfig4{f,g,h}_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

for p, title in [("f", "all matched"), ("g", "matched oracle > 0.2"), ("h", "matched and nearest oracle > 0.2")]:
    r = [a for a in mc.read_csv(Path(__file__).with_name(f"edfig4{p}.csv")) if a["near_diagonal"] == "0"]
    fig, ax = plt.subplots(figsize=(3.4, 2.9))
    sc = ax.scatter([float(a["x"]) for a in r], [float(a["y"]) for a in r], c=[float(a["oracle_score"]) for a in r],
                    s=0.3, marker="s", lw=0, cmap="icefire" if "icefire" in plt.colormaps() else "coolwarm", vmin=0, vmax=0.45)
    ax.plot([-0.3, 1.0], [-0.3, 1.0], color="k", lw=1)
    ax.set_xlim(-0.37, 1.07)
    ax.set_ylim(-0.37, 1.07)
    ax.set_title(title, fontsize=8)
    ax.set_xlabel("signal corr matched vs\nnearest non-matched", fontsize=7)
    ax.set_ylabel("signal corr matched vs matched", fontsize=7)
    fig.colorbar(sc, ax=ax, label="oracle score")
    fig.tight_layout()
    fig.savefig(Path(__file__).with_name(f"edfig4{p}_replot.png"), dpi=150)
