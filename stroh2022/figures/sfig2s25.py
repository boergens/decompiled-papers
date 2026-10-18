"""Re-plot Figure 2—figure supplements 2 and 5 of Ströh et al. 2022 from sfig2s2_*.csv / sfig2s5_*.csv
-> sfig2s2_replot.png, sfig2s5_replot.png (same layout as the MATLAB pages)."""
import csv
import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEPTHS = [200, 400, 600, 800, 1000, 1200]
TIMES = [30, 60, 120, 360, 600, 1200]


def read_map(fn):
    lines = [l for l in open(fn, encoding="utf-8") if not l.startswith("#")]
    g = [[float(v) if v else np.nan for v in l.rstrip("\n").split(",")[1:]] for l in lines[1:]]
    return np.array(g)


for stem in ("sfig2s2", "sfig2s5"):
    rows = list(csv.DictReader(l for l in open(os.path.join(HERE, f"{stem}_traces.csv"), encoding="utf-8")
                               if not l.startswith("#")))
    fig = plt.figure(figsize=(18, 10.2), dpi=100)
    fig.suptitle(rows[0]["sample"], fontsize=11, y=0.995)
    axes = []
    for k, panel in enumerate([f"x={d} μm" for d in DEPTHS] + [f"t={t} min" for t in TIMES]):
        ax = fig.add_axes([0.03 + (k % 6) * 0.169, 0.69 - (k // 6) * 0.323, 0.125, 0.235])
        q = [r for r in rows if r["panel"] == panel]
        for s, c in (("data", "b"), ("model", "k")):
            z = [r for r in q if r["series"] == s]
            if z:
                ax.vlines([float(r["x"]) for r in z], [float(r["y_lower"]) for r in z], [float(r["y_upper"]) for r in z],
                          color=c, lw=0.6)
        for r in q:
            if r["series"] == "circle":
                ax.plot(float(r["x"]), float(r["y"]), "o", ms=12, mfc="none", mec="k", mew=0.7)
        ax.set_title(panel, fontsize=9, fontweight="bold")
        ax.set_xlim(0, 1200)
        ax.set_xlabel("Time t (min)" if k < 6 else "Depth x (μm)", fontsize=8)
        ax.set_ylabel("Intensity (a.u.)", fontsize=8)
        ax.tick_params(labelsize=7)
        axes.append(ax)
    lo = min(a.get_ylim()[0] for a in axes); hi = max(a.get_ylim()[1] for a in axes)
    for a in axes:
        a.set_ylim(lo, hi)
    for j, fn in enumerate(sorted(glob.glob(os.path.join(HERE, f"{stem}_map_*.csv")), key=lambda f: "model" in f)):
        ax = fig.add_axes([0.087 + j * 0.34, 0.04, 0.13, 0.235])
        im = ax.imshow(read_map(fn), extent=(0, 1200, 0, 1200), origin="upper", aspect="auto", cmap="viridis")
        ax.set_title("data" if "_data" in fn else "model", fontsize=9, fontweight="bold")
        ax.set_xticks([0, 400, 800, 1200]); ax.set_yticks([0, 400, 800, 1200])
        ax.set_xlabel("Time t (min)", fontsize=8); ax.set_ylabel("Depth x (μm)", fontsize=8)
        fig.colorbar(im, ax=ax, fraction=0.1).set_label("Intensity (a.u.)", fontsize=7)
    fig.savefig(os.path.join(HERE, f"{stem}_replot.png"), dpi=100)
