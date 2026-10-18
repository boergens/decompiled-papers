"""Extended Data Fig. 1k (resin fluidity vs time; Epon at 95% / 4 degC, 100% / 4 degC, 100% / RT) -> edfig1k.csv

Tier 1: Edmond 'Extended Data Fig.1/Extended Data Fig.1k/resin data.pzfx' (GraphPad Prism XML; one XY table 'all data',
X = Time (hrs), 14 Y columns named by condition and date). Values marked Excluded in Prism are flagged.
Which columns are plotted: each column's points (x converted to days = hours/24) are projected onto the raster figure
(PDF p. 12, embedded image; axes fitted on the tick marks) and counted as plotted when >= 90 % of sample points along its
polyline (25 per segment between consecutive non-excluded points) sit within 2 px of a pixel of the series colour. Result: 95% 12/1, 12/2, 12/3, 11/21 * (red; n = 4),
100% 4 deg 12/7, 12/3, 10/16 (blue; n = 3), 100% RT 12/2, 10/16 (green dots on black lines; n = 2), which matches the
n given in Methods. Two columns pass the test only because they run on top of other lines and are marked 'uncertain'.
Run: python3 -I edfig1k_extract.py
"""
import os
import sys
import xml.etree.ElementTree as ET

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, SRC, WORK, fit, hsv, hue_mask, overlay, page_image, write_csv  # noqa: E402

root = ET.parse(os.path.join(SRC, "Extended Data Fig.1/Extended Data Fig.1k/resin data.pzfx")).getroot()
tag = lambda e: e.tag.split("}")[-1]  # noqa: E731
table = [e for e in root.iter() if tag(e) == "Table"][0]


def column(col):
    title = "".join(col.find("{*}Title").itertext()).strip()
    vals = []
    for d in col.find("{*}Subcolumn"):
        vals.append((None if d.text is None else float(d.text), d.attrib.get("Excluded") == "1"))
    return title, vals


xcol = [c for c in table if tag(c) == "XColumn"][0]
_, X = column(xcol)
ycols = [column(c) for c in table if tag(c) == "YColumn"]

a = page_image(12)
px2x, x2px, rx = fit([111.5, 180, 248, 316, 384, 452.5], [0, 2, 4, 6, 8, 10])
py2y, y2py, ry = fit([2306.5, 2377.5, 2448.5, 2520, 2590.5], [4, 3, 2, 1, 0])
h = hsv(a)
masks = {"95%": hue_mask(a, 170, 8, 80, 80),
         "100% 4 deg": (h[..., 0] >= 110) & (h[..., 0] <= 140) & (h[..., 1] >= 40) & (h[..., 2] >= 60),
         "100% RT": ((a.max(2) < 90) | hue_mask(a, 50, 85, 80, 60))}
dist = {k: cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 3) for k, m in masks.items()}
rows, ov, summary = [], [], []
for title, vals in ycols:
    grp = "95%" if title.startswith("95%") else "100% RT" if "RT" in title else "100% 4 deg" if "4 deg" in title and title.startswith("100%") else None
    pts = [(X[i][0], v, ex or X[i][1]) for i, (v, ex) in enumerate(vals) if v is not None]
    hit = []
    if grp:
        q = [(float(x2px(hrs / 24)), float(y2py(v))) for hrs, v, ex in pts if not ex]
        if len(q) == 1:
            hit.append(dist[grp][int(round(q[0][1])), int(round(q[0][0]))] <= 2)
        for (x0, y0), (x1, y1) in zip(q[:-1], q[1:]):   # sample the connecting line segments too
            for t in np.linspace(0, 1, 25):
                hit.append(dist[grp][int(round(y0 + t * (y1 - y0))), int(round(x0 + t * (x1 - x0)))] <= 2)
    frac = float(np.mean(hit)) if hit else 0.0
    plotted = "yes" if (grp is not None and frac >= 0.9) else "no"
    # decided by eye on a 4x zoom (work/ed1k_blue_check.png): 10/19 lies on top of the other blue lines and has no
    # visible start of its own (Methods: n = 3 at 4 degC); the single 12/08 *** point coincides with another red line.
    if title in ("100% 4 deg 10/19", "95% 12/08 ***"):
        plotted = "uncertain"
    summary.append(f"{title}: {len(pts)} points, {100 * frac:.0f}% on printed {grp} trace -> plotted: {plotted}")
    for hrs, v, ex in pts:
        rows.append([title, grp or "Spurr", plotted, "yes" if ex else "no", f"{hrs:g}", f"{hrs / 24:.4f}", f"{v:g}"])
        if plotted == "yes" and not ex:
            ov.append((x2px(hrs / 24), y2py(v)))
write_csv(os.path.join(HERE, "edfig1k.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 1k: resin fluidity (a.u.; speed of resin movement in an inverted",
    "  15-ml tube, Methods) vs time (days) for Epon 95% resin + 5% acetone at 4 degC (red), 100% resin at 4 degC (blue)",
    "  and 100% resin at RT (black lines, green dots).",
    "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU, 'Extended Data Fig.1/Extended Data Fig.1k/resin data.pzfx'",
    "  (Prism XY table 'all data'), read by edfig1k_extract.py; time_days = time_h / 24.",
    "plotted: whether the column appears in the printed panel (projection test on the raster figure + check by eye, see",
    "  script; tier-3 check, lines within 2 px). 'uncertain' = lies on top of other plotted lines, cannot be told apart:",
] + ["  " + s for s in summary] + [
    "excluded: value or its X row marked 'Excluded' in Prism (not plotted).",
    "Columns: column (Prism title); group; plotted; excluded; time_h; time_days; fluidity_au.",
], ["column", "group", "plotted", "excluded", "time_h", "time_days", "fluidity_au"], rows)
overlay(a, ov, os.path.join(WORK, "edfig1k_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig1k_overlay_full.png")).crop((0, 2250, 560, 2711)).save(os.path.join(WORK, "edfig1k_overlay.png"))
print("\n".join(summary))
