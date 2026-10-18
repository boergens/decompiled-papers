"""Re-plot Figure 1—figure supplement 3a-f of Ströh et al. 2022 from sfig1s3a.csv ... sfig1s3f.csv
-> sfig1s3a_replot.png ... sfig1s3f_replot.png"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replot_common import read, draw_lineband, plt, HERE  # noqa: E402

C = {"OsO4": "#006ebc", "2.5% (Ferro) K4[Fe(CN)6] + 2% OsO4": "#007d62", "2.5% (Ferri) K3[Fe(CN)6] + 2% OsO4": "#fa0000",
     "2.5% (Ferro) K4[Fe(CN)6] (after 2% OsO4)": "#00dc4c", "2.5% (Ferri) K3[Fe(CN)6] (after 2% OsO4)": "#fa6400"}
for p in "abcdef":
    rows = read(f"sfig1s3{p}.csv")
    fig, ax = plt.subplots(figsize=(2.8, 3.0))
    if p in "ace":
        draw_lineband(ax, rows, "depth_um", "intensity_au", "sd_low", "sd_high", C)
        ax.axhline(1, color="k", lw=0.8)
        ax.set_xlim(-200, 1200); ax.set_ylim(0.4, 1.36); ax.set_yticks([0.4, 1]); ax.set_xticks([0, 500, 1000])
        ax.set_xlabel("Depth (μm)"); ax.set_ylabel("Intensity (a.u.)")
    else:
        draw_lineband(ax, rows, "time_min", "height_change_percent", "sd_low", "sd_high", C)
        ax.axhline(0, color="k", lw=0.8)
        ax.set_xlim(0, 1210); ax.set_ylim(-10, 21); ax.set_yticks([-10, 0, 10, 20]); ax.set_xticks([0, 500, 1000])
        ax.set_xlabel("Time (min)"); ax.set_ylabel("Change in sample height (%)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=4, loc="lower right", markerscale=4)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"sfig1s3{p}_replot.png"), dpi=150)
    plt.close(fig)
