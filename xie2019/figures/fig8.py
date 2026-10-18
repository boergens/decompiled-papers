"""Re-plot the colour-key maps of Figure 8 of Xie & Fang 2019 from fig8<panel>.csv.gz -> fig8_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from colourkey_map import replot_figure  # noqa: E402

replot_figure(HERE, "fig8", "abcdef", (3,2), 3, 10, "CSP", "fig8_replot.png")
