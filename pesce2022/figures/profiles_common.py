"""Shared extraction code for the "intensity profile along depth" panels of Pesce et al. 2022 (Comm. Biol. 5:447):
Fig. 1c-f (main PDF p. 3), Supplementary Fig. 2b-e (supplement p. 3) and Supplementary Fig. 3b-f (supplement p. 4).

Every panel is an Origin line plot: x = "x position (um)" 0-700, y = "Intensity", 2-4 series, each drawn as a mean
line with a +-SD band. In the PDF each series consists of
  * one tiny filled marker per data point (1273 of them; square / circle / triangle, 0.2-0.4 pt wide),
  * a filled band polygon (grey / pink / cyan / pale green) and
  * three (or four) stroked polylines in the series colour: the mean line and the upper and lower band edge.
In the supplement the polylines are exact (one vertex per data point; the mean line is split into two pieces of
700 and 574 vertices). In the main PDF the polylines were simplified to Bezier curves by the PDF producer, so only
the marker centres carry every data point exactly; the band edges are read from the (flattened) curves at the
marker x positions, and the deviation of the simplified mean line from the markers is reported as the error of
that approximation.

Used by figN?_extract.py / sfigN?_extract.py, which call extract_panel() with the panel-specific settings.
"""
import csv
import math
import os
import sys

for _d in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * i))) for i in range(1, 6)]:
    if os.path.exists(os.path.join(_d, "tools", "digitize_common.py")):  # the collection's shared tools/, wherever this folder sits
        sys.path.insert(0, os.path.join(_d, "tools")); break
import numpy as np  # noqa: E402
import pdfplot as pp  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                   # .../pesce2022
MAIN = os.path.join(ROOT, "source", "pesce2022.pdf")
SUPP = os.path.join(ROOT, "source", "pesce2022_supplement.pdf")
WORK = os.path.join(ROOT, "work", "agent_profiles")

# series colour families (the main PDF uses pure black/red/blue, the supplement Origin's dark grey/red/blue/green)
FAMILIES = {"black": {"#000000", "#515151"}, "red": {"#ff0000", "#f14040"}, "blue": {"#0000ff", "#1a6fdf"},
            "green": {"#37ad6b"}}
# colours of the printed (bold) legend swatches
SWATCH = {"#000000": "black", "#ff0000": "red", "#0033cc": "blue", "#00b050": "green"}
BAND_FILL = {"#c0c0c0": "black", "#ffb7c1": "red", "#00ffff": "blue", "#cdf3db": "green"}


def _horizontal(s):
    return abs(s["dir"][1]) < 0.01 and s["dir"][0] > 0.99


def _tick_value(text):
    """'0' / '0,0' -> (0, False); '5,0x10' -> (5.0, True); '1x10' -> (1.0, True); else None."""
    t = text.strip()
    if t in ("0", "0,0"):
        return 0.0, False
    if t.endswith("x10"):
        m = t[:-3].replace(",", ".")
        try:
            return float(m), True
        except ValueError:
            return None
    return None


def y_axis(spans, draws, clip):
    """Axis for the y axis from the 'a,bx10' + superscript labels, refined to the tick marks."""
    hs = [s for s in spans if _horizontal(s)]
    pairs, used = [], []
    for s in hs:
        tv = _tick_value(s["text"])
        if tv is None:
            continue
        mant, needs_exp = tv
        if needs_exp:
            sup = [u for u in hs if u["text"].strip().isdigit() and u["size"] < s["size"] - 0.5
                   and abs(u["bbox"][0] - s["bbox"][2]) < 1.0 and 0 < s["cy"] - u["cy"] < 3.0]
            if len(sup) != 1:
                raise ValueError(f"no unique exponent for label {s['text']!r} at {s['bbox']}: {[u['text'] for u in sup]}")
            val = mant * 10 ** int(sup[0]["text"])
        else:
            val = 0.0
        pairs.append((s["cy"], val, s))
    # keep the most populated column (right edges within 3 pt) -> this panel's y labels
    from collections import Counter
    col = Counter(round(s["bbox"][2] / 3) for _, _, s in pairs).most_common(1)[0][0]
    pairs = [(cy, v, s) for cy, v, s in pairs if abs(round(s["bbox"][2] / 3) - col) <= 1]
    ticks = pp.tick_marks(draws, "y", max_len=6.0, min_len=0.5, region=clip)
    out, label_resid = [], 0.0
    for cy, v, s in pairs:
        near = [t for t in ticks if abs(t["pos"] - cy) < 3.0 and t["cx"] > s["bbox"][2] - 1]
        if not near:
            raise ValueError(f"no tick mark near y label {s['text']!r} at cy={cy:.2f}")
        t = min(near, key=lambda t: abs(t["pos"] - cy))
        label_resid = max(label_resid, abs(t["pos"] - cy))
        out.append((t["pos"], v))
    ax = pp.Axis(out)
    ax.label_resid = label_resid
    ax.ticks = sorted(t["pos"] for t in ticks)
    return ax


def x_axis(spans, draws, clip):
    """Axis for the x axis (labels 0, 100, ... 700) refined to the tick marks."""
    hs = [s for s in spans if _horizontal(s) and s["text"].strip().isdigit() and s["size"] > 3.5]
    from collections import Counter
    row = Counter(round(s["cy"] / 3) for s in hs).most_common(1)[0][0]
    sel = [s for s in hs if abs(round(s["cy"] / 3) - row) <= 1]
    ticks = pp.tick_marks(draws, "x", max_len=6.0, min_len=0.5, region=clip)
    out, label_resid = [], 0.0
    for s in sel:
        near = [t for t in ticks if abs(t["pos"] - s["cx"]) < 4.0 and t["cy"] < s["bbox"][1] + 1]
        if not near:
            raise ValueError(f"no tick mark near x label {s['text']!r} at cx={s['cx']:.2f}")
        t = min(near, key=lambda t: abs(t["pos"] - s["cx"]))
        label_resid = max(label_resid, abs(t["pos"] - s["cx"]))
        out.append((t["pos"], float(s["text"])))
    ax = pp.Axis(out)
    ax.label_resid = label_resid
    ax.ticks = sorted(t["pos"] for t in ticks)
    return ax


def flatten(d, n=40):
    """(points, vertices) of a stroked path from its raw PyMuPDF items: 'l' end points exactly, 'c' curves subdivided
    n times. `vertices` are the exact segment / curve end points only."""
    pts, verts = [], []
    for it in d["raw"]["items"]:
        if it[0] == "l":
            p1, p2 = it[1], it[2]
            if not pts or (abs(pts[-1][0] - p1.x) > 1e-6 or abs(pts[-1][1] - p1.y) > 1e-6):
                pts.append((p1.x, p1.y))
            pts.append((p2.x, p2.y))
            verts += [(p1.x, p1.y), (p2.x, p2.y)]
        elif it[0] == "c":
            p0, p1, p2, p3 = it[1:5]
            verts += [(p0.x, p0.y), (p3.x, p3.y)]
            if not pts or (abs(pts[-1][0] - p0.x) > 1e-6 or abs(pts[-1][1] - p0.y) > 1e-6):
                pts.append((p0.x, p0.y))
            for i in range(1, n + 1):
                t = i / n
                u = 1 - t
                pts.append((u ** 3 * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t ** 3 * p3.x,
                            u ** 3 * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t ** 3 * p3.y))
        else:
            raise ValueError("unexpected path item " + it[0])
    return pts, verts


TOL = 0.06   # pt; marker-rect centres sit up to ~0.04 pt off the polyline vertices (coordinate rounding, bbox centre)
SNAP = 0.02  # pt; a query x this close to an exact vertex returns the vertex


class Curve:
    """A polyline y(x) with linear interpolation (NaN outside its x range)."""

    def __init__(self, pts, verts, ncurve):
        xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
        order = np.argsort(xs, kind="stable")
        self.x, self.y = xs[order], ys[order]
        self.x0, self.x1 = float(self.x[0]), float(self.x[-1])
        self.n, self.ncurve = len(pts), ncurve
        self.verts = np.array(sorted(set(verts)))       # exact path vertices (segment / curve end points)

    def __call__(self, x):
        x = np.asarray(x, float)
        out = np.interp(x, self.x, self.y)          # clamps to the end vertices
        # snap to an exact vertex where one sits at this x (within SNAP), so exact polylines stay exact
        j = np.clip(np.searchsorted(self.verts[:, 0], x), 1, len(self.verts) - 1)
        near = np.where(np.abs(self.verts[j - 1, 0] - x) < np.abs(self.verts[j, 0] - x), j - 1, j)
        hit = np.abs(self.verts[near, 0] - x) < SNAP
        out[hit] = self.verts[near[hit], 1]
        out[(x < self.x0 - TOL) | (x > self.x1 + TOL)] = np.nan
        return out

    def nearest_vertex(self, x):
        """(dx, dy) from each x-nearest exact vertex to the point (x, y) is left to the caller: returns vertex rows."""
        x = np.asarray(x, float)
        j = np.clip(np.searchsorted(self.verts[:, 0], x), 1, len(self.verts) - 1)
        near = np.where(np.abs(self.verts[j - 1, 0] - x) < np.abs(self.verts[j, 0] - x), j - 1, j)
        return self.verts[near]

    def covers(self, x):
        x = np.asarray(x, float)
        return (x >= self.x0 - TOL) & (x <= self.x1 + TOL)


def legend_check(spans, draws, clip, series):
    """Printed legend: bold text lines and coloured swatches, top to bottom. Returns the list of (text, family)
    and raises if the swatch colour order does not match the families of `series`."""
    bold = [s for s in spans if _horizontal(s) and "Bold" in s["font"] and 3.9 <= s["size"] < 8.5
            and s["text"].strip() not in ("x position (µm)", "x position (μm)", "Intensity")
            and not (s["size"] > 7.5 and len(s["text"].strip()) <= 1)          # panel letters
            and s["bbox"][0] >= clip.x0 + 1 and s["bbox"][2] <= clip.x1 - 1]
    lines = []                                   # [(cy, [spans])], spans within 3 pt of a line's cy join it
    for s in sorted(bold, key=lambda s: s["cy"]):
        for ln in lines:
            if abs(ln[0] - s["cy"]) < 3.0:
                ln[1].append(s)
                break
        else:
            lines.append((s["cy"], [s]))
    texts = []
    for cy, parts in sorted(lines):
        parts = sorted(parts, key=lambda s: s["bbox"][0])
        texts.append("".join(p["text"] for p in parts).strip())
    sw = []
    for d in draws:
        x0, y0, x1, y1 = d["rect"]
        w, h = x1 - x0, y1 - y0
        if d["kind"] == "stroke" and d["n_items"] == 1 and (d["width"] or 0) > 2 and 4 < w < 20 and h < 1:
            c = pp.hexcolor(d["color"])
        elif d["kind"] == "fill" and d["n_items"] <= 4 and len(d["points"]) <= 6 and 4 < w < 30 and 0.5 < h < 6:
            c = pp.hexcolor(d["fill"])
        else:
            continue
        if c in SWATCH:
            sw.append(((y0 + y1) / 2, SWATCH[c]))
    sw.sort()
    fams = [f for _, f in sw]
    want = [f for _, f in series]
    if fams != want:
        raise ValueError(f"legend swatch order {fams} does not match the series families {want}")
    if len(texts) != len(series):
        raise ValueError(f"found {len(texts)} printed legend lines {texts} for {len(series)} series")
    return list(zip(texts, fams))


def hidden_legend(spans):
    """Text of the older, overprinted (small font) legend, top to bottom."""
    small = [s for s in spans if _horizontal(s) and s["size"] < 4.0 and "Bold" not in s["font"]
             and not s["text"].strip().isdigit() and len(s["text"].strip()) > 2 and _tick_value(s["text"]) is None]
    return [s["text"] for s in sorted(small, key=lambda s: s["cy"])]


def extract_panel(pdf, pno, clip, series, panel, comments, bezier_n=40):
    """Extract all series of one panel.

    series: list of (printed legend name, colour family) in legend order (top to bottom).
    Writes figures/<panel>.csv and work/agent_profiles/<panel>_overlay.png (+ <panel>_orig.png), returns diagnostics.
    """
    page = pp.open_page(pdf, pno)
    draws = pp.drawings(page, clip, how="inside")
    spans = pp.text_spans(page, clip)
    xax = x_axis(spans, draws, clip)
    yax = y_axis(spans, draws, clip)
    legend = legend_check(spans, draws, clip, series)
    diag = dict(xax=xax, yax=yax, legend=legend, hidden=hidden_legend(spans), series={})
    ybot, ytop = yax.ticks[-1], yax.ticks[0]        # PDF y of the lowest / highest tick (axis bottom / top)
    rows, over = [], []
    for name, fam in series:
        cols = FAMILIES[fam]
        marks = [d for d in draws if d["kind"] == "fillstroke" and pp.hexcolor(d["fill"]) in cols
                 and (d["rect"][2] - d["rect"][0]) <= 1.0 and (d["rect"][3] - d["rect"][1]) <= 1.0]
        mx = np.array(sorted(((d["rect"][0] + d["rect"][2]) / 2, (d["rect"][1] + d["rect"][3]) / 2) for d in marks))
        if len(mx) == 0:
            raise ValueError(f"{panel}: no markers for {name} ({fam})")
        strokes = [d for d in draws if d["kind"] == "stroke" and pp.hexcolor(d["color"]) in cols and d["n_items"] >= 50]
        curves = []
        for d in strokes:
            ncurve = sum(1 for it in d["raw"]["items"] if it[0] == "c")
            pts, verts = flatten(d, bezier_n)
            curves.append(Curve(pts, verts, ncurve))
        # the older (hidden) legend has one marker symbol per series next to its line sample: far from every polyline
        dist = np.full(len(mx), np.inf)
        for c in curves:
            dist = np.minimum(dist, np.nan_to_num(np.abs(c(mx[:, 0]) - mx[:, 1]), nan=np.inf))
        stray = mx[dist > 2.0]
        mx = mx[dist <= 2.0]
        # classify: delta = stroke y - marker y at the marker x positions (PDF y grows downwards)
        info = []
        for c in curves:
            sel = c.covers(mx[:, 0])
            dlt = c(mx[sel, 0]) - mx[sel, 1]
            info.append((float(np.mean(dlt)), float(np.max(np.abs(dlt))), sel.mean(), c))
        full = [i for i in info if i[2] > 0.95]
        part = [i for i in info if i[2] <= 0.95]
        if len(full) == 3 and not part:
            full.sort(key=lambda i: i[0])
            upper, mean_pieces, lower = full[0], [full[1]], full[2]
        elif len(full) == 2 and part:
            full.sort(key=lambda i: i[0])
            upper, lower, mean_pieces = full[0], full[1], part
        else:
            raise ValueError(f"{panel} {name}: unexpected stroke set {[(round(i[0], 3), round(i[1], 3), round(i[2], 2)) for i in info]}")
        if not (upper[0] < 0 < lower[0]):
            raise ValueError(f"{panel} {name}: band edges not on both sides of the markers: {upper[0]:.3f}, {lower[0]:.3f}")
        # coverage of the mean pieces and their deviation from the markers (curve-fit error in the main PDF)
        cov = np.zeros(len(mx), bool)
        for i in mean_pieces:
            cov |= i[3].covers(mx[:, 0])
        if not cov.all():
            raise ValueError(f"{panel} {name}: mean line pieces cover only {cov.sum()} of {len(mx)} markers")
        # the marker bounding-box centre sits a constant (dx, dy) off the data point (coordinate rounding of the
        # marker rectangle; a triangle's bbox centre is not its anchor): calibrate on the exact mean-line vertices
        vv = np.vstack([i[3].verts for i in mean_pieces])
        vv = vv[np.argsort(vv[:, 0])]
        j = np.clip(np.searchsorted(vv[:, 0], mx[:, 0]), 1, len(vv) - 1)
        near = np.where(np.abs(vv[j - 1, 0] - mx[:, 0]) < np.abs(vv[j, 0] - mx[:, 0]), j - 1, j)
        dv = vv[near] - mx
        ok = np.abs(dv[:, 0]) < TOL
        off = np.median(dv[ok], axis=0)
        mx = mx + off
        vres = np.abs(vv[near][ok] - mx[ok]).max(axis=0)       # residual marker-vs-vertex after the correction
        fit_err = 0.0
        for i in mean_pieces:
            c = i[3]
            sel = c.covers(mx[:, 0])
            fit_err = max(fit_err, float(np.max(np.abs(c(mx[sel, 0]) - mx[sel, 1]))))
        yu = upper[3](mx[:, 0]); yl = lower[3](mx[:, 0])
        if np.isnan(yu).any() or np.isnan(yl).any():
            raise ValueError(f"{panel} {name}: band edge does not cover all markers")
        ncurve = sum(c.ncurve for c in curves)
        x_um = xax(mx[:, 0]); mean = yax(mx[:, 1]); up = yax(yu); lo = yax(yl)
        asym = np.max(np.abs((up + lo) / 2 - mean))
        sd = (up - lo) / 2
        # a band edge cut off at the axis limit sits exactly on it; if the same edge is drawn beyond the limit anywhere
        # in the series, nothing is clipped and values near the limit are just small
        at_top = np.abs(yu - ytop) < 0.05; at_bot = np.abs(yl - ybot) < 0.05
        beyond_top = int(np.sum(yu < ytop - 0.05)); beyond_bot = int(np.sum(yl > ybot + 0.05))
        if beyond_top:
            at_top[:] = False
        if beyond_bot:
            at_bot[:] = False
        clip_top = int(at_top.sum()); clip_bot = int(at_bot.sum()); beyond = beyond_top + beyond_bot
        flags = ["+".join(f for f, c in (("upper_clipped", at_top[k]), ("lower_clipped", at_bot[k])) if c) for k in range(len(mx))]
        dx = np.diff(mx[:, 0])
        diag["series"][name] = dict(n=len(mx), fam=fam, ncurve=ncurve, stray=[(round(float(a), 2), round(float(b), 2)) for a, b in stray],
                                    marker_offset_pt=(round(float(off[0]), 4), round(float(off[1]), 4)), n_vertex_matched=int(ok.sum()),
                                    vertex_resid_pt=(round(float(vres[0]), 4), round(float(vres[1]), 4)), fit_err_pt=fit_err, fit_err_units=fit_err * abs(yax.slope),
                                    asym_units=float(asym), max_sd=float(sd.max()), x_first=float(x_um[0]), x_last=float(x_um[-1]),
                                    dx_mean=float(np.mean(dx)) * xax.slope, clip_top=clip_top, clip_bot=clip_bot, beyond=beyond,
                                    upper_delta_pt=upper[0], lower_delta_pt=lower[0],
                                    mean_pieces=[(round(i[3].x0, 2), round(i[3].x1, 2), i[3].n) for i in mean_pieces])
        for k in range(len(mx)):
            rows.append((name, f"{x_um[k]:.2f}", f"{mean[k]:.1f}", f"{lo[k]:.1f}", f"{up[k]:.1f}", flags[k]))
        over.append((fam, mx, yu, yl))
    # outputs
    os.makedirs(WORK, exist_ok=True)
    out_csv = os.path.join(HERE, panel + ".csv")
    pp.write_csv(out_csv, ["series", "x_um", "mean", "sd_lower", "sd_upper", "flag"], rows, comments(diag))
    diag["rows"] = len(rows)
    overlay(page, clip, over, os.path.join(WORK, panel + "_overlay.png"), os.path.join(WORK, panel + "_orig.png"))
    return diag


def overlay(page, clip, over, out_png, orig_png, dpi=600):
    """Render the panel and draw the extracted mean (dots) and band edges (lines) on top."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pp.render(page, clip, dpi, orig_png)
    img = plt.imread(orig_png)
    z = dpi / 72
    fig = plt.figure(figsize=(img.shape[1] / 100, img.shape[0] / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img)
    col = {"black": "#ff00ff", "red": "#00aa00", "blue": "#ff8800", "green": "#aa00ff"}
    for fam, mx, yu, yl in over:
        X = (mx[:, 0] - clip.x0) * z
        ax.plot(X, (mx[:, 1] - clip.y0) * z, ".", color=col[fam], ms=0.7, alpha=0.7)
        ax.plot(X, (yu - clip.y0) * z, "-", color=col[fam], lw=0.25, alpha=0.7)
        ax.plot(X, (yl - clip.y0) * z, "-", color=col[fam], lw=0.25, alpha=0.7)
    ax.set_xlim(0, img.shape[1]); ax.set_ylim(img.shape[0], 0); ax.axis("off")
    fig.savefig(out_png, dpi=100)
    plt.close(fig)


def describe(diag):
    """Human-readable diagnostics for the report."""
    xax, yax = diag["xax"], diag["yax"]
    out = [f"x axis: {len(xax.pairs)} labelled ticks, max residual {xax.resid:.3f} um (label-tick offset {xax.label_resid:.2f} pt); "
           f"{xax.slope:.4f} um/pt",
           f"y axis: {len(yax.pairs)} labelled ticks, max residual {yax.resid:.3g} units (label-tick offset {yax.label_resid:.2f} pt); "
           f"{-yax.slope:.4g} units/pt",
           f"printed legend: {diag['legend']}", f"hidden legend: {diag['hidden']}"]
    for name, s in diag["series"].items():
        out.append(f"  {name} [{s['fam']}]: n={s['n']}, x {s['x_first']:.2f}..{s['x_last']:.2f} um (step {s['dx_mean']:.4f}), "
                   f"bezier items={s['ncurve']}, mean-line vs markers max {s['fit_err_pt']:.3f} pt = {s['fit_err_units']:.1f} units, "
                   f"band asymmetry max {s['asym_units']:.1f} units, max SD {s['max_sd']:.0f}, clipped top/bottom {s['clip_top']}/{s['clip_bot']}, beyond axis {s['beyond']}, "
                   f"edge offsets {s['upper_delta_pt']:.3f}/{s['lower_delta_pt']:.3f} pt, mean pieces {s['mean_pieces']}, "
                   f"stray markers dropped {s['stray']}, marker offset {s['marker_offset_pt']} pt from {s['n_vertex_matched']} exact vertices, "
                   f"residual after correction {s['vertex_resid_pt']} pt")
    return "\n".join(out)


def make_comments(desc, script):
    """Return the CSV comment builder for a panel: `desc` = lines describing the panel (figure, what is plotted)."""
    def comments(d):
        s = d["series"]
        bez = sum(v["ncurve"] for v in s.values()) > 0
        n = ", ".join(str(v["n"]) for v in s.values())
        out = list(desc) + [
            "Columns: series = legend name as printed; x_um = x position (um); mean = mean intensity (camera grey levels, y axis",
            "  'Intensity'); sd_lower / sd_upper = lower and upper edge of the printed +-SD band (mean - SD, mean + SD);",
            "  flag = 'upper_clipped' / 'lower_clipped' where that band edge is cut off at the y axis limit (value = the limit).",
            f"Provenance: tier 2, vector paths in the PDF, exact up to the PDF's precision ({script} / profiles_common.py).",
            "  mean = centre of the tiny marker drawn at every data point (one per ~0.55 um pixel; " + n + " points per series),",
            "  corrected for the constant offset (<= 0.04 pt) between the marker's bounding box and the vertices of the mean polyline;",
            "  the band edges are the two polylines of the series colour above and below the markers, read at the data x positions.",
        ]
        if bez:
            out += [
                "  In this PDF the polylines were simplified to Bezier curves by the PDF producer, so between the remaining vertices",
                "  the band edges are that approximation; the simplified mean line deviates from the exact marker centres by at most",
                "  " + ", ".join(f"{v['fit_err_units']:.0f}" for v in s.values()) + " intensity units (per series, in legend order),",
                "  which is also the uncertainty of sd_lower/sd_upper.",
            ]
        else:
            out += ["  The polylines are exact (one vertex per data point, no curve simplification); the mean polyline coincides with",
                    "  the marker centres to within " + ", ".join(f"{v['fit_err_units']:.0f}" for v in s.values()) + " units."]
        out += [
            f"  Axes calibrated on the labelled tick marks: x {len(d['xax'].pairs)} ticks (0-700), max residual {d['xax'].resid:.3f} um;",
            f"  y {len(d['yax'].pairs)} ticks (labels like '5,0x10^3' with decimal commas), max residual {d['yax'].resid:.2g} units.",
            f"Uncertainty: PDF coordinate quantum ~0.03 pt = {0.03 * d['xax'].slope:.2f} um in x and ~{0.03 * abs(d['yax'].slope):.0f} units in y"
            + (" (plus the Bezier deviation above for the band edges)." if bez else "."),
            "  Band symmetry check, max |(sd_upper+sd_lower)/2 - mean|: " + ", ".join(f"{v['asym_units']:.0f}" for v in s.values()) + " units.",
        ]
        nmax = max(v["n"] for v in s.values())
        short = [(k, v) for k, v in s.items() if v["n"] < nmax or v["x_first"] > 1.0]
        for k, v in short:
            out += [f"Missing points: '{k}' has only {v['n']} points (others {nmax}), on the same x grid but starting at x = {v['x_first']:.2f} um:",
                    "  the first grid positions of this series have no marker and no line vertex in the PDF (the paper does not say why)."]
        clipped = [(k, v) for k, v in s.items() if v["clip_top"] or v["clip_bot"]]
        if clipped:
            out += ["Clipping: " + "; ".join(f"'{k}': {v['clip_top']} points with the upper band edge cut at the top of the axis and "
                                             f"{v['clip_bot']} with the lower edge cut at the bottom" for k, v in clipped)
                    + " (flag column)."]
        beyond = [(k, v) for k, v in s.items() if v["beyond"]]
        if beyond:
            out += ["The band is drawn slightly outside the axis box (not clipped) for " + "; ".join(f"'{k}': {v['beyond']} points" for k, v in beyond)
                    + "; those sd values are simply below 0 / above the top tick."]
        if not short and not clipped:
            out += ["No points are hidden or clipped: every series has all its points drawn and the band is not cut off."]
        if d["hidden"]:
            out += ["The PDF text layer also holds an older, overprinted small-font legend (" + "; ".join(repr(h) for h in d["hidden"]) + ");",
                    "  the printed bold legend names are used here (series order = legend top to bottom)."]
        return out
    return comments
