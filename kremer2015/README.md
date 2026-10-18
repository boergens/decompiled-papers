# kremer2015: decompiled

A. Kremer, S. Lippens, S. Bartunkova, B. Asselbergh, C. Blanpain, M. Fendrych, A. Goossens, M. Holt, S. Janssens,
M. Krols, J.-C. Larsimont, C. Mc Guire, M.K. Nowack, X. Saelens, A. Schertel, B. Schepens, M. Slezak, V. Timmerman,
C. Theunis, R. Van Brempt, Y. Visser, C.J. Guérin. "Developing 3D SEM in a broad biological context."
*Journal of Microscopy* **259** (2) (2015) 80–96. DOI [10.1111/jmi.12211](https://doi.org/10.1111/jmi.12211)
(printed on p. 1). Received 26 September 2014; accepted 28 November 2014. A. Kremer, S. Lippens and C.J. Guérin
"contributed equally" (footnote ∗∗∗∗).

DOI check: the DOI is printed in the PDF; verify-sources receipts **vs-20261013-05c3948c80** and
**vs-20261013-a70ad7c36f** (identity "confirmed": Crossref record for 10.1111/jmi.12211 matched to this PDF,
sha256 fb3402e9…, 2 899 898 bytes, the same file as `source/kremer2015.pdf`; receipts in
`~/.local/share/verify-sources/receipts/<id>/receipt.json`).

**Licence:** open access, "This is an open access article under the terms of the Creative Commons Attribution
License, which permits use, distribution and reproduction in any medium, provided the original work is properly
cited." (p. 1 footer); "© 2015 The Authors / Journal of Microscopy © 2015 Royal Microscopical Society". A footnote
says "The copyright line for this article was changed on June 17, 2015 after original online publication."

## Source files

| file | what it is |
|---|---|
| `source/kremer2015.pdf` | the article, 17 pp., **publisher's version of record** (Wiley typesetting with the Journal of Microscopy banner, running heads "A. KREMER *ET AL.*" / "3D SEM", page numbers 80–96, the post-correction copyright line). Born-digital: embedded Photina/Lucida/MT fonts, real text layer; each of Figs. 1–8 is one embedded JPEG (200 ppi, Fig. 5 300 ppi greyscale); Table 1 is text. Copied from `papers/kremer2015/kremer2015.pdf`. `SOURCE.txt` there says: "Fetched 2026-10-13 by the lead session (oct-12-epoxy-cutting) from NCBI's PMC Open Access bucket: https://pmc-oa-opendata.s3.amazonaws.com/PMC4670703.1/PMC4670703.1.pdf (%PDF checked)." |

`papers/kremer2015/` also holds `kremer2015.txt` (an earlier text extraction, not used).

**Not available / not named:** the paper names no supplementary material, data set or source-data file, and no
videos. Nothing is missing.

**Cited works in our collection** (keys from `decompile_work/manifest.json`): `denk2004` (Denk & Horstmann, 2004,
PLoS Biol. 2, e329) and `hayworth2014` (Hayworth et al., 2014, Front. Neural Circ. 8, 68; the collection copy was
fetched from frontiersin.org with DOI 10.3389/fncir.2014.00068, the DOI printed in this reference). The other
references (Deerinck et al. 2010 is the NCMIR protocol, not `deerinck2018`; Peddie & Collinson 2014 is not
`peddie2022`) are not in the collection.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal line, DOI, dates, title, authors,
  affiliations, the three p. 1 footnotes (placed after the affiliations), key words, Summary, the p. 1 licence
  footer, Introduction, Materials and methods (SBF-SEM, FIB-SEM, Microwave tissue processing, Image processing,
  Near infrared branding), Results (four subsections), Discussion and future prospects, Acknowledgements, the 60
  references (alphabetical, unnumbered, as printed; set with `hangpars`). Figs. 1–8 with verbatim captions,
  descriptions (`\alttext`) for every panel, and Table 1 as a `tabular`. `\pdfpage{N}` at every page start (the
  markers of the figure-only pages 7–9, 12, 13 come after the figure's anchor paragraph; notes in the file say so).
- `figures/`: `fig1.png` … `fig8.png` (200 dpi renders of each figure's image area); `fig2.csv`,
  `fig2_extract.py`, `fig2.py`, `fig2_replot.png` (the length scale of Fig. 2).
- `tables/table1.csv`: Table 1 (species, tissue), written with `csv.writer` by `work/make_table1.py`.
- `decomp.sty` (copy of the osmium tools' style). Compile from this folder:
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice). It compiles without errors and without
  missing glyphs; remaining warnings are overfull lines from two long URLs/author lines and 0.8 pt figure boxes.
- `work/`: scratch, may be deleted: page renders (`p-*.png` 100 dpi, `q-*.png` 150 dpi), embedded images
  (`img/`), the transcription pipeline (`draft.py`: poppler word boxes + PyMuPDF fonts → draft with italics,
  super/subscripts and line-end hyphens; `assemble.py`: paragraphs and hyphen decisions; `build_body.py`,
  `make_main.py`: one-off assembly of `main.tex`, later edited by hand; `alt.py`: the descriptions), check output
  (`check1.txt`, `check2.txt`), `fig2_overlay.png`, `cmp_fig2.png`.

Re-run the data: `python3 -I -B figures/fig2_extract.py`, then `python3 -I -B figures/fig2.py` (any working
directory; the script reads `source/kremer2015.pdf` relative to its own location).

## Figures

All figures are raster images; `page.get_drawings()` finds no vector paths in any figure area (only the p. 1
banner and the Table 1 rules). The embedded images have distinct digests (no duplicated plates).

The paper has no data plots. The only panel with a quantitative axis is **Fig. 2**, a schematic that places
example images on a logarithmic length scale (10⁻² m … 10⁻⁹ m). Its tick marks and the five pins were digitized
(tier 3) from the embedded image: log axis fitted to the 8 tick centres (residuals ≤ 0.03 decade), ±1 px ≈ ±0.009
decade. The pins sit at about 10^-1.79, 10^-3.72, 10^-5.83, 10^-6.93 and 10^-8.53 m; the figure prints no values
for them. **Checks done:** `work/fig2_overlay.png` (detected axis, ticks, pin tops and ends drawn on the source
image) and `work/cmp_fig2.png` (`compare.py`, original next to the re-plot); I looked at both: ticks and pins
sit on the printed ones, and the re-plot has the same order, spacing and decreasing axis direction.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A–D | schematics (SBF-SEM and FIB-SEM geometry, voxel shapes) | – | – | described |
| Fig. 2 | schematic: CLEM work-flow, LM and 3D-SEM image examples, log length scale with 5 pins | `figures/fig2.csv` | 3 digitized | scale ticks and pins only |
| Fig. 3A, C | SBF-SEM block-face images (mouse lung; mouse brain) | – | – | |
| Fig. 3B, E, F | volume renderings (lung; *Arabidopsis* root tip orthoslices; plasmodesmata) | – | – | |
| Fig. 3D | EM plane with 3D segmentation (dendrite, synapse, vesicles) | – | – | |
| Fig. 4A, C, E | FIB-SEM images (fibroblasts; lung epithelial cells; corpus callosum) | – | – | |
| Fig. 4B, D, F | segmentation / volume renderings | – | – | |
| Fig. 5A–F | SBF-SEM images (brain and root tip with UA vs lanthanide; microwave-processed brain) | – | – | |
| Fig. 6A–D | volume renderings (skin SBF-SEM; keratinocyte FIB-SEM; *Medicago* root SBF-SEM; FIB-SEM subvolume) | – | – | 6D has red axis numbers 1000/2000 (no unit) |
| Fig. 7A–E | CLEM: confocal, SEM (SE2), BSE block face, confocal 3D, FIB-SEM 3D | – | – | |
| Fig. 8A–E | CLEM with NIRB: bright field, SBF-SEM, confocal Ca²⁺, SBF-SEM, segmentation | – | – | |
| Table 1 | list of samples | `tables/table1.csv` | transcribed | |

Panel counts: tier 1: 0; tier 2: 0; tier 3: 1 (Fig. 2, a schematic's scale); tier 4: 0. All other panels
(micrographs, renderings, schematics) have descriptions only.

## Text check (`check_text.py` 2026-10-17j, no options)

| coverage of PDF tokens | without text repeated on ≥ 3 pages | running text (also without in-figure text) | tex tokens found in PDF |
|---|---|---|---|
| 97.1 % | **98.9 %** | **98.9 %** | 96.2 % |

No options were needed. Every unmatched run (`--min-run 1`, `work/check2.txt`: 66 MISSING runs, 106 tokens; 61
EXTRA runs, 387 tokens) is explained:

- **Running headers and footers** (repeated, 192 tokens): "A. KREMER *ET AL.*" / "3D SEM" with page numbers, and the
  copyright footer; on pp. 8 and 12 the header "3D SEM 87/91" is not caught by the repeat filter (2 MISSING runs).
  The © sign is a "C" plus a combining circle in the text layer (17 single-token "c" runs).
- **Words run together in the text layer** (≈ 45 MISSING runs, the matching words are the EXTRA runs): in tightly
  justified lines the PDF stores no word spaces, so PyMuPDF reads e.g. "serialsectioningofthesetissuesinsidethesemchamber"
  as one token. I checked every one of these runs by script: with spaces and punctuation removed, each is
  contained in `main.tex` (the only non-match, "…sectionedat 60 musingaleica", differs just by the µ that the
  checker drops).
- **Split tokens in the text layer**: "Beitr¨age" (diaeresis as a separate glyph), "mikroskopis chen", "sus pensions",
  "Ham precht" (line-end breaks without a hyphen glyph).
- "stain-/ing" (p. 10) is broken across a column and a page; joined to "staining".

No transcription error is left. The figures carry no text layer (in-figure count 0); their labels are in `\alttext`.

`glyph_audit.py`: **0 hidden glyphs** (no control or private-use characters in PyMuPDF's text layer). It does not
catch one mis-mapped symbol: **≥ is stored as U+08D9 (ARABIC SMALL LOW NOON WITH KASRA, LucidaSansUnicode22)**, 3×
(p. 3 "≥20 nm thick", Fig. 1 caption "≥20 nm" and "≥5 nm"); checked on the page images and written as ≥.
(poppler shows the ‖ affiliation marks as control character 0x03; PyMuPDF reads them as U+2225 ∥; written ‖.)

Read-through against the page images (all symbols counted against the text layer): × (42), µ (49), ° (6), Å
(1, stored as A + combining ring; written precomposed), ≥ (3), en dashes, ‘ ’ “ ”, superscripts µm²/µm³/nm³/Ca²⁺,
subscripts H₂O/CaCl₂, italics (*X*, *Y*, *Z*, species names, *et al.*, *en bloc*, journal names), bold volume numbers.
Typography kept as printed: "E*n bloc*" on p. 3 (only "n bloc" in italics), upright "et al." in some places, decimal
commas in the captions ("19,47 × 22,42 × 7,14 µm") next to decimal points in the text.

**Line-end hyphens.** The text check cannot see them (it joins every line-end hyphen). Kept as real hyphens:
super-resolution, block-face, FIB-SEM, wave-particle, labour-intensive, labour-intense, single-particle,
laser-scanning-microscope, open-source, re-thinking (Saka & Rizzoli title), multi-dimensional (Caplan et al. title).
All others were removed, including "ultra-/microtomes" in the Summary (written "ultramicrotomes" as in the body text;
the Fig. 1 caption has "ultra-microtome" mid-line), "tiltx-/corr" (IMOD program, written "tiltxcorr") and
"inter-/plexiform".

Author names are printed in letter-spaced capitals; they are written as words ("A. KREMER"). PyMuPDF reads them as
words too, so they match.

## Errors and oddities in the paper (kept verbatim; flagged with `\decompnote` where they matter)

- Fig. 6 caption: "reconsted" (for reconstructed).
- Fig. 3F caption gives the stack as "10,35 × 7,23 × 3,9 µm" with "Scale bar: 20 µm". Our measurement: the scale
  bar is about 87 px long in the embedded image (200 ppi) while the rendered block is about 440–470 px wide, so by
  the bar the block would be roughly 100 µm wide, ten times the stated 10.35 µm; a 2 µm bar would fit. (Perspective
  rendering, so only approximate; our calculation.)
- Fig. 7C has a scale bar but the caption gives no length for it.
- Table 1 lists "Bacteria" in the heading position and then *Pichia pastoris* first. Background knowledge, not
  from the paper: *Pichia pastoris* is a yeast, not a bacterium.
- Fig. 8 caption (C) says "Red arrows", the panels show red arrowheads (D says "Arrowheads").
- Text p. 2 "Ramon Y Cajal" vs reference "Ramon y Cajal"; "Muller-Reichert" without umlaut; "1950’s and 1960s";
  "aceton"; "Knott et al., 2009" once upright; reference entries as printed (e.g. "Histochemistry." with a full
  stop, "Gazzeta", "von Berries", "Microscopy 6–8" for the Deerinck et al. NCMIR protocol).
- Discussion p. 14: "Although many of the original biological applications for SBF-SEM are in the field of
  neuroscience and protocols were optimized for brain samples (…)." is a sentence fragment as printed.
- Cross-checks of numbers between text and captions all agree: 102 images × 70 nm = 7.14 µm (Fig. 3B depth);
  25.4 µm / 4000 px = 6.35 nm (text "6.3-nm pixels"); 2000 slices × 75 nm = 150 µm (Fig. 3E, text);
  600 × 100 nm = 60 µm (Fig. 6C depth); 5 nm isotropic voxels (text and Fig. 6D).
- Our whitepaper (`web/whitepaper.md`, "Read for this draft but not cited") notes that the paper's "≥20 nm" SBF-SEM
  section limit is attributed to Denk & Horstmann (2004); that judgement is the whitepaper's, not checked here.
