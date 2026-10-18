"""Re-plot Figure 2-figure supplement 1A and 1C from sfig2-1a.csv, sfig2-1c.csv (+ sfig2-1c_sourcedata.csv as thin
dotted lines) -> sfig2-1a_replot.png, sfig2-1c_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
COL = {"0.6% ECS": "#46378a", "5.8% ECS": "#556b30", "11.3% ECS": "#ff8c00", "23.9% ECS": "#840204"}
rows = read_csv(os.path.join(HERE, "sfig2-1a.csv"))
fig, ax = plt.subplots(figsize=(3.6, 3.4))
for s, c in COL.items():
    rr = [r for r in rows if r["series"] == s and r["kind"] == "curve"]
    x = [float(r["splits_per_object"]) for r in rr]
    if rr and rr[0]["band_low"]:
        ax.fill_between(x, [float(r["band_low"]) for r in rr], [float(r["band_high"]) for r in rr], color=c, alpha=0.3, lw=0)
    ax.plot(x, [float(r["mergers_per_object"]) for r in rr], ".", color=c, ms=2, label=s)
    p = [r for r in rows if r["series"] == s and r["kind"] != "curve"][0]
    ax.plot(float(p["splits_per_object"]), float(p["mergers_per_object"]), "o", mfc="none", color=c)
ax.set_xlim(0, 0.6); ax.set_ylim(0, 0.6); ax.set_xlabel("Splits / Object"); ax.set_ylabel("Mergers / Object"); ax.legend(frameon=False, fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "sfig2-1a_replot.png"), dpi=150)
rows = read_csv(os.path.join(HERE, "sfig2-1c.csv"))
src = read_csv(os.path.join(HERE, "sfig2-1c_sourcedata.csv"))
fig, ax = plt.subplots(figsize=(3.6, 3.4))
for s, c in COL.items():
    rr = [r for r in rows if r["series"] == s and r["kind"] == "curve"]
    ax.plot([float(r["pixels_per_object"]) for r in rr], [float(r["cdf_pct"]) for r in rr], ".", color=c, ms=2)
    p = [r for r in rows if r["series"] == s and r["kind"] != "curve"][0]
    ax.plot(float(p["pixels_per_object"]), float(p["cdf_pct"]), "x", color=c, ms=8, mew=2)
    ss = [r for r in src if r["series"] == s]
    ax.step([float(r["pixels_per_object"]) for r in ss], [float(r["cdf_pct"]) for r in ss], ":", color=c, lw=0.8, where="post")
ax.set_xscale("log"); ax.set_xlim(10, 1e5); ax.set_ylim(-5, 105); ax.set_yticks([0, 25, 50, 75, 100])
ax.set_xlabel("2D GT Pixels / Object"); ax.set_ylabel("Cumulative Distribution\nFunction (%)")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "sfig2-1c_replot.png"), dpi=150)
