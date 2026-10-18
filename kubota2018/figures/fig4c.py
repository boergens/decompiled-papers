"""Re-plot Fig. 4c of Kubota et al. 2018 from fig4c.csv -> fig4c_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig4c.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(3.6, 2.8))
for s, c in (("CNT-PET", "red"), ("Kapton", "blue"), ("cc-Kapton", "black")):
    r = [q for q in rows if q["series"] == s]
    x = np.array([float(q["wavelength_nm"]) for q in r])
    y = np.array([float(q["transmission_pct_mid"]) for q in r])
    gap = np.where(np.diff(x) > 3)[0] + 1          # break at columns hidden under another series
    ax.plot(np.insert(x, gap, np.nan), np.insert(y, gap, np.nan), color=c, lw=1.5, label=s)
ax.set_xlim(350, 850)
ax.set_ylim(0, 100)
ax.set_xticks([400, 500, 600, 700, 800])
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Transmission (%)")
ax.set_title("Transmittance spectra", fontsize=9)
if True:
    ax.legend(loc=(0.55, 0.15), fontsize=8, frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4c_replot.png"), dpi=150)
