"""Re-plot Figure 7(a) of Ta, Tran & Righi 2023 from fig7a.csv -> fig7a_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from replot import panel  # noqa: E402

panel(HERE / "fig7a.csv", HERE / "fig7a_replot.png",
      {"0%": ("dimgray", "o"), "3%": ("red", "s"), "7%": ("blue", "^"), "10%": ("#00d000", "v")},
      xlim=(-0.1, 2.6), ylim=(-6, 7.4), yticks=range(-6, 8), title="(a) Compression")
