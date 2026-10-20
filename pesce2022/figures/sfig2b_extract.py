"""Extract Supplementary Fig. 2b of Pesce et al. 2022 (supplement p. 3): NeuN intensity profile along depth, mean +- SD band,
3 series drawn as vector paths (see profiles_common.py for the path structure).
    python3 -I -B sfig2b_extract.py   -> sfig2b.csv (+ ../work/agent_profiles/sfig2b_overlay.png and sfig2b_orig.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profiles_common as pc  # noqa: E402

PANEL = "sfig2b"
CLIP = pc.pp.R(185, 70, 362, 202)                     # panel box in PDF points (axes, tick labels and legend)
SERIES = [('SHIELD – AR', 'black'),
          ('SHIELD – H2O2', 'red'),
          ('SHIELD – BSA + PBST', 'blue')]        # (printed legend name, colour family) in legend order
DESC = [
    'Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 2b (supplement p. 3): NeuN labelling intensity profile along the depth',
    '  of SHIELD-processed slices incubated with BSA + PBST, treated with AR or with H2O2 (NeuN 1:100, Alexa 647 1:500, 37 C, N = 3).',
]

if __name__ == "__main__":
    diag = pc.extract_panel(pc.SUPP, 3, CLIP, SERIES, PANEL, pc.make_comments(DESC, PANEL + "_extract.py"))
    print(pc.describe(diag))
    print("wrote", PANEL + ".csv", diag["rows"], "rows")
