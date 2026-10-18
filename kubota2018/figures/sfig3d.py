"""Re-plot sfig3d.csv (mapped depth grid) with the panel's own colour scale -> sfig3d_replot.png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfig_scm import replot  # noqa: E402

replot("sfig3d")
