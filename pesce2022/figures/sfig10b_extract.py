"""Extract Supplementary Fig. 10b of Pesce et al. 2022 (supplement p. 11): tortuosity (d/D) of N = 6 SST branches
post-clearing (grey squares) vs after stripping (red squares), pairs joined by lines; 'N.S.' bracket.

Tier 2: vector paths. The squares are 2.9-pt filled rectangles (grey #515151 at the 'Post-clearing' tick, red
#f14040 at the 'Stripping' tick); each pairing line is a 2-point black stroke drawn between the two square centres
and trimmed at the square edges, so each line end is matched to the nearest square centre in y. y axis from the
tick labels '1,00' ... '1,25' and the major tick marks.

    python3 -I -B sfig10b_extract.py  -> sfig10b.csv, ../work/agent_bars/sfig10b_overlay.png
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
CLIP = pp.R(335, 215, 525, 350)
COL = {"#515151": "post_clearing", "#f14040": "stripping"}


def main():
    page = pp.open_page(PDF, 11)
    spans, draws = pp.text_spans(page, CLIP), pp.drawings(page, CLIP)
    yax, used = y_axis(spans, draws, tick_min_len=1.8)
    print("y axis from", used, yax)
    sq = {"post_clearing": [], "stripping": []}
    for d in draws:
        if d["kind"] == "fillstroke" and pp.hexcolor(d["fill"]) in COL and not d["has_curves"]:
            r = d["rect"]
            assert 2.5 < r[2] - r[0] < 3.5 and 2.5 < r[3] - r[1] < 3.5, r
            sq[COL[pp.hexcolor(d["fill"])]].append(((r[0] + r[2]) / 2, (r[1] + r[3]) / 2))
    assert len(sq["post_clearing"]) == 6 and len(sq["stripping"]) == 6, {k: len(v) for k, v in sq.items()}
    xg = sum(p[0] for p in sq["post_clearing"]) / 6
    xr = sum(p[0] for p in sq["stripping"]) / 6
    # x tick labels under the two columns
    for x, name in ((xg, "post_clearing"), (xr, "stripping")):
        lab = [s["text"].strip() for s in spans if s["cy"] > 332 and abs(s["cx"] - x) < 25 and s["size"] > 7]
        print(f"column {name} at x={x:.1f}: visible labels {lab}")
    # pairing lines: black 2-point strokes that run from near the grey column to near the red column
    lines = []
    for d in draws:
        if d["kind"] == "stroke" and len(d["points"]) == 2 and pp.hexcolor(d["color"]) == "#000000":
            (x0, y0), (x1, y1) = sorted(d["points"])
            if abs(x0 - xg) < 4 and abs(x1 - xr) < 4 and x1 - x0 > 50:
                lines.append(((x0, y0), (x1, y1)))
    assert len(lines) == 6, len(lines)
    pairs, usedg, usedr = [], set(), set()
    for (x0, y0), (x1, y1) in lines:
        # the line is trimmed at the square edges; extrapolate it back to the square centres' x
        slope = (y1 - y0) / (x1 - x0)
        yg_line, yr_line = y0 + slope * (xg - x0), y1 + slope * (xr - x1)
        ig = min(range(6), key=lambda i: abs(sq["post_clearing"][i][1] - yg_line))
        ir = min(range(6), key=lambda i: abs(sq["stripping"][i][1] - yr_line))
        dg, drr = abs(sq["post_clearing"][ig][1] - yg_line), abs(sq["stripping"][ir][1] - yr_line)
        assert dg < 0.5 and drr < 0.5 and ig not in usedg and ir not in usedr, (dg, drr, ig, ir)
        usedg.add(ig)
        usedr.add(ir)
        pairs.append((sq["post_clearing"][ig], sq["stripping"][ir]))
    pairs.sort(key=lambda p: p[0][1])          # by the post-clearing value, highest first (smallest y)
    rows = []
    for i, (g, r) in enumerate(pairs):
        rows.append([i, f"{yax(g[1]):.4f}", f"{yax(r[1]):.4f}"])
        print(f"pair {i}: post-clearing {yax(g[1]):.3f} -> stripping {yax(r[1]):.3f}")

    z = 300 / 72
    pp.render(page, CLIP, 300, os.path.join(WORK, "sfig10b_orig_300.png"))
    img = Image.open(os.path.join(WORK, "sfig10b_orig_300.png")).convert("RGB")
    dr = ImageDraw.Draw(img)
    for g, r in pairs:
        P = [((g[0] - CLIP.x0) * z, (g[1] - CLIP.y0) * z), ((r[0] - CLIP.x0) * z, (r[1] - CLIP.y0) * z)]
        dr.line(P, fill=(255, 0, 255), width=1)
        for X, Y in P:
            dr.ellipse([X - 7, Y - 7, X + 7, Y + 7], outline=(255, 0, 255), width=2)
    img.save(os.path.join(WORK, "sfig10b_overlay.png"))

    pp.write_csv(os.path.join(HERE, "sfig10b.csv"), ["pair_index", "post_clearing", "stripping"], rows, [
        "Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 10b (supplement p. 11): tortuosity (torsional index d/D, y axis",
        "  'Tortuosity') of N = 6 individual SST branches measured post-clearing (grey squares) and after stripping (red squares);",
        "  each row is one branch (the two values are joined by a line in the figure). Bracket 'N.S.' = not significant.",
        "Columns: pair_index (0-based, ordered by decreasing post-clearing value); post_clearing; stripping (dimensionless).",
        "Provenance: tier 2, vector paths in the PDF (square marker centres; pairing from the line segments, which join the",
        f"  square centres), exact up to the PDF's precision (0.01 pt = {0.01 * abs(yax.slope):.5f}). y axis calibrated on the 6",
        f"  labelled major ticks 1,00 ... 1,25 (linear); max residual {yax.resid:.2g}.",
        "Note: the PDF carries hidden text under white boxes: earlier x labels 'SST - Post Clearing' / 'SST - Post Stripping'",
        "  and a smaller 'Tortuosity'; the visible labels are 'Post-clearing' and 'Stripping'. The caption calls both image",
        "  sets 'red' ('post-clearing (red) and after stripping (red)'); in the figure the stripping images/markers are red and",
        "  the post-clearing markers grey.",
    ])
    print("wrote sfig10b.csv")


if __name__ == "__main__":
    main()
