#!/usr/bin/env python3
"""Redraw Figure 3h: single-trial decoding accuracy (%) vs time from flash for an example session (held-out half of
neurons), decoded from the average activity (grey, top left), state 1 (orange, bottom left) and state 2 (purple,
bottom right); solid = conscious face, dashed = suppressed face. Reads fig3h_average.csv, fig3h_state1.csv,
fig3h_state2.csv; writes fig3h_replot.png.
The suppressed series is stored only where the original's dashes cover a sample (empty in the gaps), so plotting it
as a solid line with NaN gaps reproduces the dashed look of the original exactly where its dashes are."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from fig3_common import GREY, ORANGE, PURPLE, read_csv, save

fig = plt.figure(figsize=(2.9, 3.0), dpi=200)
gs = fig.add_gridspec(2, 2, hspace=0.75, wspace=0.55, left=0.17, right=0.97, top=0.9, bottom=0.14)
cells = [("average", GREY, "Average", gs[0, 0]), ("state1", ORANGE, "State 1", gs[1, 0]), ("state2", PURPLE, "State 2", gs[1, 1])]
for name, col, title, cell in cells:
    ax = fig.add_subplot(cell)
    d = read_csv(f"fig3h_{name}.csv")
    ax.plot(d["time_from_flash_s"], d["conscious_pct"], color=col, lw=1)
    ax.plot(d["time_from_flash_s"], d["suppressed_pct"], color=col, lw=1)   # NaN gaps = gaps between the original dashes
    ax.set_xlim(-0.1, 2)
    ax.set_ylim(0, 100)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 50, 100])
    ax.set_title(title, fontsize=7, pad=3)

handles = [Line2D([], [], color="k", lw=1), Line2D([], [], color="k", lw=1, ls=(0, (4, 3)))]
fig.legend(handles, ["Conscious", "Suppressed"], loc="center", bbox_to_anchor=(0.77, 0.78), frameon=False,
           handlelength=2.5, fontsize=7)
fig.supylabel("Decoding accuracy (%)", x=0.03, fontsize=7)
# the original axis label reads "(ms)"; the plotted range 0-2 is seconds (see README)
fig.supxlabel("Time from flash (ms)", y=0.02, fontsize=7)
save(fig, "fig3h")
