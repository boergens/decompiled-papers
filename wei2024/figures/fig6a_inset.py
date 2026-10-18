"""Re-plot the Fig. 6a inset from fig6a_inset.csv -> fig6a_inset_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows  # noqa: E402

rows = read_rows(HERE / "fig6a_inset.csv")
m = [r for r in rows if r["kind"] == "marker"]
d = [r for r in rows if r["kind"] == "dotted_curve"]
fig, ax = plt.subplots(figsize=(3.2, 2.4))
ax.plot([float(r["x_hz_A"]) for r in d], [float(r["y_Fz_nN"]) for r in d], ":", color="k", lw=1.5)
ax.plot([float(r["x_hz_A"]) for r in m], [float(r["y_Fz_nN"]) for r in m], "o", color="k", ms=4)
ax.set_xlim(20, 50)
ax.set_ylim(-1, 12)
ax.set_xticks([20, 30, 40, 50])
ax.set_yticks([0, 4, 8, 12])
ax.text(27, 10.5, "0.1 Å/ps")
fig.tight_layout()
fig.savefig(HERE / "fig6a_inset_replot.png", dpi=150)
