"""Re-plot the colour-key maps of Figure 9 of Xie & Fang 2019 from fig9<panel>.csv.gz -> fig9_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from colourkey_map import replot_figure  # noqa: E402

replot_figure(HERE, "fig9", "abcde", (5,1), 3, 10, "CSP", "fig9_replot.png")
