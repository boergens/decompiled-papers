"""Re-plot the Figure 1 inset of Gabričević et al. 2020 from fig1inset.csv -> fig1inset_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot_inset  # noqa: E402

# limits = inset frame positions with the CSV's calibration: x 0-5.2, y 0.5-2.30
replot_inset("fig1inset.csv", (0, 5.2), (0.5, 2.30), [0, 2, 4], [0.5, 1.0, 1.5, 2.0], "[TCE]/[Os(VIII)]",
             "$A$ (320 nm)", "fig1inset_replot.png", ycol="A_320")
