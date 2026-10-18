"""Re-plot zhangk2020 Fig. 8 from fig8.csv -> fig8_replot.png."""
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


s = series(read("fig8.csv"))
fig, ax = plt.subplots(figsize=(4.2, 3.2))
for name, m, c in (("R_tool_m", "D", "green"), ("R_tool", "s", "blue"), ("R_mark_m", "o", "red")):
    ax.plot([float(r["x_indentation_depth_nm"]) for r in s[name]], [float(r["y_radius_nm"]) for r in s[name]],
            m, mfc="none", color=c, label=name)
ax.set(xlim=(20, 180), ylim=(0, 60), xticks=[20, 60, 100, 140, 180], yticks=[0, 20, 40, 60],
       xlabel="Indentation depth  nm", ylabel="Evaluated Radius  nm")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(HERE / "fig8_replot.png", dpi=200)
