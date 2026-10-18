"""Re-plot the sectioning-event histograms (Extended Data Figs. 3d, 4d) from their CSV."""
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read(path):
    with open(path) as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def plot(csv_path, out_png, main, insets, xmax, xticks, title_fmt):
    """main: list of (series, ymax, title); insets: dict series_main -> (inset series, lo, hi)."""
    rows = read(csv_path)
    fig, axes = plt.subplots(len(main), 1, figsize=(6, 1.5 * len(main)), sharex=True)
    for ax, (s, ymax, title) in zip(axes, main):
        for r in rows:
            if r["series"] == s:
                ax.bar(float(r["z_left"]), float(r["value"]), width=float(r["z_right"]) - float(r["z_left"]),
                       align="edge", color="0.45")
        ax.set_ylim(0, ymax)
        ax.set_yticks([ymax], [f"{ymax}/50"])
        ax.set_title(title, loc="left", fontsize=9)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        if s in insets:
            iname, lo, hi = insets[s]
            ax.axvspan(lo, hi, color="#cddcff", alpha=0.7, zorder=0)
            ia = ax.inset_axes([0.45, 0.65, 0.53, 0.3])
            for r in rows:
                if r["series"] == iname:
                    ia.bar(float(r["z_left"]), float(r["value"]), width=5, align="edge", color="0.45")
            ia.set_xlim(lo, hi)
            ia.set_ylim(0, 2)
            ia.set_yticks([2], ["2/5"])
            ia.set_xticks([lo, (lo + hi) / 2, hi])
            ia.set_facecolor("#cddcff")
    axes[-1].set_xlim(0, xmax)
    axes[-1].set_xticks(xticks)
    axes[-1].set_xlabel("position in series, z")
    fig.supylabel("sections per bin")
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
