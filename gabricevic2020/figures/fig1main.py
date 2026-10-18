"""Re-plot Figure 1 (main panel) of Gabričević et al. 2020 from fig1main.csv -> fig1main_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot_spectra  # noqa: E402

# limits = frame positions with the CSV's calibration: x 249.9-502.9 nm, y 0-2.80
replot_spectra("fig1main.csv", (249.9, 502.9), (0, 2.80), [300, 400, 500], [0, 1, 2], "fig1main_replot.png")
