"""Re-plot Fig. 4h from fig4h.csv -> fig4h_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from heatmap_plot import plot  # noqa: E402

plot(HERE / "fig4h.csv", HERE / "fig4h_replot.png", 8, " µm", "h  distance difference", [2013, 5013, 8013, 11013])
