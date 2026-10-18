#!/usr/bin/env python3
"""Fig. 6h (p. 8): stacked bars / flow diagram of the output synapses of the cell in Fig. 6g. Vector paths -> fig6h.csv.
Columns: 'Connects to target' (No Soma / Postsynaptic soma), 'Target cell class' (flow bands Excitatory, Inhibitory,
Uncharacterized from the soma bar to the cell-type column), 'Target cell type' (sub-class segments) and
'Functionally matched' (Manual, Automatic bars). The y axis 'Output synapses' has unlabelled ticks every 16.82 pt above
'0' (410.87 pt). Segment names come from the printed labels or, for unlabelled segments, from the matching legend
colours of Fig. 6b,c (L4 #822778, L6CT #008344, L6IT #941245, Bipolar #575ea1, Neurogliaform #004e62)."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[7]
dr = pp.drawings(page, pp.R(286, 285, 400, 412), how="inside")
BASE = 410.87
TOTAL = 411.05 - 292.0  # height of the first column (No Soma + Postsynaptic soma)
TEXT_TOTAL = 1412  # total output synapses of this neuron, from the main text (p. 9), used only for count_est
NAMES = {
    ("Connects to target", "#939598"): "No Soma", ("Connects to target", "#000000"): "Postsynaptic soma",
    ("Target cell class", "#e82634"): "Excitatory", ("Target cell class", "#375ba4"): "Inhibitory",
    ("Target cell class", "#d1d3d4"): "Uncharacterized",
    ("Target cell type", "#dc1c32"): "L2", ("Target cell type", "#f18b2f"): "L3", ("Target cell type", "#e75f5f"): "L5ET",
    ("Target cell type", "#eb338b"): "L5IT", ("Target cell type", "#822778"): "L4 (unlabelled; colour of L4 in Fig. 6b)",
    ("Target cell type", "#008344"): "L6CT (unlabelled; colour of L6CT in Fig. 6b)",
    ("Target cell type", "#941245"): "L6IT (unlabelled; colour of L6IT in Fig. 6b)",
    ("Target cell type", "#47a1d5"): "Basket", ("Target cell type", "#987daa"): "Martinotti",
    ("Target cell type", "#575ea1"): "Bipolar (unlabelled; colour of Bipolar in Fig. 6c)",
    ("Target cell type", "#004e62"): "Neurogliaform (unlabelled; colour of Neurogliaform in Fig. 6c)",
    ("Target cell type", "#d1d3d4"): "Uncharacterized (continuation of the flow band)",
    ("Functionally matched", "#004921"): "Manual", ("Functionally matched", "#6fb758"): "Automatic",
}
rows, qa = [], []
for d in dr:
    if d["kind"] != "fill" or d["rect"][3] - d["rect"][1] < 0.3:
        continue
    c = pp.hexcolor(d["fill"])
    x0, y0, x1, y1 = d["rect"]
    if x0 > 286 and x1 <= 308.5:
        col = "Connects to target"
    elif x0 >= 307.9 and x1 <= 352 and (d["n_items"] == 4 or c == "#e82634"):
        col = "Target cell class"
        if d["n_items"] == 4:  # flow band: use its left end (at the soma bar)
            ys = sorted(y for x, y in d["points"] if abs(x - 307.97) < 0.05)
            y0, y1 = ys[0], ys[-1]
    elif x0 >= 351 and x1 <= 365:
        col = "Target cell type"
    elif x0 >= 371:
        col = "Functionally matched"
    else:
        continue
    if (col, c) not in NAMES:
        continue
    h = y1 - y0
    rows.append([col, NAMES[(col, c)], c, f"{round(BASE - y1, 2) + 0.0:.2f}", f"{round(BASE - y0, 2) + 0.0:.2f}", f"{h:.2f}", f"{h / TOTAL:.4f}",
                 f"{h / TOTAL * TEXT_TOTAL:.0f}"])
    qa += [((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)]
order = ["Connects to target", "Target cell class", "Target cell type", "Functionally matched"]
rows.sort(key=lambda r: (order.index(r[0]), float(r[3])))
mc.write_csv(Path(__file__).with_name("fig6h.csv"), [
    "Fig. 6h (p. 8 of microns2025.pdf): quantification of the output synapses of the neuron in Fig. 6g by postsynaptic category.",
    "Provenance: tier 2, vector paths (segment edges exact to ~0.01 pt).",
    "Columns: column (x category); segment (label); colour; bottom_pt, top_pt (height above the zero line in pt, 410.87 pt);",
    "height_pt; frac_of_total (height / height of the first column, 119.05 pt, which is all output synapses);",
    "count_est = frac_of_total x 1,412: the y axis has no numbers; 1,412 is the total given in the main text for this neuron",
    "(p. 9), which matches the drawn 74.5 % / 25.4 % split of the first column. With it, the unlabelled ticks every 16.82 pt",
    "are 200 synapses apart. Target cell class bands are measured at their left end (x = 307.97 pt).",
    "Note: the drawn class split (about 735 / 296 / 24) differs from the counts in the main text (662 excitatory,",
    "275 inhibitory, 116 not classified).",
], ["column", "segment", "colour", "bottom_pt", "top_pt", "height_pt", "frac_of_total", "count_est"], rows)
mc.overlay_pts(7, (255, 280, 405, 440), qa, "overlay_fig6h.png", dpi=400, r=2)
