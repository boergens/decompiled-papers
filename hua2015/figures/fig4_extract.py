"""Tier-1 data for Fig. 4d-g of Hua et al. 2015 from the authors' Supplementary Software (.mat files).

    python3 -I fig4_extract.py   -> fig4d.csv, fig4e.csv, fig4f.csv, fig4g.csv (+ ../work/fig4_compare.txt)

Source: ../source/esm_zips/extracted/supplMATLABcode_RESCOPanalysis/suppl. software/
  YH_MH_traceabilityData_fit_mh_v2.mat   data set of this paper ("This protocol", annotators' tracings, Yunfeng Hua)
  KMB_MH_traceabilityData_fit_mh_v2.mat  rOTO-stained L4 cortex comparison data set (Boergens et al.)
  YH_MH_old_e1088Data_refit_mh_v2.mat    published retina data set e1088 (ref. 21), re-fitted
The .mat files are read with scipy.io.loadmat only; no MATLAB code is run. Variable meanings are taken from
RESCOP_mh_v3_forSuppl.m (same folder):
  RP_histMeas        vote histogram, entry (T+1, N+1) = number of skeleton edges with T agreeing of N votes
  RP_histMeasStar    round(RP_histMeas ./ T), the redundancy-corrected measured histogram (row T=0: 0/0 = NaN)
  RP_histPredFinal   vote histogram predicted by the fitted prior
  RP_priorx, RP_priory  the fitted prior p(p_e) at the 81 basis points p_e
  RP_p_errN          error probability per unit length for N annotators (index N+1)
  The plotted solid curves are RP_errDist = RP_rp ./ RP_p_errN, plotted as RP_errDist(2:end) against 1..50, with
  RP_rp set in the script's final "just plot results together" section: 2*0.6 = 1.2 µm (e1088), 2*0.4 = 0.8 µm
  (YH, KMB). NB the RP_errDist stored in YH_MH_traceabilityData_fit_mh_v2.mat was computed with RP_rp = 1.2, not
  0.8; the 0.8 µm version is the one in the figure (checked against the vector paths, see ../work/fig4_compare.txt).
  The heat maps were drawn as image(log(X)) with CLim [0, log(max(RP_histMeasStar))] (MATLAB 'jet'); the prior as
  plot(RP_priorx, max(RP_priory, 1e-2)) with YLim [1e-1 1e3], XLim [-0.1 1.1].
  The dashed (focused re-annotation) curves come from a Monte-Carlo step whose results were saved to *_FocAnn.mat
  files that are NOT in the Supplementary Software, so they stay tier 2 (taken from fig4g_vector.csv).
"""
import csv
import os

import numpy as np
import scipy.io as sio

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../source/esm_zips/extracted/supplMATLABcode_RESCOPanalysis/suppl. software")
F = {"YH": "YH_MH_traceabilityData_fit_mh_v2.mat", "KMB": "KMB_MH_traceabilityData_fit_mh_v2.mat",
     "e1088": "YH_MH_old_e1088Data_refit_mh_v2.mat"}
M = {k: sio.loadmat(os.path.join(SRC, v)) for k, v in F.items()}
RP = {"e1088": 1.2, "YH": 0.8, "KMB": 0.8}
NAME = {"YH": "this protocol (cortex), data of this paper", "KMB": "rOTO (cortex), Boergens et al.",
        "e1088": "e1088 (retina), ref. 21"}
# MATLAB colours in the plotting section: e1088 'b', YH 'r', KMB 'g' (also '--b', '--r', '--g' for focused annotation)
COLOUR = {"e1088": "blue", "YH": "red", "KMB": "green"}
LEGEND_OF_COLOUR = {"red": "e1088 (retina)", "green": "This protocol (cortex)", "blue": "rOTO (cortex)"}
report = []


def head(f, lines):
    for h in lines:
        f.write("# " + h + "\n")


def fmt(v):
    return "" if v != v else f"{v:.6g}"


# ---------- Fig. 4d / 4e: vote histograms of the YH data set ----------
yh = M["YH"]
star, meas, pred = yh["RP_histMeasStar"], yh["RP_histMeas"].astype(float), yh["RP_histPredFinal"]
vmax = np.nanmax(star)
for panel, X, what in (("d", star, "RP_histMeasStar (measured, redundancy-corrected)"),
                       ("e", pred, "RP_histPredFinal (fitted)")):
    with open(os.path.join(HERE, f"fig4{panel}.csv"), "w", newline="") as f:
        head(f, [
            f"Hua, Laserstein & Helmstaedter 2015 Nat Commun 6:7923, Fig. 4{panel} ('{'Meas.' if panel == 'd' else 'Fit'}'):"
            " vote histogram, number of skeleton edges per (N, T).",
            f"Provenance: tier 1, authors' Supplementary Software, {F['YH']}, variable {what};",
            "  read with scipy.io.loadmat by fig4_extract.py. Matrix entry (T+1, N+1) -> row N, T.",
            "Columns: N = total votes for an edge (0..7); T = agreeing votes (0..7); n_edges = the plotted value"
            + (" (= round(n_edges_raw / T); NaN for T = 0);" if panel == "d" else " (fit, not rounded);"),
            ("  n_edges_raw = RP_histMeas, the vote histogram before the redundancy correction;" if panel == "d" else
             "  (the T = 0 row is the fit's prediction for edges with no agreeing vote);"),
            f"  plotted with MATLAB image(log(.)) and colour limits [0, log({vmax:.0f})] = [1, {vmax:.0f}] edges (jet); values",
            "  <= 1, 0 and NaN all show as the darkest blue.",
        ])
        w = csv.writer(f)
        w.writerow(["N", "T", "n_edges"] + (["n_edges_raw"] if panel == "d" else []))
        for T in range(8):
            for N in range(8):
                w.writerow([N, T, fmt(X[T, N])] + ([fmt(meas[T, N])] if panel == "d" else []))
    # comparison with the digitized heat map
    dig = {}
    for r in csv.DictReader(l for l in open(os.path.join(HERE, f"fig4{panel}_digitized.csv")) if not l.startswith("#")):
        dig[(int(r["N"]), int(r["T"]))] = (float(r["n_edges"]), r["flag"])
    d = []
    flags_ok = 0
    for (N, T), (v, flag) in dig.items():
        true = X[T, N]
        if flag == "bottom_colour":
            flags_ok += (true != true) or true <= 1.2
            continue
        if flag == "top_colour":
            report.append(f"4{panel} top_colour cell N={N} T={T}: digitized {v:.0f} (clipped), source {true:.1f}")
            continue
        d.append(np.log10(v / true))
    d = np.array(d)
    nb = sum(1 for v in dig.values() if v[1] == "bottom_colour")
    report.append(f"4{panel}: digitized vs source, {len(d)} cells: log10 ratio mean {d.mean():+.3f}, sd {d.std():.3f}, "
                  f"max |.| {np.abs(d).max():.3f} (= {100 * (10 ** np.abs(d).max() - 1):.0f} %); "
                  f"bottom_colour cells correct (source NaN, 0 or <= 1.2): {flags_ok}/{nb}")

# ---------- Fig. 4f: prior of the YH data set ----------
px, py = yh["RP_priorx"][0], yh["RP_priory"][0]
with open(os.path.join(HERE, "fig4f.csv"), "w", newline="") as f:
    head(f, [
        "Hua, Laserstein & Helmstaedter 2015 Nat Commun 6:7923, Fig. 4f: fitted prior of skeleton-edge difficulty p(p_e).",
        f"Provenance: tier 1, authors' Supplementary Software, {F['YH']}, variables RP_priorx (p_e, the 81 basis points",
        "  of RESCOP_priorBasisPoints(80)) and RP_priory (p(p_e), piecewise-linear 'hat' basis weights); fig4_extract.py.",
        "Columns: p_e; p_pe = RP_priory; p_pe_plotted = max(p_pe, 1e-2) as in the MATLAB plotting code. The figure's y axis",
        "  runs from 10^-1 to 10^3, so values below 0.1 lie under the axis and the last point (p_e = 1, 3867) is cut at the top.",
    ])
    w = csv.writer(f)
    w.writerow(["p_e", "p_pe", "p_pe_plotted"])
    for x, y in zip(px, py):
        w.writerow([f"{x:.6g}", fmt(y), fmt(max(y, 1e-2))])
vec = [(float(r["p_e"]), float(r["p_pe"]), r["flag"]) for r in
       csv.DictReader(l for l in open(os.path.join(HERE, "fig4f_vector.csv")) if not l.startswith("#"))]
rel, dxs = [], []
for x, y, flag in vec:
    i = int(np.argmin(np.abs(px - x)))
    if flag == "":
        dxs.append(abs(px[i] - x))
        rel.append(y / py[i] - 1)
    elif flag == "below_axis":   # where the drawn line leaves the bottom of the box: a neighbour basis point < 0.1
        j = int(np.searchsorted(px, x))
        assert min(py[max(j - 1, 0):j + 2]) < 0.1, (x, py[max(j - 1, 0):j + 2])
report.append(f"4f: {len(vec)} vector vertices; {len(rel)} visible peak vertices: max |p_e(vector) - nearest basis point| {max(dxs):.5f}; "
              f" max relative difference in p(p_e) {100 * max(map(abs, rel)):.2f} %; "
              f"every below_axis vertex lies next to a basis point with source value < 0.1; at_top vertex: source {py[-1]:.0f}")

# ---------- Fig. 4g ----------
rows = []
for k in ("e1088", "YH", "KMB"):
    perr = M[k]["RP_p_errN"][0]
    for N in range(1, len(perr)):
        rows.append([k, NAME[k], COLOUR[k], LEGEND_OF_COLOUR[COLOUR[k]], "solid (full neurite tracing)", N,
                     RP[k] / perr[N], "1 (source)", "in_figure" if N <= 23 else "beyond_figure"])
COLOUR_OF_LEGEND = {v: c for c, v in LEGEND_OF_COLOUR.items()}
SET_OF_COLOUR = {c: k for k, c in COLOUR.items()}
vrows = list(csv.DictReader(l for l in open(os.path.join(HERE, "fig4g_vector.csv")) if not l.startswith("#")))
for r in vrows:
    if r["style"].startswith("dashed"):
        c = COLOUR_OF_LEGEND[r["series"]]
        k = SET_OF_COLOUR[c]
        rows.append([k, NAME[k], c, r["series"], r["style"], float(r["n_annotators"]),
                     float(r["mean_inter_error_distance_um"]), "2 (vector, fig4g_vector.csv)", r["flag"]])
with open(os.path.join(HERE, "fig4g.csv"), "w", newline="") as f:
    head(f, [
        "Hua, Laserstein & Helmstaedter 2015 Nat Commun 6:7923, Fig. 4g: predicted mean inter-error distance (µm) against",
        "  the number of annotators, for three data sets.",
        "Provenance: solid lines tier 1, authors' Supplementary Software: RP_rp / RP_p_errN(N+1) from "
        f"{F['e1088']} (RP_rp 1.2 µm),",
        f"  {F['YH']} (0.8 µm) and {F['KMB']} (0.8 µm), RP_rp as in the final plotting section of",
        "  RESCOP_mh_v3_forSuppl.m (the YH file's stored RP_errDist uses 1.2 µm and is NOT what is plotted). N = 1..50 are",
        "  given; the figure shows N = 1..23 (column 'flag'). Dashed lines (focused re-annotation): tier 2, vector paths",
        "  (fig4g_vector.csv); their *_FocAnn.mat source files are not in the Supplementary Software.",
        "Columns: data_set = source file key (YH = this paper's data, KMB = rOTO cortex of Boergens et al., e1088 = retina);",
        "  description; colour = line colour in the figure (= MATLAB colour in the authors' plotting code); legend_label =",
        "  the legend text printed next to that colour in the figure; style; n_annotators; mean_inter_error_distance_um;",
        "  tier; flag.",
        "WARNING: the legend of the printed figure does not match the data. The red curve (legend 'e1088 (retina)') is the",
        "  YH data set of this paper, the green curve (legend 'This protocol (cortex)') is the KMB rOTO cortex data set and",
        "  the blue curve (legend 'rOTO (cortex)') is the e1088 retina data set. Evidence: the solid curves match these files",
        "  within 0.4 % at all 23 points and differ from the other files by 34-190 %; the red curve is computed from the same",
        "  fit as Fig. 4d-f (which match the YH file); the authors' code plots e1088 'b', YH 'r', KMB 'g'. The dashed curves",
        "  are assigned to data sets by colour in the same way (not checkable: no source file).",
    ])
    w = csv.writer(f)
    w.writerow(["data_set", "description", "colour", "legend_label", "style", "n_annotators",
                "mean_inter_error_distance_um", "tier", "flag"])
    for r in rows:
        w.writerow(r[:5] + [f"{r[5]:.6g}", f"{r[6]:.6g}"] + r[7:])
# comparison: vector solid curves vs source, both assignments
V = {}
for r in vrows:
    if r["style"].startswith("solid"):
        V.setdefault(r["series"], []).append(float(r["mean_inter_error_distance_um"]))
for lab, v in V.items():
    v = np.array(v)
    out = []
    for k in ("e1088", "YH", "KMB"):
        src = RP[k] / M[k]["RP_p_errN"][0][1:24]
        out.append(f"{k} {100 * np.max(np.abs(v / src - 1)):.1f} %")
    report.append(f"4g solid, vector curve with legend '{lab}' ({COLOUR_OF_LEGEND[lab]}): max relative difference to "
                  + ", ".join(out))
open(os.path.join(HERE, "../work/fig4_compare.txt"), "w").write("\n".join(report) + "\n")
print("\n".join(report))
