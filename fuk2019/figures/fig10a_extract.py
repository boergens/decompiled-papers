"""fig10a (DGEBA-MTHPA): markers, two fitted red lines and their crossing -> figures/fig10a.csv (tier 3, digitized).

Run from anywhere: python3 -I figures/fig10a_extract.py. Reads the embedded raster image on p. 10 of
source/fuk2019.pdf; the method is in tools/scatterfit.py. Writes work/fig10a_overlay.png (extracted
marker centres, error-bar ends, line end points and the dot drawn in magenta/green over the image).
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402
import fukplot as fp  # noqa: E402
import scatterfit as sf  # noqa: E402

T = [300, 350, 400, 450, 500, 550, 600]
YV = [1, 2, 3, 4, 5]
a = fp.load(10, (89.5, 573.8, 297.0, 722.3))
cal = sf.calibrate(a, T, YV, 6)
ms = sf.markers(a, cal, T, [(112, 24, 300, 75), (730, 24, 803, 62)], 12, errorbars=False)
rp = sf.red_parts(a, cal, 7, 25)  # no exclusion needed: the high line runs into the panel-letter area
print({k: v for k, v in cal.items() if k not in ("fx", "fy")})
print(ms)
print(rp)
dy = abs(cal["my"])
hdr = [
    "fig10a of Fu et al. 2019, Polymers 11, 975 (DGEBA-MTHPA): MSD (15 ps) against temperature (squares), two fitted straight lines (red) and their crossing (red dot, labelled 398.26K). y = MSD in Angstrom^2; x in K.",
    "Provenance: tier 3, digitized from the embedded raster image on p. 10 (Origin export, 300 ppi); no source data published.",
    "Axis fit: x on the inward major ticks 300-600 K (max residual %.3g K), y on ticks %s (max residual %.3g); frame edges x = %.2f..%.2f K, y = %.4f..%.4f." % (cal["rx"], YV, cal["ry"], cal["x_left"], cal["x_right"], cal["y_bot"], cal["y_top"]),
    "Rows: kind = marker (one per temperature; x is the measured marker centre, T_label the temperature it stands for), "
    "line_low / line_high (the two red fitted lines: one row per end point, as drawn), dot (the red dot at the crossing), "
    "crossing_of_digitized_lines (where the two digitized lines intersect; computed by the decompiler, not printed), label (the printed crossing temperature).",
    "y_err_low / y_err_high: ends of the error bar (the caps), only where the figure has error bars.",
    "Uncertainty: about +-1 px = +-%.4f in y and +-%.2f K in x; partly hidden markers (note column) +-2 px." % (dy, abs(cal["mx"])),
]
rows = []
for m in ms:
    rows.append(("marker", m["T_label"], m["x"], m["y"], m.get("y_err_low", float("nan")), m.get("y_err_high", float("nan")),
                 m["px"], m["py"], m["note"]))
for name in ("low", "high"):
    L = rp[name]
    note = "least-squares fit on %d columns, rms %.2f px; slope %.6g per K" % (L["n_cols"], L["rms_px"], L["slope"])
    rows.append(("line_" + name, "", L["x0"], L["y0"], float("nan"), float("nan"), L["c0"], L["slope_px"] * L["c0"] + L["icpt_px"], note))
    rows.append(("line_" + name, "", L["x1"], L["y1"], float("nan"), float("nan"), L["c1"], L["slope_px"] * L["c1"] + L["icpt_px"], ""))
rows.append(("dot", "", rp["dot_x"], rp["dot_y"], float("nan"), float("nan"), rp["dot_px"], rp["dot_py"], "centre of the red dot"))
rows.append(("crossing_of_digitized_lines", "", rp["crossing_x"], rp["crossing_y"], float("nan"), float("nan"), float("nan"), float("nan"), "computed"))
rows.append(("label", "", 398.26, float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), "printed next to the dot: 398.26K"))
dc.write_csv(str(ROOT / "figures/fig10a.csv"), hdr, ["kind", "T_label", "x_K", "y", "y_err_low", "y_err_high", "px_x", "px_y", "note"],
             rows, fmt=["{}", "{}", "{:.3f}", "{:.5f}", "{:.5f}", "{:.5f}", "{:.1f}", "{:.1f}", "{}"])
pts = [(m["px"], m["py"]) for m in ms] + [(rp["dot_px"], rp["dot_py"])]
for m in ms:
    if "err_top_px" in m:
        pts += [(m["px"], m["err_top_px"]), (m["px"], m["err_bot_px"])]
for name in ("low", "high"):
    L = rp[name]
    for c in np.linspace(L["c0"], L["c1"], 60):
        pts.append((c, L["slope_px"] * c + L["icpt_px"]))
(ROOT / "work").mkdir(exist_ok=True)
dc.overlay(a, pts, str(ROOT / "work/fig10a_overlay.png"), colour=(0, 200, 0))
