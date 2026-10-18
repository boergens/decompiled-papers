"""Re-plot Figure 2e of Ströh et al. 2022 from fig2e.csv -> fig2e_replot.png"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replot_common import read, draw_lineband, plt, HERE  # noqa: E402

rows = read("fig2e.csv")
fig, ax = plt.subplots(figsize=(2.6, 3.2))
C = {"200μm": "#7cb4dc", "600μm": "#fa7c7c", "1000μm": "#fab47c", "model 200μm": "0.3", "model 600μm": "0.45", "model 1000μm": "0.6"}
draw_lineband(ax, rows, "time_min", "density", "sd_low", "sd_high", C)
ax.set_xlim(0, 1210); ax.set_ylim(93 - 93 * (1081 - 1038.5) / 357.5, 186)
ax.set_xticks([0, 500, 1000]); ax.set_yticks([93, 186])
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Time (min)"); ax.set_ylabel("Density (nmol/mm$^3$)")
ax.legend(fontsize=5, loc="lower right", markerscale=4)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2e_replot.png"), dpi=150)
