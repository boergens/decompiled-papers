"""Re-plot the abstract graphic of Ta, Tran & Righi 2023 from toc.csv -> toc_replot.png"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from replot import panel  # noqa: E402

panel(HERE / "toc.csv", HERE / "toc_replot.png", {"Energy (eV)": ("blue", "o")},
      xlim=(-0.08, 2.58), ylim=(-1, 10), yticks=range(-1, 11), ycol="value", legend=False,
      twin=dict(ycol="value", ylim=(-1.8, 12.08), yticks=range(0, 13, 2), ylabel="Force (nN)",
                styles={"Force (nN)": ("red", "s")}))
