#!/usr/bin/env python3
"""Extended Data Fig. 3A (p. 26): bar chart of # unique root IDs per # neurons per ID, two dates, broken y axis.
Vector paths -> edfig3a.csv. Bars are filled rectangles (#296790 = 9/30/20, #65b7ce = 4/4/23). The y axis is
broken: upper part ticks 1000..6000 (y = 150.12 ... 69.83 pt), lower part ticks 0..200 step 25 (265.43 ... 172.29 pt).
Bars taller than 200 are drawn in both parts; their value is read on the upper part. Each bar carries a printed
count label (outlined glyphs, read by eye from a 300 dpi render) which is given as printed_label."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[25]
dr = pp.drawings(page, pp.R(41, 47, 559, 272), how="inside")
yt = mc.dedupe(t["pos"] for t in pp.tick_marks(dr, "y", max_len=1.5, min_len=1.0))
up = [p for p in yt if p < 160]
lo = [p for p in yt if p > 160]
assert len(up) == 6 and len(lo) == 9, (up, lo)
YU = mc.LinAxis(list(zip(sorted(up, reverse=True), [1000, 2000, 3000, 4000, 5000, 6000])))
YL = mc.LinAxis(list(zip(sorted(lo, reverse=True), [0, 25, 50, 75, 100, 125, 150, 175, 200])))
xt = sorted(set(round(t["pos"], 2) for t in pp.tick_marks(dr, "x", max_len=1.5, min_len=1.0)))
CATS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17]
assert len(xt) == len(CATS)
LABELS = {"9/30/20": [5100, 1176, 366, 179, 95, 67, 31, 15, 7, 7, 2, 1, 2, 1, 1],
          "4/4/23": [29, 3, 5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
bars = {}
for d in dr:
    c = pp.hexcolor(d["fill"])
    if c not in ("#296790", "#65b7ce"):
        continue
    x0, y0, x1, y1 = d["rect"]
    if x0 > 455 and y1 < 95:  # legend patches
        continue
    s = "9/30/20" if c == "#296790" else "4/4/23"
    ci = min(range(len(xt)), key=lambda i: abs(xt[i] - ((x0 + x1) / 2 + (4.97 if s == "9/30/20" else -4.97))))
    bars.setdefault((s, ci), []).append((y0, y1))
rows, qa = [], []
for s in ["9/30/20", "4/4/23"]:
    for ci, cat in enumerate(CATS):
        parts = bars.get((s, ci), [])
        lower = [p for p in parts if p[1] > 260]
        upper = [p for p in parts if p[1] < 163.0]
        if upper:
            top = min(p[0] for p in upper); v = YU(top); part = "upper"
        else:
            top = min(p[0] for p in lower); v = YL(top); part = "lower"
        qa.append((xt[ci] + (-4.97 if s == "9/30/20" else 4.97), top))
        rows.append([s, cat, f"{v:.2f}", LABELS[s][ci], part])
mc.write_csv(Path(__file__).with_name("edfig3a.csv"), [
    "Extended Data Fig. 3A (p. 26 of microns2025.pdf): distribution of multi-soma root IDs by number of neurons per ID,",
    "before (9/30/20, dark blue) and after (4/4/23, light blue) APL proofreading.",
    "Provenance: tier 2, vector paths (bar tops exact to ~0.01 pt); printed_label = count printed above each bar,",
    "read by eye from a 300 dpi render (exact integers; they agree with bar_height to within 1.5).",
    "Columns: date (legend); neurons_per_id (x category; the axis skips 16); bar_height (count from the bar top);",
    "printed_label; axis_part (upper = read on the 1000-6000 part of the broken axis, lower = on the 0-200 part).",
    YU.describe("upper y"), YL.describe("lower y"),
], ["date", "neurons_per_id", "bar_height", "printed_label", "axis_part"], rows)
mc.overlay_pts(25, (41, 47, 559, 272), qa, "overlay_edfig3a.png", r=3)
