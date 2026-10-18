#!/usr/bin/env python3
"""Extended Data Fig. 2B (p. 25): number of output synapses vs number of edits, log-log scatter.
Vector paths -> edfig2b.csv. Each data point is a small filled circle path (8 Bezier items); its centre
is the bbox centre. Colour -> broad cell class via the legend. Tick labels are outlined glyphs; decades
read from the render and paired with the major tick marks (x 10^2, 10^3; y 10^2, 10^3, 10^4)."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[24]
dr = pp.drawings(page, pp.R(337, 57, 560, 279))
xt = sorted(set(round(t["pos"], 2) for t in pp.tick_marks(dr, "x", max_len=1.3, min_len=1.0)))
yt = sorted(set(round(t["pos"], 2) for t in pp.tick_marks(dr, "y", max_len=1.3, min_len=1.0)), reverse=True)
assert len(xt) == 2 and len(yt) == 3, (xt, yt)
X = mc.LinAxis(list(zip(xt, [100, 1000])), log=True)
Y = mc.LinAxis(list(zip(yt, [100, 1000, 10000])), log=True)
CLASSES = {"#e82634": "Excitatory", "#004c58": "Neurogliaform", "#9d81ac": "Martinotti",
           "#515a9f": "Bipolar", "#4291c9": "Basket"}
rows = []
pts = []
for d in dr:
    c = pp.hexcolor(d["fill"])
    if d["kind"] == "fill" and c in CLASSES and d["n_items"] == 8 and d["has_curves"]:
        x0, y0, x1, y1 = d["rect"]
        pts.append(((x0 + x1) / 2, (y0 + y1) / 2))
        rows.append([CLASSES[c], f"{X((x0 + x1) / 2):.5g}", f"{Y((y0 + y1) / 2):.5g}", c])
mc.write_csv(Path(__file__).with_name("edfig2b.csv"), [
    "Extended Data Fig. 2B (p. 25 of microns2025.pdf): number of output synapses vs number of edits for clean axons with cell type annotations.",
    "Provenance: tier 2, vector paths in the PDF; marker centres exact to ~0.01 pt (= ~0.0002 decades).",
    "Columns: cell_class (from the marker colour and the legend); n_edits (x); n_output_synapses (y); colour (fill hex as drawn).",
    "Rows are in drawing order (the PDF's z order). Overlapping markers are all included.",
    X.describe("x (log10 edits)"), Y.describe("y (log10 output synapses)"),
], ["cell_class", "n_edits", "n_output_synapses", "colour"], rows)
mc.overlay_pts(24, (300, 47, 562, 305), pts, "overlay_edfig2b.png", r=2)
