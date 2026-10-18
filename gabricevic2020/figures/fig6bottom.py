"""Re-plot Figure 6 (bottom panel) of Gabričević et al. 2020 from fig6bottom.csv -> fig6bottom_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gab_common import replot  # noqa: E402

replot("fig6bottom.csv", "TCE_mol_dm3", "kobs_s-1", {"TCE": ("v", "green")},
       (0, 0.0042), (0, 1.5e-4), [0, 0.001, 0.002, 0.003, 0.004], [0, 5.0e-5, 1.0e-4, 1.5e-4],
       "[TCE] (mol/dm$^3$)", "$k_\\mathrm{obs}$ (s$^{-1}$)", "fig6bottom_replot.png", legend=None,
       ytick_labels=["0.0", "5.0x10$^{-5}$", "1.0x10$^{-4}$", "1.5x10$^{-4}$"])
