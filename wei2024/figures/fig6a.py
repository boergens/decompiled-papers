"""Re-plot Fig. 6a (main plot) from fig6a.csv -> fig6a_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows, RATE_COLOURS  # noqa: E402

rows = read_rows(HERE / "fig6a.csv")
fig, ax = plt.subplots(figsize=(5, 4))
ax.axvspan(20, 45, color="mistyrose", alpha=0.6, lw=0)
for s, c in RATE_COLOURS.items():
    m = [r for r in rows if r["series"] == s and r["kind"] == "marker"]
    d = [r for r in rows if r["series"] == s and r["kind"] == "dashed_curve"]
    if d:
        ax.plot([float(r["x_hz_A"]) for r in d], [float(r["y_Fz_nN"]) for r in d], "--", color=c, lw=1.2)
    if m:
        ax.plot([float(r["x_hz_A"]) for r in m], [float(r["y_Fz_nN"]) for r in m], "o", color=c, ms=4, label=s)
ax.set_xlim(-2.5, 47.5)
ax.set_ylim(-2, 15)
ax.set_xticks(range(0, 50, 5))
ax.set_yticks(range(-2, 15, 2))
ax.set_xlabel("Displacement of indenter $h_z$ (Å)")
ax.set_ylabel("Indenter force $F_z$ (nN)")
ax.legend(loc="upper left", fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig6a_replot.png", dpi=150)
