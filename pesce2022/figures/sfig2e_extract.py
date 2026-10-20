"""Extract Supplementary Fig. 2e of Pesce et al. 2022 (supplement p. 3): NeuN intensity profile along depth, mean +- SD band,
4 series drawn as vector paths (see profiles_common.py for the path structure).
    python3 -I -B sfig2e_extract.py   -> sfig2e.csv (+ ../work/agent_profiles/sfig2e_overlay.png and sfig2e_orig.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profiles_common as pc  # noqa: E402

PANEL = "sfig2e"
CLIP = pc.pp.R(360, 200, 545, 337)                     # panel box in PDF points (axes, tick labels and legend)
SERIES = [('SWITCH – 1 mM CuSO4 Post-Label', 'black'),
          ('SWITCH – 10 mM CuSO4 Post-Label', 'red'),
          ('SWITCH – 1 mM CuSO4', 'blue'),
          ('SWITCH – 10 mM CuSO4', 'green')]        # (printed legend name, colour family) in legend order
DESC = [
    'Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 2e (supplement p. 3): NeuN labelling intensity profile along the depth',
    '  of SWITCH-processed slices treated with 1 or 10 mM CuSO4 after (Post-Label) or before NeuN labelling (37 C, N = 3).',
]

if __name__ == "__main__":
    diag = pc.extract_panel(pc.SUPP, 3, CLIP, SERIES, PANEL, pc.make_comments(DESC, PANEL + "_extract.py"))
    print(pc.describe(diag))
    print("wrote", PANEL + ".csv", diag["rows"], "rows")
