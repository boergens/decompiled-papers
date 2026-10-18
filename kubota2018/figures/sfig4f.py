"""Re-plot Supplementary Fig. 4f from sfig4f.csv -> sfig4f_replot.png (hidden markers are skipped)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig4_extract import KEV  # noqa: E402
from sfig45_common import replot  # noqa: E402

replot(os.path.join(HERE, "sfig4f.csv"), os.path.join(HERE, "sfig4f_replot.png"), KEV,
       (-0.3, 6.6), [0, 0.8, 1.6, 3.2, 6.4], (-285, 3), [0, -50, -100, -150, -200, -250], "Dwell time (µsec)", "Depression depth (nm)", legend=False, annotate=(0.97, 0.9, 'P < 0.01'))
