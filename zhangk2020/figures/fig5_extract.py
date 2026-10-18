"""Fig. 5 (p. 7): outputs of the inside and the outside sensors vs time (50 nm command displacement).
Vector paths -> fig5.csv.

The two staircase traces are drawn as thick lines that were converted to many small filled
polygons and short strokes (about 1300 pieces per trace). For each 0.25 pt wide x bin the
script takes the lowest and highest vertex of all pieces of that colour (upper and lower edge
of the drawn line, including the vertical risers of the steps) and their mean.

Run: python3 -I -B figures/fig5_extract.py   (from any directory)
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import vec  # noqa: E402

HERE = Path(__file__).resolve().parent
PAGE, CLIP = 7, (140, 250, 455, 446)
RED, BLUE = (0.87, 0.03, 0.02), (0, 0, 0.83)
BIN = 0.25  # pt

ds = vec.drawings(PAGE, CLIP)
L, T, R, B = vec.frame(ds)
xt = vec.tick_rects(ds, "x", B)
ylt = vec.tick_rects(ds, "y", L)
yrt = vec.tick_rects(ds, "y", R)
# time: 5 s per tick interval; origin (t = 0) at the left frame line (the axis has no numbers)
sx = 5.0 / np.mean(np.diff(xt))
# inside sensor: left ticks, 110 nm per interval; outside sensor: right ticks, 50 nm per interval;
# origin (0 nm) at the bottom frame line
syl = 110.0 / np.mean(np.diff(ylt))
syr = 50.0 / np.mean(np.diff(yrt))


def verts(rgb):
    pts = []
    for d in ds:
        if not (vec.colour_is(d.get("fill"), rgb) or vec.colour_is(d.get("color"), rgb)):
            continue
        for it in d["items"]:
            if it[0] == "l":
                pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
            elif it[0] == "re":
                r = it[1]
                pts += [(r.x0, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x1, r.y0)]
            elif it[0] == "qu":
                pts += [(p.x, p.y) for p in it[1]]
            elif it[0] == "c":
                pts += [(it[1].x, it[1].y), (it[4].x, it[4].y)]
    return np.array(pts)


rows = []
summary = {}
chk = []
for name, rgb, s in (("Outside sensor", RED, syr), ("Inside sensor", BLUE, syl)):
    p = verts(rgb)
    k = np.floor((p[:, 0] - L) / BIN).astype(int)
    vals = []
    for b in np.unique(k):
        m = k == b
        ytop, ybot = p[m, 1].min(), p[m, 1].max()  # PDF y grows downwards
        xc = L + (b + 0.5) * BIN
        hi = (B - ytop) * s
        lo = (B - ybot) * s
        vals.append((xc, (hi + lo) / 2))
        chk.append((xc, (ytop + ybot) / 2))
        rows.append((name, round((xc - L) * sx, 4), round((hi + lo) / 2, 2), round(lo, 2), round(hi, 2)))
    v = np.array([q[1] for q in vals])
    summary[name] = v

# annotation check: the two double-headed arrows (black filled shapes about 5 x 18 pt) mark the
# "27 nm" (outside, upper arrow) and "52 nm" (inside, lower arrow) spans; convert their lengths
arrows = sorted([d["rect"] for d in ds if vec.is_black_fill(d) and 3 < d["rect"].width < 8 and 10 < d["rect"].height < 30],
                key=lambda r: r.y0)
notes = []
for (name, s, lab), r in zip((("Outside sensor", syr, "27 nm"), ("Inside sensor", syl, "52 nm")), arrows):
    v = summary[name]
    n = len(v) // 10
    base = np.median(np.r_[v[:n], v[-n:]])
    ext = v.max() if name == "Inside sensor" else v.min()
    notes.append(f"{name}: arrow '{lab}' spans {r.height:.2f} pt = {r.height * s:.1f} nm on the printed scale; "
                 f"trace extreme {ext:.1f} nm vs trace level at the left/right ends {base:.1f} nm")

hdr = [
    "zhangk2020 Fig. 5 (p. 7): The outputs of the inside and the outside sensors with a command displacement of 50 nm.",
    "Provenance: tier 2, vector paths in the PDF (PyMuPDF get_drawings). Each trace is a thick line split into ~1300 filled pieces;",
    f"per {BIN} pt x bin: y_low_nm / y_high_nm = lower / upper edge of the drawn line (lowest and highest vertex), y_nm = their mean.",
    "At a vertical step the bin spans the riser, so y_low/y_high there give the step's extent. Line width about 1.3 pt.",
    "The axes carry no numbers, only scales: 'Time 5 s/div.', 'Output of inside sensor 110 nm/div.' (left), 'Output of outside sensor 50 nm/div.' (right).",
    f"Origins are arbitrary: t_s = 0 at the left frame line ({L:.2f} pt); y = 0 at the bottom frame line ({B:.2f} pt) for both sensors.",
    f"Time ticks at {', '.join(f'{(x - L) * sx:.3f}' for x in xt)} s ({np.mean(np.diff(xt)):.3f} pt per 5 s).",
    f"Inside sensor (left axis) ticks at {', '.join(f'{(B - y) * syl:.2f}' for y in ylt)} nm ({np.mean(np.diff(ylt)):.3f} pt per 110 nm).",
    f"Outside sensor (right axis) ticks at {', '.join(f'{(B - y) * syr:.2f}' for y in yrt)} nm ({np.mean(np.diff(yrt)):.3f} pt per 50 nm).",
    "series 'Outside sensor' (red, upper trace) is read on the right axis, 'Inside sensor' (blue, lower trace) on the left axis.",
    "Check (decompiler): " + "; ".join(notes) + ".",
    "Uncertainty: below 0.1 pt (PDF precision), i.e. about 0.01 s, 0.3 nm (inside), 0.2 nm (outside); the line centre is +-0.65 pt of the edges.",
]
vec.write_csv(HERE / "fig5.csv", hdr, ["series", "t_s", "y_nm", "y_low_nm", "y_high_nm"], rows)
print("\n".join(hdr))
print(len(rows), "rows")

vec.overlay_pts(PAGE, CLIP, chk[::4], HERE.parent / "work" / "fig5_overlay.png")
