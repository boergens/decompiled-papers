"""Re-plot Fig. 1b of Pesce et al. 2022 from fig1b.csv -> fig1b_replot.png (uses replot() of fig1a.py)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fig1a import replot  # noqa: E402

if __name__ == "__main__":
    replot("b", (30, 760))     # the printed y axis of b starts at about 30 A.U., below the 1x10^2 tick
