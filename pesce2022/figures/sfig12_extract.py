"""Extract Supplementary Fig. 12 of Pesce et al. 2022 (supplement p. 13): "Signal retained" (signal/background) of
10 neurons per marker (CR green, SST yellow, NeuN red) acquired after staining, after 1 year, and after LSFM
bleaching; mean + SD bars, individual points, significance brackets ** (CR) and * (NeuN).

Tier 2: vector paths. Bars are filled rectangles (fill colour = marker, #404040 outline); whisker = vertical
#404040 stroke from the bar top to a horizontal cap (mean + SD upward only); points = translucent grey ellipse fills
(49 flattened points, 10.9 x 6.0 pt, alpha 0.45; the figure was scaled anisotropically). y axis from the tick
labels 0, 2, 4, 6, 8 and the major tick marks.

    python3 -I -B sfig12_extract.py  -> sfig12.csv, ../work/agent_bars/sfig12_overlay.png
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * i))) for i in range(1, 6)]:
    if os.path.exists(os.path.join(_d, "tools", "digitize_common.py")):  # the collection's shared tools/, wherever this folder sits
        sys.path.insert(0, os.path.join(_d, "tools")); break
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw  # noqa: E402
import pdfplot as pp  # noqa: E402
from sfig9_extract import y_axis  # noqa: E402

PDF = os.path.join(HERE, "..", "source", "pesce2022_supplement.pdf")
WORK = os.path.join(HERE, "..", "work", "agent_bars")
CLIP = pp.R(75, 75, 430, 255)
MARKER = {"#00ff00": "CR", "#eac429": "SST", "#ff0000": "NeuN"}
CONDITIONS = ["Acquisition after staining", "Acquisition after 1 year", "LSFM bleaching"]


def main():
    page = pp.open_page(PDF, 13)
    spans, draws = pp.text_spans(page, CLIP), pp.drawings(page, CLIP)
    yax, used = y_axis(spans, draws, tick_min_len=4)
    print("y axis from", used, yax)
    bars = []
    for d in draws:
        if d["kind"] == "fillstroke" and pp.hexcolor(d["fill"]) in MARKER:
            r = d["rect"]
            bars.append(dict(marker=MARKER[pp.hexcolor(d["fill"])], xl=r[0], xr=r[2], xc=(r[0] + r[2]) / 2, ytop=r[1], ybot=r[3],
                             ycap=None, points=[], sig=""))
    bars.sort(key=lambda b: b["xc"])
    assert [b["marker"] for b in bars] == ["CR"] * 3 + ["SST"] * 3 + ["NeuN"] * 3
    for i, b in enumerate(bars):
        b["condition"] = CONDITIONS[i % 3]
        lab = [s["text"].strip() for s in spans if "Bold" in s["font"] and s["cy"] > b["ybot"] and abs(s["cx"] - b["xc"]) < 12]
        print(f"bar {i} {b['marker']} '{b['condition']}': label spans below: {lab}")
    axis_y = bars[0]["ybot"]
    assert all(abs(b["ybot"] - axis_y) < 0.02 for b in bars)
    for d in draws:
        if d["kind"] == "stroke" and len(d["points"]) == 2 and pp.hexcolor(d["color"]) == "#404040":
            (x0, y0), (x1, y1) = d["points"]
            if abs(y0 - y1) < 0.02:                                   # cap
                b = min(bars, key=lambda b: abs(b["xc"] - (x0 + x1) / 2))
                assert abs(b["xc"] - (x0 + x1) / 2) < 0.5 and b["ycap"] is None
                b["ycap"] = y0
    for b in bars:
        whisk = [d for d in draws if d["kind"] == "stroke" and len(d["points"]) == 2 and pp.hexcolor(d["color"]) == "#404040"
                 and abs(d["points"][0][0] - b["xc"]) < 0.5 and abs(d["points"][1][0] - b["xc"]) < 0.5]
        assert len(whisk) == 1 and b["ycap"] is not None, b
        ys = sorted(p[1] for p in whisk[0]["points"])
        assert abs(ys[0] - b["ycap"]) < 0.05 and abs(ys[1] - b["ytop"]) < 0.05, (b, ys)
        b["mean"], b["sd"] = yax(b["ytop"]), yax(b["ycap"]) - yax(b["ytop"])
    dxs = []
    for d in draws:
        if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#404040" and len(d["points"]) == 49 and d["has_curves"]:
            r = d["rect"]
            cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
            b = min(bars, key=lambda b: abs(b["xc"] - cx))
            dxs.append(abs(cx - b["xc"]))
            b["points"].append((cx, cy, yax(cy)))
    print(f"points: max |dx| from bar centre {max(dxs):.1f} pt, bar half-width {(bars[0]['xr'] - bars[0]['xl']) / 2:.1f} pt, pitch "
          f"{bars[1]['xc'] - bars[0]['xc']:.1f} pt")
    # significance brackets: '*'-only text spans with a black bar line under them; they span the two bars below the line
    for s in spans:
        t = s["text"].strip()
        if t and set(t) == {"*"}:
            line = [d for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#000000" and not d["has_curves"]
                    and d["rect"][2] - d["rect"][0] > 20 and abs((d["rect"][0] + d["rect"][2]) / 2 - s["cx"]) < 10
                    and 0 < d["rect"][1] - s["cy"] < 15]
            assert len(line) == 1, (t, line)
            under = [b for b in bars if line[0]["rect"][0] - 3 < b["xc"] < line[0]["rect"][2] + 3]
            assert len(under) == 2, [b["marker"] + " " + b["condition"] for b in under]
            for b in under:
                b["sig"] = t
            print(f"bracket '{t}' over {[b['marker'] + ': ' + b['condition'] for b in under]}")
    for b in bars:
        b["points"].sort()
        print(f"{b['marker']} {b['condition']}: mean {b['mean']:.3f}, sd {b['sd']:.3f}, {len(b['points'])} points, sig '{b['sig']}'")

    z = 300 / 72
    pp.render(page, CLIP, 300, os.path.join(WORK, "sfig12_orig_300.png"))
    img = Image.open(os.path.join(WORK, "sfig12_orig_300.png")).convert("RGB")
    dr = ImageDraw.Draw(img)
    for b in bars:
        X = (b["xc"] - CLIP.x0) * z
        for yy, col, w in ((b["ytop"], (255, 0, 255), 30), (b["ycap"], (0, 200, 255), 18)):
            Y = (yy - CLIP.y0) * z
            dr.line([(X - w, Y), (X + w, Y)], fill=col, width=3)
        for cx, cy, v in b["points"]:
            X, Y = (cx - CLIP.x0) * z, (cy - CLIP.y0) * z
            dr.ellipse([X - 5, Y - 5, X + 5, Y + 5], outline=(255, 0, 255), width=2)
    img.save(os.path.join(WORK, "sfig12_overlay.png"))

    header = ["row_type", "marker", "condition", "mean", "sd", "n_points", "sig_bracket", "point_index", "value"]
    rows = [["bar", b["marker"], b["condition"], f"{b['mean']:.3f}", f"{b['sd']:.3f}", len(b["points"]), b["sig"], "", ""] for b in bars]
    for b in bars:
        rows += [["point", b["marker"], b["condition"], "", "", "", "", i, f"{v:.3f}"] for i, (cx, cy, v) in enumerate(b["points"])]
    pp.write_csv(os.path.join(HERE, "sfig12.csv"), header, rows, [
        "Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 12 (supplement p. 13): signal retained (signal/background, y axis",
        "  'Signal retained') of 10 neurons per marker acquired after immunostaining, re-acquired after 1 year in the sandwich",
        "  holder, and after LSFM bleaching; mean + SD bars (error bar upward only) and the individual values.",
        "Columns: row_type = 'bar' or 'point'; marker = CR (green bars, Alexa Fluor 488), SST (yellow, Alexa Fluor 568), NeuN (red,",
        "  Alexa Fluor 647), as labelled on the micrographs to the right; condition = bar label as printed; bar rows: mean, sd,",
        "  n_points, sig_bracket = significance mark of the bracket spanning this bar and its neighbour ('**' over CR after",
        "  staining vs after 1 year, '*' over NeuN after staining vs after 1 year; caption: P < 0.01 and P < 0.05, Mann-Whitney);",
        "  point rows: point_index (0-based, left to right) and value.",
        "Provenance: tier 2, vector paths in the PDF (bar rectangles, whisker/cap strokes, ellipse marker fills), exact up to the",
        f"  PDF's precision (0.01 pt = {0.01 * abs(yax.slope):.4f}). y axis calibrated on the 5 labelled major ticks 0 ... 8 (linear);",
        f"  max residual {yax.resid:.2g}. x axis categorical: 3 bars per marker.",
        "Note: the markers are ellipses (10.9 x 6.0 pt) because the chart was scaled anisotropically; their centres are used.",
    ])
    print("wrote sfig12.csv", len(rows), "rows")


if __name__ == "__main__":
    main()
