"""Re-plot the SI Fig. S2 inset of Gabričević et al. 2020 from sfig2inset.csv -> sfig2inset_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot_inset  # noqa: E402

# limits = inset frame positions with the CSV's calibration: x 0-5.49, y 0.4-1.50
replot_inset("sfig2inset.csv", (0, 5.49), (0.4, 1.50), [0, 1, 2, 3, 4, 5], [0.4, 0.7, 1.0, 1.3], "[cis-DCE]/[Os(VIII)]",
             "A (345 nm)", "sfig2inset_replot.png", ycol="A_345")
