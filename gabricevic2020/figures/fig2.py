"""Re-plot Figure 2 of Gabričević et al. 2020 from fig2.csv -> fig2_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot_bands  # noqa: E402

# limits = frame positions converted with the CSV's calibration (x 0-10.84 h, y 0.1796-0.4503)
replot_bands("fig2.csv", "t_h", "A_280",
             {"TCE": ("green", "violet"), "trans-DCE": ("red", "cyan"), "cis-DCE": ("blue", "violet")},
             (0, 10.84), (0.1796, 0.4503), [0, 5, 10], [0.2, 0.3, 0.4], "$t$ (h)", "$A$ (280 nm)", "fig2_replot.png")
