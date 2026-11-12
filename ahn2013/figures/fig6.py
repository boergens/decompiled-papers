"""Re-plot Fig. 6 (both panels) from figures/fig6left.csv and figures/fig6right.csv -> figures/fig6_replot.png.

    python3 -I -B figures/fig5.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "work"))
from replot_common import read_csv, series, split_gaps  # noqa: E402

L = read_csv(os.path.join(HERE, "fig6left.csv"))
R = read_csv(os.path.join(HERE, "fig6right.csv"))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6))
for name, col in (("TM", "tab:blue"), ("TE", "tab:red")):
    x, y = series(L, name, "wavelength_nm", "transmission_pct")
    a1.plot(x, y, color=col, lw=2, label=name)
a1.set(xlim=(400, 900), ylim=(0, 100), xlabel="Wavelength (nm)", ylabel="Transmission (%)", title="Transmission")
a1.set_yticks(range(0, 101, 10))
a1.legend(loc="center right")
pr = [r for r in R if r["series"] == "ER"]
a2.vlines([r["wavelength_nm"] for r in pr], [r["er_min"] for r in pr], [r["er_max"] for r in pr],
          color="#a894c8", lw=0.8, label="ER (range per pixel column)")
x, y = series(R, "200 per. Mov. Avg. (ER)", "wavelength_nm", "extinction_ratio")
for i, (sx, sy) in enumerate(split_gaps(x, y, 3)):
    a2.plot(sx, sy, color="k", lw=0.8, label="200 per. Mov. Avg. (ER)" if i == 0 else None)
a2.set(xlim=(400, 900), ylim=(0, 4000), xlabel="Wavelength (nm)", ylabel="Extinction Ratio", title="Extinction Ratio")
a2.legend(loc="upper left", fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig6_replot.png"), dpi=150)
