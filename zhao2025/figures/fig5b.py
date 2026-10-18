"""Re-plot Fig. 5b of Zhao et al. 2025 from fig5b.csv -> fig5b_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import plotpanel  # noqa: E402

# frame top (201.33 pt) maps to r_b = 320 um
plotpanel.plot(HERE / "fig5b.csv", HERE / "fig5b_replot.png", (0, 60), (0, 320), [0, 10, 20, 30, 40, 50, 60],
               [0, 100, 200, 300], "d (μm)", "r$_b$ (μm)", figsize=(3.4, 2.4))
