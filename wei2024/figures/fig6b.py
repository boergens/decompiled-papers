"""Re-plot Fig. 6b from fig6b.csv -> fig6b_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows, RATE_COLOURS  # noqa: E402

rows = read_rows(HERE / "fig6b.csv")
fig, ax = plt.subplots(figsize=(5, 4))
for s, c in RATE_COLOURS.items():
    m = [r for r in rows if r["series"] == s and r["kind"] == "marker"]
    f = [r for r in rows if r["series"] == s and r["kind"] == "fit_equation"]
    if f:
        ax.plot([float(r["x_hc_A"]) for r in f], [float(r["y_Fz_nN"]) for r in f], "--", color=c, lw=1.2, label=s)
    if m:
        ax.plot([float(r["x_hc_A"]) for r in m], [float(r["y_Fz_nN"]) for r in m], "o", color=c, ms=4)
ax.set_xlim(-2.6, 27.75)
ax.set_ylim(-2, 20)
ax.set_xticks(range(0, 30, 5))
ax.set_yticks(range(0, 21, 4))
ax.set_xlabel("Indentation depths $h_c$ (Å)")
ax.set_ylabel("Indenter force $F_z$ (nN)")
ax.legend(loc="upper left", fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig6b_replot.png", dpi=150)
