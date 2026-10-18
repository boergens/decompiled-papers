"""Re-plot Fig. 4a of Zhao et al. 2025 from fig4a.csv -> fig4a_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import plotpanel  # noqa: E402

# frame = lambda 1.0-1.5, d 0-80 (top frame unlabelled); region shading edges as read in the CSV header
plotpanel.plot(HERE / "fig4a.csv", HERE / "fig4a_replot.png", (1.0, 1.5), (0, 80), [1, 1.2, 1.4], [0, 20, 40, 60],
               "λ", "d (μm)", shades=[(1.0, 1.1423, "#eff6fb"), (1.1423, 1.4279, "#ddecf7"), (1.4279, 1.5, "#bfdaef")])
