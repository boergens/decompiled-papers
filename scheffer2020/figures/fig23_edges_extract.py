"""Write figures/fig23_edges.csv: the arrows of Fig. 23 transcribed by eye from the figure (numbers printed on the arrows)."""
import csv
from pathlib import Path
E = [  # panel, top cell, bottom type, cells in bottom type, top->bottom (blue), bottom->top (orange), line style
    ("a", "PLP008", "LC13", 82, 16, 32, "solid"),
    ("b", "PVLP011", "LLPC1", 44, 7, 25, "solid"),
    ("b", "PVLP011", "LPC1", 113, 11, 22, "solid"),
    ("b", "PVLP011", "LPLC1", 60, 40, 54, "solid"),
    ("b", "PVLP011", "LPLC2", 85, 71, 74, "solid"),
    ("b", "PVLP011", "LC17", 186, 56, 45, "solid"),
    ("b", "PVLP161", "LC17", 186, 6, 6, "dashed"),
    ("c", "AVLP086", "LC11", 70, 5, 10, "solid"),
    ("c", "AVLP077", "LC11", 70, 4, 8, "solid"),
    ("c", "AVLP079", "LC11", 70, 13, 14, "solid"),
    ("c", "PVLP094", "LC11", 70, 3, 4, "solid"),
]
out = Path(__file__).resolve().parent.parent / "figures" / "fig23_edges.csv"
with open(out, "w", newline="") as f:
    for h in ["Fig. 23 of Scheffer et al. 2020 (eLife 9:e57443), p. 45: one-to-many motifs in the optic circuits.",
              "Transcribed by eye by the decompiler from the network diagram (not a plotted panel; numbers as printed on the arrows).",
              "Per the caption, arrow numbers are the average count of synaptic connections per one cell of the bottom group.",
              "to_bottom = blue arrow from the top cell to the bottom type; to_top = orange arrow from the bottom type to the top cell.",
              "n_bottom_cells = number printed inside the orange bottom circle. style 'dashed' = both arrows drawn dashed."]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["panel", "top_cell", "bottom_type", "n_bottom_cells", "to_bottom", "to_top", "style"])
    w.writerows(E)
print(out)
