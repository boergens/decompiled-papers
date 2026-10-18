"""Re-plot Figure 5(b) of Ta, Tran & Righi 2023 from fig5b.csv -> fig5b_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from replot import panel  # noqa: E402

panel(HERE / "fig5b.csv", HERE / "fig5b_replot.png",
      {"OH": ("black", "D"), "H2": ("blue", "o"), "H2O": ("red", "s"), "OOH": ("#00c000", "^")},
      xlim=(-0.06, 2.75), ylim=(-1, 7), yticks=range(-1, 8), title="(b)", ylabel="(no axis title; energy, eV)")
