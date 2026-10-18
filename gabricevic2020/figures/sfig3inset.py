"""Re-plot the SI Fig. S3 inset of Gabričević et al. 2020 from sfig3inset.csv -> sfig3inset_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot_inset  # noqa: E402

# limits = inset frame positions with the CSV's calibration: x 0-5.41, y 0.269-0.870
replot_inset("sfig3inset.csv", (0, 5.41), (0.2694, 0.8703), [0, 1, 2, 3, 4, 5], [0.4, 0.6, 0.8], "[trans-DCE]/[Os(VIII)]",
             "A (nm)", "sfig3inset_replot.png", ycol="A")
