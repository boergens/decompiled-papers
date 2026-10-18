"""Re-plot Figure 3 of Gabričević et al. 2020 from fig3.csv -> fig3_replot.png (broken y axis as two stacked axes)"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gab_common import replot_bands  # noqa: E402

# the two y segments: frame top / break / frame bottom converted with the CSV's two calibrations;
# heights in proportion to their pixel heights in the source (213 px and 373 px)
fig, (up, lo) = plt.subplots(2, 1, sharex=True, figsize=(6, 4.3), gridspec_kw={"height_ratios": [213, 373], "hspace": 0.04})
style = {"TCE": ("green", "violet"), "cis-DCE": ("blue", "violet")}
replot_bands("fig3.csv", "t_s", "A_280", {"TCE": style["TCE"]}, (0, 5), (0.30726, 0.31119), [0, 1, 2, 3, 4, 5],
             [0.308, 0.310], "", "", None, ax=up, legend=False)
replot_bands("fig3.csv", "t_s", "A_280", {"cis-DCE": style["cis-DCE"]}, (0, 5), (0.25500, 0.26186), [0, 1, 2, 3, 4, 5],
             [0.256, 0.258, 0.260], "$t$ (s)", "", None, ax=lo, legend=False)
up.spines["bottom"].set_visible(False)
lo.spines["top"].set_visible(False)
up.tick_params(bottom=False)
fig.text(0.02, 0.5, "$A$ (280 nm)", rotation=90, va="center")
fig.legend(handles=up.collections[:1] + lo.collections[:1], labels=["TCE", "cis-DCE"], loc=(0.45, 0.45), frameon=False)
fig.subplots_adjust(left=0.17, right=0.97, top=0.97, bottom=0.12)
fig.savefig(os.path.join(HERE, "fig3_replot.png"), dpi=150)
