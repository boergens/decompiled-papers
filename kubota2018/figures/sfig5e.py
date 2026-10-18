"""Re-plot Supplementary Fig. 5e from sfig5e.csv -> sfig5e_replot.png (hidden markers are skipped)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig5_extract import DWELL  # noqa: E402
from sfig45_common import replot  # noqa: E402

replot(os.path.join(HERE, "sfig5e.csv"), os.path.join(HERE, "sfig5e_replot.png"), DWELL,
       (-0.3, 6.3), [0, 1, 2, 3, 4, 5, 6], (-0.2, 6.1), [0, 1, 2, 3, 4, 5, 6], "Acceleration voltage  (keV)", "Electron dose (ke$^-$ nm$^{-2}$)", legend=False, annotate=None)
