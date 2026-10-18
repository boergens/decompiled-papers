"""Re-plot Figure 2(a) of Ta, Tran & Righi 2023 from fig2a.csv -> fig2a_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from replot import panel  # noqa: E402

panel(HERE / "fig2a.csv", HERE / "fig2a_replot.png",
      {"C(001)": ("#00c000", "s"), "C(110)": ("red", "^"), "C(111)": ("blue", "o")},
      xlim=(-0.08, 2.6), ylim=(-1, 10.2), yticks=range(-1, 11), title="(a) Clean surface")
