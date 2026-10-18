"""edfig_extract_lib.py -- extraction helpers shared by Extended Data Fig. 2 and 3 (identical copy in both
figure folders). Builds on tools/pdfplot.py.

Panel types handled:
  * "variance" panels (explained variance of features vs feature #, 50 features)
  * "decoding" panels (decoding accuracy vs number of faces, 60 faces, with +/- shaded bands)

Solid data lines are stroke paths with one vertex per sample. Dashed data lines are NOT strokes in this
PDF: Illustrator expanded them into filled dash outlines (each dash a closed polygon, 1 pt wide, 4 pt
dash / 4 pt gap, miter joins or bevel+foot joins at polyline vertices). `recover_dashed` rebuilds the
centreline: inside a dash the two long outline edges of a polyline segment are anti-parallel and exactly
one line width apart, so their midline is the data line. Pieces are assigned to the polyline segment
(known vertex x grid) containing them, one line is fitted per segment and evaluated at its two end
vertices. Quality codes per vertex:
  direct   vertex inside / at the end of a dash (precision ~0.05 pt)
  extrap   vertex in a gap, extrapolated along the adjacent covered straight segment (~0.1-0.4 pt)
  extrap_offscale  same, but the value lies outside the axis range (line clipped by the axes box)
  interp   both adjacent segments lie in one dash gap: linear interpolation between the neighbours;
           geometric bound |error| <= ~1.2 pt (the two segments fit in a 4 pt gap)
  band_mid value taken as the midpoint of the shaded band, which is exactly symmetric about the line
           (precision ~0.01 pt; decoding panels only, wherever both band edges are unclipped)
  band     vertex in a gap, but the shaded band (which contains the line) collapses to zero height here
           or is entirely at the axis boundary, which pins the value (decoding panels only)
  clipped  the line is outside the axes box here (value unknown, NaN)
  gap      no coverage and no usable neighbours (NaN)
Shaded bands are single filled polygons (upper edge then lower edge, 1 vertex per sample, alpha 0.2),
clipped by the axes box; `band_edges` recovers lo/hi per sample and flags clipped edges.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import math
import os
import subprocess
import sys

import numpy as np

TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools")
PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "2026.10.15.759299v1.full.pdf")
sys.path.insert(0, TOOLS)
import pdfplot as pp  # noqa: E402
import fitz  # noqa: E402

DASH_LEN = 4.0  # pt, dash and gap length of the expanded dashed strokes (measured)


# ------------------------------------------------------------------ dashed-line centreline recovery

def _edges(poly):
    pts = [tuple(p) for p in poly]
    if len(pts) > 1 and abs(pts[0][0] - pts[-1][0]) < 1e-6 and abs(pts[0][1] - pts[-1][1]) < 1e-6:
        pts = pts[:-1]
    out = []
    n = len(pts)
    for i in range(n):
        p, q = np.array(pts[i]), np.array(pts[(i + 1) % n])
        v = q - p
        L = float(np.hypot(*v))
        if L < 1e-9:
            continue
        out.append(dict(p=p, q=q, u=v / L, L=L, m=(p + q) / 2))
    return out, np.array(pts)


def pieces_from_polygon(poly, width=1.0, min_len=0.25, ang_deg=1.5, dist_tol=0.04, min_overlap=0.1):
    # edges of length exactly width/2 are the foot edges of sharp joins (foot-vertex-foot); they are
    # perpendicular to the line and would pair with the dash's end cap, so they are excluded
    """Centreline pieces (c, u, t0, t1) of one closed dash-outline polygon: pairs of anti-parallel edges
    one line width apart with overlapping extent."""
    edges, pts = _edges(poly)
    cosmax = -math.cos(math.radians(ang_deg))
    out = []
    foot = lambda e: abs(e["L"] - width / 2) < 0.03
    for i in range(len(edges)):
        ei = edges[i]
        if ei["L"] < min_len or foot(ei):
            continue
        for j in range(i + 1, len(edges)):
            ej = edges[j]
            if ej["L"] < min_len or foot(ej) or float(ei["u"] @ ej["u"]) > cosmax:
                continue
            u = ei["u"] if ei["u"][0] >= 0 else -ei["u"]
            nrm = np.array([-u[1], u[0]])
            if abs(abs(float((ej["m"] - ei["m"]) @ nrm)) - width) > dist_tol:
                continue
            c = (ei["m"] + ej["m"]) / 2
            ti = sorted([float((ei["p"] - c) @ u), float((ei["q"] - c) @ u)])
            tj = sorted([float((ej["p"] - c) @ u), float((ej["q"] - c) @ u)])
            t0, t1 = max(ti[0], tj[0]), min(ti[1], tj[1])
            if t1 - t0 < min_overlap:
                continue
            out.append(dict(c=c, u=u, t0=t0, t1=t1))
    return out, pts


def recover_dashed(polys, xgrid, width=1.0, box_y=None, slack=0.06, anchor_tol=0.004, verbose=False):
    """polys: closed polygons (lists of (x,y), PDF pts) of ONE dashed series. xgrid: vertex x positions.
    box_y: (y_top, y_bottom) of the axes box (PDF y, down) for clip labelling.
    Returns dict(y=PDF y per vertex (NaN if unknown), code=list, disc=array of |difference| between the
    two adjacent-segment estimates where both exist, nbad=pieces that fitted no segment)."""
    xg = np.asarray(xgrid, float)
    N = len(xg)
    seg_pieces = [[] for _ in range(N - 1)]
    anchors = [[] for _ in range(N)]
    ends = []  # (x, y, |u_y|) of piece end points, for clip labelling
    nbad = 0
    for poly in polys:
        pcs, pts = pieces_from_polygon(poly, width=width)
        for pc in pcs:
            c, u, t0, t1 = pc["c"], pc["u"], pc["t0"], pc["t1"]
            p0, p1 = c + t0 * u, c + t1 * u
            xa, xb = sorted([p0[0], p1[0]])
            k = int(np.searchsorted(xg, (xa + xb) / 2, side="right") - 1)
            if k < 0 or k >= N - 1 or xa < xg[k] - slack or xb > xg[k + 1] + slack:
                nbad += 1
                if verbose:
                    print(f"  piece x-range [{xa:.2f},{xb:.2f}] fits no segment (k={k})")
                continue
            seg_pieces[k].append((p0, p1))
            ends.append((p0[0], p0[1], abs(u[1])))
            ends.append((p1[0], p1[1], abs(u[1])))
        # joins: the two outline points of a join (miter points, or inner foot + outer foot of a bevel join)
        # are point-symmetric about the polyline vertex -> exact anchors. (A single outline vertex sitting on
        # a grid x is NOT used: cap corners and the miter points of near-horizontal lines land there too.)
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                mx, my = (pts[i][0] + pts[j][0]) / 2, (pts[i][1] + pts[j][1]) / 2
                dd = float(np.hypot(*(pts[i] - pts[j])))
                if not (width <= dd <= 1.6 * width):
                    continue
                k = int(np.argmin(np.abs(xg - mx)))
                if abs(xg[k] - mx) <= anchor_tol:
                    anchors[k].append(my)
    seg_fit = [None] * (N - 1)
    for k in range(N - 1):
        P = seg_pieces[k]
        if not P:
            continue
        if len(P) >= 2:  # consensus: drop pieces whose direction disagrees with the longest piece by > 3 deg
            def ang(pr):
                v = pr[1] - pr[0]
                return math.atan2(v[1], v[0]) % math.pi
            ref = ang(max(P, key=lambda pr: np.hypot(*(pr[1] - pr[0]))))
            keep = [pr for pr in P if min(abs(ang(pr) - ref), math.pi - abs(ang(pr) - ref)) < math.radians(3)]
            if len(keep) < len(P):
                nbad += len(P) - len(keep)
                if verbose:
                    print(f"  segment {k}: dropped {len(P) - len(keep)} piece(s) with inconsistent direction")
                P = keep
        A = np.array([p for pr in P for p in pr])
        c = A.mean(axis=0)
        if len(A) >= 4 and np.ptp(A[:, 0]) + np.ptp(A[:, 1]) > 0.5:
            _, _, vt = np.linalg.svd(A - c)
            u = vt[0]
        else:
            u = P[0][1] - P[0][0]
            u = u / np.hypot(*u)
        if u[0] < 0:
            u = -u
        if abs(u[0]) < 1e-6:
            u = np.array([1e-6, 1.0 if u[1] >= 0 else -1.0])
            u = u / np.hypot(*u)
        seg_fit[k] = dict(c=c, u=u, cov=(float(A[:, 0].min()), float(A[:, 0].max())))

    def ev(fit, x):
        c, u = fit["c"], fit["u"]
        return float(c[1] + (x - c[0]) * u[1] / u[0])

    y = np.full(N, np.nan)
    code = [""] * N
    disc = np.full(N, np.nan)
    for k in range(N):
        cands = []
        if k > 0 and seg_fit[k - 1] is not None:
            f = seg_fit[k - 1]
            cands.append((max(0.0, xg[k] - f["cov"][1]), ev(f, xg[k])))
        if k < N - 1 and seg_fit[k] is not None:
            f = seg_fit[k]
            cands.append((max(0.0, f["cov"][0] - xg[k]), ev(f, xg[k])))
        if len(cands) == 2:
            disc[k] = abs(cands[0][1] - cands[1][1])
        if anchors[k]:
            ya = float(np.median(anchors[k]))
            if cands and min(abs(ya - c[1]) for c in cands) < 0.3:
                y[k] = ya
                code[k] = "direct"
                continue
        if not cands:
            continue
        cands.sort(key=lambda c: c[0])
        if len(cands) == 2 and cands[1][0] <= 0.3:
            y[k] = (cands[0][1] + cands[1][1]) / 2
        else:
            y[k] = cands[0][1]
        code[k] = "direct" if cands[0][0] <= 0.3 else "extrap"
    inside = lambda yy: box_y is None or (box_y[0] - 0.05 <= yy <= box_y[1] + 0.05)
    for k in range(N):
        if code[k] in ("direct", "extrap") and not inside(y[k]):  # beyond the axis limit: the line is clipped there
            code[k] = "extrap_offscale"
    # label uncovered vertices
    E = np.array(ends) if ends else np.zeros((0, 3))
    for k in range(N):
        if code[k]:
            continue
        lab = "gap"
        if box_y is not None and len(E):
            yt, yb = box_y
            left = E[E[:, 0] < xg[k]]
            right = E[E[:, 0] > xg[k]]
            if len(left):
                pl = left[np.argmax(left[:, 0])]
                if xg[k] - pl[0] > DASH_LEN:          # more than one gap without any dash: line left the box
                    lab = "clipped"
                if (abs(pl[1] - yb) < 0.08 or abs(pl[1] - yt) < 0.08) and pl[2] > 0.3:  # exits through the boundary
                    lab = "clipped"
            if len(right):
                pr = right[np.argmin(right[:, 0])]
                if (abs(pr[1] - yb) < 0.08 or abs(pr[1] - yt) < 0.08) and pr[2] > 0.3:  # re-enters at the boundary
                    lab = "clipped"
        code[k] = lab
    # interpolate isolated gap vertices between two known on-scale neighbours
    for k in range(1, N - 1):
        if code[k] == "gap" and code[k - 1] in ("direct", "extrap", "interp") and code[k + 1] in ("direct", "extrap") \
                and inside(y[k - 1]) and inside(y[k + 1]):
            y[k] = (y[k - 1] + y[k + 1]) / 2
            code[k] = "interp"
    return dict(y=y, code=code, disc=disc, nbad=nbad, seg_fit=seg_fit)


# ------------------------------------------------------------------ bands

def band_edges(poly, xgrid, line_y, ytop, ybot, tol=0.012):
    """Upper/lower edge of a band polygon per grid x. Returns (lo_y, hi_y, flag) in PDF y (lo_y is the
    larger y). flags: '' | 'hi_clipped' | 'lo_clipped' | 'hi_clipped+lo_clipped' | 'degenerate' | 'absent'."""
    P = np.array(poly)
    if len(P) > 1 and np.allclose(P[0], P[-1], atol=1e-6):
        P = P[:-1]  # drop the repeated closing vertex
    N = len(xgrid)
    lo = np.full(N, np.nan)
    hi = np.full(N, np.nan)
    flag = [""] * N
    for k, x in enumerate(xgrid):
        ys = P[np.abs(P[:, 0] - x) <= tol, 1]
        if len(ys) == 0:
            flag[k] = "absent"
            continue
        if len(ys) == 1:
            ly = line_y[k] if line_y is not None else np.nan
            if k in (0, N - 1) or (not np.isnan(ly) and abs(ys[0] - ly) < 0.03):
                lo[k] = hi[k] = ys[0]
                flag[k] = "degenerate"
            elif np.isnan(ly) and flag[k - 1] in ("lo_clipped", "hi_clipped"):
                if flag[k - 1] == "lo_clipped":
                    hi[k], lo[k], flag[k] = ys[0], ybot, "lo_clipped"
                else:
                    lo[k], hi[k], flag[k] = ys[0], ytop, "hi_clipped"
            elif ys[0] <= ly:
                hi[k], lo[k], flag[k] = ys[0], ybot, "lo_clipped"
            else:
                lo[k], hi[k], flag[k] = ys[0], ytop, "hi_clipped"
            continue
        hi[k], lo[k] = ys.min(), ys.max()
        f = []
        if abs(hi[k] - ytop) < 0.05:
            f.append("hi_clipped")
            hi[k] = ytop
        if abs(lo[k] - ybot) < 0.05:
            f.append("lo_clipped")
            lo[k] = ybot
        flag[k] = "+".join(f)
    return lo, hi, flag


# ------------------------------------------------------------------ panel extraction

def _classify(draws, colors):
    """Split draws into solid strokes, dash fills and bands per colour (keeps draw order index)."""
    out = {c: dict(solid=[], dash=[], band=[]) for c in colors}
    for i, d in enumerate(draws):
        if d["kind"] == "stroke":
            c = pp.hexcolor(d["color"])
            if c in out and len(d["points"]) >= 20:
                out[c]["solid"].append((i, d))
        elif d["kind"] == "fill":
            c = pp.hexcolor(d["fill"])
            if c not in out:
                continue
            op = d["raw"].get("fill_opacity")
            if op is None or op >= 0.99:
                out[c]["dash"].append((i, d))
            else:
                out[c]["band"].append((i, d))
    return out


def extract_panel(page, clip, xticks, xtick_region, yticks, ytick_region, series, nsamples, verbose=True):
    """series: list of dict(name, color, style in {'solid','dashed'}, band=bool).
    Returns dict(xax, yax, xgrid, n, data={name: dict(y=data values, code=..., lo=..., hi=..., bflag=...)})"""
    draws = pp.drawings(page, clip)
    xax = pp.axis_from_ticks(draws, "x", xticks, region=xtick_region)
    yax = pp.axis_from_ticks(draws, "y", yticks, region=ytick_region)
    if verbose:
        print("  x axis:", xax)
        print("  y axis:", yax)
    xgrid = np.array([xax.inv(k) for k in range(1, nsamples + 1)])
    ytop, ybot = yax.inv(yticks[-1]), yax.inv(yticks[0])
    colors = sorted(set(s["color"] for s in series))
    cl = _classify(draws, colors)
    data = {}
    pdfy = {}
    owners = {}  # draw index of the line draw -> series name (for band matching)
    for s in series:
        c = cl[s["color"]]
        if s["style"] == "solid":
            assert len(c["solid"]) == 1, (s["name"], len(c["solid"]))
            i, d = c["solid"][0]
            pts = np.array(d["points"])
            assert len(pts) >= nsamples
            pts = pts[:nsamples]
            dx = np.abs(pts[:, 0] - xgrid).max()
            assert dx < 0.03, f"{s['name']}: stroke vertices off the x grid by {dx:.3f} pt"
            yy = pts[:, 1]
            pdfy[s["name"]] = yy
            data[s["name"]] = dict(y=np.array([yax(v) for v in yy]), code=["direct"] * nsamples, disc=np.full(nsamples, np.nan))
            owners[i] = s["name"]
            if verbose:
                print(f"  {s['name']}: solid stroke draw[{i}], {len(d['points'])} pts (x grid max dev {dx:.3f} pt)")
        else:
            assert c["dash"], (s["name"], "no dash fills")
            polys = [sp for i, d in c["dash"] for sp in d["subpaths"]]
            r = recover_dashed(polys, xgrid, box_y=(ytop, ybot), verbose=verbose)
            yy = r["y"]
            pdfy[s["name"]] = yy
            data[s["name"]] = dict(y=np.array([yax(v) if not np.isnan(v) else np.nan for v in yy]), code=r["code"], disc=r["disc"])
            owners[min(i for i, d in c["dash"])] = s["name"]
            if verbose:
                cnt = {k: r["code"].count(k) for k in sorted(set(r["code"]))}
                md = np.nanmax(r["disc"]) if np.any(~np.isnan(r["disc"])) else float("nan")
                print(f"  {s['name']}: dashed, {len(polys)} dash polygons in draws {[i for i, d in c['dash']]}, codes {cnt}, "
                      f"unassigned pieces {r['nbad']}, max adjacent-fit discrepancy {md:.3f} pt")
    # bands: drawn immediately before the line they belong to (same colour)
    for s in series:
        if not s.get("band"):
            continue
        c = cl[s["color"]]
        li = [i for i, nm in owners.items() if nm == s["name"]][0]
        cand = [(i, d) for i, d in c["band"] if i < li]
        assert cand, (s["name"], "no band before line draw", li)
        i, d = max(cand, key=lambda t: t[0])
        assert len(d["subpaths"]) == 1
        lo, hi, flag = band_edges(d["subpaths"][0], xgrid, pdfy[s["name"]], ytop, ybot)
        data[s["name"]]["lo"] = np.array([yax(v) if not np.isnan(v) else np.nan for v in lo])
        data[s["name"]]["hi"] = np.array([yax(v) if not np.isnan(v) else np.nan for v in hi])
        data[s["name"]]["bflag"] = flag
        data[s["name"]]["lo_pdf"], data[s["name"]]["hi_pdf"] = lo, hi
        if verbose:
            cnt = {k: flag.count(k) for k in sorted(set(flag))}
            print(f"  {s['name']}: band draw[{i}] ({len(d['subpaths'][0])} pts, alpha {d['raw'].get('fill_opacity')}), flags {cnt}")
            # validation: the band is symmetric about the line, so its midpoint must equal the line value
            yy = pdfy[s["name"]]
            dev = [abs((lo[k] + hi[k]) / 2 - yy[k]) for k in range(nsamples)
                   if flag[k] == "" and not np.isnan(yy[k]) and not np.isnan(lo[k])]
            if dev:
                print(f"     band-midpoint vs line check over {len(dev)} unclipped vertices: max |dev| {max(dev):.3f} pt, median {np.median(dev):.3f} pt")
        if s["style"] == "dashed":
            # The band is exactly symmetric about the line, so wherever both band edges are unclipped the band
            # midpoint gives the line value to ~0.01 pt (better than the dash recovery): use it, and report how
            # well the independent dash recovery agreed. Where the band collapses to zero height it pins the
            # line too; where it is absent (entirely at/beyond the 0 or 100 boundary) the line sits on that boundary.
            dd = data[s["name"]]
            yy = pdfy[s["name"]]
            agree = {}
            for k in range(nsamples):
                if flag[k] == "":
                    mid = (lo[k] + hi[k]) / 2
                    if not np.isnan(yy[k]):
                        agree.setdefault(dd["code"][k], []).append(abs(yy[k] - mid))
                    yy[k] = mid
                    dd["y"][k] = yax(mid)
                    dd["code"][k] = "band_mid"
            dd["agree"] = {c: (len(v), float(max(v))) for c, v in agree.items()}
            if verbose:
                print("     dash recovery vs band midpoint, by dash-recovery code (n, max |dev| pt): " +
                      ", ".join(f"{c}: ({n}, {m:.3f})" for c, (n, m) in sorted(dd["agree"].items())))
            for k in range(nsamples):
                if dd["code"][k] not in ("gap", "clipped"):
                    continue
                if flag[k] == "degenerate":
                    yy[k] = lo[k]
                elif flag[k] == "absent":
                    known = [j for j in range(nsamples) if not np.isnan(yy[j]) and dd["code"][j] != "band"]
                    if not known:
                        continue
                    j = min(known, key=lambda j: abs(j - k))
                    yy[k] = ybot if abs(yy[j] - ybot) < abs(yy[j] - ytop) else ytop
                else:
                    continue
                dd["y"][k] = yax(yy[k])
                dd["code"][k] = "band"
                lo[k] = hi[k] = yy[k]
            dd["lo"] = np.array([yax(v) if not np.isnan(v) else np.nan for v in lo])
            dd["hi"] = np.array([yax(v) if not np.isnan(v) else np.nan for v in hi])
    return dict(xax=xax, yax=yax, xgrid=xgrid, data=data, pdfy=pdfy, ytop=ytop, ybot=ybot, draws=draws)


def overlay_png(page, clip, res, series, out, dpi=600):
    """QA: original crop with the recovered dashed polylines (red, green=direct, blue=extrap/interp circles)
    and band edges (magenta lo / cyan hi) drawn on top."""
    from PIL import Image, ImageDraw
    pix = page.get_pixmap(clip=clip, dpi=dpi)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    D = ImageDraw.Draw(im)
    s = dpi / 72
    P = lambda x, y: ((x - clip.x0) * s, (y - clip.y0) * s)
    xg = res["xgrid"]
    for sr in series:
        d = res["data"][sr["name"]]
        if sr["style"] == "dashed":
            yy = res["pdfy"][sr["name"]]
            ks = [k for k in range(len(xg)) if not np.isnan(yy[k])]
            for a in range(len(ks) - 1):
                if ks[a + 1] == ks[a] + 1:
                    D.line([P(xg[ks[a]], yy[ks[a]]), P(xg[ks[a + 1]], yy[ks[a + 1]])], fill=(255, 0, 0), width=2)
            for k in ks:
                x_, y_ = P(xg[k], yy[k])
                col = (0, 200, 0) if d["code"][k] == "direct" else (0, 0, 255)
                D.ellipse([x_ - 4, y_ - 4, x_ + 4, y_ + 4], outline=col, width=2)
        if sr.get("band"):
            for arr, col in ((d["lo_pdf"], (255, 0, 255)), (d["hi_pdf"], (0, 180, 180))):
                ks = [k for k in range(len(xg)) if not np.isnan(arr[k])]
                for a in range(len(ks) - 1):
                    if ks[a + 1] == ks[a] + 1:
                        D.line([P(xg[ks[a]], arr[ks[a]]), P(xg[ks[a + 1]], arr[ks[a + 1]])], fill=col, width=1)
    im.save(out)


def compare_png(orig_png, redraw_png, out):
    subprocess.run(["convert", orig_png, "-resize", "600x", redraw_png, "-resize", "600x", "+append", out], check=True)


def fmt(v, nd=2):
    if v is None or (isinstance(v, (float, np.floating)) and np.isnan(v)):
        return ""
    v = float(v)
    if abs(v) < 0.5 * 10 ** (-nd):
        v = 0.0
    return f"{v:.{nd}f}"
