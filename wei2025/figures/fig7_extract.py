"""Digitize Figure 7 (a-d) of Wei et al. 2025 (IJNAMG 49:2949), PDF p. 7.

Source: the embedded 300 ppi JPEG of Figure 7 (1500 x 1240 px). No vector data in the PDF.
    python3 -I -B figures/fig7_extract.py  -> figures/fig7a.csv ... fig7d.csv, work/fig7*_overlay.png
(a), (b), (c): coloured line series without symbols. Each series is traced with a colour mask per pixel column:
centre, upper and lower edge of the line in that column (kind=line). The lines are jagged, so in steep columns the
upper/lower edges span the vertical extent of the line. Where another series is drawn over a series, that series
has no pixels and its rows are missing in those columns (not interpolated).
(d): one blue line with sphere symbols: line trace plus symbol candidates (blobs left after an opening that removes
the thinner line).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from digitize_common import embedded_image, write_csv, overlay  # noqa: E402
from figB_common import frame, ticks_h, ticks_v, linfit, classify, overlay_series  # noqa: E402

PDF = HERE.parent / "source" / "wei2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)
a = embedded_image(str(PDF), 7, bbox_near=(117.5, 365.6, 477.5, 663.1))
ai = a.astype(int)
dark = ai.mean(2) < 130

REGIONS = {"a": (0, 0, 750, 620), "b": (750, 0, 1500, 620), "c": (0, 620, 750, 1240), "d": (750, 620, 1500, 1240)}
YLAB = {"a": [200, 0, -200, -400, -600], "b": [25, 20, 15, 10, 5, 0], "c": [12, 10, 8, 6, 4, 2, 0, -2, -4],
        "d": [1500, 1000, 500, 0]}
# series colours: the dominant saturated pixel colours inside the plots (JPEG): black, red, blue, magenta, olive, violet
COLS = {"black": (13, 17, 26), "red": (250, 20, 20), "blue": (20, 20, 250), "magenta": (250, 20, 240),
        "olive": (150, 135, 30), "violet": (128, 20, 240)}
SER = {
    "a": [("Pyramid-0°", "black"), ("Pyramid-45°", "red"), ("Sphere (R=10 Å)", "blue"), ("Sphere (R=14.5 Å)", "magenta"),
          ("Sphere (R=20 Å)", "olive"), ("Sphere (R=25 Å)", "violet")],
    "c": [("x-direction", "black"), ("y-direction", "red"), ("z-direction", "magenta"), ("overall", "blue")],
    "d": [("Pyramid-0°", "blue")],
}
SER["b"] = SER["a"]
# legend areas (x0, y0, x1, y1): ALL = excluded for every series (the sample lines), BLACK = also excluded for the
# black series (legend text, the stage labels of panel a and the "Pyramid-0°" label of panel c)
EXCL_ALL = {"a": [(138, 22, 720, 118)], "b": [(1200, 25, 1278, 226)], "c": [(505, 665, 584, 800)], "d": [(878, 668, 1075, 704)]}
EXCL_BLACK = {"a": [(170, 356, 278, 393), (359, 154, 466, 191), (531, 356, 665, 393)],  # Loading/Holding/Unloading labels
              "b": [(1200, 25, 1490, 226)], "c": [(505, 665, 715, 800), (115, 668, 285, 712)], "d": []}
YINFO = {"a": ("energy_kcal_per_mol", "Pairwise interaction energy (kcal/mol)"),
         "b": ("force_nN", "Overall pairwise interaction force (nN)"),
         "c": ("force_nN", "Pairwise interaction force (nN)"),
         "d": ("energy_change_kcal_per_mol", "Total energy change (kcal/mol)")}


def calib(p):
    f = frame(dark, REGIONS[p])
    L, R, T, B = f["left"], f["right"], f["top"], f["bottom"]
    xt = ticks_h(dark, B, -1, 8, L[1] + 2, R[0] - 1)
    yt = ticks_v(dark, L, +1, 8, T[1] + 2, B[0] - 1)
    assert len(xt) == 8 and len(yt) == len(YLAB[p]), (p, xt, yt)
    return f, linfit(xt, list(range(0, 141, 20))), linfit(yt, YLAB[p])


def band_edges(p, f, fx):
    """x extents (ps) of the three light stage bands, from the background colour along a row near the bottom."""
    L, R, B = f["left"], f["right"], f["bottom"]
    row = ai[B[0] - 23:B[0] - 17, L[1] + 2:R[0] - 1].mean(0)
    refs = {"blue": (234, 238, 249), "orange": (251, 229, 215), "green": (243, 248, 241), "": (255, 255, 255)}
    lab = [min(refs, key=lambda k: np.sum((px - np.array(refs[k])) ** 2)) if min(px) > 200 else "" for px in row]
    out = {}
    for name in ("blue", "orange", "green"):
        idx = [i for i, v in enumerate(lab) if v == name]
        if idx:
            # longest consecutive stretch (ignores stray pixels where a line crosses the sampled rows)
            runs = np.split(np.array(idx), np.where(np.diff(idx) > 3)[0] + 1)
            run = max(runs, key=len)
            out[name] = (float(fx(L[1] + 2 + run[0])), float(fx(L[1] + 2 + run[-1])))
    return out


def trace_series(m, c0, c1, gap=6, jump=60):
    """Per column: centre/upper/lower row of the series line, following continuity from the left.

    Runs of mask pixels closer than `gap` rows are joined; the run nearest the previous centre is taken; if it is
    more than `jump` rows away the column is left empty (another curve); after 3 empty columns the tracker restarts
    on the longest run.
    """
    out, prev, miss = [], None, 0
    for c in range(c0, c1):
        r = np.where(m[:, c])[0]
        if len(r) == 0:
            out.append((c, np.nan, np.nan, np.nan))
            miss += 1
            if miss >= 3:
                prev = None
            continue
        runs = np.split(r, np.where(np.diff(r) > gap)[0] + 1)
        if prev is None:
            run = max(runs, key=len)
        else:
            run = min(runs, key=lambda q: 0 if q[0] - 3 <= prev <= q[-1] + 3 else min(abs(q[0] - prev), abs(q[-1] - prev)))
            if min(abs(run[0] - prev), abs(run[-1] - prev)) > jump and not (run[0] <= prev <= run[-1]):
                out.append((c, np.nan, np.nan, np.nan))
                miss += 1
                if miss >= 3:
                    prev = None
                continue
        miss = 0
        top, bot = run[0] + 2, run[-1] - 2
        if top > bot:
            top = bot = run.mean()
        prev = (top + bot) / 2
        out.append((c, prev, top, bot))
    return out


sat = ai.max(2) - ai.min(2)
lab_col = classify(a, [COLS[k] for k in ("red", "blue", "magenta", "olive", "violet")], max_dist=85, min_sat=70)
CMASK = {"black": (ai.max(2) < 100) & (sat < 60)}
for i, k in enumerate(("red", "blue", "magenta", "olive", "violet")):
    CMASK[k] = lab_col == i

for p in ("a", "b", "c", "d"):
    f, (fx, rx, sx), (fy, ry, sy) = calib(p)
    L, R, T, B = f["left"], f["right"], f["top"], f["bottom"]
    keep = np.zeros(dark.shape, bool)
    keep[T[1] + 2:B[0] - 1, L[1] + 2:R[0] - 1] = True
    for x0, y0, x1, y1 in EXCL_ALL[p]:
        keep[y0:y1, x0:x1] = False
    bands = band_edges(p, f, fx)
    rows, pts, sp = [], [], []
    if p == "c":
        bands = {}
    yname, ytitle = YINFO[p]
    counts = {}
    for s, cname in SER[p]:
        m = CMASK[cname] & keep
        if cname == "black":
            m[B[0] - 12:B[0], :] = False            # inward ticks
            m[:, L[1] + 2:L[1] + 13] = False
            m[:, R[0] - 12:R[0]] = False
            m[T[1]:T[1] + 12, :] = False
            for x0, y0, x1, y1 in EXCL_BLACK[p]:
                m[y0:y1, x0:x1] = False
        if p == "d":
            # symbols: isolated blobs of a loose blue mask (red channel low, blue well above red) that do not touch the
            # line; the line itself is one large connected component
            loose = (ai[:, :, 0] < 190) & (ai[:, :, 2] > ai[:, :, 0] + 30) & keep
            lb, n = ndimage.label(loose, structure=np.ones((3, 3)))
            mk = []
            for i, sl in enumerate(ndimage.find_objects(lb), 1):
                mm = lb[sl] == i
                h, w = mm.shape
                if 20 <= mm.sum() <= 110 and h <= 13 and w <= 13:
                    cy, cx = ndimage.center_of_mass(lb == i)
                    mk.append((cx, cy))
            for cx, cy in sorted(mk):
                rows.append((s, "marker", float(fx(cx)), float(fy(cy)), float("nan"), float("nan")))
                pts.append((cx, cy))
            counts["isolated symbols"] = len(mk)
            sp.append(((0, 0, 0), mk, 3))
        tr = trace_series(m, L[1] + 2, R[0] - 1)
        n_ok = 0
        for c, ym, yu, yl in tr:
            if ym == ym:
                rows.append((s, "line", float(fx(c)), float(fy(ym)), float(fy(yu)), float(fy(yl))))
                pts.append((c, ym))
                n_ok += 1
        counts[s] = n_ok
        rgb = COLS[cname] if cname != "black" else (255, 140, 0)
        sp.insert(0, (tuple(int(0.85 * v) for v in rgb), [(t[0], t[1]) for t in tr], 1))
    overlay(a, pts, str(WORK / f"fig7{p}_overlay.png"))
    overlay_series(a, sp, str(WORK / f"fig7{p}_series_overlay.png"), crop=(L[0] - 5, T[0] - 5, R[1] + 5, B[1] + 5), scale=2)
    ncol = R[0] - 1 - (L[1] + 2)
    hdr = [
        f"Wei et al. 2025, Figure 7({p}): {ytitle} vs time (ps).",
        "Columns: series (legend text); kind = line (one row per pixel column of the source image; value = line centre in",
        f"  that column, value_upper/value_lower = upper and lower edge of the line there){'; marker = symbol centre' if p == 'd' else ''};",
        f"  t_ps = time in ps; {yname} = value.",
        "Provenance: tier 3, digitized from the embedded 300 ppi JPEG of Figure 7 (no vector data in the PDF) by fig7_extract.py.",
        f"  x calibrated on the 8 major ticks 0-140 ps (max residual {rx:.3f} ps); y on the {len(YLAB[p])} major ticks"
        f" {YLAB[p][-1]} to {YLAB[p][0]} (max residual {ry:.3g}).",
        f"Uncertainty: about +-{2*abs(sx):.2f} ps in x and +-{2*abs(sy):.3g} in y (2 px; the lines are ~5-7 px wide, JPEG).",
        "Columns traced per series (of " + str(ncol) + " inside the frame): " + ", ".join(f"{k} {v}" for k, v in counts.items()) + ".",
        "  Missing columns: the line is hidden under another series drawn on top, or outside the colour mask (JPEG blending);",
        "  nothing is interpolated. Near crossings a few rows may belong to a neighbouring curve of similar colour (red/magenta,",
        "  magenta/violet, blue/violet); see work/fig7" + p + "_series_overlay.png.",
        "The legend area was excluded from tracing.",
        "Not data: the light background bands; measured x extents (ps) along a row near the bottom frame: "
        + ", ".join(f"{k} {v[0]:.1f}-{v[1]:.1f}" for k, v in bands.items()) + ".",
    ]
    if p == "a":
        hdr.append("  The bands carry the printed labels Loading (blue), Holding (orange) and Unloading (green).")
    if p == "d":
        hdr += ["Symbols: blue spheres (~9 px) on a smoothed (spline-like) line that does not pass through all of them.",
                "  Listed (kind=marker) are only the symbols that stand free of the line (separate blobs of 20-110 px);",
                "  symbols touching or lying on the ~7 px line cannot be separated from it and are missing, so kind=marker",
                "  is incomplete. The symbols found all lie within 0.1 ps of a whole picosecond and include neighbours 1 ps",
                "  apart (e.g. 3 and 4 ps, 20, 21 ps), consistent with one symbol per ps."]
    write_csv(str(HERE / f"fig7{p}.csv"), hdr, ["series", "kind", "t_ps", yname, yname + "_upper", yname + "_lower"], rows)
    print(p, "xres", rx, "yres", ry, counts, bands)
