"""Extract Supplementary Fig. 3e of Pesce et al. 2022 (supplement p. 4): NeuN intensity profile along depth, mean +- SD band,
3 series drawn as vector paths (see profiles_common.py for the path structure).
    python3 -I -B sfig3e_extract.py   -> sfig3e.csv (+ ../work/agent_profiles/sfig3e_overlay.png and sfig3e_orig.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profiles_common as pc  # noqa: E402

PANEL = "sfig3e"
CLIP = pc.pp.R(375, 74, 545, 207)                     # panel box in PDF points (axes, tick labels and legend)
SERIES = [('SHIELD NeuN 1:50; SA 1:200', 'black'),
          ('SHIELD NeuN 1:50; SA 1:500', 'red'),
          ('SHIELD NeuN 1:50; SA 1:1000', 'blue')]        # (printed legend name, colour family) in legend order
DESC = [
    'Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 3e (supplement p. 4): NeuN labelling intensity profile along the depth',
    '  of SHIELD-processed slices, NeuN 1:50 with secondary antibody (SA) 1:200, 1:500 or 1:1000 (37 C, n = 3).',
]

if __name__ == "__main__":
    diag = pc.extract_panel(pc.SUPP, 4, CLIP, SERIES, PANEL, pc.make_comments(DESC, PANEL + "_extract.py"))
    print(pc.describe(diag))
    print("wrote", PANEL + ".csv", diag["rows"], "rows")
