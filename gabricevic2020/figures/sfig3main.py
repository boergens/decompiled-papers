"""Re-plot SI Fig. S3 (main panel) of Gabričević et al. 2020 from sfig3main.csv -> sfig3main_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot_spectra  # noqa: E402

# limits = frame positions with the CSV's calibration: x 250-500 nm, y 0-1.85
replot_spectra("sfig3main.csv", (250, 500), (0, 1.852), [250, 300, 350, 400, 450, 500], [0.0, 0.5, 1.0, 1.5], "sfig3main_replot.png")
