"""Re-plot Supplementary Fig. 4g from sfig4g.csv -> sfig4g_replot.png (hidden markers are skipped)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig4_extract import KEV  # noqa: E402
from sfig45_common import replot  # noqa: E402

replot(os.path.join(HERE, "sfig4g.csv"), os.path.join(HERE, "sfig4g_replot.png"), KEV,
       (-0.3, 6.6), [0, 0.8, 1.6, 3.2, 6.4], (-0.2, 6.1), [0, 1, 2, 3, 4, 5, 6], "Dwell time (µsec)", "Electron dose (e$^-$ nm$^{-2}$)", legend=True, annotate=None)
