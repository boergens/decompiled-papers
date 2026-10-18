"""Re-plot Fig. 4g from fig4g.csv -> fig4g_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from heatmap_plot import plot  # noqa: E402

plot(HERE / "fig4g.csv", HERE / "fig4g_replot.png", 180, "°", "g  angle difference", [2013, 5013, 8013, 11013])
