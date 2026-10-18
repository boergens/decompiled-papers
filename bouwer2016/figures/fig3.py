"""Re-plot Fig. 3a and 3c of Bouwer et al. 2016 (depth envelopes of the trajectory clouds) from fig3a.csv,
fig3c.csv -> fig3_replot.png. Panels b and d are 3D meshes; only their peak height was measured (fig3bd_peak.csv),
which is printed in the panel titles here."""
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
                try:
                    cols.setdefault(k, []).append(float(v) if v else float("nan"))
                except ValueError:
                    cols.setdefault(k, []).append(v)
    return cols


pk = load("fig3bd_peak.csv")
peaks = dict(zip(pk["panel"], pk["peak_height"]))
fig, axes = plt.subplots(2, 1, figsize=(5.5, 6.5))
for ax, p, ymax, ticks in ((axes[0], "a", 50, [0, 25, 50]), (axes[1], "c", 150, [0, 50, 100, 150])):
    d = load(f"fig3{p}.csv")
    x = d["x_px"]
    ax.fill_between(x, 0, d["depth_all_pw_nm"], color="0.55", step="mid", label="all trajectories (grey)")
    ax.fill_between(x, 0, d["depth_bse_pw_nm"], color="k", step="mid", label="BSE (black)")
    ax.axhline(0, color="darkred")
    ax.set_ylim(ymax * 1.1, -ymax * 0.25)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{t} nm" for t in ticks])
    ax.yaxis.tick_right()
    ax.set_xlabel("source image column (px); no lateral scale in the figure")
    ax.text(0.01, 0.95, p, transform=ax.transAxes, fontweight="bold", fontsize=13, va="top")
axes[0].legend(loc="lower left", fontsize=7)
axes[0].set_title(f"peak heights read from the meshes: b {peaks['b']:.2f}, d {peaks['d']:.2f}", fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig3_replot.png", dpi=150)
