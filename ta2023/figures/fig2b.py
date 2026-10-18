"""Re-plot Figure 2(b) of Ta, Tran & Righi 2023 from fig2b.csv -> fig2b_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from replot import panel  # noqa: E402

panel(HERE / "fig2b.csv", HERE / "fig2b_replot.png",
      {"C(001)": ("#00c000", "s"), "C(110)": ("red", "^"), "C(111)": ("blue", "o")},
      xlim=(-0.1, 2.1), ylim=(-1, 10.2), yticks=range(-1, 11), title="(b) Ether", xticks=(0, 0.5, 1, 1.5, 2), legend=False)
