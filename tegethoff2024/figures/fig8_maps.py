"""Shared driver for the three hardness maps of Figure 8 (A, C, E); called by fig8a/c/e_extract.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

# geometry in the embedded Figure 8 image (1400 x 1842 px, ~337 ppi), found with image_box() and by inspection
BAR_A = dict(bar_cols=(236, 252), bar_rows=(54, 505), label_rows=[52.5, 205.0, 357.0, 504.0])
LABELS = [25, 20, 15, 10]
PANELS = {
    "a": dict(region=(0, 40, 220, 620), bar=BAR_A, scale_px=45, sb="row 618, cols 165-209"),
    "c": dict(region=(0, 700, 240, 1185), bar=BAR_A, scale_px=44, sb="row 1189, cols 182-225"),
    "e": dict(region=(0, 1290, 240, 1750), bar=BAR_A, scale_px=53, sb="row 1749, cols 177-229"),
}
CAPTION = {
    "a": "Figure 8A (left): blockface image of a ROTO stained brain embedded in EMbed 812 MH resin, with hardness dots.",
    "c": "Figure 8C (left): blockface image of a ROTO + UA + Pb stained brain surrounded first with 12% gelatin and then"
         " embedded in EMbed 812 medium hard resin, with hardness dots.",
    "e": "Figure 8E (left): blockface image of a ROTO + UA + Pb stained brain surrounded first with 12% gelatin stained with"
         " ROTO and then embedded in EMbed 812 medium hard resin, with hardness dots.",
}


def run(panel):
    P = PANELS[panel]
    a = img(11)
    box = image_box(a, P["region"])
    inner = (box[0] + 2, box[1] + 2, box[2] - 2, box[3] - 2)
    dots, res, slope = dotmap(a, inner, label_vals=LABELS, **P["bar"])
    um = 200.0 / P["scale_px"]
    # grid indices: cluster the x and y centres
    def clusters(v, tol=12):
        v = sorted(v)
        c = [[v[0]]]
        for x in v[1:]:
            (c[-1].append(x) if x - c[-1][-1] < tol else c.append([x]))
        return [np.mean(k) for k in c]
    cx = clusters([d[0] for d in dots])
    cy = clusters([d[1] for d in dots])
    rows = []
    for x, y, v, dist, lo, hi, rgb in sorted(dots, key=lambda d: (round(d[1] / 12), d[0])):
        r = int(np.argmin([abs(y - k) for k in cy])) + 1
        c = int(np.argmin([abs(x - k) for k in cx])) + 1
        rows.append((r, c, (x - box[0]) * um, (y - box[1]) * um, v, max(v - lo, hi - v), dist,
                     "%d %d %d" % rgb))
    over = mark(a, [(d[0], d[1]) for d in dots], colour=(0, 0, 0), r=2)
    save(over[box[1] - 30:box[3] + 40, box[0]:min(a.shape[1], box[2] + 160)], f"fig8{panel}_overlay.png")
    barnote = "the colour bar printed in panel A (labels 10-25, 'HV')" + ("" if panel == "a" else
               "; panel " + panel.upper() + " has no colour bar of its own, the same bar is assumed")
    write_csv(os.path.join(HERE, f"fig8{panel}.csv"), [
        "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, " + CAPTION[panel],
        f"image_extent_um: {(box[2] - box[0]) * um:.0f} {(box[3] - box[1]) * um:.0f}  (width, height of the blockface image)",
        "Hardness map: one row per coloured measurement dot on the blockface image, value read through the colour bar.",
        "Columns: grid_row (1 = top), grid_col (1 = left) of the measurement grid;",
        "  x_um, y_um = dot centre from the top-left corner of the blockface image, in micrometres via the 200 um scale",
        f"  bar ({P['scale_px']} px, {P['sb']}; +-2 px, so +-{2 / P['scale_px'] * 100:.0f} % in scale);",
        "  hardness_HV = Vickers hardness from the dot colour; hv_uncert = half-range of colour-bar values whose colour lies",
        "  within 3 Lab units of the best match (how sharply the colour fixes the value); lab_dist = Lab distance of the",
        "  dot colour to the best colour-bar match (JPEG colour error); rgb = median colour of the dot core (r <= 2.5 px).",
        f"Colour bar: {barnote}; 10-25 HV labels, mapped linearly on the label centres",
        f"  (max residual {res:.3f} HV).",
        "Provenance: tier 3, digitized from the embedded ~337 ppi JPEG (no vector data in the PDF) by fig8"
        + panel + "_extract.py.",
        "Uncertainty: about +-0.3 HV typical (the bar spans 15 HV over ~450 px), larger where the colour scale changes slowly with value or the JPEG",
        "  shifted the colour (see hv_uncert and lab_dist); positions +-1 px (" + f"{um:.0f} um).",
    ], ["grid_row", "grid_col", "x_um", "y_um", "hardness_HV", "hv_uncert", "lab_dist", "rgb"], rows)
    print(panel, len(rows), "dots; grid", len(cy), "x", len(cx), "; colour-bar residual", res,
          "; max lab_dist", max(r[6] for r in rows), "; HV range", min(r[4] for r in rows), max(r[4] for r in rows))
    return rows
