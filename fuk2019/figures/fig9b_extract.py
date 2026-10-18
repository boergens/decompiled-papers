"""Fig. 9b (DGEBA-NA): MSD-time curves at 300-600 K -> figures/fig9b.csv (tier 3, digitized).

Run from anywhere: python3 -I figures/fig9b_extract.py. Reads the embedded raster image
(865 x 618 px, 300 ppi) on p. 10 of source/fuk2019.pdf; the method is in tools/msdtime.py.
Also writes work/fig9b_overlay.png (extracted points drawn in magenta over the source image).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402
import msdtime  # noqa: E402

a, rows, info = msdtime.extract(10, (297.0, 394.3, 504.5, 542.8), [1, 2, 3, 4])
print(info)
dx = abs(info["mx"])
dy = abs(info["my"])
hdr = [
    "Fig. 9b of Fu et al. 2019, Polymers 11, 975: MSD-time curves of DGEBA-NA at seven temperatures.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image on p. 10 (Origin export); no source data published.",
    "Columns: series = legend label (temperature); time_ps = x in ps; msd_A2 = MSD in Angstrom^2 (line centre); px_x, px_y = pixel in the embedded image.",
    "Axis fit: x on the inward major ticks 5, 10, 15, 20 ps (max residual %.4f ps); y on ticks %s (max residual %.4f A^2)." % (info["rx"], [1, 2, 3, 4], info["ry"]),
    "Frame edges map to x = %.3f and %.3f ps, y = %.3f and %.3f A^2." % (info["x_left"], info["x_right"], info["y_bot"], info["y_top"]),
    "One row per pixel column (%.4f ps). Uncertainty about +-1 px: +-%.3f A^2 in y; lines are about 2-3 px wide." % (dx, dy),
    "Columns where a curve is hidden under another curve or the legend are missing; for 350K (red) also the columns around the red dashed 15-ps marker.",
]
dc.write_csv(str(ROOT / "figures/fig9b.csv"), hdr, ["series", "time_ps", "msd_A2", "px_x", "px_y"],
             [(s, x, y, int(c), py) for s, x, y, c, py in rows], fmt=["{}", "{:.4f}", "{:.4f}", "{}", "{:.1f}"])
(ROOT / "work").mkdir(exist_ok=True)
dc.overlay(a, [(c, py) for _, _, _, c, py in rows], str(ROOT / "work/fig9b_overlay.png"))
print(len(rows), "rows")
