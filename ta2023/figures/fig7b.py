"""Re-plot Figure 7(b) of Ta, Tran & Righi 2023 from fig7b.csv -> fig7b_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from replot import panel  # noqa: E402

panel(HERE / "fig7b.csv", HERE / "fig7b_replot.png",
      {"0%": ("dimgray", "o"), "3%": ("red", "s"), "7%": ("blue", "^"), "10%": ("#00d000", "v")},
      xlim=(-0.1, 2.6), ylim=(-1, 7.4), yticks=range(-1, 8), title="(b) Expansion")
