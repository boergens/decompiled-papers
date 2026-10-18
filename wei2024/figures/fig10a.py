"""Re-plot Fig. 10a from fig10a.csv -> fig10a_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows  # noqa: E402

rows = read_rows(HERE / "fig10a.csv")
STY = {"0.10 Å/ps": ("black", "o", "black"), "0.25 Å/ps": ("red", "o", "none"), "0.50 Å/ps": ("limegreen", "^", "none"),
       "0.75 Å/ps": ("blue", "v", "none"), "1.00 Å/ps": ("cyan", "D", "none"), "1.50 Å/ps": ("olive", "s", "none"),
       "2.00 Å/ps": ("darkorange", "p", "none")}
fig, ax = plt.subplots(figsize=(5, 3.8))
for s, (c, mk, fc_) in STY.items():
    m = [r for r in rows if r["series"] == s and r["kind"] == "marker"]
    d = [r for r in rows if r["series"] == s and r["kind"] == "dashed_curve"]
    if d:
        ax.plot([float(r["x_hz_A"]) for r in d], [float(r["y_total_energy_kcal_per_mol"]) for r in d], "--", color=c)
    ax.plot([float(r["x_hz_A"]) for r in m], [float(r["y_total_energy_kcal_per_mol"]) for r in m], mk, mec=c,
            mfc=c if fc_ != "none" else "none", ms=4, label=s, ls="none")
ax.set_xlim(-5, 50)
ax.set_ylim(5000, 10500)
ax.set_xticks(range(-5, 55, 5))
ax.set_xlabel("Displacement of indenter $h_z$ (Å)")
ax.set_ylabel("Total energy (kcal/mol)")
ax.legend(loc="upper left", fontsize=7, frameon=False, ncol=2)
fig.tight_layout()
fig.savefig(HERE / "fig10a_replot.png", dpi=150)
