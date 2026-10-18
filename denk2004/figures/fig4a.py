"""Re-plot Figure 4A of Denk & Horstmann 2004 from fig4a.csv -> fig4a_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig4a.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4.2, 4.3))
env = [r for r in rows if r["series"] == "all_traces"]
x = np.array([float(r["slice"]) for r in env])
ax.fill_between(x, [float(r["shift_lower_nm"]) for r in env], [float(r["shift_upper_nm"]) for r in env],
                color="0.85", lw=0, label="all traces (envelope)")
cols = {"pink": "#e0709a", "orange": "#f0a030", "teal": "#30b0a0", "lavender": "#7070c0", "black": "k"}
for name, c in cols.items():
    s = [r for r in rows if r["series"] == name]
    xs = np.array([float(r["slice"]) for r in s])
    ys = np.array([float(r["shift_nm"]) for r in s])
    gap = np.where(np.diff(xs) > 2)[0] + 1          # break the line where the colour is not found
    xs, ys = np.insert(xs, gap, np.nan), np.insert(ys, gap, np.nan)
    ax.plot(xs, ys, color=c, lw=0.6, label=name)
ax.set_xlim(0, 343)
ax.set_ylim(-200, 200)
ax.set_xticks([50, 100, 150, 200, 250, 300])
ax.set_yticks([-200, -100, 0, 100, 200])
ax.set_xlabel("slice (#)")
ax.set_ylabel("shift (nm)")
ax.legend(fontsize=6, loc="lower right")
fig.tight_layout()
fig.savefig(HERE / "fig4a_replot.png", dpi=150)
