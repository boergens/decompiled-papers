"""Re-plot SI Fig. S2 (main panel) of Gabričević et al. 2020 from sfig2main.csv -> sfig2main_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot_spectra  # noqa: E402

# limits = frame positions with the CSV's calibration: x 260-500 nm, y 0-2.0
replot_spectra("sfig2main.csv", (260, 500), (0, 2.0), [300, 350, 400, 450, 500], [0.0, 0.5, 1.0, 1.5, 2.0], "sfig2main_replot.png")
