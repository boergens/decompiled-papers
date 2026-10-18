#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 5b and 5c from edfig5b.csv / edfig5c.csv -> edfig5b_replot.png, edfig5c_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PatchCollection  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

for panel, lim, lab in [("b", (0.8, 1.0), "precision"), ("c", (0, 40000), "# neurons")]:
    r = mc.read_csv(Path(__file__).with_name(f"edfig5{panel}.csv"))
    fig, axs = plt.subplots(1, 3, figsize=(10, 3))
    for ax, name in zip(axs, ["fiducial-based automatch", "vessel-based automatch", "fiducial-vessel agreements"]):
        s = [a for a in r if a["automatch"] == name]
        pc = PatchCollection([Rectangle((float(a["sep_lo"]), float(a["res_lo"])), float(a["sep_hi"]) - float(a["sep_lo"]),
                                        float(a["res_hi"]) - float(a["res_lo"])) for a in s],
                             cmap="inferno", array=[float(a["value"]) for a in s])
        pc.set_clim(*lim)
        ax.add_collection(pc)
        ax.set_xlim(0, 1)
        ax.set_ylim(1.0, 0.0)
        ax.set_title(name, fontsize=8, fontweight="bold")
        ax.set_xlabel("min separation percentile")
        ax.set_ylabel("max residual percentile")
        fig.colorbar(pc, ax=ax, label=lab)
    fig.tight_layout()
    fig.savefig(Path(__file__).with_name(f"edfig5{panel}_replot.png"), dpi=150)
