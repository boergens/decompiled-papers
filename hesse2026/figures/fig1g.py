"""Redraw Figure 1g (spike raster, 429 cells, ML above AM) from fig1g_spikes.csv.
Run from inside figures/:  python3 fig1g.py  ->  fig1g_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("fig1g_spikes.csv", comment="#")
lay = pd.read_csv("fig1g_layout.csv", comment="#").set_index("element")["value"].astype(float)
n_rows = int(lay["n_rows_between_y_ticks"]); sep = lay["ml_am_separator_row"]; extra = int(lay["rows_below_bottom_tick_in_axis_box"])

fig, ax = plt.subplots(figsize=(6.6, 3.3), dpi=200)
# each spike is a short vertical tick (in the PDF: 2 pt tall, hairline wide; the figure here is ~2x the original)
ax.plot(df["time_from_flash_s"], df["row_from_top"], linestyle="none", marker="|", color="k", ms=3.5, mew=0.22, zorder=3)
ax.axhline(sep, color="k", lw=0.5)                        # ML / AM separator
ax.axvline(0, color="k", lw=0.8, ls=(0, (5, 4)), zorder=2)  # flash onset
ax.set_xlim(-1, 1); ax.set_ylim(n_rows + extra, 1)          # row 1 at the top, as in the original
ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.set_yticks([1, n_rows]); ax.set_yticklabels([])
ax.set_xlabel("Time from flash (seconds)", fontsize=8); ax.set_ylabel("429 cells", fontsize=8)
ax.tick_params(labelsize=8)
ax.text(1.01, sep / 2, "ML", transform=ax.get_yaxis_transform(), fontsize=8, va="center")
ax.text(1.01, (sep + n_rows) / 2, "AM", transform=ax.get_yaxis_transform(), fontsize=8, va="center")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("fig1g_replot.png")
