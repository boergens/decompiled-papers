"""Re-plot Fig. 9a and 9b of Bouwer et al. 2016 (fan envelopes) from fig9a.csv, fig9b.csv -> fig9_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def load(name):
    cols = {}
    with open(HERE / name) as f:
        for r in csv.DictReader(l for l in f if not l.startswith("#")):
            for k, v in r.items():
                cols.setdefault(k, []).append(float(v) if v else float("nan"))
    return cols


fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
for ax, p in zip(axes, "ab"):
    d = load(f"fig9{p}.csv")
    h = d["height_mm"]
    ax.fill_betweenx(h, d["bse_left_mm"], d["bse_right_mm"], color="#4040ff", alpha=0.6, lw=0, label="BSE (blue)")
    ax.fill_betweenx(h, d["se_left_mm"], d["se_right_mm"], color="#00e000", lw=0, label="SE (green)")
    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 6.6)
    ax.set_xticks(range(-10, 11, 2))
    ax.set_yticks(range(0, 7))
    ax.set_xlabel("Distance (mm)")
    ax.set_ylabel("Height (mm)")
    ax.text(-11.5, 6.4, p, fontweight="bold", fontsize=14)
axes[1].legend(loc="lower right", fontsize=8)
fig.suptitle("Electron Trajectories with Applied Deceleration (envelopes of the fans)")
fig.tight_layout()
fig.savefig(HERE / "fig9_replot.png", dpi=150)
