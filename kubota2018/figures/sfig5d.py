"""Re-plot Supplementary Fig. 5d from sfig5d.csv -> sfig5d_replot.png (hidden markers are skipped)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig5_extract import DWELL  # noqa: E402
from sfig45_common import replot  # noqa: E402

replot(os.path.join(HERE, "sfig5d.csv"), os.path.join(HERE, "sfig5d_replot.png"), DWELL,
       (-0.3, 6.3), [0, 1, 2, 3, 4, 5, 6], (-285, 3), [0, -50, -100, -150, -200, -250], "Acceleration voltage (keV)", "Depression depth (nm)", legend=True, annotate=None)
