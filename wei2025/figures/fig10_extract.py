"""Digitize Figure 10 (a-d) of Wei et al. 2025 (IJNAMG 49:2949), PDF p. 9.

Source: the embedded 300 ppi JPEG of Figure 10 (1427 x 1330 px). No vector data in the PDF.
    python3 -I -B figures/fig10_extract.py  -> figures/fig10a.csv ... fig10d.csv, work/fig10*_overlay.png
(a), (b): six coloured line+symbol series. Each series is traced with a colour mask per pixel column
(kind=line: centre, upper and lower edge of the line in that column) and its open-circle symbols are located
as the small white holes enclosed by the series colour (kind=marker).
(c), (d): bar charts; bar top = centre of the bar's top outline.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from digitize_common import embedded_image, write_csv, overlay  # noqa: E402
from figB_common import frame, ticks_h, ticks_v, mid, linfit, classify, groups, overlay_series  # noqa: E402

PDF = HERE.parent / "source" / "wei2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)
a = embedded_image(str(PDF), 9, bbox_near=(126.5, 32.7, 468.6, 351.5))
ai = a.astype(int)
dark = ai.mean(2) < 130

SERIES = ["Pyramid-0°", "Pyramid-45°", "Sphere (R=10 Å)", "Sphere (R=14.5 Å)", "Sphere (R=20 Å)", "Sphere (R=25 Å)"]
REFS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255)]
REGIONS = {"a": (0, 0, 713, 640), "b": (713, 0, 1427, 640), "c": (0, 640, 713, 1330), "d": (713, 640, 1427, 1330)}
LEGEND = {"a": (355, 45, 705, 240), "b": (1110, 45, 1400, 240)}   # legend boxes (pixel x0,y0,x1,y1), excluded


def calib(p):
    f = frame(dark, REGIONS[p])
    L, R, T, B = f["left"], f["right"], f["top"], f["bottom"]
    xt = ticks_h(dark, B, -1, 8, L[1] + 2, R[0] - 1)       # major ticks (inward, long)
    yt = ticks_v(dark, L, +1, 8, T[1] + 2, B[0] - 1)
    return f, xt, yt


def series_masks(p, f):
    lab = classify(a, REFS[1:], max_dist=150, min_sat=110)
    blk = (ai.mean(2) < 105) & ((ai.max(2) - ai.min(2)) < 70)
    masks = [blk] + [lab == i for i in range(5)]
    L, R, T, B = f["left"], f["right"], f["top"], f["bottom"]
    keep = np.zeros(dark.shape, bool)
    keep[T[1] + 1:B[0], L[1] + 1:R[0]] = True
    keep[B[0] - 11:B[0], :] = False   # inward tick marks along the bottom
    keep[:, L[1] + 1:L[1] + 12] &= ~blk[:, L[1] + 1:L[1] + 12]  # inward ticks on the left (black only)
    keep[:, R[0] - 11:R[0]] &= ~blk[:, R[0] - 11:R[0]]
    keep[T[1] + 1:T[1] + 12, :] &= ~blk[T[1] + 1:T[1] + 12, :]
    lx0, ly0, lx1, ly1 = LEGEND[p]
    keep[ly0:ly1, lx0:lx1] = False
    return [m & keep for m in masks], keep


def trace_series(m, c0, c1, gap=6, jump=60):
    """Per column: centre/upper/lower row of the series line, following continuity from the left.

    Runs of mask pixels closer than `gap` rows are joined (JPEG breaks steep lines into pieces). The run nearest to
    the previous column's centre is taken; if it is more than `jump` rows away it is taken to be another curve and the
    column is left empty. After 3 empty columns the tracker restarts on the longest run.
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
                out.append((c, np.nan, np.nan, np.nan))   # nearest run too far: another curve, not this one
                miss += 1
                if miss >= 3:
                    prev = None
                continue
        miss = 0
        top, bot = run[0] + 1.5, run[-1] - 1.5
        if top > bot:
            top = bot = run.mean()
        prev = (top + bot) / 2
        out.append((c, prev, top, bot))
    return out


def markers(m, light):
    """Open-circle symbols: a light pixel with series colour at distance 2-4 px in at least 7 of 8 directions.

    Candidate pixels are clustered (8-connected) and each cluster's centroid is one symbol centre.
    """
    H, W = m.shape
    dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    hit = np.zeros((H, W), int)
    for dx, dy in dirs:
        anyd = np.zeros((H, W), bool)
        for d in (2, 3, 4):
            sh = np.zeros((H, W), bool)
            ys, xs = slice(max(0, -dy * d), H - max(0, dy * d)), slice(max(0, -dx * d), W - max(0, dx * d))
            yd, xd = slice(max(0, dy * d), H - max(0, -dy * d)), slice(max(0, dx * d), W - max(0, -dx * d))
            sh[ys, xs] = m[yd, xd]
            anyd |= sh
        hit += anyd
    cand = light & ~m & (hit >= 7)
    lab, n = ndimage.label(cand, structure=np.ones((3, 3)))
    pts = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if (lab[sl] == i).sum() <= 12:
            cy, cx = ndimage.center_of_mass(lab == i)
            pts.append((cx, cy))
    return sorted(pts)


YLAB = {"a": [70, 60, 50, 40, 30, 20, 10, 0], "b": [10, 8, 6, 4, 2, 0]}
YNAME = {"a": ("Er_GPa", "Reduced modulus E_r (GPa)"), "b": ("H_GPa", "Hardness (GPa)")}

for p in ("a", "b"):
    f, xt, yt = calib(p)
    xlab = [0, 5, 10, 15, 20, 25]
    assert len(xt) == 6 and len(yt) == len(YLAB[p]), (p, xt, yt)
    fx, rx, sx = linfit(xt, xlab)
    fy, ry, sy = linfit(yt, YLAB[p])
    masks, keep = series_masks(p, f)
    light = ai.mean(2) > 150
    L, R = f["left"], f["right"]
    rows, pts = [], []
    nmark = {}
    sp = []
    for s, m in zip(SERIES, masks):
        mk = markers(m, light & keep)
        # merge repeated detections of one symbol (< 6 px apart) and keep only candidates near an integer h_c:
        # the symbols are drawn every 1 Å (the last one sits on the 25 Å tick), so off-grid hits are false positives
        merged = []
        for cx, cy in mk:
            for q in merged:
                if abs(q[0] - cx) < 8 and abs(q[1] - cy) < 8:
                    q[2].append((cx, cy))
                    break
            else:
                merged.append([cx, cy, [(cx, cy)]])
        mk = [tuple(np.mean(q[2], 0)) for q in merged]
        mk = [(cx, cy) for cx, cy in mk if abs(fx(cx) - np.round(fx(cx))) < 0.2]
        nmark[s] = len(mk)
        for cx, cy in mk:
            rows.append((s, "marker", float(fx(cx)), float(fy(cy)), float("nan"), float("nan")))
            pts.append((cx, cy))
        sp.append(((120, 60, 0) if s == SERIES[0] else (0, 0, 0), mk, 4))
    for s, m in zip(SERIES, masks):
        # start each trace at its leftmost marker column region (hc ~ 1 Å); the curves start at hc = 1
        c0 = int(np.ceil(xt[0] + 0.8 * (xt[1] - xt[0]) / 5))
        tr = trace_series(m, c0, R[0])
        sp.insert(0, (tuple(int(0.8 * v) for v in REFS[SERIES.index(s)]) if s != SERIES[0] else (255, 140, 0), [(t[0], t[1]) for t in tr], 1))
        for c, ym, yu, yl in tr:
            if ym == ym:
                rows.append((s, "line", float(fx(c)), float(fy(ym)), float(fy(yu)), float(fy(yl))))
                pts.append((c, ym))
        cs = np.array([t[0] for t in tr], float)
        ys = np.array([t[1] for t in tr], float)
        for h in range(1, 26):
            c = (h - fx(0)) / sx            # column of h_c = h
            i = int(round(c - cs[0]))
            if 0 <= i < len(ys) and ys[i] == ys[i]:
                rows.append((s, "line_at_integer_hc", float(h), float(fy(ys[i])), float("nan"), float("nan")))
    overlay(a, pts, str(WORK / f"fig10{p}_overlay.png"))
    L_, R_, T_, B_ = f["left"], f["right"], f["top"], f["bottom"]
    overlay_series(a, sp, str(WORK / f"fig10{p}_series_overlay.png"), crop=(L_[0] - 5, T_[0] - 5, R_[1] + 5, B_[1] + 5), scale=2)
    yname, ytitle = YNAME[p]
    write_csv(str(HERE / f"fig10{p}.csv"), [
        f"Wei et al. 2025, Figure 10({p}): {ytitle} vs indentation depth h_c (Å) for all six indenter systems.",
        f"Columns: series (legend text); kind = marker (centre of an open-circle symbol) or line (the connecting line,",
        f"  one row per pixel column of the source image); hc_A = h_c in Å; {yname} = value at the symbol centre or line centre;",
        f"  {yname}_upper / {yname}_lower = upper and lower edge of the line inside that pixel column (differ on steep segments).",
        "Provenance: tier 3, digitized from the embedded 300 ppi JPEG of Figure 10 (no vector data in the PDF) by fig10_extract.py.",
        f"  x calibrated on the 6 major ticks 0-25 Å (max residual {rx:.3f} Å); y on the {len(yt)} major ticks"
        f" {YLAB[p][-1]}-{YLAB[p][0]} GPa (max residual {ry:.3f} GPa).",
        f"Uncertainty: about +-{2*abs(sx):.2f} Å in x and +-{2*abs(sy):.2f} GPa in y (2 px; the lines are ~4 px wide, JPEG).",
        "Series colours: Pyramid-0° black, Pyramid-45° red, R=10 green, R=14.5 blue, R=20 cyan, R=25 magenta.",
        "Where one line is drawn over another, the hidden series has no pixels in those columns: its line rows are missing",
        "  there (not interpolated) and hidden symbols are not listed. Symbols found per series: "
        + ", ".join(f"{k} {v}" for k, v in nmark.items()) + ".",
        "  The symbols sit at integer h_c = 1, 2, ..., 25 Å (one per Å; detected symbol centres lie at integer h_c - 0.05 Å on",
        "  average); symbols not found were covered by other series or their open centre was filled in by JPEG blur.",
        "  kind = line_at_integer_hc: the line centre read in the pixel column of h_c = 1, ..., 25 Å (derived from the line",
        "  trace, for convenience; missing where the line is hidden). Near sharp peaks the line centre may sit up to a few",
        "  GPa from the symbol centre.",
        "A few line rows near crossings can belong to a neighbouring curve of a similar colour after JPEG blending; check the overlay.",
        "The legend box area was excluded from tracing.",
    ], ["series", "kind", "hc_A", yname, yname + "_upper", yname + "_lower"], rows)
    print(p, "x res", rx, "y res", ry, "markers", nmark, "rows", len(rows))

# ---- bar charts (c), (d)
LABELS = SERIES
YBAR = {"c": ([7, 6, 5, 4, 3, 2, 1], "Er_avg_GPa", "Average reduced modulus E_r (GPa)", (0, 0, 255)),
        "d": ([2.0, 1.5, 1.0, 0.5], "H_avg_GPa", "Average hardness (GPa)", (255, 0, 0))}
for p in ("c", "d"):
    f, xt, yt = calib(p)
    ylab, col, ytitle, ref = YBAR[p]
    assert len(yt) == len(ylab), (p, yt)
    fy, ry, sy = linfit(yt, ylab)
    lab = classify(a, [ref], max_dist=120, min_sat=150) == 0
    L, R, T, B = f["left"], f["right"], f["top"], f["bottom"]
    sub = lab[T[1] + 1:B[0], L[1] + 1:R[0]]
    cols = groups(np.where(sub.sum(0) > 5)[0])
    rows, pts = [], []
    assert len(cols) == 6, cols
    for (c0, c1), name in zip(cols, LABELS):
        cc0, cc1 = c0 + L[1] + 1, c1 + L[1] + 1
        cm = (cc0 + cc1) // 2
        fill_top = T[1] + 1 + np.where(sub[:, c0 + 3:c1 - 2].any(1))[0].min()
        # top outline: dark row(s) just above the fill
        band = dark[fill_top - 6:fill_top + 1, cc0 + 3:cc1 - 2].mean(1)
        orow = [fill_top - 6 + i for i, v in enumerate(band) if v > 0.5]
        top = float(np.mean(orow)) if orow else fill_top - 0.5
        tick = min(xt, key=lambda t: abs(t - cm))
        rows.append((name, float(cm), float(tick), float(fy(top)), float(fy(fill_top))))
        pts.append((cm, top))
    overlay(a, pts, str(WORK / f"fig10{p}_overlay.png"))
    write_csv(str(HERE / f"fig10{p}.csv"), [
        f"Wei et al. 2025, Figure 10({p}): {ytitle}, one bar per indenter system (average over h_c = 15-25 Å per the caption).",
        "Category x axis: bars are evenly spaced, centred on the major x ticks, labelled (rotated) with the system names.",
        f"Columns: label = printed category label; bar_centre_px / tick_px = bar centre and nearest major tick, column of the",
        f"  1427 px wide embedded image; {col} = bar top (centre of the bar's black top outline);",
        f"  {col}_fill_top = top edge of the coloured fill (a check, ~1 px lower).",
        "Provenance: tier 3, digitized from the embedded 300 ppi JPEG of Figure 10 by fig10_extract.py;",
        f"  y calibrated on the {len(yt)} labelled major ticks {ylab[-1]}-{ylab[0]} (max residual {ry:.4f} GPa).",
        f"Uncertainty: about +-{abs(sy):.3f} GPa (1 px).",
    ], ["label", "bar_centre_px", "tick_px", col, col + "_fill_top"], rows, fmt="{:.4g}")
    print(p, [(r[0], round(r[3], 3)) for r in rows], "yres", ry)
