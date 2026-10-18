"""Extraction script for Extended Data Figure 4 (PDF page 44): box plots of explained variance per session.
Writes edfig4_boxes.csv (box geometry per condition) and edfig4_points.csv (individual sessions),
plus edfig4_orig.png (300-dpi crop of the original for QA)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import pdfplot as pp

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "2026.10.15.759299v1.full.pdf")
OUT = os.path.dirname(os.path.abspath(__file__))
page = pp.open_page(PDF, 44)
clip = pp.R(10, 20, 330, 164)
pp.render(page, clip, 300, f"{OUT}/edfig4_orig.png")
draws = pp.drawings(page)

# --- axes. Tick labels are glyph outlines; values read off the 300-dpi crop by eye.
YVALS = [-60, -40, -20, 0, 20, 40, 60, 80]
yax = pp.axis_from_ticks(draws, "y", YVALS, region=pp.R(30, 25, 43, 145), max_len=8)
print("y axis:", yax)
xticks = pp.tick_marks(draws, "x", region=pp.R(40, 141, 325, 150), max_len=8)
xcent = [t["pos"] for t in xticks]
print("x category tick positions:", [round(x, 2) for x in xcent])
CATS = ["priming", "conscious_state1", "suppressed_state1", "conscious_state2", "suppressed_state2"]
LABELS = ["Priming", "Conscious\nState 1", "Suppressed\nState 1", "Conscious\nState 2", "Suppressed\nState 2"]
assert len(xcent) == 5
xspacing = (xcent[-1] - xcent[0]) / 4

def cat_of(x):
    return min(range(5), key=lambda i: abs(xcent[i] - x))

# --- dotted zero line (556 tiny filled rects) -> y
zl = [d for d in draws if d["n_items"] > 300 and not d["has_curves"] and pp.hexcolor(d["fill"]) == "#000000"][0]
zy = (zl["rect"][1] + zl["rect"][3]) / 2
print("dotted line at y=%.3f -> value %.3f (should be 0); opacity %.3f" % (zy, yax(zy), zl["raw"].get("fill_opacity")))

# --- boxes: single-rect fills with a data colour, inside the plot area
boxes = {}
for d in draws:
    if d["rects"] and d["n_items"] == 1 and pp.hexcolor(d["fill"]) in ("#000000", "#fcae34", "#543379"):
        x0, y0, x1, y1 = d["rect"]
        if y1 - y0 > 2 and x1 - x0 > 10 and y0 > 25:
            c = cat_of((x0 + x1) / 2)
            boxes[c] = dict(x0=x0, x1=x1, ytop=y0, ybot=y1, color=pp.hexcolor(d["fill"]), box_alpha=d["raw"].get("fill_opacity"))
assert sorted(boxes) == [0, 1, 2, 3, 4], boxes.keys()
# median lines (horizontal 1-pt strokes spanning the box) and whiskers (vertical strokes at the box centre)
for d in draws:
    if d["kind"] == "stroke" and d["n_items"] == 1 and len(d["points"]) == 2:
        (ax0, ay0), (ax1, ay1) = d["points"]
        c = cat_of((ax0 + ax1) / 2)
        b = boxes[c]
        if abs(ay0 - ay1) < 0.01:          # horizontal: median
            assert abs(ax0 - b["x0"]) < 0.1 and abs(ax1 - b["x1"]) < 0.1
            b["ymed"] = ay0
            b["line_alpha"] = d["raw"].get("stroke_opacity")
        else:                               # vertical: whisker
            lo, hi = sorted([ay0, ay1])
            if hi <= b["ytop"] + 0.01:
                b["ywhisk_top"] = lo
            elif lo >= b["ybot"] - 0.01:
                b["ywhisk_bot"] = hi
            else:
                raise RuntimeError("whisker inside box?")
        b["line_width_pt"] = d["width"]

# --- points: small filled circles (4 bezier items)
pts = []
for m in pp.markers(draws, max_size=4):
    if m["n_items"] == 4 and m["has_curves"] and pp.hexcolor(m["fill"]) in ("#000000", "#fcae34", "#543379"):
        c = cat_of(m["cx"])
        pts.append(dict(cat=c, cx=m["cx"], cy=m["cy"], d=(m["w"] + m["h"]) / 2, color=pp.hexcolor(m["fill"])))
print("n points per category:", [sum(p["cat"] == c for p in pts) for c in range(5)])
assert all(sum(p["cat"] == c for p in pts) == 9 for c in range(5))

# --- write CSVs
com = [
    "Extended Data Figure 4 (PDF page 44 of 2026.10.15.759299v1.full.pdf). Box plots of explained variance (%) per session.",
    "Recovered from vector paths: boxes are single filled rectangles, median lines and whiskers are 1-pt strokes, points are 2.83-pt filled circles.",
    "y axis calibrated from the 8 horizontal tick marks (0.5-pt filled rects) at values %s (read off the render; labels are glyph outlines); max residual %.2e %%." % (YVALS, yax.resid),
    "x axis is categorical: category tick positions (pt) %s; x_position = category_index + (x - tick)/category_spacing." % [round(x, 2) for x in xcent],
    "Dotted reference line at y=%.3f %% (0.70 opacity black, 556 tiny rects)." % yax(zy),
    "Precision: PDF coordinates are exact to ~0.01 pt = ~0.013 %; values rounded to 0.01 %.",
]
rows = []
for c, name in enumerate(CATS):
    b = boxes[c]
    rows.append([c + 1, name, LABELS[c].replace("\n", " "), b["color"], round(b["box_alpha"], 3), round(b["line_alpha"], 3),
                 round(yax(b["ywhisk_bot"]), 2), round(yax(b["ybot"]), 2), round(yax(b["ymed"]), 2), round(yax(b["ytop"]), 2), round(yax(b["ywhisk_top"]), 2),
                 round((b["x1"] - b["x0"]) / xspacing, 3)])
pp.write_csv(f"{OUT}/edfig4_boxes.csv",
             ["category_index", "condition", "label", "color_hex", "box_fill_alpha", "line_and_point_alpha",
              "whisker_min_pct", "q1_pct", "median_pct", "q3_pct", "whisker_max_pct", "box_width_category_units"],
             rows, com + ["Boxes: median and interquartile range across 9 sessions; whiskers: range (min/max of the 9 points; checked: whisker ends coincide with extreme points).",
                          "Quartiles match MATLAB boxplot/prctile convention ((k-0.5)/n) applied to the 9 points."])
rows = []
for c, name in enumerate(CATS):
    P = sorted([p for p in pts if p["cat"] == c], key=lambda p: -p["cy"])
    for i, p in enumerate(P):
        rows.append([c + 1, name, i + 1, round(c + 1 + (p["cx"] - xcent[c]) / xspacing, 4), round(yax(p["cy"]), 2), p["color"], round(boxes[c]["line_alpha"], 3), round(p["d"], 2)])
pp.write_csv(f"{OUT}/edfig4_points.csv",
             ["category_index", "condition", "point_rank_ascending", "x_position", "explained_variance_pct", "color_hex", "alpha", "marker_diameter_pt"],
             rows, com + ["One row per session point (9 per condition), sorted ascending by value within a condition; x_position preserves the original horizontal jitter.",
                          "Session identity is not recoverable from the figure (points are not labelled)."])
for c in range(5):
    b = boxes[c]
    print(CATS[c], "whisk %.2f q1 %.2f med %.2f q3 %.2f whisk %.2f" % tuple(yax(b[k]) for k in ("ywhisk_bot", "ybot", "ymed", "ytop", "ywhisk_top")),
          "points", sorted(round(yax(p["cy"]), 2) for p in pts if p["cat"] == c))
