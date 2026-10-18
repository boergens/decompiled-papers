"""Redraw Figure 6b (explained variance of face features vs feature index, PFC) from fig6b.csv.
Run from inside figures/:  python3 fig6b.py  ->  fig6b_replot.png
Also used by fig6d.py (same panel type) via PANEL = 'd'."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PANEL = sys.argv[1] if len(sys.argv) > 1 else "b"

SERIES = [  # column, legend label, colour, linestyle
    ("priming_average_pct", "Priming, average", "#1c0f29", "-"),
    ("binocular_conscious_state1_pct", "Binocular conscious, state 1", "#fcae34", "-"),
    ("binocular_conscious_state2_pct", "Binocular conscious, state 2", "#543379", "-"),
    ("binocular_suppressed_state1_pct", "Binocular suppressed, state 1", "#fcae34", "--"),
    ("binocular_suppressed_state2_pct", "Binocular suppressed, state 2", "#543379", "--"),
]


def main():
    df = pd.read_csv(f"fig6{PANEL}.csv", comment="#")
    # fig6b_offaxis.csv (and fig6d_offaxis.csv when run as fig6d.py): values outside the axes, not drawn
    off = pd.read_csv(f"fig6{PANEL}_offaxis.csv", comment="#")
    x = df["feature_index"].to_numpy()

    fig, ax = plt.subplots(figsize=(2.3, 2.45), dpi=200)
    for col, label, color, ls in SERIES:
        y = df[col].to_numpy(dtype=float)
        # points below -100 % were clipped by the axes in the original; fig6X_offaxis.csv holds the
        # values extrapolated from the straight segments so that the line leaves the axes at the right slope
        o = off[(off["series"] == col) & off["extrapolated_value_pct"].notna()]
        for k, v in zip(o["feature_index"], o["extrapolated_value_pct"]):
            y[int(k) - 1] = v
        ax.plot(x, y, color=color, ls=ls, lw=1.0, label=label, dashes=(3, 2) if ls == "--" else (None, None),
                solid_joinstyle="miter", solid_capstyle="butt")

    ax.set_xlim(1, 50)
    ax.set_ylim(-100, 100)
    ax.set_xticks([10, 20, 30, 40, 50])
    ax.set_yticks([-100, -50, 0, 50, 100])
    ax.set_xlabel("Feature #", fontsize=6)
    ax.set_ylabel("Explained variance of features (%)", fontsize=6)
    ax.tick_params(labelsize=6, length=2, width=0.5, direction="out")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(0.5)
    # brackets above the axes: shape features 1-20, appearance features 21-50
    for (x0, x1, txt) in ((1, 20, "Shape"), (21, 50, "Appearance")):
        yb = 106
        ax.plot([x0, x0, x1, x1], [yb - 4, yb, yb, yb - 4], color="k", lw=0.5, clip_on=False)
        ax.text((x0 + x1) / 2, yb + 3, txt, ha="center", va="bottom", fontsize=6, clip_on=False)
    # legend in the empty lower-left corner (shape features never go below -50 %)
    ax.legend(loc="lower left", fontsize=4.0, frameon=False, handlelength=2.0, borderaxespad=0.3, labelspacing=0.25,
              handletextpad=0.5)
    fig.tight_layout(pad=0.3)
    fig.savefig(f"fig6{PANEL}_replot.png", dpi=200)


if __name__ == "__main__":
    main()
