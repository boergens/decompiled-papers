"""Re-plot Figure 1e of Ströh et al. 2022 from fig1e.csv -> fig1e_replot.png"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replot_common import read, draw_lineband, plt, HERE

rows = read("fig1e.csv")
fig, ax = plt.subplots(figsize=(2.8, 3.2))
C = {"OsO4": "#006ebc", "Ferro-redOs": "#007d62", "5.56% CH3NO + Ferro-redOs": "#fa6400", "11.25% CH3NO + Ferro-redOs": "#fa0000"}
draw_lineband(ax, rows, "depth_um", "intensity_au", "sd_low", "sd_high", C)
ax.axhline(1, color="k", lw=0.8)
ax.set_xlim(-200, 1200); ax.set_ylim(0.4, 1.36)
ax.set_xticks([0, 500, 1000]); ax.set_yticks([0.4, 1])
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Depth (μm)"); ax.set_ylabel("Intensity (a.u.)")
ax.legend(fontsize=5, loc="lower right", markerscale=4)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1e_replot.png"), dpi=150)
