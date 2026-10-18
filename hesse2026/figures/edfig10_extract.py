"""Extract Extended Data Figure 10 (page 50) panels into figures/."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import helpers as H  # noqa: E402
import pdfplot as pp  # noqa: E402

OUT = os.path.join(H.PROJ, "figures")
page = pp.open_page(H.PDF, 50)
PAGE_NOTE = "source: Hesse et al. 2026 bioRxiv 10.64898/2026.10.15.759299v1, Extended Data Figure 10, PDF page 50 (vector graphics; bars, error bars and in-bar labels are drawn inside form XObjects)"
MODELS = ["Real", "2-state", "Average", "Uncoord"]

# ------------------------------------------------------------------ a: model x test matrix (transcribed)
draws = H.drawings_ext(page, pp.R(2, 14, 262, 142))
colx = {"Real": 83.9, "2-state": 120.0, "C-only": 156.2, "Average": 192.4, "Uncoord": 228.6}   # column tick x
rowy = {"Reconstruction": 50.9, "Reconstruction^coord": 73.9, "Reversal": 97.0, "Log likelihood": 120.0}  # row tick y
marks = {}
for d in draws:
    c = pp.hexcolor(d["fill"])
    if c in ("#33a13d", "#d63030"):
        cx, cy = (d["rect"][0] + d["rect"][2]) / 2, (d["rect"][1] + d["rect"][3]) / 2
        col = min(colx, key=lambda k: abs(colx[k] - cx)); row = min(rowy, key=lambda k: abs(rowy[k] - cy))
        assert abs(colx[col] - cx) < 5 and abs(rowy[row] - cy) < 5
        marks[(row, col)] = "pass" if c == "#33a13d" else "fail"
assert len(marks) == 20
rows = [[r] + [marks[(r, c)] for c in colx] for r in rowy]
pp.write_csv(os.path.join(OUT, "edfig10a.csv"), ["test"] + list(colx), rows,
             [PAGE_NOTE + ", panel a", "Model x test matrix: green check (#33a13d) = pass, red cross (#d63030) = fail; mark colours read from the vector paths, row/column assignment by position"])
for r in rows:
    print(r)
pp.render(page, pp.R(2, 14, 262, 142), 300, os.path.join(OUT, "edfig10a_orig.png"))


# ------------------------------------------------------------------ bar panels b, d, e, f
def ticks_axis(draws, orient, values, region):
    ax = pp.axis_from_ticks(draws, orient, values, region=region, min_len=3.0, max_len=6.0)
    print("   ", orient, ax)
    return ax


def bar_panel(letter, clip, yvals, yregion, xregion, palette, printed, unit_scale=1.0, ytitle=""):
    draws = H.drawings_ext(page, clip)
    xax = ticks_axis(draws, "x", [0, 1, 2, 3], xregion)
    yax = ticks_axis(draws, "y", yvals, yregion)
    y0 = yax.inv(0.0)
    bars = []
    for d in draws:
        if d["kind"] not in ("fill", "fillstroke"):
            continue
        col = pp.hexcolor(d["fill"]); op = round(d["raw"].get("fill_opacity") or 1.0, 2)
        if (col, op) not in palette:
            continue
        x0, yy0, x1, yy1 = d["rect"]
        if not (abs(yy0 - y0) < 0.6 or abs(yy1 - y0) < 0.6):  # must touch the zero line (excludes legend swatches)
            continue
        if x1 - x0 < 4:
            continue
        top = yy0 if abs(yy1 - y0) < 0.6 else yy1
        bars.append(dict(x0=x0, x1=x1, cx=(x0 + x1) / 2, value=yax(top), series=palette[(col, op)], col=col, op=op,
                         clipped=abs(top - yax.inv(yvals[0])) < 0.3))  # bar drawn down to the lower axis limit
    bars.sort(key=lambda b: b["cx"])
    # error bars: black 0.5-pt vertical strokes at the bar centre
    for b in bars:
        ys = []
        for d in draws:
            if d["kind"] != "stroke" or pp.hexcolor(d["color"]) not in ("#000000", "#262626", "#333333"):
                continue
            for sp in d["subpaths"]:
                if len(sp) == 2 and abs(sp[0][0] - sp[1][0]) < 0.05 and abs(sp[0][0] - b["cx"]) < 0.4:
                    ys += [sp[0][1], sp[1][1]]
        b["err_lo"] = yax(max(ys)) if ys else float("nan")
        b["err_hi"] = yax(min(ys)) if ys else float("nan")
        b["n_err_segments"] = len(ys) // 2
    # printed numbers (glyph outlines, #222222) inside bars
    labels = []
    for d in draws:
        if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#222222" and d["has_curves"]:
            x0, yy0, x1, yy1 = d["rect"]
            if x1 - x0 < 4 and yy1 - yy0 < 9 and x0 > clip.x0 + 40:  # small rotated number inside a bar (not the y title)
                labels.append(((x0 + x1) / 2, (yy0 + yy1) / 2))
    labels.sort()
    assert len(labels) == len(printed), (letter, len(labels), labels)
    for (lx, ly), txt in zip(labels, printed):
        b = min(bars, key=lambda b: abs(b["cx"] - lx))
        assert abs(b["cx"] - lx) < 2.5, (lx, b["cx"])
        b["printed"] = txt
    # group index from the x axis (models at 0..3)
    rows = []
    for b in bars:
        g = round(xax(b["cx"]))
        assert abs(xax(b["cx"]) - g) < 0.4, (b["cx"], xax(b["cx"]))
        val = b["value"]
        printed_v = b.get("printed", "")
        assert b["clipped"] == bool(printed_v), (letter, b)
        rows.append([MODELS[g], b["series"], round(val * unit_scale, 3) if not b["clipped"] else float(printed_v),
                     round(val * unit_scale, 3), round(b["err_lo"] * unit_scale, 3), round(b["err_hi"] * unit_scale, 3),
                     printed_v, b["col"].lstrip("#"), b["op"], b["n_err_segments"]])
    print(f"  panel {letter}: {len(bars)} bars")
    for r in rows:
        print("   ", r)
    hdr = ["model", "series", "value" + ytitle, "bar_drawn_to" + ytitle, "err_lo" + ytitle, "err_hi" + ytitle,
           "printed_label", "bar_colour_rgbhex", "bar_fill_opacity", "n_error_bar_segments"]
    comments = [
        PAGE_NOTE + f", panel {letter}",
        "value = bar height read from the bar rectangle (top edge mapped through the y axis); for bars clipped at the lower axis limit the value is the number printed inside the bar (transcribed by eye from a 300-dpi render) and bar_drawn_to gives the drawn extent",
        "err_lo / err_hi = ends of the black error bar (vertical 0.5-pt strokes at the bar centre; the geometry is unclipped even where the figure clips it at the axis limit); n_error_bar_segments = 2 normally (one segment each way from the bar top)",
        "x axis: 4 tick marks calibrated to the four model positions 0..3 (Real, 2-state, Average, Uncoord) (resid %.1e)" % xax.resid,
        "y axis: %d tick marks calibrated to %s (resid %.1e)" % (len(yvals), yvals, yax.resid),
        "bar colours as in the PDF: #fcae34 orange (state 1), #543379 purple (state 2); light variants are the same colour at fill opacity 0.35",
    ]
    pp.write_csv(os.path.join(OUT, f"edfig10{letter}.csv"), hdr, rows, comments)
    pp.render(page, clip, 300, os.path.join(OUT, f"edfig10{letter}_orig.png"))


PAL4 = {("#fcae34", 1.0): "state1_conscious", ("#fcae34", 0.35): "state1_suppressed",
        ("#543379", 0.35): "state2_conscious", ("#543379", 1.0): "state2_suppressed"}
print("== b")
bar_panel("b", pp.R(262, 12, 516, 142), [-100, -50, 0, 50, 100], pp.R(311, 30, 316.6, 130), pp.R(320, 126.3, 500, 132),
          PAL4, ["-183", "-182", "-108", "-106", "-109", "-105"], ytitle="_ev_pct")
print("== d")
bar_panel("d", pp.R(262, 142, 516, 276), [-100, -50, 0, 50, 100], pp.R(311, 150, 316.7, 248), pp.R(320, 244.2, 500, 250),
          PAL4, ["-124", "-128"], ytitle="_ev_pct")
print("== e")
bar_panel("e", pp.R(2, 276, 262, 392), [-1, -0.5, 0, 0.5, 1], pp.R(71, 282, 76.4, 378), pp.R(80, 376.9, 240, 382),
          {("#fcae34", 1.0): "state1", ("#543379", 1.0): "state2"}, [], ytitle="_tuning_r")
print("== f")
bar_panel("f", pp.R(262, 276, 516, 392), [-0.15, -0.1, -0.05, 0, 0.05, 0.1], pp.R(318, 290, 323.4, 378), pp.R(330, 377.2, 500, 382),
          {("#262626", 1.0): "two_state_minus_one_state"}, [], ytitle="_loglik")

# ------------------------------------------------------------------ c: reconstruction EV vs achieved dwell time
clip = pp.R(2, 142, 262, 276)
draws = H.drawings_ext(page, clip)
xax = ticks_axis(draws, "x", [0, 50, 100, 150, 200, 250, 300], pp.R(60, 244.9, 240, 250))
yax = ticks_axis(draws, "y", [45, 50, 55, 60, 65], pp.R(61, 150, 66.1, 246))
P_LABELS = ["0.50", "0.60", "0.70", "0.80", "0.87", "0.92", "0.95", "0.97", "0.99"]  # read by eye, left to right
series = {"#cc2929": "real_data", "#2970bf": "average_model"}
rows = []
for col, name in series.items():
    line = [d for d in draws if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == col and d["width"] == 1.0
            and len(d["points"]) > 2]  # (the 2-point one is the legend line sample)
    assert len(line) == 1 and len(line[0]["points"]) == 9, [len(l["points"]) for l in line]
    pts = line[0]["points"]
    # markers (3-pt filled circles), excluding the legend marker
    mk = [m for m in pp.markers(draws, max_size=3.2) if pp.hexcolor(m["fill"]) == col and not (170 < m["cx"] < 178 and 160 < m["cy"] < 174)]
    assert len(mk) == 9, len(mk)
    mk.sort(key=lambda m: m["cx"])
    # x error bars: 0.5-pt horizontal strokes of the series colour at the point's y
    for i, (px, py) in enumerate(pts):
        m = mk[i]
        assert abs(m["cx"] - px) < 0.05 and abs(m["cy"] - py) < 0.05, (m, px, py)
        xs = []
        for d in draws:
            if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == col and d["width"] == 0.5:
                for sp in d["subpaths"]:
                    if len(sp) == 2 and abs(sp[0][1] - sp[1][1]) < 0.05 and abs(sp[0][1] - py) < 0.3:
                        xs += [sp[0][0], sp[1][0]]
        rows.append([name, P_LABELS[i], round(xax(px), 3), round(yax(py), 4),
                     round(xax(min(xs)), 3) if xs else "", round(xax(max(xs)), 3) if xs else "", len(xs) // 2])
# label glyph groups: check there are 9 per series near the points
lab = [d for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#222222" and d["has_curves"]
       and 4 < d["rect"][2] - d["rect"][0] < 9 and d["rect"][3] - d["rect"][1] < 4 and d["rect"][0] > 80 and d["rect"][1] < 240]
print("  c: point labels found:", len(lab))
for r in rows:
    print("   ", r)
pp.write_csv(os.path.join(OUT, "edfig10c.csv"),
             ["series", "self_transition_p", "achieved_mean_dwell_ms", "reconstruction_ev_conscious_pct",
              "dwell_err_lo_ms", "dwell_err_hi_ms", "n_x_error_bar_segments"], rows, [
        PAGE_NOTE + ", panel c",
        "Conscious-face reconstruction explained variance in state 1 (%) vs achieved mean HMM dwell time (ms), for the recorded data (red #cc2929) and the averaging model (blue #2970bf)",
        "point coordinates from the 9-vertex stroke polylines (markers coincide to < 0.05 pt); self_transition_p = the label printed next to each point, transcribed by eye from a 300-dpi render (9 labels per series found as glyph outlines, one per point, in the same left-to-right order)",
        "dwell_err_lo/hi = extent of the small horizontal error bar drawn through each point (0.5-pt strokes of the series colour), about +/-0.1 to +/-3 ms; no vertical error bars are drawn",
        "x axis: 7 tick marks calibrated to 0..300 ms (resid %.1e); y axis: 5 tick marks calibrated to 45..65 %% (resid %.1e)" % (xax.resid, yax.resid),
    ])
pp.render(page, clip, 300, os.path.join(OUT, "edfig10c_orig.png"))
