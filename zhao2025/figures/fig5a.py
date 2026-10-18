"""Re-plot Fig. 5a of Zhao et al. 2025 from fig5a.csv -> fig5a_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import plotpanel  # noqa: E402

plotpanel.plot(HERE / "fig5a.csv", HERE / "fig5a_replot.png", (0, 2.4), (0, 600), [0, 0.6, 1.2, 1.8, 2.4],
               [0, 200, 400, 600], "Σexp (chains · m$^{-2}$) × 10$^{18}$", "Γ (J m$^{-2}$)", figsize=(3.4, 2.8))
