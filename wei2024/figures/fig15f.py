"""Re-plot wei2024 Fig. 15f from figures/fig15f.csv (markers) and figures/fig15f_fits.csv (fit curves)
-> figures/fig15f_replot.png. Run: python3 -I -B figures/fig15f.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import STYLE, plt, plot_series, series  # noqa: E402

fig, ax = plt.subplots(figsize=(4.2, 3.2), dpi=150)
plot_series(ax, series(HERE / "fig15f.csv"), lines=False, labels={k: "_" + k for k in STYLE})
for name, pts in series(HERE / "fig15f_fits.csv").items():
    xs, ys = zip(*pts)
    ax.plot(xs, ys, "--", color=STYLE[name][0], lw=1.2, label=name.replace(" A/ps", " Å/ps"))
ax.set_xlim(-2.5, 32)
ax.set_xticks(range(0, 31, 5))
ax.set_ylim(-20, 2.02)
ax.set_yticks(range(-20, 1, 4))
ax.set_xlabel("Sliding distance (Å)")
ax.set_ylabel("Force along y-direction $F_y$ (nN)")
ax.legend(loc="lower left", fontsize=6, frameon=False, ncol=2)
fig.tight_layout()
fig.savefig(HERE / "fig15f_replot.png")
