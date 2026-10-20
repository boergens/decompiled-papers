"""Extract Supplementary Fig. 3b of Pesce et al. 2022 (supplement p. 4): NeuN intensity profile along depth, mean +- SD band,
2 series drawn as vector paths (see profiles_common.py for the path structure).
    python3 -I -B sfig3b_extract.py   -> sfig3b.csv (+ ../work/agent_profiles/sfig3b_overlay.png and sfig3b_orig.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profiles_common as pc  # noqa: E402

PANEL = "sfig3b"
CLIP = pc.pp.R(55, 228, 217, 347)                     # panel box in PDF points (axes, tick labels and legend)
SERIES = [('SHORT NeuN 1:100; SA 1:500', 'black'),
          ('SHORT NeuN 1:50; SA 1:500', 'red')]        # (printed legend name, colour family) in legend order
DESC = [
    'Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 3b (supplement p. 4): NeuN labelling intensity profile along the depth',
    "  of SHORT-processed slices, the two best antibody conditions (NeuN 1:100 or 1:50 with Alexa Fluor 647 'SA' 1:500; 37 C, n = 3).",
]

if __name__ == "__main__":
    diag = pc.extract_panel(pc.SUPP, 4, CLIP, SERIES, PANEL, pc.make_comments(DESC, PANEL + "_extract.py"))
    print(pc.describe(diag))
    print("wrote", PANEL + ".csv", diag["rows"], "rows")
