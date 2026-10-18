"""Re-plot Figure 7 (a, b) of Fu et al. 2025 from fig7a.csv and fig7b.csv -> fig7a_replot.png, fig7b_replot.png.
Also used for Figure 8: python3 -I fig7.py fig8a fig8b fig8c fig8d (default: fig7a fig7b)."""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
COLOURS = {"60nm": "black", "80nm": "red", "100nm": "blue", "120nm": "magenta", "150nm": "green", "200nm": "navy"}
LIMITS = {"fig7a": (0, 810, 0, 60), "fig7b": (0, 820, 0, 80)}

for panel in (sys.argv[1:] or ["fig7a", "fig7b"]):
    data = {}
    with open(HERE / f"{panel}.csv") as f:
        for r in csv.DictReader(line for line in f if not line.startswith("#")):
            data.setdefault(r["series"], []).append(
                (float(r["time_us"]), float(r["force_N_per_m"]), float(r["force_upper"]), float(r["force_lower"])))
    fig, ax = plt.subplots(figsize=(5, 3.8))
    for name, pts in data.items():
        t, y, yu, yl = map(np.array, zip(*pts))
        col = COLOURS[name.split()[-1]]
        # one or more runs per pixel column: draw each run as a vertical stroke from its top to its bottom,
        # plus its centre point (no connecting lines, since a column can hold several runs)
        ax.vlines(t, yl, yu, color=col, lw=0.8)
        ax.plot(t, y, ".", color=col, ms=1.2, label=name)
    x0, x1, y0, y1 = LIMITS.get(panel, (0, 820, 0, 80))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_xlabel("Time (µs)")
    ax.set_ylabel("Resultant cutting force (N/m)")
    ax.legend(fontsize=6, frameon=False, ncol=2 if panel != "fig7a" else 1, loc="upper right")
    fig.tight_layout()
    fig.savefig(HERE / f"{panel}_replot.png", dpi=150)
    plt.close(fig)
    print(panel)
