"""Re-plot zhangk2020 Fig. 13 from fig13.csv -> fig13_replot.png (two y axes)."""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def read(name):
    with open(HERE / name) as f:
        rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
    return rows


def series(rows, key="series"):
    d = defaultdict(list)
    for r in rows:
        d[r[key]].append(r)
    return d


s = series(read("fig13.csv"))
fig, ax = plt.subplots(figsize=(4.4, 3.0))
ax2 = ax.twinx()
a = s["Cutting edge radius"]
u = s["Uncertainty"]
ax.plot([float(q["x_indentation_depth_nm"]) for q in a], [float(q["y_nm"]) for q in a], "s", color="blue", mfc="none", label="Cutting edge radius")
ax2.plot([float(q["x_indentation_depth_nm"]) for q in u], [float(q["y_nm"]) for q in u], "x", color="red", label="Uncertainty")
ax.set(xlim=(20, 180), ylim=(38, 44), xticks=[20, 60, 100, 140, 180], yticks=[38, 40, 42, 44],
       xlabel="Indentation depth  nm", ylabel="The actual cutting edge radius  nm")
ax2.set(ylim=(1.85, 2.15), yticks=[1.85, 1.95, 2.05, 2.15], ylabel="Uncertainty  nm")
fig.legend(loc="upper left", bbox_to_anchor=(0.18, 0.95), fontsize=7)
fig.tight_layout()
fig.savefig(HERE / "fig13_replot.png", dpi=200)
