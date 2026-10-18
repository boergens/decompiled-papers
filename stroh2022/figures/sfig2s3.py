"""Re-plot Figure 2—figure supplement 3a,b of Ströh et al. 2022 from sfig2s3a.csv, sfig2s3b.csv -> *_replot.png"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replot_common import read, plt, HERE, f  # noqa: E402

for p in "ab":
    rows = read(f"sfig2s3{p}.csv")
    fig, ax = plt.subplots(figsize=(2.8, 3.0))
    xn, yn = ("depth_um", "intensity_au") if p == "a" else ("time_min", "height_change_percent")
    for s, c in (("t = 0 hrs after in H2O", "#006ebc"), ("t = 20 hrs after in H2O", "k"), ("height change", "k")):
        r = [q for q in rows if q["series"] == s]
        if r:
            ax.plot([f(q[xn]) for q in r], [f(q[yn]) for q in r], ".", ms=2, color=c, label=s)
    if p == "a":
        ax.axhline(1, color="k", lw=0.8); ax.set_xlim(-200, 1200); ax.set_ylim(0.4, 1.27); ax.set_yticks([0.4, 1])
        ax.set_xlabel("Depth (μm)"); ax.set_ylabel("Intensity (a.u.)"); ax.legend(fontsize=6)
    else:
        ax.axhline(0, color="k", lw=0.8); ax.set_xlim(0, 1210); ax.set_ylim(-10, 21); ax.set_yticks([-10, 0, 10, 20])
        ax.set_xlabel("Time (min)"); ax.set_ylabel("Change in sample height (%)")
    ax.set_xticks([0, 500, 1000])
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"sfig2s3{p}_replot.png"), dpi=150)
    plt.close(fig)
