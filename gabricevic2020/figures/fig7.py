"""Re-plot Figure 7 of Gabričević et al. 2020 from fig7.csv -> fig7_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot  # noqa: E402

# limits = frame positions converted with the CSV's calibration
replot("fig7.csv", "pH", "kobs_s-1", {"trans-DCE": ("o", "red"), "cis-DCE": ("D", "blue"), "TCE": ("v", "green")},
       (11.42, 13.09), (2.9e-5, 1.81e-3), [11.5, 12.0, 12.5, 13.0], [1e-4, 1e-3], "pH", "$k_\\mathrm{obs}$ (s$^{-1}$)",
       "fig7_replot.png", logy=True, legend=(0.38, 0.22), ytick_labels=["1x10$^{-4}$", "1x10$^{-3}$"])
