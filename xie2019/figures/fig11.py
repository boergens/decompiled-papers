"""Re-plot the colour-key maps of Figure 11 of Xie & Fang 2019 from fig11<panel>.csv.gz -> fig11_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from colourkey_map import replot_figure  # noqa: E402

replot_figure(HERE, "fig11", "abcd", (2,2), -10.2, 2.2, "x-displacement (Å)", "fig11_replot.png")
