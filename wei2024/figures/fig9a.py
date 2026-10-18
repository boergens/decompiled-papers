"""Re-plot Fig. 9a (main plot) from fig9a.csv -> fig9a_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows  # noqa: E402

rows = read_rows(HERE / "fig9a.csv")
STY = {"x-direction": ("black", "s"), "y-direction": ("red", "o"), "z-direction": ("magenta", "^"),
       "overall": ("darkorange", "v")}
fig, ax = plt.subplots(figsize=(5, 3.8))
for s, (c, mk) in STY.items():
    cu = [r for r in rows if r["series"] == s and r["kind"] == "curve"]
    m = [r for r in rows if r["series"] == s and r["kind"] == "marker"]
    ax.plot([float(r["x_hz_A"]) for r in cu], [float(r["y_force_nN"]) for r in cu], "-", color=c, lw=1.5, label=s)
    ax.plot([float(r["x_hz_A"]) for r in m], [float(r["y_force_nN"]) for r in m], mk, mfc="none", mec=c, ms=4)
ax.set_xlim(-2.6, 48.6)
ax.set_ylim(-4.3, 15)
ax.set_xticks(range(0, 50, 5))
ax.set_yticks(range(-3, 16, 3))
ax.set_xlabel("Displacement of indenter $h_z$ (Å)")
ax.set_ylabel("Pairwise interaction force (nN)")
ax.text(0, 13.5, "Loading rate of 1.0 Å/ps")
ax.legend(loc="center left", fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig9a_replot.png", dpi=150)
