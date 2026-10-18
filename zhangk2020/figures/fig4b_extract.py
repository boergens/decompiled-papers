"""Fig. 4b (p. 6): roughness profile of section A-A' of the copper workpiece. Digitized -> fig4b.csv.

Source: the embedded 300-ppi JPEG of Figure 4 (1797 x 662 px, xref 363); panel b is its right part.
Run: python3 -I -B figures/fig4b_extract.py  (from any directory) -> fig4b.csv, ../work/fig4b_overlay.png
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import (embedded_image, gray, frame_lines, tick_positions, tick_positions_v,  # noqa: E402
                             fit_axis, trace_envelope, write_csv, overlay)

PDF = str(ROOT / "source" / "zhangk2020.pdf")
a = embedded_image(PDF, 6, bbox_near=(82, 477.2, 513.3, 636.1))
g = gray(a)
dark = g < 80
X0 = 900  # panel b lies right of this column
rows_ = frame_lines(dark[:, X0:], 1, 0.5)
TOP, BOT = rows_[0], rows_[-1]
cols_ = [c for c in frame_lines(dark, 0, 0.5) if c[0] > X0]
LEFT, RIGHT = cols_[0], cols_[-1]
xl, xr = (LEFT[0] + LEFT[1]) / 2, (RIGHT[0] + RIGHT[1]) / 2
yt, yb = (TOP[0] + TOP[1]) / 2, (BOT[0] + BOT[1]) / 2
xt = tick_positions(dark, BOT, -1, 8, LEFT[1] + 3, RIGHT[0] - 3)
yt_r = tick_positions_v(dark, RIGHT, -1, 8, TOP[1] + 3, BOT[0] - 3)  # right-frame ticks (left ones touch the trace)
assert len(xt) == 3 and len(yt_r) == 3, (xt, yt_r)
# axes: "X-position 50 nm/div.", "Z-position 5 nm/div."; no numbers -> origin at the frame's lower left corner
fx, rx, _ = fit_axis([xl] + xt + [xr], [0, 50, 100, 150, 200])
fz, rz, _ = fit_axis([yb] + yt_r[::-1] + [yt], [0, 5, 10, 15, 20])

red = (a[:, :, 0].astype(int) > 170) & (a[:, :, 1].astype(int) < 110) & (a[:, :, 2].astype(int) < 110)
red[:, :LEFT[1] + 1] = False
red[:, RIGHT[0]:] = False
# line width: median vertical run length in flat parts
env = trace_envelope(red, LEFT[1] + 1, RIGHT[0], TOP[1] + 1, BOT[0], half_width=3, min_px=2)

out, pts = [], []
for c, ym, yu, yl in env:
    if ym != ym:
        continue
    out.append((float(fx(c)), float(fz(ym)), float(fz(yl)), float(fz(yu))))
    pts.append((c, ym))
z = np.array([o[1] for o in out])
rms = float(np.sqrt(np.mean((z - z.mean()) ** 2)))
# the two thin black horizontal annotation lines of "2.43 nm"
ann = []
for r in range(TOP[1] + 3, BOT[0] - 3):
    run = (a[r, LEFT[1] + 3:RIGHT[0] - 3].max(1) < 90)
    if run.sum() > 100:
        ann.append(r)
groups = np.split(np.array(ann), np.where(np.diff(ann) > 2)[0] + 1) if ann else []
ann_rows = [float(np.mean(q)) for q in groups]
ann_txt = (f"two thin black annotation lines at z = {', '.join(f'{float(fz(r)):.2f}' for r in ann_rows)} nm "
           f"(spacing {abs(float(fz(ann_rows[0]) - fz(ann_rows[-1]))):.2f} nm)") if len(ann_rows) >= 2 else "annotation lines not found"

hdr = [
    "zhangk2020 Fig. 4b (p. 6): Roughness of the section A-A' (Figure 4. Copper workpiece).",
    "Provenance: tier 3, digitized from the embedded 300-ppi JPEG (xref 363, 1797 x 662 px); red colour mask, per pixel column",
    "the run of red pixels nearest the previous column; z_low/z_high = run ends moved inward by 3 px (half the line width), z_nm = their mean.",
    "Axes carry no numbers: 'X-position 50 nm/div.', 'Z-position 5 nm/div.'. Origin arbitrary: x = 0 at the left frame line, z = 0 at the bottom frame line.",
    f"Calibration: frame columns {xl:.1f}/{xr:.1f} px, x ticks at columns {', '.join(f'{v:.1f}' for v in xt)} (= 50, 100, 150 nm), max residual {rx:.2f} nm;",
    f"frame rows {yt:.1f}/{yb:.1f} px, z ticks at rows {', '.join(f'{v:.1f}' for v in yt_r)} (= 15, 10, 5 nm), max residual {rz:.3f} nm.",
    f"One source pixel = {200 / (xr - xl):.3f} nm in x and {20 / (yb - yt):.4f} nm in z; uncertainty about 1 px (JPEG, line width ~6 px).",
    "Labels in the panel: A' (left end) and A (right end); '2.43 nm' with arrows between two short horizontal lines.",
    f"Check (decompiler): RMS of z_nm about its mean over the whole trace = {rms:.2f} nm (text: RMS roughness 2.43 nm); {ann_txt}.",
]
write_csv(ROOT / "figures" / "fig4b.csv", hdr, ["x_nm", "z_nm", "z_low_nm", "z_high_nm"], out, fmt=["{:.2f}", "{:.3f}", "{:.3f}", "{:.3f}"])
overlay(a, pts, str(ROOT / "work" / "fig4b_overlay.png"))
print("\n".join(hdr))
print(len(out), "rows")
