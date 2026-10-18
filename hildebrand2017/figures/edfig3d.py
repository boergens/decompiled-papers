"""Re-plot Extended Data Fig. 3d from edfig3d.csv -> edfig3d_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from histo_plot import plot  # noqa: E402

plot(HERE / "edfig3d.csv", HERE / "edfig3d_replot.png",
     [("lost", 12, "lost (244 sections, 1.34%)"), ("partial", 10, "partial (283 sections, 1.55%)"),
      ("adjacent", 1, "adjacent (5 section pairs, 0.03%)")],
     {"lost": ("lost_inset", 5000, 5500), "partial": ("partial_inset", 1250, 1750)},
     18207, [0, 6000, 12000, 18000], None)
