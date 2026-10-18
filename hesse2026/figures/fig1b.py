"""Redraw Figure 1b (human psychophysics, binocular flash suppression) from the two CSVs.
Run from inside figures/:  python3 fig1b.py  ->  fig1b_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SERIES = [("left_eye", "Left eye", "#d95319"), ("right_eye", "Right eye", "#0072bd"), ("mixed", "Mixed", "#edb120")]
SUBPLOTS = [("fig1b_left_eye_suppressed.csv", "Left eye suppressed"), ("fig1b_right_eye_suppressed.csv", "Right eye suppressed")]

fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.6), dpi=200, sharey=True)
for ax, (csv, title) in zip(axes, SUBPLOTS):
    df = pd.read_csv(csv, comment="#")
    t = df["time_from_flash_s"]
    for key, label, col in SERIES:
        ax.fill_between(t, df[f"{key}_band_lo_pct"], df[f"{key}_band_hi_pct"], color=col, alpha=0.3, lw=0)
        ax.plot(t, df[f"{key}_pct"], color=col, lw=1.5, label=label)
    ax.axvline(0, color="k", lw=0.8, ls=(0, (5, 4)))           # flash onset
    ax.set_title(title, fontsize=9)
    ax.set_xlim(-2, 6); ax.set_ylim(0, 100)
    ax.set_xticks([-2, 0, 2, 4, 6]); ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.tick_params(labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("Proportion percept", fontsize=8)
axes[1].tick_params(labelleft=True)
axes[1].legend(frameon=False, fontsize=8, loc="upper right")
fig.supxlabel("Time from flash (seconds)", fontsize=8, y=0.02)
fig.tight_layout(w_pad=1.5)
fig.savefig("fig1b_replot.png")
