"""Re-plot Figure 6 (top panel) of Gabričević et al. 2020 from fig6top.csv -> fig6top_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot  # noqa: E402

# axis limits: frame positions converted with the CSV's calibration (x 0-0.0216, y 0-0.0110)
replot("fig6top.csv", "substrate_mol_dm3", "kobs_s-1", {"trans-DCE": ("o", "red"), "cis-DCE": ("D", "blue")},
       (0, 0.0216), (0, 0.0110), [0, 0.005, 0.010, 0.015, 0.020], [0, 0.003, 0.006, 0.009],
       "[Substrate] (mol/dm$^3$)", "$k_\\mathrm{obs}$ (s$^{-1}$)", "fig6top_replot.png", legend="upper left")
