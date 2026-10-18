"""Re-plot Figure 1-figure supplement 1A from sfig1-1a.csv -> sfig1-1a_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = read_csv(os.path.join(HERE, "sfig1-1a.csv"))
PX = 0   # 'perfused' category, left of the axis break
fig, ax = plt.subplots(figsize=(4.0, 3.0))
for r in rows:
    x = PX if r["category"] == "perfused" else float(r["osmolarity_mOsm"])
    m, lo, hi = float(r["thickness_um"]), float(r["err_low_um"]), float(r["err_high_um"])
    ax.errorbar(x, m, yerr=[[m - lo], [hi - m]], fmt="o", color="k", capsize=3, ms=5)
ax.set_xlim(-50, 500); ax.set_ylim(0, 600)
ax.set_xticks([PX, 200, 300, 400, 500]); ax.set_xticklabels(["perfused", "200", "300", "400", "500"])
ax.set_xlabel("Fix vehicle osmolarity (mOsm)"); ax.set_ylabel("Slice thickness (um)")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "sfig1-1a_replot.png"), dpi=150)
