#!/usr/bin/env python3
"""Fig. 6f (p. 8): percentage of output synapses with a postsynaptic soma vs number of output synapses (log x),
per neuron, coloured by cell class. Vector paths -> fig6f.csv. Each point is a filled circle path (8 Bezier items);
centre = bbox centre. Axes: tick labels are text; x major ticks 10^2, 10^3, 10^4 at 441.83, 484.25, 526.66 pt;
y ticks every 5 % from 100 (184.47 pt) to 55 (258.94 pt), labelled 60 ... 100."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[7]
CLIP = (395, 170, 540, 300)
dr = pp.drawings(page, pp.R(*CLIP), how="inside")
xt = sorted(set(round(t["pos"], 2) for t in pp.tick_marks(dr, "x", max_len=3, min_len=2.0)))
yt = mc.dedupe(t["pos"] for t in pp.tick_marks(dr, "y", max_len=2, min_len=1.5))
assert len(xt) == 3 and len(yt) == 10, (xt, yt)
X = mc.LinAxis(list(zip(xt, [100, 1000, 10000])), log=True)
Y = mc.LinAxis(list(zip(yt, [100, 95, 90, 85, 80, 75, 70, 65, 60, 55])))
CL = {"#e82634": "Excitatory", "#004d62": "Neurogliaform", "#997eab": "Martinotti", "#565da0": "Bipolar", "#47a2d5": "Basket"}
rows, qa = [], []
for d in dr:
    c = pp.hexcolor(d["fill"])
    if d["kind"] == "fill" and c in CL and d["n_items"] == 8:
        x0, y0, x1, y1 = d["rect"]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rows.append([CL[c], f"{X(cx):.5g}", f"{Y(cy):.3f}", c])
        qa.append((cx, cy))
mc.write_csv(Path(__file__).with_name("fig6f.csv"), [
    "Fig. 6f (p. 8 of microns2025.pdf): number of output synapses per neuron (x, log) vs percentage of output synapses",
    "with a postsynaptic soma (y, axis label 'Percentage with post-synaptic soma'), coloured by cell class (legend).",
    "Provenance: tier 2, vector paths (marker centres exact to ~0.01 pt).",
    "Columns: cell_class; n_output_synapses; pct_with_postsynaptic_soma; colour (marker fill). Rows in drawing order.",
    X.describe("x (log10)"), Y.describe("y"),
], ["cell_class", "n_output_synapses", "pct_with_postsynaptic_soma", "colour"], rows)
mc.overlay_pts(7, CLIP, qa, "overlay_fig6f.png", dpi=400, r=2)
