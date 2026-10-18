"""Re-plot Fig. 10d from fig10d.csv -> fig10d_replot.png."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from f2_plot import read_rows  # noqa: E402

rows = read_rows(HERE / "fig10d.csv")
cats = list(dict.fromkeys(r["loading_rate_A_per_ps"] for r in rows))
fig, ax = plt.subplots(figsize=(5, 3.8))
for j, (s, c) in enumerate((("pe", "darkorange"), ("ke", "red"), ("total", "blue"))):
    v = {r["loading_rate_A_per_ps"]: float(r["delta_E_kcal_per_mol"]) for r in rows if r["series"] == s}
    ax.bar([i + (j - 1) * 0.18 for i in range(len(cats))], [v[k] for k in cats], width=0.15, color=c, label=s)
ax.set_xticks(range(len(cats)))
ax.set_xticklabels(cats)
ax.set_ylim(0, 4500)
ax.set_xlabel("Loading rate (Å/ps)")
ax.set_ylabel("ΔE (kcal/mol)")
ax.legend(loc="upper right", frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig10d_replot.png", dpi=150)
