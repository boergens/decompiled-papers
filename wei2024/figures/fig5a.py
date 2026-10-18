"""Re-plot Fig. 5a from figures/fig5a.csv -> figures/fig5a_replot.png."""
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
rows = list(csv.reader(l for l in open(HERE / "fig5a.csv") if not l.startswith("#")))
hdr, rows = rows[0], rows[1:]
i = {k: n for n, k in enumerate(hdr)}
STY = {"x": ("k", "s"), "y": ("r", "o"), "z": ("m", "^")}
FITS = {"x": "y = -158.95e^(-x/0.045) + 151.39, R² = 0.66", "y": "y = -152.11e^(-x/0.041) + 139.91, R² = 0.63",
        "z": "y = -139.06e^(-x/0.040) + 143.88, R² = 0.51"}
fig, ax = plt.subplots(figsize=(5.6, 4.4))
for s, (c, m) in STY.items():
    mk = [(float(r[i["tensile_strain"]]), float(r[i["tensile_stress_MPa"]]), r[i["flag"]]) for r in rows
          if r[i["series"]] == s and r[i["kind"]] == "marker" and r[i["tensile_stress_MPa"]]]
    clear = [(x, y) for x, y, f in mk if f == ""]
    unc = [(x, y) for x, y, f in mk if f == "uncertain"]
    ax.plot(*zip(*clear), m, mfc="none", color=c, ms=4, ls="none", label=f"{s}  {FITS[s]}")
    if unc:
        ax.plot(*zip(*unc), m, mfc="none", color=c, ms=4, ls="none", alpha=0.4)
    fc = sorted((float(r[i["tensile_strain"]]), float(r[i["tensile_stress_MPa"]])) for r in rows
                if r[i["series"]] == s and r[i["kind"]] == "fit_curve_digitized")
    ax.plot(*zip(*fc), ".", color=c, ms=1.5)
ax.set_xlim(-0.025, 0.315)
ax.set_ylim(-50, 250)
ax.set_xticks([0, .05, .1, .15, .2, .25, .3])
ax.set_xlabel("Tensile strain")
ax.set_ylabel("Tensile stress (MPa)")
ax.legend(title="Tensile direction", loc="lower right", fontsize=7, frameon=False)
ax.set_title("(a) Tensile stress-strain (faint markers: flagged uncertain)", y=-0.22, fontsize=9)
fig.tight_layout()
fig.savefig(HERE / "fig5a_replot.png", dpi=150)
