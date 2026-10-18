"""Re-plot Supplementary Fig. 3f from sfig3f.csv -> sfig3f_replot.png."""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig_common import read_csv  # noqa: E402

rows = read_csv(os.path.join(HERE, "sfig3f.csv"))
fig, ax = plt.subplots(figsize=(2.2, 2.6))
ax.plot([float(q["eht_keV"]) for q in rows], [float(q["electron_dose_ke_per_nm2"]) for q in rows], "o", ms=4, color="k")
ax.set_xlim(-0.4, 10.4)
ax.set_xticks(range(0, 11, 2))
ax.set_ylim(3.95, 7.5)
ax.set_yticks([4, 5, 6, 7])
ax.set_xlabel("EHT (keV)")
ax.set_ylabel("Electron dose (ke$^-$ nm$^{-2}$)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig3f_replot.png"), dpi=150)
