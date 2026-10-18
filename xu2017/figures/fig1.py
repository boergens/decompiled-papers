"""Re-plot Figure 1 of Xu et al. 2017 from fig1.csv -> fig1_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig1.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
els = {}
for r in rows:
    els.setdefault(r["element"], []).append((float(r["size_um"]), float(r["resolution_nm"])))
colours = {"orange": "#f08030", "yellow": "#ffe600", "purple": "#8a85c0", "light blue": "#a8cdfa",
           "blue band": "#1060f0", "teal": "#00a890", "green": "#9ccc70"}
fig, ax = plt.subplots(figsize=(7, 5.8))
for name, pts in els.items():
    if name.startswith("red"):
        ax.plot(*zip(*pts), color="red", lw=2)
        ax.text(*pts[1], name.split("'")[1], fontsize=7)
    elif name == "yellow star":
        ax.plot(*pts[0], "*", color="gold", ms=14, mec="k", mew=0.3)
    else:
        col = next(c for k, c in colours.items() if k in name)
        ax.add_patch(Polygon(pts, closed=True, fc=col, ec="k", lw=0.5, alpha=0.8,
                             zorder=1 if "green" in name else 2))
        xs, ys = zip(*pts)
        ax.text(sum(xs) / len(xs) if "band" not in name else 30, (min(ys) * max(ys)) ** 0.5,
                name.split(" (")[0], fontsize=6, ha="center", zorder=3)
ax.set_xscale("log")
ax.set_yscale("log", base=2)
ax.set_xlim(0.1, 1500)
ax.set_ylim(1, 80)
ax.set_xticks([0.1, 1, 10, 100, 1000])
ax.set_xticklabels(["0.1 [1e-3]", "1 [1e0]", "10 [1e3]", "100 [1e6]", "1000 [1e9]"])
ax.set_yticks([1, 2, 4, 8, 16, 32, 64])
ax.set_yticklabels(["1", "2", "4", "8", "16", "32", "64"])
ax.set_xlabel("Size (μm) [ Volume (μm³) ]")
ax.set_ylabel("Resolution (nm)")
fig.tight_layout()
fig.savefig(HERE / "fig1_replot.png", dpi=150)
