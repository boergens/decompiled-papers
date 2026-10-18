"""Re-plot Fig. 4b of Zhao et al. 2025 from fig4b.csv -> fig4b_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import plotpanel  # noqa: E402

plotpanel.plot(HERE / "fig4b.csv", HERE / "fig4b_replot.png", (1.0, 1.5), (0, 8), [1, 1.2, 1.4], [0, 2, 4, 6, 8],
               "λ", r"$\bar{\Sigma}$", shades=[(1.0, 1.1429, "#eff6fb"), (1.1429, 1.4280, "#ddecf7"), (1.4280, 1.5, "#bfdaef")])
