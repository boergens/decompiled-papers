"""Digitize Figure 2c of He et al. 2018 (Sci Rep 8:12985), main PDF p.5: 15 small bar charts.

Source: the embedded raster image of Figure 2 (1650 x 1820 px, ~300 ppi), panel c in its lower third.
Each mini chart (one per primary beam energy, 0.8-2.2 keV) has four bars (blue, red, green, purple)
and faint unlabelled horizontal gridlines (major and minor); the shared axes are 'Depth (nm)' and 'Relative intensity'
without numbers. Bars are found as connected components of the four bar colours; gridlines as rows
of light-grey pixels in a strip just left of each chart's bars.
    python3 -I fig2c_extract.py   -> fig2c.csv (+ ../work/fig2c_overlay.png for checking)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/admin/ephemeral/oct_17_papers/he2018/tools")
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from digitize_common import embedded_image, write_csv, overlay  # noqa: E402

PDF = os.path.join(HERE, "../source/he2018.pdf")
a = embedded_image(PDF, 5)
assert a.shape == (1820, 1650, 3), a.shape
ai = a.astype(int)
Y0, Y1 = 1150, 1760                     # panel c
COLOURS = {  # Excel default palette, as measured in the image (RGB)
    "blue": (76, 129, 188), "red": (192, 80, 77), "green": (155, 187, 89), "purple": (128, 100, 162)}
ENERGIES = [["0.8", "0.9", "1.0", "1.1", "1.2"], ["1.3", "1.4", "1.5", "1.6", "1.7"],
            ["1.8", "1.9", "2.0", "2.1", "2.2"]]
# depth layer of each bar colour, from the caption of Fig. 2a / the colour key of panel a
LAYER = {"blue": "0-12.5 nm", "red": "12.5-25 nm", "green": "25-37.5 nm", "purple": "37.5-50 nm"}

bars = []
for name, rgb in COLOURS.items():
    d = np.abs(ai - np.array(rgb)).max(2)
    m = (d < 30).astype(np.uint8)
    m[:Y0] = 0
    m[Y1:] = 0
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 60 or w < 20:          # specks; legend-free figure, so every large blob is a bar
            continue
        # bar edges: rows/columns where at least half the bar width/height is filled
        sub = (lab[y:y + h, x:x + w] == i)
        rows = np.where(sub.mean(1) >= 0.5)[0]
        cols = np.where(sub.mean(0) >= 0.5)[0]
        bars.append(dict(colour=name, x0=x + cols[0], x1=x + cols[-1] + 1, top=y + rows[0], bottom=y + rows[-1] + 1))
print(len(bars), "bars")
assert len(bars) == 60, [(b["colour"], b["x0"], b["top"]) for b in bars]

# group into 3 rows x 5 columns of charts
bars.sort(key=lambda b: b["bottom"])
rows_of = [bars[i * 20:(i + 1) * 20] for i in range(3)]
out, pts = [], []
g = ai.mean(2)
for r, rb in enumerate(rows_of):
    rb.sort(key=lambda b: b["x0"])
    for c in range(5):
        cb = rb[c * 4:(c + 1) * 4]
        assert [b["colour"] for b in cb] == ["blue", "red", "green", "purple"], [b["colour"] for b in cb]
        base = float(np.median([b["bottom"] for b in cb]))
        # gridlines in a strip left of the blue bar (inside the chart's plot area)
        xs0, xs1 = cb[0]["x0"] - 28, cb[0]["x0"] - 4
        yr0, yr1 = int(base) - 74, int(base) + 4      # the gridded box is ~67 px tall; titles start above it
        prof = g[yr0:yr1, xs0:xs1].mean(1)
        # gridlines are local minima of the mean grey level: major ones darker (~230-245), minor ones fainter (~246-251)
        mins = [i for i in range(1, len(prof) - 1) if 215 < prof[i] < 252 and prof[i] <= prof[i - 1] and prof[i] <= prof[i + 1]]
        mins = [i for k, i in enumerate(mins) if k == 0 or i - mins[k - 1] > 2]   # a flat 2-row minimum counts once
        lines = []
        for i in mins:
            # sub-pixel centre: grey-level-weighted mean of the 3 rows around the minimum
            w = 255 - prof[i - 1:i + 2]
            lines.append((yr0 + i - 1 + float((w * np.arange(3)).sum() / w.sum()), prof[i]))
        lo, hi = min(v for _, v in lines), max(v for _, v in lines)
        lines = [(y, v < (lo + hi) / 2) for y, v in lines]        # darker half = major gridlines
        major = [y for y, mj in lines if mj]
        minor = [y for y, mj in lines if not mj]
        top = major[0]
        maj_sp = float(np.median(np.diff(major)))
        min_sp = float(np.median(np.diff(sorted(major + minor))))
        assert abs(major[-1] - base) < 3, (ENERGIES[r][c], major, base)
        for b in cb:
            h_px = base - b["top"]
            out.append((ENERGIES[r][c], b["colour"], LAYER[b["colour"]], (b["x0"] + b["x1"]) / 2, h_px,
                        h_px / (base - top), h_px / maj_sp, h_px / min_sp, len(major), len(minor), maj_sp, min_sp))
            pts += [(x, b["top"]) for x in range(b["x0"], b["x1"])] + [(x, base) for x in range(b["x0"], b["x1"])]
        pts += [(x, y) for y in major + minor for x in range(xs0, xs1, 2)]
overlay(a[Y0:Y1], [(x, y - Y0) for x, y in pts], os.path.join(HERE, "../work/fig2c_overlay.png"))

write_csv(os.path.join(HERE, "fig2c.csv"), [
    "He et al. 2018 Sci Rep 8:12985, Figure 2c: 'Corresponding intensity profiles for cuboids shown in (b)', one small",
    "  bar chart per primary beam energy (0.8-2.2 keV, 0.1 keV steps). Shared axes: 'Relative intensity' (y, no numbers) and",
    "  'Depth (nm)' (x, no numbers). Each chart has 4 bars; their colours match the four cuboids of Fig. 2a (blue 0-12.5 nm,",
    "  red 12.5-25 nm, green 25-37.5 nm, purple 37.5-50 nm, from the colour key of panel a).",
    "Columns: energy_keV (chart title); colour; layer (depth range of that cuboid, from panel a); bar_centre_px (x of the",
    "  bar centre in the source image, for ordering only); height_px = bar height in source pixels above the chart's",
    "  baseline (its bottom major gridline); height_frac = height as fraction of the chart's gridded box (0 = bottom,",
    "  1 = top major gridline); height_major / height_minor = height in units of the chart's major / minor gridline",
    "  spacing; n_major, n_minor = number of major (darker) and minor (fainter) unlabelled gridlines; major_px, minor_px",
    "  = their median spacing in source pixels.",
    "  The charts have no y numbers. Charts 0.8-1.4 keV have 2 major gridlines (one major interval of ~67 px, 5 minor",
    "  steps); charts 1.5-2.2 keV have 3 (two major intervals of ~33.5 px). If the major gridline step is the same",
    "  quantity in all charts, the y scale of the 1.5-2.2 keV charts is half that of the others; the figure does not",
    "  say, so heights are given both in pixels and in gridline units.",
    "Provenance: tier 3, digitized from the embedded raster image (no vector data in the PDF) by fig2c_extract.py.",
    "Uncertainty: +-1 px in height_px (about +-0.01-0.02 in height_frac).",
], ["energy_keV", "colour", "layer", "bar_centre_px", "height_px", "height_frac", "height_major",
    "height_minor", "n_major", "n_minor", "major_px", "minor_px"], out, fmt="{:.4g}")
print("wrote fig2c.csv", len(out), "rows")
