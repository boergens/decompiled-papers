"""Extract Fig. 1e of Pesce et al. 2022 (main PDF p. 3): NeuN intensity profile along depth, mean +- SD band,
3 series drawn as vector paths (see profiles_common.py for the path structure).
    python3 -I -B fig1e_extract.py   -> fig1e.csv (+ ../work/agent_profiles/fig1e_overlay.png and fig1e_orig.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profiles_common as pc  # noqa: E402

PANEL = "fig1e"
CLIP = pc.pp.R(360, 280, 520, 400)                     # panel box in PDF points (axes, tick labels and legend)
SERIES = [('1 mM CuSO4 – 37 °C', 'black'),
          ('10 mM CuSO4 – 37 °C', 'red'),
          ('SHORT – 37 °C', 'blue')]        # (printed legend name, colour family) in legend order
DESC = [
    'Pesce et al. 2022 Commun Biol 5:447, Fig. 1e (main PDF p. 3): NeuN immunofluorescence intensity profile along the depth,',
    '  autofluorescence treatment with 1 mM or 10 mM CuSO4 vs untreated SHORT, all at 37 C; mean +- SD of three regions.',
]

if __name__ == "__main__":
    diag = pc.extract_panel(pc.MAIN, 3, CLIP, SERIES, PANEL, pc.make_comments(DESC, PANEL + "_extract.py"))
    print(pc.describe(diag))
    print("wrote", PANEL + ".csv", diag["rows"], "rows")
