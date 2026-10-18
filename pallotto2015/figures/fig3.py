"""Re-plot Figure 3C, 3D, 3E from fig3c/d/e.csv -> fig3c_replot.png, fig3d_replot.png, fig3e_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import numpy as np
COL = {"LowECS": "#0072bd", "HighECS": "#d95319"}
LBL = ["0.3", "", "0.5", "", "0.7", "", "0.9", "0.95", "0.975", "0.99", "", "0.999", "", "0.9999", "", "0.99999", "", "0.999999"]
for k, ylab, ylim in (("c", "Adapted Rand Error", (0.6, 1.0)), ("e", "Total Error Free\nPath Length (%)", (-2, 50))):
    rows = read_csv(os.path.join(HERE, f"fig3{k}.csv"))
    fig, ax = plt.subplots(figsize=(3.4, 3.2))
    ths = list(dict.fromkeys(r["threshold"] for r in rows))
    for s, c in COL.items():
        rr = [(ths.index(r["threshold"]), r) for r in rows if r["series"] == s and r["y"]]
        x = [i for i, r in rr]
        ax.plot(x, [float(r["y"]) for i, r in rr], color=c, lw=2, label=s)
        bb = [(i, float(r["band_low"]), float(r["band_high"])) for i, r in rr if r["band_low"]]
        ax.fill_between([b[0] for b in bb], [b[1] for b in bb], [b[2] for b in bb], color=c, alpha=0.3, lw=0)
    ax.set_xticks(range(len(ths))); ax.set_xticklabels(LBL, rotation=-60, fontsize=7)
    ax.set_ylim(*ylim); ax.set_xlim(-0.5, len(ths) - 0.5); ax.set_xlabel("Threshold"); ax.set_ylabel(ylab)
    if k == "c":
        ax.legend(loc="lower left", frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, f"fig3{k}_replot.png"), dpi=150)
rows = read_csv(os.path.join(HERE, "fig3d.csv"))
fig, ax = plt.subplots(figsize=(3.4, 3.2))
for s, c in COL.items():
    rr = [r for r in rows if r["series"] == s and r["kind"] == "curve"]
    x = np.array([float(r["split_edges_pct"]) for r in rr])
    ax.fill_between(x, [float(r["band_low"]) for r in rr], [float(r["band_high"]) for r in rr], color=c, alpha=0.3, lw=0)
    ax.plot(x, [float(r["merged_nodes_pct"]) for r in rr], color=c, lw=2)
    p = [r for r in rows if r["series"] == s and r["kind"] != "curve"][0]
    ax.plot(float(p["split_edges_pct"]), float(p["merged_nodes_pct"]), "o", color=c, ms=6)
ax.set_xlim(-5, 102); ax.set_ylim(-5, 102); ax.set_xticks(range(0, 101, 20)); ax.set_yticks(range(0, 101, 20))
ax.set_xlabel("Split Edges (%)"); ax.set_ylabel("Merged Nodes (%)")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig3d_replot.png"), dpi=150)
