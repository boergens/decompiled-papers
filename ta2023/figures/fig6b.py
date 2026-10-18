"""Re-plot Figure 6(b) of Ta, Tran & Righi 2023 from fig6b.csv -> fig6b_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from replot import panel  # noqa: E402

panel(HERE / "fig6b.csv", HERE / "fig6b_replot.png",
      {"Case #1": ("blue", "s"), "Case #2": ("red", "o"), "Case #3": ("black", "^")},
      xlim=(-0.1, 2.6), ylim=(-1, 7.1), yticks=range(-1, 8), title="(b)")
