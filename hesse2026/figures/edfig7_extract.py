"""Extract Extended Data Figure 7 (page 47) panels into figures/."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import helpers as H  # noqa: E402
import pdfplot as pp  # noqa: E402

OUT = os.path.join(H.PROJ, "figures")
page = pp.open_page(H.PDF, 47)
PAGE_NOTE = "source: Hesse et al. 2026 bioRxiv 10.64898/2026.10.15.759299v1, Extended Data Figure 7, PDF page 47 (vector graphics)"

# ------------------------------------------------------------------ a, d: face grids (embedded rasters)
cols = ["gt_conscious", "recon_state1", "gt_suppressed", "recon_state2"]
for letter, x0 in (("a", 0.0), ("d", 256.81)):
    ims = pp.images(page, pp.R(10 + x0, 45, 248 + x0, 316))
    # group into rows by y
    rows = {}
    for im in ims:
        rows.setdefault(round(im["bbox"][1] / 50), []).append(im)
    assert len(rows) == 5, rows.keys()
    for ri, key in enumerate(sorted(rows), start=1):
        r = sorted(rows[key], key=lambda i: i["bbox"][0])
        assert len(r) == 4
        for ci, im in enumerate(r):
            fn = f"edfig7{letter}_r{ri}_{cols[ci]}.png"
            w, h = pp.extract_image(page, im["xref"], os.path.join(OUT, fn))
            print(fn, "xref", im["xref"], f"{w}x{h}", "bbox", [round(v, 1) for v in im["bbox"]])

# ------------------------------------------------------------------ b, e: explained variance per feature
SERIES_BE = {  # (kind, colour) -> name; colours read from the paths
    ("stroke", "#1c0f29"): "priming_average",
    ("stroke", "#fcae34"): "binocular_conscious_state1",
    ("stroke", "#543379"): "binocular_conscious_state2",
    ("fill", "#fcae34"): "binocular_suppressed_state1",
    ("fill", "#543379"): "binocular_suppressed_state2",
}


def extract_be(letter, dx):
    clip = pp.R(2 + dx, 316, 128 + dx, 463)
    draws = pp.drawings(page, clip)
    xax = pp.axis_from_ticks(draws, "x", [10, 20, 30, 40, 50], region=pp.R(20 + dx, 442.4, 128 + dx, 446))
    yax = pp.axis_from_ticks(draws, "y", [-100, -50, 0, 50, 100], region=pp.R(27 + dx, 330, 31.4 + dx, 443))
    print(letter, xax, "\n ", yax)
    xgrid = [xax.inv(k) for k in range(1, 51)]
    data = {}
    qa = {}
    for d in draws:
        key = (d["kind"], pp.hexcolor(d["color"] if d["kind"] == "stroke" else d["fill"]))
        if key not in SERIES_BE:
            continue
        name = SERIES_BE[key]
        if d["kind"] == "stroke":
            pts = d["points"]
            xs = [xax(x) for x, y in pts]
            vals = []
            for k in range(1, 51):
                j = min(range(len(pts)), key=lambda j: abs(xs[j] - k))
                assert abs(xs[j] - k) < 0.02, (k, xs[j])
                vals.append(yax(pts[j][1]))
            print(f"  {name}: {len(pts)} points on the stroke (50 vertices used)")
            data[name] = vals
        else:
            ys, spread, nev = H.dashed_polyline2(d, xgrid, w=1.0)
            ys, interp = H.fill_gaps(xgrid, ys)
            data[name] = [yax(y) if not math.isnan(y) else float("nan") for y in ys]
            qa[name] = (spread, nev, interp)
            sp = [s * abs(yax.slope) for s in spread if not math.isnan(s)]
            print(f"  {name}: {len(d['subpaths'])} dashes, vertices recovered {sum(1 for n in nev if n)}/50, "
                  f"max spread {max(sp):.3f} %, mean spread {sum(sp)/len(sp):.3f} %, "
                  f"n-estimates per vertex min {min(nev)} max {max(nev)}")
            big = [(i + 1, round(s * abs(yax.slope), 2)) for i, s in enumerate(spread) if not math.isnan(s) and s * abs(yax.slope) > 0.5]
            if big:
                print("   vertices with spread > 0.5 %:", big)
            miss = [i + 1 for i, n in enumerate(nev) if n == 0]
            if miss:
                print("   vertices inside a dash gap (interpolated):", miss)
    hdr = ["feature_index", "feature_type", "priming_average_ev_pct", "binocular_conscious_state1_ev_pct",
           "binocular_conscious_state2_ev_pct", "binocular_suppressed_state1_ev_pct",
           "binocular_suppressed_state2_ev_pct", "suppressed_state1_n_estimates", "suppressed_state1_spread_pct",
           "suppressed_state2_n_estimates", "suppressed_state2_spread_pct"]
    rows = []
    for i in range(50):
        q1, q2 = qa["binocular_suppressed_state1"], qa["binocular_suppressed_state2"]
        rows.append([i + 1, "shape" if i < 20 else "appearance"] +
                    [round(data[n][i], 3) for n in ["priming_average", "binocular_conscious_state1",
                                                     "binocular_conscious_state2", "binocular_suppressed_state1",
                                                     "binocular_suppressed_state2"]] +
                    [q1[1][i], round(q1[0][i] * abs(yax.slope), 3) if q1[1][i] else "",
                     q2[1][i], round(q2[0][i] * abs(yax.slope), 3) if q2[1][i] else ""])
    comments = [
        PAGE_NOTE + f", panel {letter}",
        "Explained variance (%) of each of the 50 face features (1-20 shape, 21-50 appearance) for five series, see legend",
        "x axis: 5 tick marks calibrated to feature # 10,20,30,40,50 (resid %.1e); vertices lie exactly on integer features 1..50" % xax.resid,
        "y axis: 5 tick marks calibrated to -100,-50,0,50,100 %% (resid %.1e); 1 %% = %.4f pt" % (yax.resid, abs(1 / yax.slope)),
        "solid series (priming_average black #1c0f29, binocular_conscious_state1 orange #fcae34, binocular_conscious_state2 purple #543379): 50-vertex stroke paths, exact to the PDF coordinate precision (0.001 pt = 0.002 %)",
        "dashed series (binocular_suppressed_state1 orange dashed, binocular_suppressed_state2 purple dashed): drawn as filled dash outlines (1 pt wide, 4 pt long butt-capped dashes), not strokes;",
        "  each vertex value is the weighted mean of estimates from the straight dash pieces in the two adjacent inter-vertex intervals (pair of parallel offset edges -> centreline, extrapolated to the vertex x);",
        "  *_n_estimates = number of estimates, *_spread_pct = max-min of those estimates (precision indicator); n_estimates = 0 means the vertex lies inside a dash gap",
        "  with no dash in either adjacent interval: the value is NOT in the PDF and was linearly interpolated between the neighbouring vertices (approximation)",
    ]
    pp.write_csv(os.path.join(OUT, f"edfig7{letter}.csv"), hdr, rows, comments)
    pp.render(page, clip, 300, os.path.join(OUT, f"edfig7{letter}_orig.png"))
    return data, qa


be_b = extract_be("b", 0.0)
be_e = extract_be("e", 256.81)

# ------------------------------------------------------------------ c, f: decoding accuracy vs number of faces
SERIES_CF = {"#1c0f29": "priming_average", "#fcae34": ("binocular_conscious_state1", "binocular_suppressed_state1"),
             "#543379": ("binocular_conscious_state2", "binocular_suppressed_state2")}


def extract_cf(letter, dx):
    clip = pp.R(130 + dx, 316, 258 + dx, 463)
    draws = pp.drawings(page, clip)
    xax = pp.axis_from_ticks(draws, "x", [0, 20, 40, 60], region=pp.R(150 + dx, 441.6, 258 + dx, 446))
    yax = pp.axis_from_ticks(draws, "y", [0, 20, 40, 60, 80, 100], region=pp.R(152 + dx, 329, 156.1 + dx, 442))
    print(letter, xax, "\n ", yax)
    xgrid = [xax.inv(k) for k in range(1, 61)]
    lines, bands, dashed = {}, {}, {}
    for d in draws:
        col = pp.hexcolor(d["color"] if d["kind"] == "stroke" else d["fill"])
        if col not in SERIES_CF:
            continue
        op = d["raw"].get("fill_opacity")
        if d["kind"] == "stroke":
            assert len(d["points"]) == 60
            xs = [xax(x) for x, y in d["points"]]
            assert all(abs(x - (i + 1)) < 0.01 for i, x in enumerate(xs))
            lines.setdefault(col, []).append([yax(y) for x, y in d["points"]])
        elif op is not None and op < 0.5:
            ext = [H.vertical_extent(d["subpaths"][0], x) for x in xgrid]
            lo = [yax(e[1]) if e else float("nan") for e in ext]  # larger PDF y = smaller value
            hi = [yax(e[0]) if e else float("nan") for e in ext]
            bands.setdefault(col, []).append((lo, hi, len(d["points"])))
        else:
            ys, spread, nev = H.dashed_polyline2(d, xgrid, w=1.0)
            ys, interp = H.fill_gaps(xgrid, ys)
            dashed[col] = ([yax(y) if not math.isnan(y) else float("nan") for y in ys], spread, nev)
            sp = [s * abs(yax.slope) for s in spread if not math.isnan(s)]
            print(f"  dashed {col}: {len(d['subpaths'])} dashes, recovered {sum(1 for n in nev if n)}/60, max spread {max(sp):.3f} %, mean {sum(sp)/len(sp):.3f} %")
            miss = [i + 1 for i, n in enumerate(nev) if n == 0]
            if miss:
                print("   vertices inside a dash gap (interpolated):", miss)
    series = {}
    for col, names in SERIES_CF.items():
        if isinstance(names, str):
            (lo, hi, n), = bands[col]
            series[names] = (lines[col][0], lo, hi, None)
            continue
        solid, dsh = lines[col][0], dashed[col][0]
        # assign the two bands to solid / dashed by which centre they track
        assigned = {}
        for (lo, hi, n) in bands[col]:
            mid = [(a + b) / 2 for a, b in zip(lo, hi)]
            ok = [i for i in range(60) if not (math.isnan(mid[i]) or math.isnan(dsh[i]))]
            ds = sum(abs(mid[i] - solid[i]) for i in ok)
            dd = sum(abs(mid[i] - dsh[i]) for i in ok)
            tgt = "solid" if ds < dd else "dashed"
            print(f"  band {col} ({n} pts): dist to solid {ds:.1f}, to dashed {dd:.1f} -> {tgt}")
            assert tgt not in assigned
            assigned[tgt] = (lo, hi)
        series[names[0]] = (solid, *assigned["solid"], None)
        series[names[1]] = (dsh, *assigned["dashed"], dashed[col][2])
    # band symmetry: the band is symmetric about its line, so (lo+hi)/2 == line wherever the band is not clipped
    # at 0 / 100 %. Validation for all series; for the dashed lines also the source of the gap vertices.
    fills = {}
    for n in list(series):
        m, lo, hi, nev = series[n]
        mid = [(a + b) / 2 if not (math.isnan(a) or math.isnan(b)) and a > 0.05 and b < 99.95 else float("nan")
               for a, b in zip(lo, hi)]
        diffs = [abs(mid[i] - m[i]) for i in range(60)
                 if not (math.isnan(mid[i]) or math.isnan(m[i])) and (nev is None or nev[i] > 0)]
        print(f"  band-midpoint check {n}: n={len(diffs)}, max |mid-line| = {max(diffs):.3f} %, mean {sum(diffs)/len(diffs):.3f} %")
        if nev is not None:
            fill = [""] * 60
            for i in range(60):
                if nev[i] == 0:
                    if not math.isnan(mid[i]):
                        m[i] = mid[i]; fill[i] = "band_midpoint"
                    elif not math.isnan(m[i]):
                        fill[i] = "interpolated"
                    else:
                        fill[i] = "none"
            fills[n] = fill
            print(f"    gap vertices of {n}: band_midpoint {[i+1 for i in range(60) if fill[i]=='band_midpoint']}, "
                  f"interpolated {[i+1 for i in range(60) if fill[i]=='interpolated']}, none {[i+1 for i in range(60) if fill[i]=='none']}")
    order = ["priming_average", "binocular_conscious_state1", "binocular_conscious_state2",
             "binocular_suppressed_state1", "binocular_suppressed_state2"]
    hdr = ["number_of_faces"]
    for n in order:
        hdr += [f"{n}_pct", f"{n}_band_lo_pct", f"{n}_band_hi_pct"]
    hdr += ["suppressed_state1_n_estimates", "suppressed_state1_gap_fill", "suppressed_state2_n_estimates", "suppressed_state2_gap_fill"]
    rows = []
    for i in range(60):
        r = [i + 1]
        for n in order:
            m, lo, hi, _ = series[n]
            r += [round(m[i], 3), round(lo[i], 3), round(hi[i], 3)]
        r += [series["binocular_suppressed_state1"][3][i], fills["binocular_suppressed_state1"][i],
              series["binocular_suppressed_state2"][3][i], fills["binocular_suppressed_state2"][i]]
        rows.append(r)
    comments = [
        PAGE_NOTE + f", panel {letter}",
        "Decoding accuracy (%) as a function of the number of faces (1..60) for five series (see legend of panel b); *_band_lo/_hi = lower/upper edge of the shaded band around each line",
        "x axis: 4 tick marks calibrated to 0,20,40,60 faces (resid %.1e); vertices lie exactly on integers 1..60" % xax.resid,
        "y axis: 6 tick marks calibrated to 0..100 %% (resid %.1e); 1 %% = %.4f pt" % (yax.resid, abs(1 / yax.slope)),
        "solid lines: 60-vertex stroke paths (exact to ~0.01 pt = 0.02 %); bands: filled polygons (opacity 0.2) clipped to 0..100 %, read as the vertical extent of the polygon at each integer x",
        "dashed lines (binocular_suppressed_*): drawn as filled dash outlines (1 pt wide, 4 pt dashes), not strokes; each vertex = weighted mean of the centreline estimates from the straight dash pieces",
        "  (pairs of parallel offset edges) in the two adjacent intervals, extrapolated to the integer x; *_n_estimates = number of estimates; 0 = vertex inside a dash gap with no dash in either",
        "  adjacent interval; such vertices were taken from the midpoint of the (gap-free, symmetric) error band where the band is not clipped at 0/100 % (*_gap_fill = band_midpoint),",
        "  otherwise linearly interpolated between neighbours (approximation, *_gap_fill = interpolated), or left nan (*_gap_fill = none: end of the line, band clipped)",
        "the band belonging to the dashed line was identified as the band whose centre tracks the dashed line (both bands of a colour have the same opacity)",
        "band edges are clipped at the axis limits in the PDF: a band_lo of 0.0 (or -0.01) or a band_hi of 100.0 means the true edge lies beyond the axis; values at the limit are what is drawn",
        "band_lo/hi = nan where the band polygon does not extend to that x (band collapsed onto the 0 % axis and was not drawn)",
    ]
    pp.write_csv(os.path.join(OUT, f"edfig7{letter}.csv"), hdr, rows, comments)
    pp.render(page, clip, 300, os.path.join(OUT, f"edfig7{letter}_orig.png"))
    return series


cf_c = extract_cf("c", 0.0)
cf_f = extract_cf("f", 256.81)
pp.render(page, pp.R(2, 462, 270, 484), 300, os.path.join(OUT, "edfig7_legend_orig.png"))
