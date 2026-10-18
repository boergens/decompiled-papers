#!/usr/bin/env python3
"""QA for Figure 3: render each panel of the original page at 300 dpi and put it side by side with the regenerated
PNG fig3<p>_replot.png (-> fig3<p>_compare.png). For panel e, a montage of the extracted face images is compared with the original crop.
Run after the fig3<p>.py scripts (any working directory). Needs ImageMagick (convert, montage)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "tools"))
import pdfplot as pp  # noqa: E402

PDF = os.path.join(ROOT, "source", "2026.10.15.759299v1.full.pdf")
page = pp.open_page(PDF, 37)
clips = {
    "a": pp.R(5, 17, 100, 100), "b": pp.R(108, 17, 252, 108), "c": pp.R(270, 17, 396, 108), "d": pp.R(398, 17, 519, 108),
    "e": pp.R(5, 118, 250, 415), "f": pp.R(258, 112, 390, 280), "g": pp.R(388, 112, 519, 280),
    "h": pp.R(258, 276, 390, 417), "i": pp.R(388, 276, 519, 417),
}
tmp = os.environ.get("FIG3_QA_TMP", os.path.join(ROOT, "work", "fig3_qa"))  # montage scratch; the 300-dpi crops go to figures/ as fig3<p>_orig.png
os.makedirs(tmp, exist_ok=True)
for p, clip in clips.items():
    orig = os.path.join(HERE, f"fig3{p}_orig.png")
    pp.render(page, clip, 300, orig)
    if p == "e":
        files = [os.path.join(HERE, f"fig3e_r{r}_{c}.png") for r in range(1, 6)
                 for c in ("gt_conscious", "recon_state1", "gt_suppressed", "recon_state2")]
        mont = os.path.join(tmp, "montage_e.png")
        subprocess.run(["montage"] + files + ["-tile", "4x5", "-geometry", "143x143+6+6", mont], check=True)
        new = mont
    else:
        new = os.path.join(HERE, f"fig3{p}_replot.png")
    subprocess.run(["convert", orig, "-resize", "600x", new, "-resize", "600x", "+append",
                    os.path.join(HERE, f"fig3{p}_compare.png")], check=True)
    print("wrote", f"fig3{p}_compare.png")
