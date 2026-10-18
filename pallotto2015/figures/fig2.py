"""Re-plot Figure 2B, 2C, 2D from fig2b/c/d.csv -> fig2b_replot.png, fig2c_replot.png, fig2d_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
for k, ylab, ylim, yt in (("b", "Classification Error", 0.12, [0, .02, .04, .06, .08, .10]),
                          ("c", "Resampled\nAdapted Rand Error", 0.225, [0, 0.1, 0.2]),
                          ("d", "(Splits + Mergers) / Object", 1.05, [0, .2, .4, .6, .8, 1.0])):
    rows = read_csv(os.path.join(HERE, f"fig2{k}.csv"))
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    f = [(float(r["x_axis"]), float(r["y"])) for r in rows if r["kind"] == "fold"]
    m = [(float(r["x_axis"]), float(r["y"])) for r in rows if r["kind"] == "median"]
    ax.plot(*zip(*f), "o", mfc="none", color="0.6", ms=6)
    ax.plot(*zip(*m), "+", color="r", ms=14, mew=3)
    ax.set_xlim(-2, 27); ax.set_ylim(0, ylim); ax.set_yticks(yt)
    ax.set_xticks([0.6, 6, 11, 24]); ax.set_xticklabels(["0.6", "6", "11", "24"])
    ax.set_xlabel("ECS fraction (%)"); ax.set_ylabel(ylab)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, f"fig2{k}_replot.png"), dpi=150)
