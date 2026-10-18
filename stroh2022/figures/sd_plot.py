"""Re-plot the source-data pages of Ströh et al. 2022 from the CSVs written by sd_extract.py.

    python3 -I sd_plot.py fig1-data1      (or any stem, or 'all')
-> sd/<stem>_replots/<stem>_pNN_replot.png: one figure per PDF page with the same layout as the source page
   (top row intensity vs time at 6 depths, middle row intensity vs depth at 6 times, bottom row the colour maps).
Reads only sd/<stem>_traces.csv and sd/<stem>_maps/*.csv.
"""
import csv
import glob
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SD = os.path.join(HERE, "sd")
STEMS = ["fig1-data1", "fig1-data2", "fig1-data3", "fig1-data4", "fig1-data5", "fig2-data1", "fig2-data2"]
DEPTHS = [200, 400, 600, 800, 1000, 1200]
TIMES = [30, 60, 120, 360, 600, 1200]


def read_map(fn):
    lines = [l for l in open(fn, encoding="utf-8") if not l.startswith("#")]
    xs = [float(v) for v in lines[0].strip().split(",")[1:]]
    ys, g = [], []
    for l in lines[1:]:
        p = l.rstrip("\n").split(",")
        ys.append(float(p[0]))
        g.append([float(v) if v else np.nan for v in p[1:]])
    return np.array(xs), np.array(ys), np.array(g)


def run(stem):
    rows = list(csv.DictReader(l for l in open(os.path.join(SD, f"{stem}_traces.csv"), encoding="utf-8")
                               if not l.startswith("#")))
    out = os.path.join(SD, f"{stem}_replots")
    os.makedirs(out, exist_ok=True)
    pages = sorted(set(int(r["page"]) for r in rows))
    for p in pages:
        pr = [r for r in rows if int(r["page"]) == p]
        fig = plt.figure(figsize=(24.41, 13.70), dpi=100)
        fig.suptitle(pr[0]["sample"], fontsize=11, y=0.995)
        ylims = []
        for k, panel in enumerate([f"x={d} μm" for d in DEPTHS] + [f"t={t} min" for t in TIMES]):
            ax = fig.add_axes([0.033 + (k % 6) * 0.1652, 0.69 - (k // 6) * 0.319, 0.122, 0.23])
            q = [r for r in pr if r["panel"] == panel]
            for s, c in (("data", "b"), ("model", "k")):
                z = [r for r in q if r["series"] == s]
                if z:
                    x = np.array([float(r["x"]) for r in z])
                    ax.vlines(x, [float(r["y_lower"]) for r in z], [float(r["y_upper"]) for r in z], color=c, lw=0.6)
            for r in q:
                if r["series"] == "circle":
                    ax.plot(float(r["x"]), float(r["y"]), "o", ms=12, mfc="none", mec="k", mew=0.7)
            ax.set_title(panel, fontsize=9, fontweight="bold")
            ax.set_xlim(0, 1200)
            ax.set_xlabel("Time t (min)" if k < 6 else "Depth x (μm)", fontsize=8)
            ax.set_ylabel("Intensity (a.u.)", fontsize=8)
            ax.tick_params(labelsize=7)
            ylims.append(ax)
        lo = min(a.get_ylim()[0] for a in ylims); hi = max(a.get_ylim()[1] for a in ylims)
        for a in ylims:
            a.set_ylim(lo, hi)
        maps = sorted(glob.glob(os.path.join(SD, f"{stem}_maps", f"{stem}_p{p:02d}_*.csv")))
        for j, fn in enumerate(sorted(maps, key=lambda f: "model" in f)):
            xs, ys, g = read_map(fn)
            ax = fig.add_axes([0.087 + j * 0.33, 0.05, 0.13, 0.23])
            im = ax.imshow(g, extent=(0, 1200, 0, 1200), origin="upper", aspect="auto", cmap="viridis")
            ax.set_title("data" if "_data" in fn else "model", fontsize=9, fontweight="bold")
            ax.set_xticks([0, 400, 800, 1200]); ax.set_yticks([0, 400, 800, 1200])
            ax.set_xlabel("Time t (min)", fontsize=8); ax.set_ylabel("Depth x (μm)", fontsize=8)
            ax.tick_params(labelsize=7)
            fig.colorbar(im, ax=ax, fraction=0.1).set_label("Intensity (a.u.)", fontsize=7)
        fig.savefig(os.path.join(out, f"{stem}_p{p:02d}_replot.png"), dpi=100)
        plt.close(fig)
        print(stem, p)


if __name__ == "__main__":
    for s in (STEMS if len(sys.argv) < 2 or sys.argv[1] == "all" else sys.argv[1:]):  # no argument = all
        run(s)
