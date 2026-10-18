"""Shared driver for the three hardness maps of Figure 1 (D, E, G); called by fig1d/e/g_extract.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

# geometry in the embedded Figure 1 image (1031 x 1989 px, ~404 ppi), found with image_box() and by inspection
BAR_E = dict(bar_cols=(905, 928), bar_rows=(987, 1248), label_rows=[1015.5, 1077.0, 1134.0, 1191.0, 1249.5])
BAR_G = dict(bar_cols=(904, 926), bar_rows=(1671, 1931), label_rows=[1699.0, 1760.5, 1818.0, 1874.5, 1933.0])
LABELS = [12.6, 12.2, 11.8, 11.4, 11.0]
PANELS = {
    "d": dict(region=(0, 980, 410, 1252), bar=BAR_E, scale_px=63, sb="row 1258-1260, cols 336-398"),
    "e": dict(region=(478, 980, 890, 1252), bar=BAR_E, scale_px=62, sb="row 1258-1260, cols 820-881"),
    "g": dict(region=(0, 1665, 875, 1945), bar=BAR_G, scale_px=84, sb="rows 1953-1956, cols 784-867"),
}
CAPTION = {
    "d": "Figure 1D: hardness measurements from an EMbed 812 MH block cured in a silicon mold.",
    "e": "Figure 1E: hardness measurements from EMbed 812 MH resin that was first degassed prior to curing.",
    "g": "Figure 1G: hardness measurements from EMbed 812 MH resin that was first cured on a stub (cross-section of the dome).",
}


def run(panel):
    P = PANELS[panel]
    a = img(4)
    box = image_box(a, P["region"])
    inner = (box[0] + 2, box[1] + 2, box[2] - 2, box[3] - 2)
    dots, res, slope = dotmap(a, inner, label_vals=LABELS, **P["bar"])
    um = 500.0 / P["scale_px"]
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
    save(over[box[1] - 30:box[3] + 40, box[0]:min(a.shape[1], box[2] + 160)], f"fig1{panel}_overlay.png")
    barnote = "the colour bar printed to the right of panel E (panel D has none of its own; the same bar is assumed)" \
        if panel == "d" else ("its own colour bar (right of panel E)" if panel == "e" else "its own colour bar (right of panel G)")
    write_csv(os.path.join(HERE, f"fig1{panel}.csv"), [
        "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, " + CAPTION[panel],
        f"image_extent_um: {(box[2] - box[0]) * um:.0f} {(box[3] - box[1]) * um:.0f}  (width, height of the blockface image)",
        "Hardness map: one row per coloured measurement dot on the blockface image, value read through the colour bar.",
        "Columns: grid_row (1 = top, the side labelled 'top'), grid_col (1 = left) of the measurement grid;",
        "  x_um, y_um = dot centre from the top-left corner of the blockface image, in micrometres via the 500 um scale",
        f"  bar ({P['scale_px']} px, {P['sb']}; +-2 px, so +-{2 / P['scale_px'] * 100:.0f} % in scale);",
        "  hardness_HV = Vickers hardness from the dot colour; hv_uncert = half-range of colour-bar values whose colour lies",
        "  within 3 Lab units of the best match (how sharply the colour fixes the value); lab_dist = Lab distance of the",
        "  dot colour to the best colour-bar match (JPEG colour error); rgb = median colour of the dot core (r <= 2.5 px).",
        f"Colour bar: {barnote}; 11.0-12.6 HV labels, mapped linearly on the label centres",
        f"  (max residual {res:.3f} HV); the bar extends a little above the 12.6 label.",
        "Provenance: tier 3, digitized from the embedded ~404 ppi JPEG (no vector data in the PDF) by fig1"
        + panel + "_extract.py.",
        "The dot values lie within ~0.04 HV of multiples of 0.1 HV (most within 0.02), which suggests the hardness values were recorded to 0.1 HV.",
        "Uncertainty: about +-0.05 HV typical, larger where the colour scale changes slowly with value or the JPEG",
        "  shifted the colour (see hv_uncert and lab_dist); positions +-1 px (" + f"{um:.0f} um).",
    ], ["grid_row", "grid_col", "x_um", "y_um", "hardness_HV", "hv_uncert", "lab_dist", "rgb"], rows)
    print(panel, len(rows), "dots; grid", len(cy), "x", len(cx), "; colour-bar residual", res,
          "; max lab_dist", max(r[6] for r in rows), "; HV range", min(r[4] for r in rows), max(r[4] for r in rows))
    return rows
