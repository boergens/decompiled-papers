"""Extended Data Fig. 4d: histograms of lost, partial and adjacent sectioning events (7 dpf series),
digitized from the 150 ppi raster image on PDF page 36 (tier 3). Writes edfig4d.csv + overlay in work/.

The events are sparse, so each separate bar (group of touching pixel columns) is read as one bin of
50 sections: z range of its columns, height = tallest column, value = height / (px per unit), rounded.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, fit_axis, overlay, write_csv  # noqa: E402
from histo_common import column_heights, group_bars, tick_centres  # noqa: E402

PDF = ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"
a = embedded_image(str(PDF), 36)
g = a.astype(float).mean(2)
ink = 255 - g

xt = [480 + t for t in tick_centres(ink[775, 480:975], 100)]
assert len(xt) == 7, xt
fx, resx, mx = fit_axis(xt, [0, 2500, 5000, 7500, 10000, 12500, 15000])

panels = {
    "lost": dict(axis=666, ticks=(648, 667), vals=[2, 1, 0], total=6),
    "partial": dict(axis=727, ticks=(700, 728), vals=[4, 3, 2, 1, 0], total=25),
    "adjacent": dict(axis=772, ticks=(760, 773), vals=[1, 0], total=6),
}
rows, pts, notes = [], [], []
for name, p in panels.items():
    tr = [p["ticks"][0] + t for t in tick_centres(ink[p["ticks"][0]:p["ticks"][1], 489], 100)]
    assert len(tr) == len(p["vals"]), (name, tr)
    fy, resy, my = fit_axis(tr, p["vals"])
    pxu = abs(1 / my)
    c0 = 496
    h = column_heights(g, p["axis"] - 1, c0, 955, thr=215)
    # bars are drawn ~1 px wide; light 1-px stubs beside them are anti-aliasing. A column belongs to a
    # bar if its pixels just above the axis are dark (< 150); touching dark columns form one run.
    dark = [hh > 0 and g[p["axis"] - 3:p["axis"] - 1, c0 + i].min() < 150 for i, hh in enumerate(h)]
    runs, cur = [], None
    for i, d in enumerate(dark):
        if d and cur and i == cur[1] + 1:
            cur[1] = i
        elif d:
            if cur:
                runs.append(cur)
            cur = [i, i]
        elif cur:
            runs.append(cur)
            cur = None
    if cur:
        runs.append(cur)
    n = 0
    for r0, r1 in runs:
        hh = h[r0:r1 + 1]
        w = r1 - r0 + 1
        units = [int(round(x / pxu)) for x in hh]
        if len(set(units)) == 1:  # flat run: one bin per ~1.5 px of width
            cnt = units[0] * max(1, int(round(w / abs(50 / mx))))
        else:  # stepped run: each column is its own bin
            cnt = sum(units)
        n += cnt
        z0, z1 = float(fx(c0 + r0 - 0.5)), float(fx(c0 + r1 + 0.5))
        flag = "run of %d columns, may hold more than one bin" % w if w > 1 else ""
        rows.append((name, round(z0, 1), round(z1, 1), round((z0 + z1) / 2, 1), w,
                     " ".join(str(int(x)) for x in hh), cnt, flag))
        pts += [(c0 + i, p["axis"] - h[i]) for i in range(r0, r1 + 1)]
    notes.append(f"{name}: {n} events in the digitized bars (the panel prints {p['total']}); "
                 f"y scale {pxu:.2f} px per section/bin, tick-fit residual {resy:.2f}")

hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Extended Data Fig. 4d: lost, partial and adjacent (lost-partial or",
    "partial-partial) events per bin of 50 sections along the 7dpf series (x: position in series, z).",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster image on PDF page 36 (figures/edfig4d_extract.py).",
    f"x calibrated on 7 ticks 0..15000 step 2500 (labels 0, 5000, 10000, 15000), max residual {resx:.1f} sections;",
    f"one pixel column = {abs(mx):.1f} sections, so the 50-section bin of a bar is known only to about +-1 bin (z_left..z_right).",
    "One row per bar (run of touching dark pixel columns): width_px, heights_px = bar height in each column, value = number of",
    "events read from the run (height / px per unit, rounded; a flat run wider than one bin counts one bin per ~1.5 px).",
    "Runs wider than one column may hold neighbouring bins that cannot be separated (flagged in 'note').",
] + notes + ["columns: series; z_left; z_right (z range of the run); z_centre; width_px; heights_px; value; note"]
write_csv(HERE / "edfig4d.csv", hdr, ["series", "z_left", "z_right", "z_centre", "width_px", "heights_px", "value", "note"], rows,
          fmt=["{}"] * 8)
(ROOT / "work").mkdir(exist_ok=True)
overlay(a, pts, str(ROOT / "work" / "edfig4d_overlay.png"))
print("\n".join(notes))
