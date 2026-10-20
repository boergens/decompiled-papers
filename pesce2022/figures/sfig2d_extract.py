"""Extract Supplementary Fig. 2d of Pesce et al. 2022 (supplement p. 3): NeuN intensity profile along depth, mean +- SD band,
4 series drawn as vector paths (see profiles_common.py for the path structure).
    python3 -I -B sfig2d_extract.py   -> sfig2d.csv (+ ../work/agent_profiles/sfig2d_overlay.png and sfig2d_orig.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profiles_common as pc  # noqa: E402

PANEL = "sfig2d"
CLIP = pc.pp.R(360, 70, 545, 202)                     # panel box in PDF points (axes, tick labels and legend)
SERIES = [('SWITCH – Hepes buffer', 'black'),
          ('SWITCH – Hepes buffer + Q/U', 'red'),
          ('SHIELD – Hepes buffer', 'blue'),
          ('SHIELD – Hepes buffer + Q/U', 'green')]        # (printed legend name, colour family) in legend order
DESC = [
    'Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 2d (supplement p. 3): NeuN labelling intensity profile along the depth,',
    '  antibody in HEPES buffer or HEPES + 2.5% Quadrol + 0.5 M urea (Q/U), SWITCH- and SHIELD-processed slices (37 C, N = 3).',
]

if __name__ == "__main__":
    diag = pc.extract_panel(pc.SUPP, 3, CLIP, SERIES, PANEL, pc.make_comments(DESC, PANEL + "_extract.py"))
    print(pc.describe(diag))
    print("wrote", PANEL + ".csv", diag["rows"], "rows")
