"""Re-plot Fig. 14 from fig14.csv -> fig14_replot.png (each blob drawn as the box spanned by its outermost marker
centres, padded by half a marker, with its centroid)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
COL = {"ER3p_a": "#5b92be", "ER2_c": "#c2d2eb", "ER2_d": "#f39d52", "ExR7": "#f7ca9b", "EPG": "#6eaf5f",
       "ER3p_b": "#b9e2a8", "ER2_a": "#ce5b58", "ExR6": "#f2b1ad", "ER2_b": "#a288c5"}
with open(HERE / "fig14.csv", newline="") as f:
    rows = list(csv.DictReader(r for r in f if not r.startswith("#")))
half = 0.19                                   # half a marker width in AU
fig, ax = plt.subplots(figsize=(7, 6.5))
seen = set()
for r in rows:
    s = r["series"]
    x0, x1, y0, y1 = (float(r[k]) for k in ("x_min", "x_max", "y_min", "y_max"))
    ax.add_patch(Rectangle((x0 - half, y0 - half), x1 - x0 + 2 * half, y1 - y0 + 2 * half, color=COL[s], alpha=0.8,
                           label=None if s in seen else s))
    seen.add(s)
    ax.plot(float(r["x_centroid"]), float(r["y_centroid"]), "k+", ms=5)
ax.set_xlim(-14.2, 9.6)
ax.set_ylim(-13.8, 10.4)
ax.set_xticks([-10, -5, 0, 5])
ax.set_yticks([-10, -5, 0, 5, 10])
ax.grid(True, color="#e8e8e8")
ax.set_xlabel("dim1 (AU)")
ax.set_ylabel("dim2 (AU)")
h, l = ax.get_legend_handles_labels()
order = [l.index(s) for s in COL]
ax.legend([h[i] for i in order], [l[i] for i in order], loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig14_replot.png", dpi=100)
