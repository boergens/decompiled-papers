"""Re-plot Figure 3-figure supplement 1A-C from sfig3-1a.csv (tier 1), sfig3-1b.csv, sfig3-1c.csv (tier 3; the NML-derived
sfig3-1b/c_sourcedata.csv as thin dotted lines) -> sfig3-1a_replot.png, sfig3-1b_replot.png, sfig3-1c_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import numpy as np
COL = {"LowECS": "#0072bd", "HighECS": "#d95319"}
rows = read_csv(os.path.join(HERE, "sfig3-1a.csv"))
fig, ax = plt.subplots(figsize=(3.4, 3.4))
for s, c in COL.items():
    v = [float(r["voxels"]) for r in rows if r["series"] == s]
    y = [float(r["cdf_pct"]) for r in rows if r["series"] == s]
    ax.step([10] + v + [2e6], [0] + y + [100], color=c, lw=2, where="post", label=s)
    ax.plot(np.median(v), 50, "x", color=c, ms=10, mew=2)
ax.set_xscale("log"); ax.set_xlim(10, 3e6); ax.set_ylim(-5, 105); ax.set_yticks([0, 25, 50, 75, 100])
ax.set_xlabel("3D GT Voxels / Object"); ax.set_ylabel("Cumulative Distribution\nFunction (%)"); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "sfig3-1a_replot.png"), dpi=150)
for k, xlab, log, xlim, col in (("b", "Path Length / Skeleton (um)", True, (0.1, 160), "path_length_um"),
                                ("c", "Nodes / Skeleton", False, (0, 150), "n_nodes")):
    rows = read_csv(os.path.join(HERE, f"sfig3-1{k}.csv"))
    src = read_csv(os.path.join(HERE, f"sfig3-1{k}_sourcedata.csv"))
    fig, ax = plt.subplots(figsize=(3.4, 3.4))
    for s, c in COL.items():
        rr = [r for r in rows if r["series"] == s and r["kind"] == "curve"]
        ax.plot([float(r["x"]) for r in rr], [float(r["cdf_pct"]) for r in rr], ".", color=c, ms=2)
        p = [r for r in rows if r["series"] == s and r["kind"] != "curve"][0]
        ax.plot(float(p["x"]), float(p["cdf_pct"]), "x", color=c, ms=10, mew=2)
        ss = [r for r in src if r["series"] == s]
        ax.step([float(r[col]) for r in ss], [float(r["cdf_pct"]) for r in ss], ":", color=c, lw=0.8, where="post")
    if log:
        ax.set_xscale("log")
    ax.set_xlim(*xlim); ax.set_ylim(-5, 105); ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel(xlab); ax.set_ylabel("Cumulative Distribution\nFunction (%)")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, f"sfig3-1{k}_replot.png"), dpi=150)
