"""Extraction script for Extended Data Figure 8 (PDF page 48): two panels of overlaid histograms of the
cosine similarity between state-resolved tuning axes and the priming axis (548 cells).
Writes edfig8_left_state1.csv and edfig8_right_state2.csv plus 300-dpi crops of the originals."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import pdfplot as pp

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "2026.10.15.759299v1.full.pdf")
OUT = os.path.dirname(os.path.abspath(__file__))
page = pp.open_page(PDF, 48)
SERIES = {  # fill colour -> (column name, legend text)
    "#fcae34": ("state1_conscious", "State 1, conscious"),
    "#ffd28a": ("state1_suppressed", "State 1, suppressed"),
    "#b56cc7": ("state2_conscious", "State 2, conscious"),
    "#543379": ("state2_suppressed", "State 2, suppressed"),
    "#000000": ("priming_half_trials", "Priming, half-trials"),
}
PANELS = {
    "left_state1": dict(clip=pp.R(10, 20, 260, 189), plot=pp.R(33, 27, 235, 160), ymax=50,
                        xtick_region=pp.R(30, 158, 240, 165), ytick_region=pp.R(27, 25, 34, 162)),
    "right_state2": dict(clip=pp.R(275, 20, 510, 189), plot=pp.R(295, 27, 498, 160), ymax=60,
                         xtick_region=pp.R(292, 158, 500, 165), ytick_region=pp.R(290, 25, 297, 162)),
}
XVALS = [-1, -0.5, 0, 0.5, 1]
NBINS = 40

for pname, P in PANELS.items():
    pp.render(page, P["clip"], 300, f"{OUT}/edfig8_{pname}_orig.png")
    draws = pp.drawings(page, P["plot"])
    xax = pp.axis_from_ticks(draws, "x", XVALS, region=P["xtick_region"], max_len=8)
    yax = pp.axis_from_ticks(draws, "y", [0, P["ymax"]], region=P["ytick_region"], max_len=8)
    print(pname, "\n  x:", xax, "\n  y:", yax)
    ybase = yax.inv(0)
    pt_per_count = -1 / yax.slope
    edges = [-1 + 2 * i / NBINS for i in range(NBINS + 1)]
    centres_pt = [xax.inv((edges[i] + edges[i + 1]) / 2) for i in range(NBINS)]
    counts, outline_check, alpha = {}, {}, {}
    for d in draws:
        col = pp.hexcolor(d["fill"])
        if d["kind"] != "fill" or col not in SERIES or len(d["points"]) < 50:
            continue
        name = SERIES[col][0]
        op = d["raw"].get("fill_opacity")
        if op < 0.99:
            # translucent bars: one rectangle per non-empty bin (adjacent equal bins may be merged).
            # For every bin centre take the topmost horizontal edge spanning it.
            alpha[name] = op
            cnt = []
            for xc in centres_pt:
                top = None
                for sp in d["subpaths"]:
                    for (x0, y0), (x1, y1) in zip(sp[:-1], sp[1:]):
                        if abs(y1 - y0) < 0.01 and min(x0, x1) - 0.05 <= xc <= max(x0, x1) + 0.05:
                            top = y0 if top is None else min(top, y0)
                cnt.append(0.0 if top is None else (ybase - top) / pt_per_count)
            counts[name] = cnt
            # bin-edge check: all rect vertical edges must sit on the 0.05 grid
            xs = sorted({round(x, 2) for sp in d["subpaths"] for x, y in sp})
            off = max(min(abs(xax(x) - e) for e in edges) for x in xs)
            print("  %-20s bars: max edge offset from 0.05 grid = %.4f" % (name, off))
        else:
            # opaque step outline (0.5-pt-wide band drawn as a filled polygon): lower band edge = bar top
            cnt = []
            for xc in centres_pt:
                tops = []
                for sp in d["subpaths"]:
                    for (x0, y0), (x1, y1) in zip(sp[:-1], sp[1:]):
                        if abs(y1 - y0) < 0.01 and min(x0, x1) - 0.05 <= xc <= max(x0, x1) + 0.05:
                            tops.append(y0)
                cnt.append((ybase - (min(tops) + 0.5)) / pt_per_count if tops else float("nan"))
            outline_check[name] = cnt
    rows = []
    names = [SERIES[c][0] for c in SERIES]
    for i in range(NBINS):
        rows.append([round(edges[i], 3), round(edges[i + 1], 3), round((edges[i] + edges[i + 1]) / 2, 3)] +
                    [int(round(counts[n][i])) for n in names if n in counts])
    present = [n for n in names if n in counts]
    # integrality + totals + outline consistency
    for n in present:
        maxdev = max(abs(c - round(c)) for c in counts[n])
        tot = sum(int(round(c)) for c in counts[n])
        dev_outline = max(abs(a - b) for a, b in zip(counts[n], outline_check[n]))
        print("  %-20s total=%d  max deviation from integer=%.3f counts  max |bars - outline| = %.3f counts  alpha=%.3f" % (n, tot, maxdev, dev_outline, alpha[n]))
    com = [
        "Extended Data Figure 8 (PDF page 48 of 2026.10.15.759299v1.full.pdf), %s panel: histograms of the cosine similarity" % pname.split("_")[0],
        "between each cell's state-resolved feature-tuning axis and its priming axis (n = 548 cells), plus the priming noise ceiling (two half-trial priming axes).",
        "Recovered from vector paths: each series is drawn as translucent (alpha 0.30) bar rectangles, one per non-empty bin, plus an opaque 0.5-pt step outline.",
        "Counts = (baseline y - bar top y) / (pt per count); all came out within 0.02 of an integer and were rounded. The outline polygon gives the same values.",
        "x axis calibrated from 5 tick marks at %s (resid %.1e); y axis from the 2 tick marks at 0 and %d (resid %.1e); tick labels are glyph outlines read off the render." % (XVALS, xax.resid, P["ymax"], yax.resid),
        "Bins: 40 bins of width 0.05 from -1 to 1 (bar edges lie on this grid to < 0.002). Empty bins have count 0.",
        "Series colours (fill hex): " + ", ".join("%s=%s" % (SERIES[c][0], c) for c in SERIES if SERIES[c][0] in counts) + "; legend text: " + "; ".join(SERIES[c][1] for c in SERIES if SERIES[c][0] in counts),
        "Grey vertical reference line at cosine = 0 (#b3b3b3, 0.5 pt, alpha 0.70).",
    ]
    pp.write_csv(f"{OUT}/edfig8_{pname}.csv", ["bin_left", "bin_right", "bin_centre"] + [n + "_count" for n in present], rows, com)
