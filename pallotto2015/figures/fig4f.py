"""Re-plot Figure 4F from fig4f.csv -> fig4f_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = read_csv(os.path.join(HERE, "fig4f.csv"))
COL = {"AII (blue)": "#0000ff", "cone bipolar (green)": "#00ff00", "presynaptic amacrine cell (cyan)": "#00ffff", "other (black)": "k"}
fig, ax = plt.subplots(figsize=(3.0, 3.0))
for i, bar in enumerate(["Tight contacts", "Cleft contacts"]):
    for r in rows:
        if r["bar"] == bar:
            b, t = float(r["y_bottom"]), float(r["y_top"])
            ax.bar(i, t - b, bottom=b, width=0.5, color=COL[r["segment"]], edgecolor="k")
ax.set_xticks([0, 1]); ax.set_xticklabels(["Tight\ncontacts", "Cleft\ncontacts"]); ax.set_xlim(-0.6, 1.6)
ax.set_ylim(0, 175); ax.set_yticks([0, 50, 100, 150]); ax.set_ylabel("# of contacts")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig4f_replot.png"), dpi=150)
