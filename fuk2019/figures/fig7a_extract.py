"""Fig. 7a (DGEBA-MTHPA): 3D surface of total energy vs. torsion angles phi1, phi2 -> figures/fig7a.csv
(regular grid), figures/fig7a_pixels.csv.gz (one row per surface pixel) and figures/fig7a_key.csv
(the colour key). Tier 3, digitized.

Run from anywhere: python3 -I figures/fig7a_extract.py. Embedded image p. 8 of source/fuk2019.pdf.
Method: tools/fig7common.py and tools/surf3d.py (camera from the axis ticks, energy from the
colour, angles by intersecting each pixel's view ray with the plane of its energy).
Rough axis end points (pixels) are given by hand below and refined on the black axis lines.
Writes work/fig7a_check.png (axis/box grid projected with the fitted camera over the image).
"""
import csv
import gzip
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import fig7common as f7  # noqa: E402
import surf3d as s3  # noqa: E402

AXES = {'phi1': ((129, 338.5), (340, 415.5), 1, [-80, -60, -40, -20, 0, 20]), 'phi2': ((341, 415), (507, 327.5), 1, [-150, -100, -50, 0, 50, 100, 150]), 'E': ((128.5, 338), (117.5, 69), -1, [480, 500, 520, 540, 560])}
KEY = (561, 589, 465.5, 577.0)           # key columns and the values printed at its top and bottom
a, d, info = f7.run(8, (76.7, 307.0, 289.1, 460.6), AXES, KEY)
L, F, P = info["lines"], info["fits"], info["P"]
E_top = s3.proj1d_inv(F["E"], L["E"]["tmax"])
phi2_back = s3.proj1d_inv(F["phi2"], L["phi2"]["tmax"])
box1 = (info["phi1_left"], info["phi1_front"])
box2 = (info["phi2_front"], phi2_back)
back_top = s3.project(P, [(box1[0], box2[1], E_top)])[0]
print(dict(box_phi1=box1, box_phi2=box2, E_floor=info["E_floor"], E_top=E_top, back_corner_top_projected=back_top,
           dlt_rms=info["dlt_res_rms"], dlt_max=info["dlt_res_max"], key_rows=info["key_rows"], n_pix=info["n_pix"],
           tick_rms={k: F[k]["rms"] for k in F}))
# sensitivity of the angles to the energy uncertainty
p1a, p2a = s3.invert(P, d["px"].astype(float), d["py"].astype(float), d["E"] - d["Eerr"])
p1b, p2b = s3.invert(P, d["px"].astype(float), d["py"].astype(float), d["E"] + d["Eerr"])
dphi1, dphi2 = np.abs(p1b - p1a) / 2, np.abs(p2b - p2a) / 2
inbox = (d["phi1"] >= box1[0] - 1) & (d["phi1"] <= box1[1] + 1) & (d["phi2"] >= box2[0] - 1) & (d["phi2"] <= box2[1] + 1)
common = [
    "Fig. 7a of Fu et al. 2019, Polymers 11, 975: potential energy of the bonds phi1 and phi2 in DGEBA-MTHPA (3D surface, colour = total energy).",
    "Provenance: tier 3, digitized from the embedded 220 ppi raster image on p. 8 (Origin 3D colour-mapped surface); no source data published.",
    "Camera: 3x4 perspective matrix fitted (DLT) on the tick marks of the three axes (phi1 ticks -80..20 (the -100 tick is at the left corner, hidden in the E axis), phi2 ticks -150..150, E ticks 480..560); rms %.2f px, max %.2f px." % (info["dlt_res_rms"], info["dlt_res_max"]),
    "Box from the axis fits: phi1 %.1f..%.1f deg, phi2 %.1f..%.1f deg, energy %.1f..%.1f kcal/mol (the colour key spans %.1f..%.1f: the box and the key agree)." % (
        box1[0], box1[1], box2[0], box2[1], info["E_floor"], E_top, KEY[2], KEY[3]),
    "Check: the projected top of the back box corner falls at pixel (%.1f, %.1f); the image shows it at about (306, %d)." % (back_top[0], back_top[1], int(round(back_top[1]))),
    "Energy of a pixel: its colour matched to the colour key (key rows mapped linearly from %.1f at the top to %.1f at the bottom);" % (KEY[2], KEY[3]),
    "where several key rows have nearly the same colour (long runs of plain red) the mean is taken and E_err gives the half range plus half a key row.",
    "Angles: intersection of the pixel's view ray with the plane E = const. They are only as good as E: dphi1/dphi2 = change for E +- E_err.",
    "Only the visible (front) part of the surface is covered; parts hidden behind peaks or ridges are missing. Mesh and contour lines are skipped.",
]
(ROOT / "figures").mkdir(exist_ok=True)
with gzip.open(ROOT / "figures/fig7a_pixels.csv.gz", "wt", newline="") as f:
    for h in common + ["One row per surface pixel. px, py = pixel in the embedded image; in_box = 1 if the angles fall inside the box (+-1 deg)."]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["px", "py", "E_kcal_mol", "E_err", "phi1_deg", "phi2_deg", "dphi1", "dphi2", "in_box"])
    for i in range(len(d["px"])):
        w.writerow([int(d["px"][i]), int(d["py"][i]), "%.2f" % d["E"][i], "%.2f" % d["Eerr"][i], "%.2f" % d["phi1"][i],
                    "%.2f" % d["phi2"][i], "%.2f" % dphi1[i], "%.2f" % dphi2[i], int(inbox[i])])
# regular grid: 5 deg in phi1 x 10 deg in phi2, mean energy of the in-box pixels with E_err below the median
good = inbox & (d["Eerr"] <= np.median(d["Eerr"]) * 3)
dd = {k: v[good] for k, v in d.items()}
e1 = np.arange(np.floor(box1[0] / 5) * 5, box1[1] + 5, 5)
e2 = np.arange(np.floor(box2[0] / 10) * 10, box2[1] + 10, 10)
mean, sd, N = f7.grid(dd, e1, e2, box1, box2)
with open(ROOT / "figures/fig7a.csv", "w", newline="") as f:
    for h in common + [
        "Grid: cells of 5 deg (phi1) x 10 deg (phi2); E_mean / E_sd = mean and spread of the pixel energies in the cell (pixels with E_err <= 3x median only);",
        "n_px = number of pixels; cells with fewer than 3 pixels are left out. Full per-pixel data: fig7a_pixels.csv.gz."]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["phi1_deg", "phi2_deg", "E_mean", "E_sd", "n_px"])
    for i in range(len(e1) - 1):
        for j in range(len(e2) - 1):
            if N[i, j] >= 3:
                w.writerow(["%.1f" % ((e1[i] + e1[i + 1]) / 2), "%.1f" % ((e2[j] + e2[j + 1]) / 2), "%.2f" % mean[i, j], "%.2f" % sd[i, j], int(N[i, j])])
r0, r1 = info["key_rows"]
kc, kv = s3.colour_key(a, (KEY[0] + 3, KEY[1] - 3), r0, r1, KEY[2], KEY[3])
with open(ROOT / "figures/fig7a_key.csv", "w", newline="") as f:
    f.write("# Colour key of Fig. 7a: rows %d..%d of the embedded image (median over the key's inner columns), energy linear from %.1f (top) to %.1f (bottom).\n" % (r0, r1, KEY[2], KEY[3]))
    w = csv.writer(f)
    w.writerow(["row", "R", "G", "B", "E_kcal_mol"])
    for r, c, v in zip(range(r0, r1 + 1), kc, kv):
        w.writerow([r, int(c[0]), int(c[1]), int(c[2]), "%.2f" % v])
# check image: projected floor grid, back walls and box edges
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
fig, ax = plt.subplots(figsize=(9, 6.5))
ax.imshow(a)
for v in AXES["phi1"][3]:
    q = s3.project(P, [(v, y, info["E_floor"]) for y in np.linspace(*box2, 20)]); ax.plot(q[:, 0], q[:, 1], "m-", lw=0.6)
for v in AXES["phi2"][3]:
    q = s3.project(P, [(x, v, info["E_floor"]) for x in np.linspace(*box1, 20)]); ax.plot(q[:, 0], q[:, 1], "m-", lw=0.6)
for v in AXES["E"][3]:
    q = s3.project(P, [(box1[0], y, v) for y in np.linspace(*box2, 20)]); ax.plot(q[:, 0], q[:, 1], "c-", lw=0.6)
    q = s3.project(P, [(x, box2[1], v) for x in np.linspace(*box1, 20)]); ax.plot(q[:, 0], q[:, 1], "c-", lw=0.6)
for X in [(box1[0], box2[0]), (box1[0], box2[1]), (box1[1], box2[1])]:
    q = s3.project(P, [(X[0], X[1], info["E_floor"]), (X[0], X[1], E_top)]); ax.plot(q[:, 0], q[:, 1], "y-", lw=0.8)
fig.savefig(ROOT / "work/fig7a_check.png", dpi=110)
