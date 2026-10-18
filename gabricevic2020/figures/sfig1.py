"""Re-plot SI Fig. S1 of Gabričević et al. 2020 from sfig1.csv -> sfig1_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot_spectra  # noqa: E402

# limits = frame positions with the CSV's calibration: x 260-550 nm, y 0-1.80
replot_spectra("sfig1.csv", (260, 550), (0, 1.80), [300, 350, 400, 450, 500, 550], [0.0, 0.5, 1.0, 1.5], "sfig1_replot.png")
