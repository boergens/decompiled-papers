"""Re-plot the colour-key maps of Figure 6 of Xie & Fang 2019 from fig6<panel>.csv.gz -> fig6_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from colourkey_map import replot_figure  # noqa: E402

replot_figure(HERE, "fig6", "abcdef", (3,2), -232, -200, "z-direction height (Å)", "fig6_replot.png")
