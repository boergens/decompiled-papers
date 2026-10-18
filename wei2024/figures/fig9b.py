"""Re-plot Fig. 9b from fig9b.csv -> fig9b_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows  # noqa: E402

rows = read_rows(HERE / "fig9b.csv")
fig, ax = plt.subplots(figsize=(4.6, 3.6))
for s, c in (("average: h_z of 40 ∼ 45 Å", "blue"), ("average: h_z of 20 ∼ 45 Å", "red")):
    m = [r for r in rows if r["series"] == s and r["kind"] == "marker"]
    f = [r for r in rows if r["series"] == s and r["kind"] == "fit_equation"]
    ax.plot([float(r["x_rate_A_per_ps"]) for r in m], [float(r["y_force_nN"]) for r in m], "o", color=c, label=s)
    ax.plot([float(r["x_rate_A_per_ps"]) for r in f], [float(r["y_force_nN"]) for r in f], "--", color=c, label="Fitting")
ax.set_xlim(-0.24, 2.26)
ax.set_ylim(1.25, 9)
ax.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0])
ax.set_yticks(range(2, 10))
ax.set_xlabel("Loading rate (Å/ps)")
ax.set_ylabel("Average overall pairwise\ninteraction force (nN)")
ax.legend(loc="upper left", fontsize=7, frameon=False, ncol=2)
fig.tight_layout()
fig.savefig(HERE / "fig9b_replot.png", dpi=150)
