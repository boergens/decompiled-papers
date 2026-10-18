"""Re-plot Fig. 10b from fig10b.csv -> fig10b_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows  # noqa: E402

rows = read_rows(HERE / "fig10b.csv")
COL = {"E_pe": "black", "E_ke": "red", "E_total": "blue", "E_vdwl": "black", "E_angle": "blue", "E_coul": "red",
       "E_dihed": "cyan", "E_bond": "olive", "E_imp": "magenta"}
fig, ax = plt.subplots(figsize=(5, 3.8))
for s in dict.fromkeys(r["series"] for r in rows):
    d = [r for r in rows if r["series"] == s]
    ax.plot([float(r["x_hz_A"]) for r in d], [float(r["y_energy_increment_kcal_per_mol"]) for r in d], "-",
            color=COL[s], lw=1.5, label=s)
ax.set_xlim(-5, 50)
ax.set_xticks(range(-5, 55, 5))
ax.set_ylim(-300, 2800)
ax.set_xlabel("Displacement of indenter $h_z$ (Å)")
ax.set_ylabel("Energy increment (kcal/mol)")
ax.set_title("Loading rate of 1.0 Å/ps", fontsize=9)
ax.legend(loc="upper left", fontsize=7, frameon=False, ncol=2)
fig.tight_layout()
fig.savefig(HERE / "fig10b_replot.png", dpi=150)
