"""Re-plot Fig. 4e from fig4e.csv -> fig4e_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from pairs_plot import plot  # noqa: E402

plot(HERE / "fig4e.csv", HERE / "fig4e_replot.png", 180.0, 8.0, "°", "µm", "difference matrix at z = 5560 (upper a, lower d)")
