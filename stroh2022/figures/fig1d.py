"""Re-plot Figure 1d of Ströh et al. 2022 from fig1d.csv -> fig1d_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig1d.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(2.6, 3.0))
m = [r for r in rows if r["series"] == "OsO4 mean"]
mb = [r for r in m if r["sd_low_um"] and r["sd_high_um"]]
ax.fill_between([float(r["time_min"]) for r in mb], [float(r["sd_low_um"]) for r in mb],
                [float(r["sd_high_um"]) for r in mb], color="#98aacc", lw=0)
mm = [r for r in m if r["depth_um"]]
ax.plot([float(r["time_min"]) for r in mm], [float(r["depth_um"]) for r in mm], ".", ms=2, color="#006ebc", label="OsO$_4$")
k = [r for r in rows if r["series"] == "model sqrt(t)"]
ax.plot([float(r["time_min"]) for r in k], [float(r["depth_um"]) for r in k], ".", ms=2, color="k", label="√t ∝ x")
ax.set_xlim(0, 420); ax.set_ylim(0, 1000)
ax.set_xticks([0, 200, 400]); ax.set_yticks([0, 500, 1000])
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Time t (min)"); ax.set_ylabel("Depth x (μm)")
ax.legend(loc="lower right", fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1d_replot.png"), dpi=150)
