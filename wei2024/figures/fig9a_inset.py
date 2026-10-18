"""Re-plot the Fig. 9a inset from fig9a_inset.csv -> fig9a_inset_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows  # noqa: E402

rows = read_rows(HERE / "fig9a_inset.csv")
STY = {"x-direction": ("black", "s"), "y-direction": ("red", "o"), "z-direction": ("magenta", "^"),
       "overall": ("darkorange", "v")}
fig, ax = plt.subplots(figsize=(3.4, 2.4))
for s, (c, mk) in STY.items():
    cu = [r for r in rows if r["series"] == s and r["kind"] == "curve"]
    m = [r for r in rows if r["series"] == s and r["kind"] == "marker"]
    ax.plot([float(r["x_hz_A"]) for r in cu], [float(r["y_force_nN"]) for r in cu], "-", color=c, lw=1.2)
    ax.plot([float(r["x_hz_A"]) for r in m], [float(r["y_force_nN"]) for r in m], mk, mfc="none", mec=c, ms=3)
ax.set_xlim(15, 25)
ax.set_ylim(-0.2, 0.7)
ax.set_xticks([15, 20, 25])
ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6])
fig.tight_layout()
fig.savefig(HERE / "fig9a_inset_replot.png", dpi=150)
