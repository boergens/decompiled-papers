"""Re-plot Figure 4(b) of Ta, Tran & Righi 2023 from fig4b.csv -> fig4b_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from replot import panel  # noqa: E402

panel(HERE / "fig4b.csv", HERE / "fig4b_replot.png", {"O3": ("red", "s"), "O4": ("blue", "o")},
      xlim=(-0.1, 2.62), ylim=(-1, 7), yticks=range(-1, 8), title="(b)")
