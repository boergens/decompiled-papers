"""Redraw Extended Data Fig. 9a (spike raster with four-state shading) from edfig9a_spikes.csv and
edfig9a_state_epochs.csv. Run from this folder: python3 edfig9a.py -> edfig9a_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
from _style import plt, save, ORANGE, PURPLE

spikes = pd.read_csv("edfig9a_spikes.csv", comment="#")
epochs = pd.read_csv("edfig9a_state_epochs.csv", comment="#")

fig, ax = plt.subplots(figsize=(3.6, 1.85))
# state shading: two 20 %-opacity layers, exactly as in the original (orange/purple = conscious/suppressed; white/black = On/Off)
for _, e in epochs.iterrows():
    ax.axvspan(e.t_start_s, e.t_end_s, color=ORANGE if e.percept == "conscious" else PURPLE, alpha=0.2, lw=0)
    ax.axvspan(e.t_start_s, e.t_end_s, color="white" if e.on_off == "On" else "black", alpha=0.2, lw=0)
# spikes: 1-pt-tall ticks (about 4 rows tall at the original row pitch of 0.232 pt)
ax.vlines(spikes.time_s, spikes.row_index - 2.15, spikes.row_index + 2.15, color="black", lw=0.2)
ax.axhline(158.5, color="black", lw=0.25)   # ML (above) / AM (below) separator
ax.axvline(0, color="black", lw=0.5)        # flash onset
ax.set_xlim(-1.015, 1.004)
ax.set_ylim(417, 1)                         # row 1 at the upper tick, rows increase downwards
ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.set_xticklabels(["-1", "-0.5", "0", "0.5", "1"])
ax.set_yticks([1, 412]); ax.set_yticklabels([])
ax.set_xlabel("Time from flash (seconds)")
ax.set_ylabel("429 cells")
ax.text(1.03, 80, "ML", transform=ax.transData, va="center", ha="left", fontsize=6, clip_on=False)
ax.text(1.03, 290, "AM", transform=ax.transData, va="center", ha="left", fontsize=6, clip_on=False)
fig.subplots_adjust(left=0.07, right=0.92, top=0.97, bottom=0.2)
save(fig, "edfig9a")
