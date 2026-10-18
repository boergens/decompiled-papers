"""Fig. 4a: bond-length distributions of DGEBA and the primary crosslinking structures
DGEBA-MTHPA and DGEBA-NA -> figures/fig4a.csv (tier 3, digitized).

Run from anywhere: python3 -I figures/fig4a_extract.py. Embedded image 650 x 486 px, 220 ppi,
p. 6 of source/fuk2019.pdf. Method: tools/bondlen.py. Writes work/fig4a_overlay.png.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bondlen as bl  # noqa: E402
import digitize_common as dc  # noqa: E402
import fukplot as fp  # noqa: E402

a = fp.load(6, (84.8, 557.4, 297.2, 716.4))
frame = (79, 646, 12, 427)        # axis box lines (frame_lines)
cal = bl.calibrate(a, frame, [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6], [0, 10, 20, 30, 40])
NAMES = ["DGEBA", "DGEBA-MTHPA", "DGEBA-NA"]   # legend: blue, red, black
rows, _ = bl.traces(a, cal, frame, [(0, 0, 255), (255, 0, 0), (0, 0, 0)], NAMES,
                    [(114, 20, 295, 88), (590, 15, 640, 60)],   # legend; panel letter "(a)"
                    min_extent={"DGEBA": 8, "DGEBA-MTHPA": 8, "DGEBA-NA": 18})
print({k: v for k, v in cal.items() if k not in ("fx", "fy")})
hdr = [
    "Fig. 4a of Fu et al. 2019, Polymers 11, 975: bond-length distributions of the primary crosslinking structures and DGEBA.",
    "Provenance: tier 3, digitized from the embedded 220 ppi raster image on p. 6 (Origin export); no source data published.",
    "Columns: series = legend entry (DGEBA blue, DGEBA-MTHPA red, DGEBA-NA black); r_A = bond length in Angstrom; density_mid = line centre;",
    "density_upper / density_lower = upper and lower end of the line in that pixel column (half a line width inside the ink); use density_upper",
    "for peak heights. px_x, px_y = pixel in the embedded image. Missing columns: the series is hidden under another curve there.",
    "Axis fit on inward major ticks: x 1.0-1.6 (max residual %.4f A), y 0-40 (max residual %.3f); frame x = %.4f..%.4f A, y = %.2f..%.2f." % (
        cal["rx"], cal["ry"], cal["x_left"], cal["x_right"], cal["y_bot"], cal["y_top"]),
    "One row per pixel column: %.5f A. Uncertainty about +-1 px = +-%.2f in density. Black text labels and arrows removed as components < 18 px, red/blue specks (dotted ellipse) as components < 8 px." % (
        abs(cal["mx"]), abs(cal["my"])),
]
dc.write_csv(str(ROOT / "figures/fig4a.csv"), hdr,
             ["series", "r_A", "density_mid", "density_upper", "density_lower", "px_x", "px_y"], rows,
             fmt=["{}", "{:.5f}", "{:.3f}", "{:.3f}", "{:.3f}", "{}", "{:.1f}"])
img = a.copy()
COLS = {"DGEBA": (255, 160, 0), "DGEBA-MTHPA": (0, 200, 0), "DGEBA-NA": (255, 0, 255)}
for n, x, y, yu, yl, c, ym in rows:
    img[int(round(ym)), c] = COLS[n]
from PIL import Image  # noqa: E402
(ROOT / "work").mkdir(exist_ok=True)
Image.fromarray(img).save(ROOT / "work/fig4a_overlay.png")
