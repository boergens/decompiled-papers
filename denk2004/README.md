# denk2004: decompiled

Winfried Denk, Heinz Horstmann. "Serial Block-Face Scanning Electron Microscopy to Reconstruct
Three-Dimensional Tissue Nanostructure." *PLoS Biology* **2**(11): e329, pp. 1900–1909 (November 2004).
DOI [10.1371/journal.pbio.0020329](https://doi.org/10.1371/journal.pbio.0020329) (printed on p. 1).
Received May 23, 2004; accepted July 29, 2004; published October 19, 2004. Academic editor: Kristen M. Harris.

**DOI check:** the DOI is printed in the PDF (p. 1 footnote block and every figure caption). verify-sources receipt
`vs-20261012-b994974778` (`~/.local/share/verify-sources/receipts/`) matched this exact file (sha256
`5091d193…bbea93`, identical to `source/denk2004.pdf`) to the Crossref record of 10.1371/journal.pbio.0020329
(identity level "confirmed", not retracted). Further receipts for the same paper are in `web/checks/receipts/`
(e.g. `vs-20261013-06372c088c`).

**Licence:** "Copyright: © 2004 Denk and Horstmann. This is an open-access article distributed under the terms of
the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any
medium, provided the original work is properly cited." (p. 1)

## Source files

| file | what it is |
|---|---|
| `source/denk2004.pdf` | copied from `papers/denk2004/denk2004.pdf`; 10 pp. (journal pp. 1900–1909). **Publisher's version of record** (PLoS Biology typesetting, 3B2 Total Publishing System, PDF created 8 Nov 2004). Born-digital with a text layer; all figures are embedded raster images (JPEG, 150 ppi; the two video stills 72 ppi). |

Fetch note, quoted from `papers/denk2004/SOURCE.txt`: "denk2004.pdf: https://journals.plos.org/plosbiology/article/file?id=10.1371/journal.pbio.0020329&type=printable (curl, 2026-10-12)".
`papers/denk2004/denk2004.txt` and `.raw.txt` (earlier text extractions) were not used.

No supplement PDF is in `papers/denk2004/`. The paper's supporting information (below) is not available here.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: title, authors, affiliation, abstract, citation line,
  the p. 1 footnote block (dates, DOI, abbreviations, copyright, academic editor, correspondence; placed after the
  citation line), Introduction, Results, Discussion with Equation (1), Materials and Methods (Imaging, Specimen
  preparation, Data analysis, Microtome), Supporting Information (legends of Datasets S1–S20 and Figures S1–S5),
  Acknowledgments, Conflicts of interest, Author contributions, 44 references (author–year, unnumbered).
  `\pdfpage{1}`…`\pdfpage{10}` mark the PDF pages.
- Figures are placed after the paragraph that spans their position: Fig. 1 after the paragraph ending at the top of
  p. 3, Fig. 2 after the one ending at the top of p. 4, Fig. 3 before "Discussion", Fig. 4 after the first paragraph
  on p. 6, Fig. 5 before "Materials and Methods"; the stills of Video 1 (p. 7) and Video 2 (p. 8) both after the
  Specimen preparation paragraph, which runs from p. 7 into p. 8.
- `figures/fig1.png` … `fig5.png`, `video1.png`, `video2.png`: rendered at 200 dpi with `crop.py`.
- `figures/fig4a.*`, `figures/fig4b.*`: data of the two plotted panels (CSV, `_extract.py`, plot `.py`, `_replot.png`).
- `tools/digitize_common.py`: copy of the osmium tool (used by the extract scripts for `embedded_image()` and `fit_axis()`).
- `decomp.sty`: copy of the osmium macros; `lualatex -interaction=nonstopmode -halt-on-error main.tex` compiles from this folder.
- `tables/`: not created; the paper has no tables.
- `work/`: scratch (page renders, native figure images, overlays `fig4a_overlay.png`, `fig4b_overlay.png`, side-by-side
  checks `cmp_fig4a.png`, `cmp_fig4b.png`, checker JSON, the scripts that built the first draft of main.tex from the
  text layer: `draft4.py` maps the symbol fonts, `scripts/assemble.py` + `scripts/fill.py` + `scripts/template.tex` + `scripts/figs/` assemble it;
  main.tex was edited by hand after that, so re-running `fill.py` would overwrite those edits). May be deleted.

Compiles cleanly with lualatex (run twice; 0 errors); only overfull boxes of 0.8–1.7 pt.

## Figures

All figures are raster images; `get_drawings()` finds no plot paths (only a rule on p. 1 and one on p. 6), so
no panel is tier 2. Fig. 4 is the only figure with quantitative axes; both its panels are **tier 3 (digitized)**
from the embedded 500 × 852 px JPEG (150 ppi), axis calibration on the tick marks (max residuals 0.22 nm and 0.19 slice in 4A,
0.20 and 0.22 nm in 4B; see CSV headers).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A | BSE block-face micrograph (motor endplate), arrows SV, SF, bar 0.50 μm | – | – | |
| Fig. 1B | BSE micrograph (muscle, actin array), arrow AA, bar 0.50 μm | – | – | |
| Fig. 1C | BSE micrograph (neocortex), dashed rectangle, bar 10 μm | – | – | |
| Fig. 1D | BSE micrograph (cortex, Epon), bar 5 μm | – | – | |
| Fig. 1E | BSE micrograph (cortex), arrows SD, bar 1 μm | – | – | |
| Fig. 2A | schematic of the cutting cycle {1}–{3} with two block-face images | – | – | |
| Fig. 2B | SEM photograph of knife, block and cut-off slices, bar 500 μm | – | – | |
| Fig. 2C | CAD rendering, microtome overview | – | – | |
| Fig. 2D | CAD rendering, knife and sample close-up | – | – | |
| Fig. 3A | five block-face slices in perspective (muscle), red reslice line, arrow MS, bar 2 μm | – | – | |
| Fig. 3B | reslice image, arrows PS, ZB, bar 2 μm | – | – | |
| Fig. 3C | cerebellum, two block faces with direction arrows, bar (blurred; appears to read "5μm") | – | – | |
| Fig. 3D | cerebellum rendered as a cube, arrow NM, bar 1 μm | – | – | |
| Fig. 4A | line plot, x shift (nm) vs slice, 5 overlapping traces | `figures/fig4a.csv` | 3 digitized | envelope of all traces per pixel column (robust) + approximate per-colour traces |
| Fig. 4B | scatter, shift_y vs shift_x (nm) | `figures/fig4b.csv` | 3 digitized | 54 separable markers; the dense central cluster as one row (centroid, extent, ~136 markers estimated from ink area) |
| Fig. 5A | BSE block-face image at 7.5 kV, bar 2 μm | – | – | |
| Fig. 5B | same field at 4 kV, bar 2 μm | – | – | |
| Fig. 5C | reslice with 7.5 kV band marked, red box, inset with arrows EM, bars 2 μm and 500nm | – | – | |
| Video 1 still | BSE block-face image (muscle) | – | – | video not available |
| Video 2 still | BSE block-face image (cortex) | – | – | video not available |

Every panel has an `\alttext` description.

**Fig. 4A in detail.** The five traces (four 256×256 subregions plus the 512×512 one, "black trace") are 1-px lines in a
chroma-subsampled JPEG and overlap almost everywhere, so they cannot be separated reliably. The CSV gives, per pixel column
(~1.26 px per slice), series `all_traces` (upper/lower envelope and ink-weighted mean) and five colour series assigned by
CIELAB hue/lightness (pink, orange, teal, lavender, black; colour names are mine, the caption names only the black trace),
flagged `mixed` where a colour class spans > 6 px in a column. The dark trace looks black to dark green in the JPEG and is
partly classified as teal, so the `black` series is sparse. On the tick calibration the two big spikes come out at slice ~58
and ~200.6, while the caption says 59 and 202 (offset of 1–1.5 slices, not corrected; noted in the CSV header).

**Checks:** both extractions were drawn back onto the source image (`work/fig4a_overlay.png`, `work/fig4b_overlay.png`) and the
replots were put side by side with the originals (`work/cmp_fig4a.png`, `work/cmp_fig4b.png`); I looked at all four: axes,
ranges and series match, the envelope follows the traces and the spikes, and every separable marker in 4B is found.

## Not available (named in the paper)

- **Tier-1 data / supporting information, none in `papers/denk2004/`:** Datasets S1–S20 ("Cortical Tissue Slices", ZIPs of
  numbered TIF images, 248–256 MB each, DOIs 10.1371/journal.pbio.0020329.sd001–sd020); Figures S1–S5 (TIFs, DOIs …sg001–sg005;
  only their legends are in the PDF); Video 1 and Video 2 (DOIs …v001, …v002; only stills are printed). None of these hold the
  Fig. 4 shift values, so Fig. 4 has no tier-1 source even in principle; the raw image stack behind Fig. 4 (muscle,
  same dataset as Figs. 3A/3B and Video 1) is not among the listed datasets either (S1–S20 are cortical tissue).

## Text check (`check_text.py` version 2026-10-17j, no options)

`python3 -I -B /home/admin/ephemeral/sep_28__osmium_chemistry/decompiled/tools/check_text.py main.tex source/denk2004.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 97.4 % | **99.4 %** (176 repeated tokens) | 99.4 % (0 in-figure tokens: the figure labels are part of the raster images) | 99.6 % | 1 | 0 |

- REPEATED: the running header "Serial Block-Face SEM" and the page footer "PLoS Biology | www.plosbiology.org … November 2004 |
  Volume 2 | Issue 11 | e329" with page numbers (boilerplate, left out).
- MISSING ≥ 6: "Open access, freely available online PLoS BIOLOGY", the p. 1 masthead (boilerplate, left out; noted in main.tex).
- All other unmatched tokens (`--min-run 1`: 34 MISSING runs / 47 tokens, 23 EXTRA runs / 35 tokens) are text-layer glyph
  problems, the same words on both sides: the symbol fonts give μ as "l" (μm, μs), × as "3" (256×256, 512×512,
  54.8 × 47.3), ° as "8" (90°, 35°, 6°, 4°C), τ as "s", η as "g"; Equation (1) is scrambled in the text layer
  ("sd ¼ RSN ð Þ2e gIb ; ð1Þ"); "vertébrés" in the Cajal reference has separate accent glyphs; and "z-axis" (p. 4) is a real
  hyphen at a line end that the checker joins.

Read-through against the page images (step 4) done for: the abstract (bold), Equation (1) (τ\_d = (R\_SN)² e / (η I\_b)) and the
italic symbols around it ((R\_SN), (τ\_d), (η), I\_B, e), E^1.67, H₂O subscripts, μm/μs, °C spacing as printed ("4 °C" on p. 7,
"4°C" on p. 8), ×, en dashes in ranges, ligatures, the umlauts (Jürgen, Schröder, Düsseldorf), the curly quotes ("smooth",
"dark field"), the italic *Caenorhabditis elegans* (text and White et al. reference), the line-end hyphens kept as real hyphens
(Low-vacuum, labor-intensive, charge-balance, secondary-electron, low-energy, heavy-metal, z-axis, one-third, computer-aided,
direct-current-motor-driven, block-face, surface-ablation, heavy-metal-stained, wide-ranging, phosphate-buffered, z-positions,
custom-machined, large-displacement, patch-clamp, cell-free, three-dimensional, electron-microscope, epsilon-subunit-deficient),
and the 44 reference entries.

## Errors and oddities in the paper (kept verbatim)

- "light microcopy" (p. 2, Martone et al.) and "multi-photon microcopy" (p. 2) for "microscopy".
- "SBFESM" for SBFSEM (p. 4).
- "on a environmental SEM" (p. 7); "crossed leave flexures" (p. 3) and "The leave springs" (p. 9) for leaf.
- Fig. 3 caption: "along the red line show in the top image"; Fig. S3 legend: "slightly more that two pixels".
- Equation (1) uses I\_b (lower-case subscript); the following text defines I\_B.
- Fig. 1 caption, (D and E): "electron energy, 7.5 keV beam current; spot, 3" (the words "beam current" have no value).
- Fig. 3 caption abbreviates "nuclear envelope" as "(NM)".
- Fig. 5 panel labels read "7.5 kV" and "4 kV" where the caption and text say keV.
- "Spotsize was 3.4" (Fig. S2 legend) while the Materials and Methods list beam currents only for spot sizes 2.5, 3 and 3.5.
- Materials and Methods: oscillating knife used for "Figures 5 and S2–S5" (p. 9), but the Imaging paragraph (p. 7) lists
  "Figures 5 and S2–S4"; the Discussion cites "Figures 5 and S2–S4".
- Fig. 4A: the spikes plot at slice ~58 and ~200.6 on the printed ticks, vs. 59 and 202 in the caption (see above).
- Background knowledge (not from the paper, not in main.tex): the reference "Frank W (1992)" is usually cited as Frank J;
  "Minski M" is Marvin Minsky; "Leichester" is Leicester; "Hukui I" is probably Fukui. These are kept as printed.

## Suggestions (tools / spec)

- `digitize_common.fit_axis()` docstring says it returns `(f, max residual)`, but it returns three values `(f, residual, slope)`;
  unpacking two values raises "too many values to unpack". Fix the docstring (or return a named tuple).
