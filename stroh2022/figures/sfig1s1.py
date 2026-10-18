"""Re-plot Figure 1—figure supplement 1 panels a, d, g, j, m, p of Ströh et al. 2022 from sfig1s1?.csv
-> sfig1s1?_replot.png"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replot_common import read, plt, HERE, f  # noqa: E402

LIM = {"a": ((0, 1320), (-3.5, 1.4), [0, 400, 800, 1200], [-3, -2, -1, 0, 1]),
       "g": ((0, 1200), (-3, 3), [0, 400, 800, 1200], [-3, -2, -1, 0, 1, 2, 3]),
       "m": ((0, 1600), (-5, 2), [0, 400, 800, 1200, 1600], [-5, -4, -3, -2, -1, 0, 1, 2]),
       "d": ((44, 103), (186, 223), [50, 60, 70, 80, 90, 100], [190, 200, 210, 220]),
       "j": ((100, 180), (145, 170), [100, 120, 140, 160, 180], [150, 160, 170]),
       "p": ((50, 100), (55, 120), [50, 60, 70, 80, 90, 100], [60, 80, 100, 120])}
for p, (xl, yl, xt, yt) in LIM.items():
    rows = read(f"sfig1s1{p}.csv")
    xn, yn = list(rows[0].keys())[1:3]
    fig, ax = plt.subplots(figsize=(3.0, 2.6))
    if p in "agm":
        for s, c in (("SEM", "#0072bd"), ("μCT", "#d95319")):
            r = [q for q in rows if q["series"] == s]
            ax.vlines([f(q[xn]) for q in r], [f(q["line_bottom"]) for q in r], [f(q["line_top"]) for q in r], color=c, lw=1, label=s)
        ax.legend(loc="lower right", fontsize=7)
    else:
        ax.scatter([f(q[xn]) for q in rows], [f(q[yn]) for q in rows], s=0.3, color="k", lw=0)
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_xticks(xt); ax.set_yticks(yt)
    ax.set_xlabel(xn); ax.set_ylabel(yn)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"sfig1s1{p}_replot.png"), dpi=150)
    plt.close(fig)
