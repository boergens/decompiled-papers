"""Digitize Figure 2b of Ströh et al. 2022 (PDF p.7), a colour map, through its colour bar -> fig2b.csv

Source: embedded raster of Figure 2 (1949 x 2653 px, ~322 ppi). The map image spans columns 758-1104 and rows
108-453 (axis lines at the left and bottom edge; the edges are the axis limits 0 and 1200, as the tick marks show).
Colour bar: interior columns 1175-1194, rows 386-453; tick marks at row 385 (label 186) and row 446.75 (label 93).
    python3 -I fig2b_extract.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import fig_image, map_grid, save_crop  # noqa: E402

a = fig_image(2)
val, m, b = map_grid(a, (108, 453, 758, 1104), (386, 453, 1175, 1194), [(385, 186), (446.75, 93)],
                     os.path.join(HERE, "fig2b.csv"), [
    "Ströh et al. 2022 eLife, Figure 2b: average experimentally measured spatio-temporal osmium density accumulation (n=13) in 2% buffered OsO4, title 'Accumulation of OsO4'; values = Density (nmol/mm3).",
    "Grid: first column y = Depth (μm) at the pixel-row centre (top row = 1200 μm side); header = Time (min) at the",
    "  pixel-column centres; cells = value read through the colour bar.",
    "Provenance: tier 3, digitized from the embedded ~322 ppi raster (no vector data) by fig2b_extract.py: every map",
    "  pixel is assigned the value of the colour-bar row with the nearest colour; the bar is calibrated on its two",
    "  labelled ticks. Axes: the image edges are taken as 0 and 1200; the tick marks (x: 0, 400, 800, 1200 every 115.3 px;",
    "  y: 400, 800 on the right edge) agree with that within 0.5 px.",
    "Uncertainty: ±1.7 min and ±1.7 μm (half a pixel); value quantized to the bar's colour steps (see below), ±1 step.",
])
save_crop(a, (100, 470, 758 - 10, 1194 + 70), os.path.join(HERE, "../work/fig2b_src.png"))
print("fig2b.csv", val.shape, float(m), float(b))
