"""Re-plot Figure 1f of Ströh et al. 2022 from fig1f.csv -> fig1f_replot.png"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replot_common import read, draw_lineband, plt, HERE

rows = read("fig1f.csv")
fig, ax = plt.subplots(figsize=(2.8, 3.2))
C = {"OsO4": "#006ebc", "Ferro-redOs": "#007d62", "Ferro-redOs + 5.56% formamide": "#fa6400",
     "Ferro-redOs + 11.25% formamide": "#fa0000", "Model": "k"}
draw_lineband(ax, rows, "time_min", "height_change_percent", "sd_low", "sd_high", C)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlim(0, 1210); ax.set_ylim(-10, 21)
ax.set_xticks([0, 500, 1000]); ax.set_yticks([-10, 0, 10, 20])
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Time (min)"); ax.set_ylabel("Change in sample height (%)")
ax.legend(fontsize=5, loc="lower left", markerscale=4)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1f_replot.png"), dpi=150)
