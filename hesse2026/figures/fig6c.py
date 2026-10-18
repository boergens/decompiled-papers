"""Redraw Figure 6c (decoding accuracy vs number of faces, PFC) from fig6c.csv.
Run from inside figures/:  python3 fig6c.py  ->  fig6c_replot.png
Also used by fig6e.py (same panel type) via PANEL = 'e'."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PANEL = sys.argv[1] if len(sys.argv) > 1 else "c"

SERIES = [  # column prefix, legend label, colour, linestyle
    ("priming_average", "Priming, average", "#1c0f29", "-"),
    ("binocular_conscious_state1", "Binocular conscious, state 1", "#fcae34", "-"),
    ("binocular_conscious_state2", "Binocular conscious, state 2", "#543379", "-"),
    ("binocular_suppressed_state1", "Binocular suppressed, state 1", "#fcae34", "--"),
    ("binocular_suppressed_state2", "Binocular suppressed, state 2", "#543379", "--"),
]


def interp_nan(x, y):
    """Linear interpolation across empty cells (dash-gap vertices that could not be recovered; see CSV
    comments). Drawing only: the CSV keeps them empty."""
    y = y.copy()
    m = np.isnan(y)
    if m.any() and (~m).sum() >= 2:
        y[m] = np.interp(x[m], x[~m], y[~m])
    return y


def main():
    df = pd.read_csv(f"fig6{PANEL}.csv", comment="#")
    x = df["number_of_faces"].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(2.3, 2.45), dpi=200)
    for pre, label, color, ls in SERIES:
        y = interp_nan(x, df[pre + "_pct"].to_numpy(dtype=float))
        lo = df[pre + "_band_lo_pct"].to_numpy(dtype=float)
        hi = df[pre + "_band_hi_pct"].to_numpy(dtype=float)
        ok = ~np.isnan(lo) & ~np.isnan(hi)
        ax.fill_between(x[ok], lo[ok], hi[ok], color=color, alpha=0.25, lw=0)
    for pre, label, color, ls in SERIES:
        y = interp_nan(x, df[pre + "_pct"].to_numpy(dtype=float))
        ax.plot(x, y, color=color, ls=ls, lw=1.0, label=label, dashes=(3, 2) if ls == "--" else (None, None))

    ax.set_xlim(0, 60)
    ax.set_ylim(0, 100)
    ax.set_xticks([0, 20, 40, 60])
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("Number of faces", fontsize=6)
    ax.set_ylabel("Decoding accuracy (%)", fontsize=6)
    ax.tick_params(labelsize=6, length=2, width=0.5, direction="out")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(0.5)
    ax.legend(loc="upper right", fontsize=4.2, frameon=False, handlelength=2.2, borderaxespad=0.2, labelspacing=0.3)
    fig.tight_layout(pad=0.3)
    fig.savefig(f"fig6{PANEL}_replot.png", dpi=200)


if __name__ == "__main__":
    main()
