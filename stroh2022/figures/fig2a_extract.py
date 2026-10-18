"""Digitize Figure 2a of Ströh et al. 2022 (PDF p.7), a colour map, through its colour bar -> fig2a.csv

Source: embedded raster of Figure 2 (1949 x 2653 px, ~322 ppi). The map image spans columns 136-481 and rows
108-453 (axis lines at the left and bottom edge; the edges are the axis limits 0 and 1200, as the tick marks show).
Colour bar: interior columns 531-550, rows 386-453; tick marks at row 385 (label 1) and row 446.75 (label 0.5).
    python3 -I fig2a_extract.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import fig_image, map_grid, save_crop  # noqa: E402

a = fig_image(2)
val, m, b = map_grid(a, (108, 453, 136, 481), (386, 453, 531, 550), [(385, 1), (446.75, 0.5)],
                     os.path.join(HERE, "fig2a.csv"), [
    "Ströh et al. 2022 eLife, Figure 2a: spatio-temporal washout of osmium in samples incubated in 2.5% potassium ferrocyanide K4[Fe(CN)6] (n=6), title 'Washout of OsO4 in K4[Fe(CN)6]'; values = Intensity (a.u.).",
    "Grid: first column y = Depth (μm) at the pixel-row centre (top row = 1200 μm side); header = Time (min) at the",
    "  pixel-column centres; cells = value read through the colour bar.",
    "Provenance: tier 3, digitized from the embedded ~322 ppi raster (no vector data) by fig2a_extract.py: every map",
    "  pixel is assigned the value of the colour-bar row with the nearest colour; the bar is calibrated on its two",
    "  labelled ticks. Axes: the image edges are taken as 0 and 1200; the tick marks (x: 0, 400, 800, 1200 every 115.3 px;",
    "  y: 400, 800 on the right edge) agree with that within 0.5 px.",
    "Uncertainty: ±1.7 min and ±1.7 μm (half a pixel); value quantized to the bar's colour steps (see below), ±1 step.",
])
save_crop(a, (100, 470, 136 - 10, 550 + 70), os.path.join(HERE, "../work/fig2a_src.png"))
print("fig2a.csv", val.shape, float(m), float(b))
