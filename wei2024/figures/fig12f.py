"""Re-plot wei2024 Fig. 12f from figures/fig12f.csv -> figures/fig12f_replot.png. Run: python3 -I -B figures/fig12f.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import plt, plot_series, series  # noqa: E402

fig, ax = plt.subplots(figsize=(4.2, 3.2), dpi=150)
plot_series(ax, series(HERE / "fig12f.csv"), labels={k: k.replace(" A", " Å") for k in ["5 A", "10 A", "15 A", "20 A", "25 A"]})
ax.set_xlim(-2.5, 32)
ax.set_xticks(range(0, 31, 5))
ax.set_ylim(7000, 13000)
ax.set_xlabel("Sliding distance (Å)")
ax.set_ylabel("Total energy (kcal/mol)")
ax.text(0.5, 0.93, "$h_c$ (legend), 1.0 Å/ps", transform=ax.transAxes, ha="center", va="top", fontsize=9)
ax.legend(loc="upper left", fontsize=7, frameon=False, bbox_to_anchor=(0, 0.88))
fig.tight_layout()
fig.savefig(HERE / "fig12f_replot.png")
