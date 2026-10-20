"""Extract Fig. 1c of Pesce et al. 2022 (main PDF p. 3): NeuN intensity profile along depth, mean +- SD band,
3 series drawn as vector paths (see profiles_common.py for the path structure).
    python3 -I -B fig1c_extract.py   -> fig1c.csv (+ ../work/agent_profiles/fig1c_overlay.png and fig1c_orig.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profiles_common as pc  # noqa: E402

PANEL = "fig1c"
CLIP = pc.pp.R(360, 50, 520, 172)                     # panel box in PDF points (axes, tick labels and legend)
SERIES = [('SHORT – 4 °C', 'black'),
          ('SHORT – 37 °C', 'red'),
          ('Classic SWITCH', 'blue')]        # (printed legend name, colour family) in legend order
DESC = [
    'Pesce et al. 2022 Commun Biol 5:447, Fig. 1c (main PDF p. 3): NeuN immunofluorescence intensity profile along the depth of',
    '  SWITCH-processed human brain slices: SHORT protocol at 4 C vs 37 C and classic SWITCH; mean +- SD of three regions.',
]

if __name__ == "__main__":
    diag = pc.extract_panel(pc.MAIN, 3, CLIP, SERIES, PANEL, pc.make_comments(DESC, PANEL + "_extract.py"))
    print(pc.describe(diag))
    print("wrote", PANEL + ".csv", diag["rows"], "rows")
