"""Re-plot helpers for wei2024 Figs. 12 and 15 (fork F3). Read only the panel CSV ('#' lines skipped)."""
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

STYLE = {  # series -> (colour, marker, filled)
    "Fx": ("black", "s", False), "Fy": ("red", "o", True), "Fz": ("magenta", "^", False),
    "5 A": ("black", "s", False), "10 A": ("red", "o", True), "15 A": ("limegreen", "^", False),
    "20 A": ("blue", "v", False), "25 A": ("magenta", "D", False),
    "0.1 A/ps": ("black", "s", False), "0.5 A/ps": ("red", "^", False), "1.0 A/ps": ("darkorange", "v", False),
    "1.5 A/ps": ("blue", "D", False), "2.0 A/ps": ("magenta", "o", False),
}


def read(path):
    rows = list(csv.reader(line for line in open(path) if not line.startswith("#")))
    head, data = rows[0], rows[1:]
    return head, data


def series(path, ycol=2):
    head, data = read(path)
    out = {}
    for r in data:
        if r[ycol] == "":
            continue
        out.setdefault(r[0], []).append((float(r[1]), float(r[ycol])))
    return out


def plot_series(ax, ser, lines=True, labels=None):
    for name, pts in ser.items():
        c, mk, filled = STYLE[name]
        xs, ys = zip(*sorted(pts))
        lab = labels.get(name, name) if labels else name
        ax.plot(xs, ys, ls="--" if lines else "none", color=c, marker=mk, ms=3.5, lw=1,
                mfc=c if filled else "none", mec=c, label=lab)


def force_panel(csv_path, out_png, title, ylim=(-15, 10), yticks=range(-15, 11, 5)):
    fig, ax = plt.subplots(figsize=(4.2, 3.2), dpi=150)
    plot_series(ax, series(csv_path), labels={"Fx": "$F_x$", "Fy": "$F_y$", "Fz": "$F_z$"})
    ax.set_xlim(-2.5, 32)
    ax.set_xticks(range(0, 31, 5))
    ax.set_ylim(*ylim)
    ax.set_yticks(list(yticks))
    ax.set_xlabel("Sliding distance (Å)")
    ax.set_ylabel("Force (nN)")
    ax.text(0.3, 0.93, title, transform=ax.transAxes, ha="center", va="top", fontsize=9)
    ax.legend(loc="lower left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(out_png)
    plt.close(fig)
