"""Re-plot zhangk2020 Fig. 10 from fig10.csv -> fig10_replot.png."""
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


r = read("fig10.csv")
fig, ax = plt.subplots(figsize=(4.2, 3.2))
ax.plot([float(q["x_indentation_depth_nm"]) for q in r], [float(q["y_elastic_recovery_nm"]) for q in r], "s-", color="red", mfc="none")
ax.set(xlim=(20, 180), ylim=(0, 0.006), xticks=[20, 60, 100, 140, 180], yticks=[0, 0.002, 0.004, 0.006],
       xlabel="Indentation depth  nm", ylabel="Theoretical elastic recovery  nm")
fig.tight_layout()
fig.savefig(HERE / "fig10_replot.png", dpi=200)
