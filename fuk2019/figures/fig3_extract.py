"""Fig. 3: bond-length distributions of the monomers NA, MTHPA, DGEBA -> figures/fig3.csv (main
plot) and figures/fig3inset.csv (inset). Tier 3, digitized. Both panels come from the same
embedded image (702 x 518 px, 220 ppi, p. 6 of source/fuk2019.pdf), so one script does both.

Run from anywhere: python3 -I figures/fig3_extract.py. Method: tools/bondlen.py. Writes
work/fig3_overlay.png (traced line centres in magenta/green/orange over the image).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bondlen as bl  # noqa: E402
import digitize_common as dc  # noqa: E402
import fukplot as fp  # noqa: E402

a = fp.load(6, (182.5, 209.9, 411.9, 379.4))
PAL = [(0, 0, 0), (255, 0, 0), (0, 0, 255)]
NAMES = ["NA", "MTHPA", "DGEBA"]            # legend: NA black, MTHPA red, DGEBA blue
COLS = {"NA": (255, 0, 255), "MTHPA": (0, 200, 0), "DGEBA": (255, 160, 0)}
img = a.copy()

# main plot: axis box lines at columns 83 / 686 and rows 13 / 454 (found with frame_lines)
frame = (83, 686, 13, 454)
cal = bl.calibrate(a, frame, [1.1, 1.2, 1.3, 1.4, 1.5], [0, 10, 20, 30, 40])
blank = [(120, 20, 246, 94),     # legend
         (378, 12, 690, 192)]    # inset with its tick labels
rows, _ = bl.traces(a, cal, frame, PAL, NAMES, blank, min_extent=18)
# inset: frame columns 410 / 652, rows 20 / 190; ticks 1.44-1.54 (1.56 at the right frame), 0-40
iframe = (410, 652, 20, 190)
ical = bl.calibrate(a, iframe, [1.44, 1.46, 1.48, 1.50, 1.52, 1.54], [0, 5, 10, 15, 20, 25, 30, 35, 40], tick_len=2)
irows, _ = bl.traces(a, ical, iframe, PAL, NAMES, [(412, 22, 475, 58)], min_extent=10)
print({k: v for k, v in cal.items() if k not in ("fx", "fy")})
print({k: v for k, v in ical.items() if k not in ("fx", "fy")})

common = [
    "Provenance: tier 3, digitized from the embedded 220 ppi raster image on p. 6 (Origin export); no source data published.",
    "Columns: series = legend entry (NA black, MTHPA red, DGEBA blue); r_A = bond length in Angstrom; density_mid = line centre;",
    "density_upper / density_lower = upper and lower end of the line in that pixel column (half a line width inside the drawn ink): on steep flanks",
    "the curve passes through that whole range; use density_upper for peak heights. px_x, px_y = pixel in the embedded image (centre).",
    "Missing columns: the series is hidden under another curve there (e.g. NA under MTHPA at C=O, C=C, C-O and along the zero baseline).",
]
hdr = ["Fig. 3 (main plot) of Fu et al. 2019, Polymers 11, 975: bond-length distributions of the monomers DGEBA, MTHPA and NA."] + common + [
    "Axis fit on inward major ticks: x 1.1-1.5 (max residual %.2g A), y 0-40 (max residual %.3f); frame x = %.4f..%.4f A, y = %.2f..%.2f." % (
        cal["rx"], cal["ry"], cal["x_left"], cal["x_right"], cal["y_bot"], cal["y_top"]),
    "One row per pixel column: %.5f A. Uncertainty about +-1 px = +-%.2f in density; text labels and the red dotted circle removed as small components." % (
        abs(cal["mx"]), abs(cal["my"])),
]
ihdr = ["Fig. 3 (inset) of Fu et al. 2019, Polymers 11, 975: zoom of the C-C / C-O region of the bond-length distributions."] + common + [
    "Inset axis fit on its own inward ticks: x 1.44-1.54 (1.56 at the right frame; max residual %.4f A), y 0-40 (max residual %.3f); frame x = %.4f..%.4f, y = %.2f..%.2f." % (
        ical["rx"], ical["ry"], ical["x_left"], ical["x_right"], ical["y_bot"], ical["y_top"]),
    "The inset is small (about 240 x 170 px): one row per pixel column = %.5f A; uncertainty about +-1 px = +-%.2f in density." % (
        abs(ical["mx"]), abs(ical["my"])),
]
cols = ["series", "r_A", "density_mid", "density_upper", "density_lower", "px_x", "px_y"]
fmt = ["{}", "{:.5f}", "{:.3f}", "{:.3f}", "{:.3f}", "{}", "{:.1f}"]
dc.write_csv(str(ROOT / "figures/fig3.csv"), hdr, cols, [r[:5] + (r[5], r[6]) for r in rows], fmt=fmt)
dc.write_csv(str(ROOT / "figures/fig3inset.csv"), ihdr, cols, [r[:5] + (r[5], r[6]) for r in irows], fmt=fmt)
for n, x, y, yu, yl, c, ym in rows + irows:
    img[int(round(ym)), c] = COLS[n]
from PIL import Image  # noqa: E402
(ROOT / "work").mkdir(exist_ok=True)
Image.fromarray(img).save(ROOT / "work/fig3_overlay.png")
print(len(rows), len(irows))
