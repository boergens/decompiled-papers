"""Fig. 20 (p. 42): digitize panels (a) and (b) from the embedded raster (2138 x 850 px, native resolution).

Tier 3 (digitized). The authors' source data (Figure 20-source data 1-6) are not in the local collection.
Calibration: white gridlines on the grey plot background (x = 1..8 in (a); y = 0.1..0.9 in both panels) and, for the
log x axis of (b), the major and minor tick marks below the axis (1, 2, ..., 10, 20, ..., 100). Each series is traced
with a colour mask per pixel column (centre of the line); the legend boxes are blanked first. For (a) the plotted
polyline vertices at integer x are also read off the trace (mean of the columns within +-2 px of the x position).
Writes figures/fig20a.csv, figures/fig20b.csv and work/fig20a_overlay.png, work/fig20b_overlay.png.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import fc_dig as fd  # noqa: E402

a = fd.embedded(42)
SERIES = {"Threshold 1": (7, 115, 180), "Threshold 3": (204, 121, 168), "Threshold 5": (24, 159, 116),
          "Threshold 10": (213, 97, 40), "Threshold 20": (231, 160, 35)}

PANELS = {
    # name: plot box (x0, y0, x1, y1) in native px, legend box, log x?
    "a": dict(box=(66, 45, 1042, 790), legend=(760, 600, 1042, 760), log=False),
    "b": dict(box=(1168, 40, 2125, 790), ybot=781, legend=(1905, 595, 2125, 760), log=True),
}


def calib(p):
    x0, y0, x1, y1 = p["box"]
    ys = fd.white_lines(a, x0 + 5, x1 - 5, y0 + 5, y1 - 15, "h")
    ys = [y for y in ys if y > y0 + 40][:9]          # gridlines 0.9 ... 0.1 (top to bottom)
    fy, ry = fd.fit(ys, [0.9 - 0.1 * i for i in range(len(ys))])
    if not p["log"]:
        xs = fd.white_lines(a, x0 + 30, x1 + 2, y0 + 20, y1 - 20, "v")   # x = 1 .. 8
        fx, rx = fd.fit(xs, list(range(1, len(xs) + 1)))
        ticks = list(zip(xs, range(1, len(xs) + 1)))
    else:
        g = a.astype(int).min(axis=2)
        row = g[786, x0:x1] < 200                       # tick marks under the x axis (major and minor)
        cols, cur = [], []
        for i in np.where(row)[0]:
            if cur and i != cur[-1] + 1:
                cols.append(np.mean(cur)); cur = []
            cur.append(i)
        cols.append(np.mean(cur))
        cols = [x0 + c for c in cols]
        vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        cols = cols[-len(vals):] if len(cols) >= len(vals) else cols
        assert len(cols) == len(vals), cols
        fx, rx = fd.fit(cols, vals, log=True)
        ticks = list(zip(cols, vals))
    return fx, fy, rx, ry, ys, ticks


rows_all = {}
for name, p in PANELS.items():
    fx, fy, rx, ry, ygrid, ticks = calib(p)
    x0, y0, x1, y1 = p["box"]
    rows, ov = [], {}
    masks = {k: fd.blank(fd.colour_mask(a, c, 45), [p["legend"]]) for k, c in SERIES.items()}
    dm = fd.blank(fd.dark_mask(a, 80), [p["legend"]])
    masks["Human designed"] = dm
    for k, m in masks.items():
        if k == "Human designed":   # dotted line: one row per dot (connected component centroid)
            bl = fd.blobs(m, x0 + 2, y0 + 2, x1, y1 - 2, amin=4, amax=120)
            tr = [(b[0], b[1], b[1], b[1]) for b in sorted(bl)]
        else:
            tr = fd.trace(m, x0 + 2, x1, y0 + 2, p.get("ybot", y1 - 2), min_px=2)
        ov[k] = [(t[0], t[1]) for t in tr]
        for t in tr:
            rows.append(["trace", k, float(fx(t[0])), float(fy(t[1])), float(fy(t[3])), float(fy(t[2]))])
        if name == "a" and k != "Human designed":
            inv = fd.inverse(fx, x0, x1)
            for xv in range(0, 9):
                px = inv(xv)
                sel = [t[1] for t in tr if abs(t[0] - px) <= 2]
                if sel:
                    rows.append(["vertex", k, float(xv), float(fy(np.mean(sel))), "", ""])
    rows_all[name] = rows
    ox = max(0, x0 - 70)
    fd.overlay(a[:, ox:x1 + 15], {k: [(x - ox, y) for x, y in v] for k, v in ov.items()},
               HERE.parent / "work" / f"fig20{name}_overlay.png", r=1)
    hdr = [f"Fig. 20({name}) of Scheffer et al. 2020 (eLife 9:e57443), p. 42: 'Fraction of paths vs synaptic distance'.",
           "x = Number of interneurons needed" + (" (log axis, 1 to ~200)" if p["log"] else " (linear, 0 to 8)")
           + "; y = Fraction of all possible pairs connected (0 to 1).",
           "Provenance: tier 3, digitized from the embedded raster image (2138 x 850 px) by colour mask per pixel column;"
           " the authors' Figure 20-source data 1-6 (threshold 1, 3, 5, 10, 20 and human designed traces) were not available locally.",
           f"Calibration: y on {len(ygrid)} white gridlines 0.9..0.1 (max residual {ry:.4f});"
           + (f" x on the 19 major/minor tick marks 1..100 (log fit, max residual {rx:.4f} decades)." if p["log"]
              else f" x on the gridlines x = 1..8 (max residual {rx:.4f})."),
           "Uncertainty: about +-0.003 in y and +-0.01 in x (a)/+-0.003 decades (b) from one source pixel; lines are ~4 px wide."
           " Where lines overlap, the series drawn on top hides the others (missing columns).",
           "kind = trace: one row per pixel column (y = line centre, y_low/y_high = lower/upper edge of the line ink);"
           + (" kind = vertex: value read at integer x (the polyline vertices; x = 3 has a gridline but no printed tick label)." if not p["log"] else "")
           + " 'Human designed' is a dotted black line: one trace row per dot (centroid of the dot), y_low = y_high = y.",
           "Columns: kind, series (legend name), x, y, y_low, y_high."]
    fd.write_csv(HERE / f"fig20{name}.csv", hdr, ["kind", "series", "x", "y", "y_low", "y_high"], rows)
    print(name, "rx", rx, "ry", ry, len(rows))
