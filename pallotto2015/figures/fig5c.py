"""Re-plot Figure 5C from fig5c.csv -> fig5c_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = read_csv(os.path.join(HERE, "fig5c.csv"))
fig, ax = plt.subplots(figsize=(2.8, 3.2))
for i, r in enumerate(rows):
    m, lo, hi = float(r["mean_um"]), float(r["err_low_um"]), float(r["err_high_um"])
    ax.errorbar(i, m, yerr=[[m - lo], [hi - m]], fmt="o", color="k", capsize=3, ms=5)
ax.set_xticks(range(4)); ax.set_xticklabels([f"{r['condition'].replace(' ', chr(10))}\n{r['antibody']}" for r in rows], fontsize=7)
ax.set_xlim(-0.6, 3.6); ax.set_ylim(0, 30); ax.set_ylabel("FWHM labeling distance (µm)")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig5c_replot.png"), dpi=150)
