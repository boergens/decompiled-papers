"""Re-plot Fig 5(f) of Lee et al. 2018 from fig5f.csv -> fig5f_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig5f.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
S = lambda k: [r for r in rows if r["series"] == k]
fig = plt.figure(figsize=(5.5, 5.5))
ax = fig.add_axes([0.15, 0.12, 0.5, 0.5])
axt = fig.add_axes([0.15, 0.68, 0.5, 0.25], sharex=ax)
axr = fig.add_axes([0.71, 0.12, 0.25, 0.5], sharey=ax)
for r in S("scatter"):
    ax.plot(float(r["x_mm"]), float(r["y_mm"]), "x", color="0.3" if not r["flag"] else "0.6", ms=3, mew=0.6)
for r in S("x_histogram"):
    lo, hi = float(r["bin_low_mm"]), float(r["bin_high_mm"])
    axt.bar(lo, float(r["count"]), width=hi - lo, align="edge", color="k", edgecolor="w", linewidth=0.3)
for r in S("y_histogram"):
    lo, hi = float(r["bin_low_mm"]), float(r["bin_high_mm"])
    axr.barh(lo, float(r["count"]), height=hi - lo, align="edge", color="k", edgecolor="w", linewidth=0.3)
xs = [float(r["x_mm"]) for r in S("dashed_line_x")]
ys = [float(r["y_mm"]) for r in S("dashed_line_y")]
ax.plot([xs[0], xs[1], xs[1], xs[0], xs[0]], [ys[0], ys[0], ys[1], ys[1], ys[0]], "k--", lw=1)
for x in xs:
    axt.axvline(x, color="k", ls="--", lw=1)
for y in ys:
    axr.axhline(y, color="k", ls="--", lw=1)
ax.set_xlim(-0.7, 0.7); ax.set_ylim(-0.7, 0.7)
ax.set_xticks([-0.7, 0, 0.7]); ax.set_yticks([-0.7, 0, 0.7])
axt.set_ylim(0, 100); axt.set_yticks([0, 100]); axt.tick_params(labelbottom=False)
axr.set_xlim(0, 100); axr.set_xticks([0, 100]); axr.tick_params(labelleft=False)
axr.xaxis.set_ticks_position("top")
ax.set_xlabel("Section centroid\nx-position [mm]")
ax.set_ylabel("Section centroid\ny-position [mm]")
fig.savefig(HERE / "fig5f_replot.png", dpi=150)
