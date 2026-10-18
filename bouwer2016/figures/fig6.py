"""Re-plot Fig. 6 of Bouwer et al. 2016 from fig6.csv -> fig6_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
data = {}
with open(HERE / "fig6.csv") as f:
    for r in csv.DictReader(l for l in f if not l.startswith("#")):
        data.setdefault(r["series"], []).append((float(r["landing_energy_keV"]), float(r["signal"])))
style = {
    "FEI CBS": dict(marker="o", mfc="none", mec="k", color="k"),
    "Gatan BS": dict(marker="s", mfc="none", mec="b", color="b"),
    "FEI CBS 3keV HT with Deceleration": dict(marker="D", mfc="darkgreen", mec="darkgreen", color="darkgreen"),
    "FEI CBS 4keV HT with Deceleration": dict(marker="v", mfc="k", mec="k", color="k"),
}
fig, ax = plt.subplots(figsize=(4.5, 4.6))
for name, st in style.items():
    x, y = zip(*data[name])
    ax.plot(x, y, ls="none", ms=5, label=name, clip_on=False, **{k: v for k, v in st.items() if k != "color"})
ax.set_xlim(0, 5)
ax.set_ylim(0, 1)
ax.set_xticks(range(6))
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax.grid(color="#8080c0", lw=0.6)
ax.set_xlabel("Landing Energy (keV)")
ax.set_ylabel("Normalized Gold BS Signal (Arbitrary Units)")
ax.set_title("Gatan BS Detector and FEI CBS Detector\nNormalized Gold BS Signal Vs.\nElectron Probe Beam Landing Energy",
             fontsize=9)
ax.legend(loc="lower right", fontsize=7)
fig.tight_layout()
fig.savefig(HERE / "fig6_replot.png", dpi=150)
