"""Extract Fig. 1a (and, via fig1b_extract.py, Fig. 1b) of Pesce et al. 2022 (Commun Biol 5:447): autofluorescence
(mean + SD bars, 20 individual ROI values per bar) of 7 (a) / 6 (b) treatments at 4 excitation wavelengths.

Source of the numbers (tier 2): in the published main PDF (p. 3) the bars, error bars, points and asterisks of
Fig. 1a/b are one 300-ppi raster image (only the axes, tick marks, tick labels and group labels are vector).
The authors' point-by-point response in the Peer Review File (source/pesce2022_peer_review.pdf, p. 21)
reproduces the same figure as VECTOR graphics: each bar is a 4-point open stroke (BL, BR, TR, TL) in the series
colour, each error bar a vertical 2-point stroke from the bar top up to a short horizontal cap (mean + SD, no
lower whisker), each data point a translucent (alpha 0.2) black circle 'fill' path (49 flattened points), and the
significance stacks are tiny embedded raster images (4 distinct xrefs = 1, 2, 4, 4 asterisks; counted from their
soft masks). Values are read from that copy and CHECKED against the published raster: the published panel's own
vector tick labels/marks give its axis calibration, the extracted bar tops / SD ends are drawn over a 600-dpi
render of the published panel, and the bar-top and SD-cap rows of the published raster are measured per bar
(series-colour mask) and compared with the prediction.

    python3 -I -B fig1a_extract.py  -> fig1a.csv, ../work/agent_bars/fig1a_overlay.png (vector copy, 300 dpi),
                                       ../work/agent_bars/fig1a_overlay_published.png (published raster, 600 dpi)
fig1b_extract.py imports extract() from this file and runs it with panel="b".
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * i))) for i in range(1, 6)]:
    if os.path.exists(os.path.join(_d, "tools", "digitize_common.py")):  # the collection's shared tools/, wherever this folder sits
        sys.path.insert(0, os.path.join(_d, "tools")); break
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
import pdfplot as pp  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, ".."))
PR_PDF = os.path.join(ROOT, "source", "pesce2022_peer_review.pdf")
MAIN_PDF = os.path.join(ROOT, "source", "pesce2022.pdf")
WORK = os.path.join(ROOT, "work", "agent_bars")

SERIES = {"#0000ff": 405, "#00ff00": 488, "#ff8000": 561, "#ff0000": 638}   # stroke colour -> excitation (nm)
ASTERISK_IMAGES = {70: 4, 72: 4, 74: 1, 76: 2}   # xref of the asterisk-stack image (Peer Review p. 21) -> count
PANELS = {
    "a": dict(pr_clip=pp.R(100, 270, 362, 476), pub_clip=pp.R(85, 50, 362, 282), pub_page=3,
              groups=["SHIELD", "SWITCH", "0.6% H2O2", "15% H2O2", "30% H2O2", "AR", "25% Quadrol"]),
    "b": dict(pr_clip=pp.R(100, 476, 362, 700), pub_clip=pp.R(85, 282, 362, 495), pub_page=3,
              groups=["6 mM Ascorbic Acid", "20 mM Hydroquinone", "SB", "0.1% NaBH4", "1 mM CuSO4", "10 mM CuSO4"]),
}


def y_axis(spans, draws):
    """Linear y axis from the '<m>x10' + '<exponent>' tick-label span pairs and the major tick marks beside them."""
    pairs, used = [], []
    for s in spans:
        t = s["text"].strip()
        if s["dir"] != (1.0, 0.0) or not re.fullmatch(r"\d(,\d)?x10", t):
            continue
        ex = [e for e in spans if abs(e["bbox"][0] - s["bbox"][2]) < 1.0 and abs(e["cy"] - s["cy"]) < 4
              and re.fullmatch(r"\d", e["text"].strip())]
        assert len(ex) == 1, (t, [e["text"] for e in ex])
        val = float(t[:-3].replace(",", ".")) * 10 ** int(ex[0]["text"])
        ticks = [g for g in pp.segments(draws, orientation="h", max_len=6, min_len=2.5)
                 if pp.hexcolor(g["color"]) == "#000000" and abs((g["y0"] + g["y1"]) / 2 - s["cy"]) < 3
                 and s["bbox"][2] - 1 < min(g["x0"], g["x1"]) < s["bbox"][2] + 12]
        assert len(ticks) == 1, (t, ticks)
        pairs.append(((ticks[0]["y0"] + ticks[0]["y1"]) / 2, val))
        used.append(t + "^" + ex[0]["text"])
    ax = pp.Axis(pairs)
    return ax, used


def x_ticks(draws, axis_y):
    """x positions of the short vertical tick marks hanging below the x-axis line at axis_y."""
    t = [(g["x0"] + g["x1"]) / 2 for g in pp.segments(draws, orientation="v", max_len=6, min_len=2.5)
         if abs(min(g["y0"], g["y1"]) - axis_y) < 0.3]
    return sorted(t)


def extract(panel):
    P = PANELS[panel]
    page = pp.open_page(PR_PDF, 21)
    clip = P["pr_clip"]
    spans = pp.text_spans(page, clip)
    draws = pp.drawings(page, clip)
    yax, labels = y_axis(spans, draws)
    print(f"[{panel}] vector-copy y axis from {labels}: {yax}")

    # bars: open 4-point strokes (bottom-left, bottom-right, top-right, top-left) in a series colour
    bars = []
    for d in draws:
        if d["kind"] == "stroke" and len(d["points"]) == 4 and pp.hexcolor(d["color"]) in SERIES:
            (x0, y0), (x1, y1), (x2, y2), (x3, y3) = d["points"]
            assert abs(y0 - y1) < 0.02 and abs(y2 - y3) < 0.02 and abs(x0 - x3) < 0.02 and abs(x1 - x2) < 0.02, d["points"]
            bars.append(dict(ex=SERIES[pp.hexcolor(d["color"])], xl=x0, xr=x1, xc=(x0 + x1) / 2, ytop=y2, ybot=y0,
                             points=[], ast=0, ycap=None))
    bars.sort(key=lambda b: b["xc"])
    axis_y = bars[0]["ybot"]
    assert all(abs(b["ybot"] - axis_y) < 0.02 for b in bars)
    # error bars: horizontal cap (2-point stroke, series colour) at the top of a vertical line from the bar top
    for d in draws:
        if d["kind"] == "stroke" and len(d["points"]) == 2 and pp.hexcolor(d["color"]) in SERIES:
            (x0, y0), (x1, y1) = d["points"]
            if abs(y0 - y1) < 0.02 and 1.0 < abs(x1 - x0) < 3.0:        # cap (the left bar edge and the whisker are vertical)
                b = min(bars, key=lambda b: abs(b["xc"] - (x0 + x1) / 2))
                assert abs(b["xc"] - (x0 + x1) / 2) < 0.3 and b["ex"] == SERIES[pp.hexcolor(d["color"])]
                assert b["ycap"] is None
                b["ycap"] = y0
    for b in bars:
        assert b["ycap"] is not None, b
        whisk = [d for d in draws if d["kind"] == "stroke" and len(d["points"]) == 2
                 and SERIES.get(pp.hexcolor(d["color"])) == b["ex"]            # (a black x tick sits at each bar centre too)
                 and abs(d["points"][0][0] - b["xc"]) < 0.3 and abs(d["points"][1][0] - b["xc"]) < 0.3]
        assert len(whisk) == 1, (b, len(whisk))
        ys = sorted(p[1] for p in whisk[0]["points"])
        assert abs(ys[0] - b["ycap"]) < 0.05 and abs(ys[1] - b["ytop"]) < 0.05, (b, ys)
        b["mean"] = yax(b["ytop"])
        b["sd"] = yax(b["ycap"]) - b["mean"]
    # groups: clusters of bar centres separated by a wider gap (one empty tick slot between groups)
    gaps = np.diff([b["xc"] for b in bars])
    cut = np.where(gaps > 1.5 * np.median(gaps))[0]
    assert len(cut) + 1 == len(P["groups"]), (len(cut) + 1, gaps)
    gi = 0
    for i, b in enumerate(bars):
        if i > 0 and (i - 1) in cut:
            gi += 1
        b["group_index"], b["group"] = gi, P["groups"][gi]
    for gi, name in enumerate(P["groups"]):
        gb = [b for b in bars if b["group_index"] == gi]
        assert [b["ex"] for b in gb] == [405, 488, 561, 638], gb
        lab = [s["text"].strip() for s in spans if "Bold" in s["font"] and s["cy"] > axis_y
               and gb[0]["xl"] - 8 < s["cx"] < gb[-1]["xr"] + 8]
        print(f"[{panel}] group {gi} '{name}': bars x {gb[0]['xl']:.1f}-{gb[-1]['xr']:.1f}, label spans there: {lab}")
    # individual points: translucent black circles (49 flattened points), assigned to the nearest bar centre
    dxs = []
    for d in draws:
        if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#000000" and len(d["points"]) == 49:
            r = d["rect"]
            cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
            b = min(bars, key=lambda b: abs(b["xc"] - cx))
            dxs.append(abs(b["xc"] - cx))
            b["points"].append((cx, cy, yax(cy)))
    print(f"[{panel}] {sum(len(b['points']) for b in bars)} points; |dx| from bar centre: max {max(dxs):.2f} pt, "
          f"bar half-width {(bars[0]['xr'] - bars[0]['xl']) / 2:.2f} pt, bar pitch {np.median(gaps):.2f} pt")
    for b in bars:
        b["points"].sort(key=lambda p: p[0])
        if len(b["points"]) != 20:
            print(f"[{panel}] NOTE: {b['group']} {b['ex']} nm has {len(b['points'])} points (caption: n = 20)")
    # significance stacks: embedded images, assigned to the nearest bar centre
    for info in page.get_image_info(xrefs=True):
        x0, y0, x1, y1 = info["bbox"]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if not (clip.x0 < cx < clip.x1 and clip.y0 < cy < clip.y1):
            continue
        b = min(bars, key=lambda b: abs(b["xc"] - cx))
        assert abs(b["xc"] - cx) < 2.0 and cy < b["ytop"], (info, b["group"], b["ex"])   # stack sits above the bar
        assert b["ast"] == 0
        b["ast"] = ASTERISK_IMAGES[info["xref"]]

    # ---- check against the published raster (main PDF p. 3) through the published panel's vector axes
    pub = pp.open_page(MAIN_PDF, P["pub_page"])
    pclip = P["pub_clip"]
    pspans, pdraws = pp.text_spans(pub, pclip), pp.drawings(pub, pclip)
    pyax, plabels = y_axis(pspans, pdraws)
    print(f"[{panel}] published y axis from {plabels}: {pyax}")
    long_h = [g for g in pp.thin_segments(pdraws) if g["orient"] == "h" and g["len"] > 150 and pp.hexcolor(g["color"]) == "#000000"]
    assert len(long_h) == 1, long_h
    p_axis_y = long_h[0]["y0"]
    vt, pt = x_ticks(draws, axis_y), x_ticks(pdraws, p_axis_y)
    assert len(vt) == len(pt), (len(vt), len(pt))
    for b in bars:        # each bar sits on one tick of the categorical x axis
        k = int(np.argmin([abs(t - b["xc"]) for t in vt]))
        assert abs(vt[k] - b["xc"]) < 0.3, (b["xc"], vt[k])
        b["slot"] = k
        b["pub_xc"] = pt[k]
    print(f"[{panel}] {len(vt)} x tick slots in both versions; bars occupy slots {[b['slot'] for b in bars]}")
    dpi = 600
    z = dpi / 72
    img = Image.open(_render(pub, pclip, dpi, os.path.join(WORK, f"fig1{panel}_pub_{dpi}.png"))).convert("RGB")
    a = np.asarray(img).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    masks = {405: (B > 150) & (R < 110) & (G < 110), 488: (G > 150) & (R < 110) & (B < 110),
             561: (R > 180) & (G > 80) & (G < 190) & (B < 90), 638: (R > 180) & (G < 90) & (B < 90)}
    px = lambda x: (x - pclip.x0) * z   # noqa: E731
    py = lambda y: (y - pclip.y0) * z   # noqa: E731
    dr = ImageDraw.Draw(img)
    diffs = []
    base = int(round(py(p_axis_y)))
    for b in bars:
        xc = px(b["pub_xc"])
        ytop_pred = py(pyax.inv(b["mean"]))
        ycap_pred = py(pyax.inv(b["mean"] + b["sd"]))
        M = masks[b["ex"]]
        # bar outline edges: coloured columns 2 pt above the baseline, within +-4 pt of the slot centre
        c0 = int(xc - 4 * z)
        cols = np.where(M[base - int(2 * z) - 3:base - int(2 * z) + 4, c0:int(xc + 4 * z)].any(0))[0] + c0
        runs = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1)
        assert len(runs) >= 2, (b["group"], b["ex"], runs)
        gap = int(1.5 * z)                                # tolerate gaps where a point's outline crosses the line

        def run_top(col, k0):
            """Walk up the coloured column `col` (index 0 = baseline row) from k0; the top of the run."""
            k, last = k0, k0
            while k < len(col):
                if col[k]:
                    last = k
                elif k - last > gap:
                    break
                k += 1
            return last

        edge_tops = []
        for run in (runs[0], runs[-1]):                 # left and right edge of the hollow bar
            c = int(round(run.mean()))
            col = M[:base, c - 2:c + 3].any(1)[::-1]     # coloured rows, counted up from the baseline
            edge_tops.append(base - 1 - run_top(col, 0))
        ytop_outer = np.mean(edge_tops)
        ytop_meas = ytop_outer + 0.3 * z                  # outer top of the ~0.6 pt outline -> its centre line
        # SD whisker + cap: walk up the centre column from the bar top
        colc = M[:base, int(xc) - 4:int(xc) + 5].any(1)[::-1]
        ycap_meas = base - 1 - run_top(colc, int(base - 1 - ytop_outer)) + 0.3 * z
        b["chk_top_px"] = (ytop_meas - ytop_pred) / (z / 300 * 72)   # in native 300-ppi pixels of the raster
        b["chk_cap_px"] = (ycap_meas - ycap_pred) / (z / 300 * 72)
        diffs.append((b["chk_top_px"], b["chk_cap_px"]))
        dr.line([(xc - 14, ytop_pred), (xc + 14, ytop_pred)], fill=(255, 0, 255), width=2)
        dr.line([(xc - 8, ycap_pred), (xc + 8, ycap_pred)], fill=(0, 200, 255), width=2)
        for cx, cy, v in b["points"]:
            X, Y = xc + (cx - b["xc"]) * z, py(pyax.inv(v))
            dr.ellipse([X - 4, Y - 4, X + 4, Y + 4], outline=(255, 0, 255), width=1)
        dr.text((xc - 6, ycap_pred - 60 - 12 * b["ast"]), str(b["ast"]), fill=(0, 120, 0))
    img.save(os.path.join(WORK, f"fig1{panel}_overlay_published.png"))
    d = np.array(diffs)
    unit_per_px = abs(pyax.slope) * 72 / 300
    print(f"[{panel}] published-raster check, measured - predicted (native 300-ppi px): bar top mean {np.nanmean(d[:, 0]):+.2f}, "
          f"max |.| {np.nanmax(np.abs(d[:, 0])):.2f}; SD cap mean {np.nanmean(d[:, 1]):+.2f}, max |.| {np.nanmax(np.abs(d[:, 1])):.2f}; "
          f"1 px = {unit_per_px:.2f} A.U.")
    worst = sorted(bars, key=lambda b: -max(abs(b["chk_top_px"]), abs(b["chk_cap_px"])))[:3]
    for b in worst:
        print(f"    worst: {b['group']} {b['ex']} nm: top {b['chk_top_px']:+.2f} px, cap {b['chk_cap_px']:+.2f} px")

    # ---- overlay on the vector copy itself (300 dpi)
    dpi2 = 300
    z2 = dpi2 / 72
    img2 = Image.open(_render(page, clip, dpi2, os.path.join(WORK, f"fig1{panel}_pr_{dpi2}.png"))).convert("RGB")
    d2 = ImageDraw.Draw(img2)
    for b in bars:
        X = (b["xc"] - clip.x0) * z2
        for yy, col, w in ((b["ytop"], (255, 0, 255), 8), (b["ycap"], (0, 200, 255), 5)):
            Y = (yy - clip.y0) * z2
            d2.line([(X - w, Y), (X + w, Y)], fill=col, width=2)
        for cx, cy, v in b["points"]:
            X, Y = (cx - clip.x0) * z2, (cy - clip.y0) * z2
            d2.ellipse([X - 3, Y - 3, X + 3, Y + 3], outline=(255, 0, 255), width=1)
    img2.save(os.path.join(WORK, f"fig1{panel}_overlay.png"))

    # ---- CSV
    header = ["row_type", "group", "group_index", "excitation_nm", "mean", "sd", "n_points", "asterisks", "point_index", "value"]
    rows = []
    for b in bars:
        rows.append(["bar", b["group"], b["group_index"], b["ex"], f"{b['mean']:.2f}", f"{b['sd']:.2f}", len(b["points"]), b["ast"], "", ""])
    for b in bars:
        for i, (cx, cy, v) in enumerate(b["points"]):
            rows.append(["point", b["group"], b["group_index"], b["ex"], "", "", "", "", i, f"{v:.2f}"])
    n_missing = [f"{b['group']} {b['ex']} nm ({len(b['points'])})" for b in bars if len(b["points"]) != 20]
    extra = {"a": ["The blue bracket under SHIELD and the red bracket under SWITCH ... 25% Quadrol mark the two tissue-transformation",
                   "  protocols (SHIELD vs SWITCH); all treatments except SHIELD were applied to SWITCH-processed slices."],
             "b": ["All six treatments in b are on SWITCH-processed slices (vertical 'SWITCH' label at the x axis).",
                   "The y axis line starts below the 1x10^2 tick (at about 30 A.U.), so the bars are drawn from that baseline."]}[panel]
    comments = [
        f"Pesce et al. 2022 Commun Biol 5:447, Fig. 1{panel}: autofluorescence (A.U.) of processed human cortex slices for",
        f"  {len(P['groups'])} treatment groups x 4 excitation wavelengths (405, 488, 561, 638 nm); mean + SD bars and the individual",
        "  ROI values (n = 20 ROIs of 20x500 um^2 per bar, per the caption and the authors' response to reviewer 1).",
        "Columns: row_type = 'bar' or 'point'; group = treatment as printed on the x axis (subscripts flattened: H2O2, NaBH4,",
        "  CuSO4); group_index = 0-based position along the x axis; excitation_nm = series (legend 405/488/561/638);",
        "  bar rows: mean, sd (A.U.; the error bar is drawn upward only, mean to mean+SD), n_points = number of individual",
        "  points found for that bar, asterisks = number of '*' printed above the bar (0 = none; caption: *P<0.05, **P<0.01,",
        "  ***P<0.001, ****P<0.0001, Mann-Whitney test, SWITCH vs SHIELD and each treatment vs classic SWITCH);",
        "  point rows: point_index (0-based, left to right within the bar's horizontal jitter) and value (A.U.).",
        "Provenance: tier 2, vector paths in the Peer Review File's copy of Fig. 1 (source/pesce2022_peer_review.pdf p. 21),",
        "  exact up to the PDF's precision (about 0.01 pt = 0.04 A.U.), checked against the published raster of the main PDF",
        "  (p. 3): the published panel's own vector tick labels/marks calibrate it; measured bar-top and SD-cap rows of the",
        f"  published 300-ppi raster differ from the prediction by at most {np.nanmax(np.abs(d)):.1f} native px (= {np.nanmax(np.abs(d)) * unit_per_px:.1f} A.U.)",
        f"  across all {len(bars)} bars (fig1{panel}_extract.py, overlay fig1{panel}_overlay_published.png). The published raster also",
        "  draws the points as open circles instead of translucent discs; their positions coincide on the overlay.",
        f"y axis calibration (both versions): 7 labelled major ticks 1x10^2 ... 7x10^2, linear; max residual {yax.resid:.3g} A.U.",
        f"  (vector copy), {pyax.resid:.3g} A.U. (published). x axis is categorical: 4 bars per group on consecutive tick slots.",
        "Asterisk counts come from the Peer Review copy (4 distinct tiny images, 1/2/4 asterisks, counted from their soft masks)",
        "  and were compared by eye with the published raster. Bars with 0 asterisks have no mark printed.",
    ] + ([f"Point count differs from 20 for: {', '.join(n_missing)} (the missing point is not drawn in either version)."] if n_missing else []) + extra
    pp.write_csv(os.path.join(HERE, f"fig1{panel}.csv"), header, rows, comments)
    print(f"[{panel}] wrote fig1{panel}.csv: {len(bars)} bars, {sum(len(b['points']) for b in bars)} points")
    return bars


def _render(page, clip, dpi, out):
    pp.render(page, clip, dpi, out)
    return out


if __name__ == "__main__":
    extract("a")
