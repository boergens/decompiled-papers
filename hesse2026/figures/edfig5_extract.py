"""Extract all plot panels of Extended Data Figs 5 and 6 into CSVs (+ 300-dpi original crops for QA)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import sys, itertools, json
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools")
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work")
os.makedirs(SCR, exist_ok=True)
sys.path.insert(0, TOOLS); sys.path.insert(0, SCR)
import numpy as np
import pdfplot as pp, dashgeo as _dg
class dashgeo:
    _edges = staticmethod(_dg._edges); parse_polygon = staticmethod(_dg.parse_polygon)
    @staticmethod
    def recover(subs, xv, w, **kw):
        r = _dg.recover(subs, xv, w, **kw)
        r['n_blanked'] = 0
        return r


def dashgeo_slice(poly, x):
    ys = []
    for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
        if x0 == x1:
            continue
        if (x0 <= x < x1) or (x1 <= x < x0):
            ys.append(y0 + (x - x0) / (x1 - x0) * (y1 - y0))
    return ys
SE_MAX = 3.0  # % units: recovered dashed values with larger uncertainty are blanked
from collections import Counter
PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "2026.10.15.759299v1.full.pdf")
ROOT = os.path.dirname(os.path.abspath(__file__))
COL = {"#1c0f29": "priming_average", "#fcae34": "state1", "#543379": "state2"}
REPORT = {}

def fmt(v, nd=2):
    return "" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{nd}f}"

def xgrid_from_stroke(d, expected):
    pts = np.array(d["points"])
    if len(pts) == expected + 1 and pts[-1, 0] - pts[-2, 0] < 0.05:
        dup = pts[-1]; pts = pts[:-1]
        return pts, dup
    assert len(pts) == expected, (len(pts), expected)
    return pts, None

def se_to_pct(se, yax):
    return np.abs(se * yax.slope)

def blank_uncertain(r, yax):
    sep = se_to_pct(r["se"], yax)
    bad = np.isnan(r["y"]) | np.isnan(sep) | (sep > SE_MAX)
    r["n_blanked"] = int((bad & ~np.isnan(r["y"])).sum())
    r["y"] = np.where(bad, np.nan, r["y"]); r["se"] = np.where(bad, np.nan, r["se"])
    return r

# ------------------------------------------------------------------ explained-variance panels (EDF5 b,e; EDF6 b)
def panel_feature(pno, clip, xreg, yreg, figid, letter):
    page = pp.open_page(PDF, pno)
    out = f"{ROOT}/{figid}{letter}"
    pp.render(page, clip, 300, f"{ROOT}/{figid}{letter}_orig.png")
    draws = pp.drawings(page, clip, how="inside")
    xax = pp.axis_from_ticks(draws, "x", [10, 20, 30, 40, 50], region=xreg)
    yax = pp.axis_from_ticks(draws, "y", [-100, -50, 0, 50, 100], region=yreg)
    solids = {pp.hexcolor(d["color"]): d for d in draws if d["kind"] == "stroke" and d["n_items"] in (49, 50) and pp.hexcolor(d["color"]) in COL}
    assert len(solids) == 3, solids.keys()
    grids = {}; dups = {}
    for c, d in solids.items():
        grids[c], dups[c] = xgrid_from_stroke(d, 50)
    xverts = grids["#1c0f29"][:, 0]
    for c in grids:
        assert np.allclose(grids[c][:, 0], xverts, atol=0.02)
    feat = np.array([xax(x) for x in xverts])
    assert np.allclose(feat, np.arange(1, 51), atol=0.02), feat[:3]
    solid_rng = {COL[c]: (round(float(yax(g[:, 1].max())), 2), round(float(yax(g[:, 1].min())), 2)) for c, g in grids.items()}
    print("   solid line value ranges (min,max):", solid_rng)
    dashed = {}
    for c in ("#fcae34", "#543379"):
        subs = [sp for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == c and d["raw"].get("fill_opacity", 1) == 1 for sp in d["subpaths"]]
        r = blank_uncertain(dashgeo.recover(subs, xverts, 1.0, clip_y=[yax.inv(-100), yax.inv(100)]), yax)
        dashed[c] = r
    # shape/appearance brackets
    br = sorted([(xax(d["rect"][0]), xax(d["rect"][2])) for d in draws if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == "#000000" and d["has_curves"] and d["width"] == 0.5])
    hdr = ["feature_index", "priming_average_pct", "binocular_conscious_state1_pct", "binocular_conscious_state2_pct",
           "binocular_suppressed_state1_pct", "binocular_suppressed_state1_se_pct", "binocular_suppressed_state2_pct", "binocular_suppressed_state2_se_pct"]
    rows = []
    for i in range(50):
        r1, r2 = dashed["#fcae34"], dashed["#543379"]
        rows.append([i + 1, fmt(yax(grids["#1c0f29"][i, 1])), fmt(yax(grids["#fcae34"][i, 1])), fmt(yax(grids["#543379"][i, 1])),
                     fmt(yax(r1["y"][i])), fmt(se_to_pct(r1["se"][i], yax)), fmt(yax(r2["y"][i])), fmt(se_to_pct(r2["se"][i], yax))])
    meth = {c: Counter(dashed[c]["method"]) for c in dashed}
    maxse = {c: float(np.nanmax(se_to_pct(dashed[c]["se"], yax))) for c in dashed}
    nnan = {c: int(np.isnan(dashed[c]["y"]).sum()) for c in dashed}
    below = {c: int(np.sum(np.nan_to_num(np.array([yax(v) for v in dashed[c]["y"]]), nan=0) < -100)) for c in dashed}
    comments = [
        f"Extended Data Figure {figid[-1]}, panel {letter} (PDF page {pno}, clip x={clip.x0:.0f}-{clip.x1:.0f}, y={clip.y0:.0f}-{clip.y1:.0f} pt): explained variance of face features vs feature index.",
        "Series: priming_average = black solid line (priming stimulus features from average priming activity); binocular_conscious_state1/2 = orange/purple solid lines; binocular_suppressed_state1/2 = orange/purple dashed lines (legend names).",
        "Solid lines: 50-point stroke paths read directly (one vertex per feature). Dashed lines were exported as filled dash polygons; the centre line was recovered geometrically (vertex points contained in the dash outlines are exact; vertices falling in dash gaps were solved from the dash-pattern gap length (4.000 pt) and the adjacent segments' directions). *_se_pct = estimated uncertainty of each recovered dashed value in % units (0 = read exactly, coordinate precision ~0.02 pt = 0.04 %).",
        f"x axis calibrated on tick marks at features 10,20,30,40,50 (residual {xax.resid:.2e} pt); y axis on ticks -100,-50,0,50,100 (residual {yax.resid:.2e} pt). 1 % = {abs(1/yax.slope):.3f} pt.",
        f"Shape/Appearance brackets above the plot span features {br[0][0]:.1f}-{br[0][1]:.1f} (Shape) and {br[1][0]:.1f}-{br[1][1]:.1f} (Appearance) in x-axis units.",
        f"Dashed-line recovery: state1 methods {dict(meth['#fcae34'])}, max se {maxse['#fcae34']:.2f} %, empty {nnan['#fcae34']} (of which {dashed['#fcae34']['n_blanked']} blanked for se > {SE_MAX} %); state2 methods {dict(meth['#543379'])}, max se {maxse['#543379']:.2f} %, empty {nnan['#543379']} (of which {dashed['#543379']['n_blanked']} blanked for se > {SE_MAX} %). Empty = not recoverable from the PDF.",
    ]
    if below["#fcae34"] or below["#543379"]:
        comments.append(f"Values below -100 % are outside the plotted axis range (the original line is clipped at -100 there); they are extrapolations of the visible straight segments to the vertex and carry the stated se. Count: state1 {below['#fcae34']}, state2 {below['#543379']}.")
    if any(v is not None for v in dups.values()):
        comments.append("The solid-line strokes contain a near-duplicate 51st point 0.01 pt right of feature 50 (same value); it was dropped.")
    pp.write_csv(out + ".csv", hdr, rows, comments)
    REPORT[figid + letter] = dict(type="feature", xax=repr(xax), yax=repr(yax), methods=meth, maxse=maxse, nnan=nnan, below=below, brackets=br, dups={c: (v is not None) for c, v in dups.items()})
    print(f"{figid}{letter}: x {xax.resid:.1e} y {yax.resid:.1e}; dashed: s1 {dict(meth['#fcae34'])} maxse {maxse['#fcae34']:.2f} nan {nnan['#fcae34']} below {below['#fcae34']}; s2 {dict(meth['#543379'])} maxse {maxse['#543379']:.2f} nan {nnan['#543379']} below {below['#543379']}; brackets {np.round(br,2).tolist()}")
    return dashed, xverts, yax

# ------------------------------------------------------------------ decoding-accuracy panels (EDF5 c,f; EDF6 c)
def panel_decoding(pno, clip, xreg, yreg, figid, letter):
    page = pp.open_page(PDF, pno)
    out = f"{ROOT}/{figid}{letter}"
    pp.render(page, clip, 300, f"{ROOT}/{figid}{letter}_orig.png")
    draws = pp.drawings(page, clip, how="inside")
    xax = pp.axis_from_ticks(draws, "x", [0, 20, 40, 60], region=xreg)
    yax = pp.axis_from_ticks(draws, "y", [0, 20, 40, 60, 80, 100], region=yreg)
    solids = {pp.hexcolor(d["color"]): d for d in draws if d["kind"] == "stroke" and d["n_items"] in (59, 60) and pp.hexcolor(d["color"]) in COL}
    assert len(solids) == 3
    grids = {c: xgrid_from_stroke(d, 60)[0] for c, d in solids.items()}
    xverts = grids["#1c0f29"][:, 0]
    for c in grids:
        assert np.allclose(grids[c][:, 0], xverts, atol=0.02)
    nf = np.array([xax(x) for x in xverts]); assert np.allclose(nf, np.arange(1, 61), atol=0.03), nf[:3]
    # bands: single-subpath fills with opacity 0.2
    bands = []
    for d in draws:
        if d["kind"] == "fill" and len(d["subpaths"]) == 1 and len(d["points"]) > 60 and abs(d["raw"].get("fill_opacity", 1) - 0.2) < 0.01:
            poly = [(xax(x), yax(y)) for x, y in d["points"]]
            if poly[0] != poly[-1]:
                poly.append(poly[0])
            env = {}
            for k in range(1, 61):
                xs_ = k + 1e-4 if k == 1 else k - 1e-4
                ys_ = dashgeo_slice(poly, xs_)
                if len(ys_) >= 2:
                    env[k] = (max(0.0, float(min(ys_))), min(100.0, float(max(ys_))))   # clip-rectangle edges sit ~0.02 % outside the axes
            bands.append(dict(color=pp.hexcolor(d["fill"]), env=env, n=len(d["points"]), offint=[]))
    # dashed lines (opacity 1, multiple subpaths)
    dashed = {}
    for c in ("#fcae34", "#543379"):
        subs = [sp for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == c and d["raw"].get("fill_opacity", 1) == 1 for sp in d["subpaths"]]
        dashed[c] = blank_uncertain(dashgeo.recover(subs, xverts, 1.0, clip_y=[yax.inv(0), yax.inv(100)]), yax)
    # assign bands to series: nearest line (solid or dashed) by mean absolute distance of band centre
    series = {"priming_average": ("#1c0f29", np.array([yax(y) for y in grids["#1c0f29"][:, 1]])),
              "binocular_conscious_state1": ("#fcae34", np.array([yax(y) for y in grids["#fcae34"][:, 1]])),
              "binocular_conscious_state2": ("#543379", np.array([yax(y) for y in grids["#543379"][:, 1]])),
              "binocular_suppressed_state1": ("#fcae34", np.array([yax(v) for v in dashed["#fcae34"]["y"]])),
              "binocular_suppressed_state2": ("#543379", np.array([yax(v) for v in dashed["#543379"]["y"]]))}
    band_of = {}
    for b in bands:
        best = None
        for name, (c, vals) in series.items():
            if c != b["color"]:
                continue
            ks = [k for k in b["env"] if not np.isnan(vals[k - 1]) and b["env"][k][0] > 0.05 and b["env"][k][1] < 99.95]
            # a band is symmetric about its line: score = mean |midpoint - line| over unclipped faces
            score = np.mean([abs((b["env"][k][0] + b["env"][k][1]) / 2 - vals[k - 1]) for k in ks]) if ks else 99
            if best is None or score < best[0]:
                best = (score, name)
        assert best[1] not in band_of, "two bands for one series"
        band_of[best[1]] = (b, best[0])
    hdr = ["n_faces"]
    for name in series:
        hdr += [f"{name}_pct"] + ([f"{name}_se_pct"] if "suppressed" in name else []) + [f"{name}_band_lo_pct", f"{name}_band_hi_pct"]
    rows = []
    for i in range(60):
        row = [i + 1]
        for name, (c, vals) in series.items():
            row.append(fmt(vals[i]))
            if "suppressed" in name:
                row.append(fmt(se_to_pct(dashed[c]["se"][i], yax)))
            env = band_of[name][0]["env"] if name in band_of else {}
            lo, hi = env.get(i + 1, (np.nan, np.nan))
            row += [fmt(lo), fmt(hi)]
        rows.append(row)
    clipnote = []
    for name, (b, sc) in band_of.items():
        if b["offint"]:
            clipnote.append(f"{name}: {len(b['offint'])} band-polygon vertices at non-integer x (where the axis clip cuts the band, e.g. {b['offint'][:3]}) were ignored.")
        ks = sorted(b["env"]); 
        at0 = [k for k in ks if abs(b["env"][k][0]) < 0.05]
        if at0 or ks[-1] < 60:
            clipnote.append(f"{name}: band polygon covers faces {ks[0]}-{ks[-1]}" + (f", lower edge clipped at 0 % for faces {at0[0]}-{at0[-1]}" if at0 else "") + ".")
    meth = {c: Counter(dashed[c]["method"]) for c in dashed}
    maxse = {c: float(np.nanmax(se_to_pct(dashed[c]["se"], yax))) for c in dashed}
    comments = [
        f"Extended Data Figure {figid[-1]}, panel {letter} (PDF page {pno}, clip x={clip.x0:.0f}-{clip.x1:.0f}, y={clip.y0:.0f}-{clip.y1:.0f} pt): decoding accuracy (%) vs number of faces (1-60).",
        "Series (legend names): priming_average = black solid; binocular_conscious_state1/2 = orange/purple solid; binocular_suppressed_state1/2 = orange/purple dashed. *_band_lo/hi = lower/upper edge of the shaded band (fill opacity 0.2) drawn around that line; the legend does not state whether the band is SD or SEM across the 30 stimulus pairs.",
        "Band edges that coincide with the axis limits (the band is clipped there) are reported as 0 or 100.",
        "Solid lines: 60-point strokes read directly. Dashed lines: exported as filled dash polygons, centre line recovered geometrically (vertex points in the outline are exact; gap vertices from the 4.000-pt dash-pattern gap length and adjacent segment directions); *_se_pct = estimated uncertainty in % units.",
        f"x axis calibrated on ticks 0,20,40,60 (residual {xax.resid:.2e} pt); y axis on ticks 0,20,...,100 (residual {yax.resid:.2e} pt); 1 % = {abs(1/yax.slope):.3f} pt.",
        f"Band assignment/validation: each band polygon was matched to the same-colour line it is symmetric about (mean |band midpoint - line| over unclipped faces {', '.join(f'{n}: {sc:.2f} %' for n, (b, sc) in band_of.items())}).",
        f"Dashed-line recovery: state1 methods {dict(meth['#fcae34'])}, max se {maxse['#fcae34']:.2f} %, empty {int(np.isnan(dashed['#fcae34']['y']).sum())} (blanked for se > {SE_MAX} %: {dashed['#fcae34']['n_blanked']}); state2 methods {dict(meth['#543379'])}, max se {maxse['#543379']:.2f} %, empty {int(np.isnan(dashed['#543379']['y']).sum())} (blanked: {dashed['#543379']['n_blanked']}). Empty = not recoverable from the PDF.",
    ] + clipnote
    pp.write_csv(out + ".csv", hdr, rows, comments)
    REPORT[figid + letter] = dict(type="decoding", xax=repr(xax), yax=repr(yax), methods=meth, maxse=maxse, bands={n: (len(b["env"]), sc) for n, (b, sc) in band_of.items()}, clipnote=clipnote)
    print(f"{figid}{letter}: x {xax.resid:.1e} y {yax.resid:.1e}; bands {[(n, len(b['env']), round(sc,3)) for n,(b,sc) in band_of.items()]}; dashed s1 {dict(meth['#fcae34'])} maxse {maxse['#fcae34']:.2f}; s2 {dict(meth['#543379'])} maxse {maxse['#543379']:.2f}; {clipnote}")

# ------------------------------------------------------------------ EDF6 d: time courses
def panel_timecourse(pno, clip, figid, letter):
    page = pp.open_page(PDF, pno)
    out = f"{ROOT}/{figid}{letter}"
    pp.render(page, clip, 300, f"{ROOT}/{figid}{letter}_orig.png")
    draws = pp.drawings(page, clip, how="inside")
    sub = {"average": ("#808080", pp.R(283, 232.6, 330, 235), pp.R(281, 187, 283.7, 234)),
           "state1": ("#fcae34", pp.R(283, 297.8, 330, 300), pp.R(281, 252, 283.6, 299)),
           "state2": ("#543379", pp.R(343, 297.5, 390, 300), pp.R(341, 252, 344, 299))}
    data = {}; notes = []
    for name, (c, xreg, yreg) in sub.items():
        xax = pp.axis_from_ticks(draws, "x", [0, 1, 2], region=xreg)
        yax = pp.axis_from_ticks(draws, "y", [0, 50, 100], region=yreg)
        solid = [d for d in draws if d["kind"] == "stroke" and d["n_items"] == 211 and pp.hexcolor(d["color"]) == c][0]
        pts, dup = xgrid_from_stroke(solid, 211)
        t = np.array([xax(x) for x in pts[:, 0]])
        assert np.allclose(t, -0.1 + 0.01 * np.arange(211), atol=0.004), (t[:3], t[-3:])
        subs = [sp for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == c and d["n_items"] > 300 for sp in d["subpaths"]]
        r = dashgeo.recover(subs, pts[:, 0], 1.0, clip_y=[yax.inv(0), yax.inv(100)])
        # keep only well-determined values (se <= 0.5 pt ~ 1.1 %)
        ysup = np.array([yax(v) for v in r["y"]]); sesup = se_to_pct(r["se"], yax)
        bad = np.isnan(ysup) | (sesup > SE_MAX)
        ysup[bad] = np.nan; sesup[bad] = np.nan
        runs = [len(list(g)) for k, g in itertools.groupby(bad) if k]
        data[name] = dict(t=t, cons=np.array([yax(y) for y in pts[:, 1]]), sup=ysup, se=sesup, xax=xax, yax=yax, dup=dup is not None,
                          n_ok=int((~bad).sum()), n_exact=int(sum(1 for m, b in zip(r["method"], bad) if m.startswith("vertex") and not b)), longest_gap=max(runs) if runs else 0, methods=Counter(r["method"]))
        print(f"{figid}{letter} {name}: x {xax.resid:.1e} y {yax.resid:.1e}; dup {dup is not None}; suppressed recovered {data[name]['n_ok']}/211 (exact {data[name]['n_exact']}), longest NaN run {data[name]['longest_gap']}, methods {dict(data[name]['methods'])}")
    hdr = ["time_from_flash_s"]
    for name in sub:
        hdr += [f"{name}_conscious_pct", f"{name}_suppressed_pct", f"{name}_suppressed_se_pct"]
    rows = []
    for i in range(211):
        row = [f"{data['average']['t'][i]:.2f}"]
        for name in sub:
            row += [fmt(data[name]["cons"][i]), fmt(data[name]["sup"][i]), fmt(data[name]["se"][i])]
        rows.append(row)
    comments = [
        f"Extended Data Figure 6, panel d (PDF page {pno}, clip x={clip.x0:.0f}-{clip.x1:.0f}, y={clip.y0:.0f}-{clip.y1:.0f} pt): single-trial decoding accuracy (%) vs time from flash, three sub-panels (Average = grey, State 1 = orange, State 2 = purple); solid = decoded identity compared to the conscious stimulus, dashed = compared to the suppressed stimulus.",
        "Time axis: the printed axis label reads 'Time from flash (ms)' but the ticks are 0, 1, 2 and the lines have 211 samples spaced 0.01 axis units from -0.1 to 2.0; the unit is therefore seconds (the same window is labelled 'seconds' in Fig. 2c). Column time_from_flash_s gives seconds.",
        "Conscious (solid) lines: 211-point strokes read directly (a near-duplicate 212th point 0.005 pt right of the last sample was dropped). Suppressed (dashed) lines were exported as filled dash polygons: samples inside a dash are exact (the dash outline contains the vertex); samples inside a dash gap (pattern 4 pt on / 4 pt off along the path) are unrecoverable and left empty, except the first sample beyond a dash end, which was extrapolated along the dash's end segment when its uncertainty was <= 3 % (uniform rule for all dashed values in these figures). *_suppressed_se_pct = estimated uncertainty (% units); empty = not recovered.",
    ]
    for name in sub:
        d = data[name]
        comments.append(f"{name}: x ticks 0,1,2 (residual {d['xax'].resid:.2e} pt), y ticks 0,50,100 (residual {d['yax'].resid:.2e} pt), 1 % = {abs(1/d['yax'].slope):.3f} pt; suppressed samples recovered {d['n_ok']}/211 ({d['n_exact']} exact), longest run of missing samples {d['longest_gap']} (= {d['longest_gap']*10} ms).")
    pp.write_csv(out + ".csv", hdr, rows, comments)
    REPORT[figid + letter] = dict(type="timecourse", **{n: dict(n_ok=d["n_ok"], n_exact=d["n_exact"], longest_gap=d["longest_gap"], xax=repr(d["xax"]), yax=repr(d["yax"])) for n, d in data.items()})

# ------------------------------------------------------------------ EDF6 e: paired plot
def panel_paired(pno, clip, figid, letter):
    page = pp.open_page(PDF, pno)
    out = f"{ROOT}/{figid}{letter}"
    pp.render(page, clip, 300, f"{ROOT}/{figid}{letter}_orig.png")
    draws = pp.drawings(page, clip, how="inside")
    xt = pp.tick_marks(draws, "x", region=pp.R(413, 297.6, 519, 301))
    assert len(xt) == 3, xt
    xcat = np.array([t["pos"] for t in xt])
    yax = pp.axis_from_ticks(draws, "y", [0, 20, 40, 60, 80, 100], region=pp.R(410, 185, 413.6, 299))
    thin_solid = [d for d in draws if d["kind"] == "stroke" and d["n_items"] == 2 and d["width"] < 0.5]
    thick_solid = [d for d in draws if d["kind"] == "stroke" and d["n_items"] == 2 and d["width"] >= 0.5]
    assert len(thin_solid) == 10 and len(thick_solid) == 1
    fills = [d for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#000000" and len(d["subpaths"]) >= 5]
    assert len(fills) == 11
    def width_of(d):
        Ls = sorted(e["L"] for sp in d["subpaths"] for e in dashgeo._edges(sp)[1])
        return 1.0 if any(0.45 < L < 0.55 for L in Ls) and not any(0.09 < L < 0.11 for L in Ls) else 0.1
    thick_dashed = [d for d in fills if width_of(d) == 1.0]; thin_dashed = [d for d in fills if width_of(d) == 0.1]
    assert len(thick_dashed) == 1 and len(thin_dashed) == 10
    def vals_stroke(d):
        pts = np.array(d["points"]); assert np.allclose(pts[:, 0], xcat, atol=0.05); return [yax(y) for y in pts[:, 1]]
    rows = []; ses = []
    for k, d in enumerate(thin_solid):
        rows.append([k + 1, "conscious"] + [fmt(v) for v in vals_stroke(d)] + ["", "", ""])
    for k, d in enumerate(thin_dashed):
        r = dashgeo.recover(d["subpaths"], xcat, 0.1)
        rows.append([k + 1, "suppressed"] + [fmt(yax(v)) for v in r["y"]] + [fmt(se_to_pct(s, yax)) for s in r["se"]])
        ses.append(se_to_pct(r["se"], yax))
    mean_c = vals_stroke(thick_solid[0])
    r = dashgeo.recover(thick_dashed[0]["subpaths"], xcat, 1.0); mean_s = [yax(v) for v in r["y"]]
    rows.append(["mean", "conscious"] + [fmt(v) for v in mean_c] + ["", "", ""])
    rows.append(["mean", "suppressed"] + [fmt(v) for v in mean_s] + [fmt(se_to_pct(s, yax)) for s in r["se"]])
    # markers
    marks = []
    for d in draws:
        if d["kind"] == "fill" and d["has_curves"] and d["n_items"] == 8 and pp.hexcolor(d["fill"]) in ("#808080", "#fcae34", "#543379"):
            x0, y0, x1, y1 = d["rect"]; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            # filled or open: is there a same-colour 4-item disc or a white disc at the centre?
            disc = [e for e in draws if e["kind"] == "fill" and e["has_curves"] and e["n_items"] == 4 and abs((e["rect"][0] + e["rect"][2]) / 2 - cx) < 0.3 and abs((e["rect"][1] + e["rect"][3]) / 2 - cy) < 0.3]
            kind = "open" if disc and pp.hexcolor(disc[0]["fill"]) == "#ffffff" else "filled"
            marks.append((pp.hexcolor(d["fill"]), kind, int(np.argmin(np.abs(xcat - cx))), yax(cy)))
    # consistency: session means vs thick lines
    cons = np.array([[float(v) for v in r[2:5]] for r in rows if r[1] == "conscious" and r[0] != "mean"])
    supp = np.array([[float(v) if v else np.nan for v in r[2:5]] for r in rows if r[1] == "suppressed" and r[0] != "mean"])
    hdr = ["session", "condition", "average_pct", "state1_pct", "state2_pct", "average_se_pct", "state1_se_pct", "state2_se_pct"]
    comments = [
        f"Extended Data Figure 6, panel e (PDF page {pno}, clip x={clip.x0:.0f}-{clip.x1:.0f}, y={clip.y0:.0f}-{clip.y1:.0f} pt): single-trial decoding accuracy (%) per session for activity averaged over the whole trial (Average), state 1 or state 2; condition = decoded identity compared to the conscious (solid lines, filled circles) or suppressed (dashed lines, open circles) stimulus.",
        "Rows session 1-10: thin lines (one per session), numbered in drawing order within each condition; the conscious and suppressed lines of a given session cannot be paired from the PDF (rows with the same number are probably, but not verifiably, the same session). Row 'mean': thick lines (average across the ten sessions).",
        "Conscious values: 3-point strokes read directly. Suppressed values: dashed lines exported as filled dash polygons (thin lines 0.1 pt wide, mean line 1 pt), centre line recovered geometrically; *_se_pct = estimated uncertainty in % units (coordinate precision ~0.02 pt).",
        f"x categories = tick marks at PDF x {', '.join(f'{v:.2f}' for v in xcat)} (Average, State 1, State 2); y axis calibrated on ticks 0,20,...,100 (residual {yax.resid:.2e} pt); 1 % = {abs(1/yax.slope):.3f} pt.",
        f"Consistency check: mean of the 10 session rows = conscious {np.round(cons.mean(0), 2).tolist()} vs thick line {np.round(mean_c, 2).tolist()}; suppressed {np.round(np.nanmean(supp, 0), 2).tolist()} vs thick dashed line {np.round(mean_s, 2).tolist()}.",
        "Circle markers at the mean values: " + "; ".join(f"{c} {k} at x-category {i} = {v:.2f} %" for c, k, i, v in sorted(marks)) + ".",
        "Chance level is 10 % (ten stimulus identities), not drawn.",
    ]
    pp.write_csv(out + ".csv", hdr, rows, comments)
    REPORT[figid + letter] = dict(type="paired", yax=repr(yax), mean_c=mean_c, mean_s=mean_s, sess_mean_c=cons.mean(0).tolist(), sess_mean_s=np.nanmean(supp, 0).tolist(), marks=marks, maxse=float(np.max(ses)))
    print(f"{figid}{letter}: y {yax.resid:.1e}; thick cons {np.round(mean_c,2)} vs session mean {np.round(cons.mean(0),2)}; thick supp {np.round(mean_s,2)} vs {np.round(np.nanmean(supp,0),2)}; max se {np.max(ses):.3f} %; marks {marks}")

# ------------------------------------------------------------------ face grids
def face_grid(pno, clip, figid, letter):
    page = pp.open_page(PDF, pno)
    ims = pp.images(page, clip)
    assert len(ims) == 20, len(ims)
    cols = ["gt_conscious", "recon_state1", "gt_suppressed", "recon_state2"]
    # sort into rows by y, columns by x
    ims.sort(key=lambda im: (round(im["bbox"][1] / 10), im["bbox"][0]))
    rows = [ims[i:i + 4] for i in range(0, 20, 4)]
    files = []
    for r, row in enumerate(rows, 1):
        row.sort(key=lambda im: im["bbox"][0])
        for c, im in enumerate(row):
            fn = f"{figid}{letter}_r{r}_{cols[c]}.png"
            w, h = pp.extract_image(page, im["xref"], f"{ROOT}/{fn}")
            files.append((fn, im["xref"], w, h, tuple(round(v, 1) for v in im["bbox"])))
    REPORT[figid + letter] = dict(type="faces", files=files)
    print(f"{figid}{letter}: {len(files)} images; xrefs by row: {[[f[1] for f in files[i:i+4]] for i in range(0,20,4)]}; sizes {Counter((f[2], f[3]) for f in files)}")

if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    if "all" in which or "edfig5" in which:
        face_grid(45, pp.R(10, 50, 250, 322), "edfig5", "a")
        face_grid(45, pp.R(265, 50, 505, 322), "edfig5", "d")
        panel_feature(45, pp.R(0, 320, 128, 468), pp.R(30, 446.5, 128, 451), pp.R(27, 330, 31.4, 450), "edfig5", "b")
        panel_decoding(45, pp.R(128, 320, 262, 468), pp.R(150, 446.6, 262, 451), pp.R(152, 330, 156.3, 450), "edfig5", "c")
        panel_feature(45, pp.R(256, 320, 385, 468), pp.R(287, 446.5, 385, 451), pp.R(284, 330, 288.2, 450), "edfig5", "e")
        panel_decoding(45, pp.R(385, 320, 519, 468), pp.R(407, 446.6, 519, 451), pp.R(409, 330, 413.1, 450), "edfig5", "f")
    if "all" in which or "edfig6" in which:
        face_grid(46, pp.R(10, 42, 250, 313), "edfig6", "a")
        panel_feature(46, pp.R(256, 14, 385, 161), pp.R(288, 139.4, 385, 143), pp.R(285, 20, 289, 141), "edfig6", "b")
        panel_decoding(46, pp.R(385, 14, 519, 161), pp.R(408, 138.8, 519, 143), pp.R(410, 22, 413.8, 141), "edfig6", "c")
        panel_timecourse(46, pp.R(256, 177, 388, 317), "edfig6", "d")
        panel_paired(46, pp.R(388, 177, 519, 317), "edfig6", "e")
    json.dump(REPORT, open(f"{SCR}/report.json", "w"), indent=1, default=str)
