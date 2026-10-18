#!/usr/bin/env python3
"""Fig. 3c (p. 4): mean depth of posterior (Post.) and anterior (Ant.) registered fields relative to the pial surface.
The plotted lines are an embedded raster (241 x 547 px, indexed, 600 ppi, placed at 368.70..397.62 x 85.68..151.32 pt);
the axis is vector: ticks 100 ... 600 um at 88.89 ... 155.13 pt (labels are text). -> fig3c.csv.
Each field is one horizontal black line spanning its column; its depth is the centre of its dark pixel rows, mapped
image row -> page y (placement transform) -> depth (tick fit). Lines closer than ~2 px merge into one dark band; such bands
are split by their thickness (n_lines = round(thickness / single-line thickness)) and flagged."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(mc.PDF), 4, bbox_near=(369, 86, 398, 151)).astype(float).mean(2)
H, W = a.shape
Y0, Y1 = 85.6772, 151.3172
D = mc.LinAxis(list(zip([88.89, 102.14, 115.38, 128.63, 141.88, 155.13], [100, 200, 300, 400, 500, 600])))
rows = []
cols = {"Post.": (5, 115), "Ant.": (123, 233)}
for name, (c0, c1) in cols.items():
    dark = (a[:, c0 + 5:c1 - 5] < 128).mean(1) > 0.8
    runs, cur = [], []
    for i, v in enumerate(dark):
        if v:
            cur.append(i)
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    th = np.median([len(r) for r in runs])
    for r in runs:
        n = max(1, int(round(len(r) / th)))
        for k in range(n):
            seg = r[k * len(r) // n:(k + 1) * len(r) // n]
            yc = np.mean(seg) + 0.5
            ypt = Y0 + yc / H * (Y1 - Y0)
            rows.append([name, f"{D(ypt):.1f}", len(r), n, f"{yc:.1f}", "merged band split" if n > 1 else ""])
mc.write_csv(Path(__file__).with_name("fig3c.csv"), [
    "Fig. 3c (p. 4 of microns2025.pdf): mean depth of registered imaging fields, posterior (Post.) and anterior (Ant.) columns.",
    "Provenance: tier 3, digitized from the embedded raster (1 px = 0.12 pt = 0.91 um depth); axis tier 2 (vector ticks).",
    "Uncertainty about +-1 um for isolated lines; lines in merged bands are evenly divided, +-2 um.",
    "Columns: column (Post./Ant.); depth_um (distance from pial surface); band_px (thickness of the dark band in image px);",
    "n_lines_in_band; row_px (line centre, image row); flag.",
    f"Single-line thickness (median band): Post. / Ant. as in the data; {D.describe('depth axis')}",
], ["column", "depth_um", "band_px", "n_lines_in_band", "row_px", "flag"], rows)
print({k: sum(1 for r in rows if r[0] == k) for k in cols})
