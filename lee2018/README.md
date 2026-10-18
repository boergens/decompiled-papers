# lee2018: decompiled

Timothy J. Lee, Aditi Kumar, Aishwarya H. Balwani, Derrick Brittain, Sam Kinn, Craig A. Tovey, Eva L. Dyer,
Nuno M. da Costa, R. Clay Reid, Craig R. Forest, Daniel J. Bumbarger. "Large-scale neuroanatomy using LASSO:
Loop-based Automated Serial Sectioning Operation." *PLoS ONE* **2018**, 13(10): e0206172.
DOI [10.1371/journal.pone.0206172](https://doi.org/10.1371/journal.pone.0206172) (printed in the PDF on every page).
Received July 19, 2018; accepted October 8, 2018; published October 23, 2018. Editor: Konradin Metze.

DOI check: verify-sources receipts `vs-20261013-7abb3bf228` and `vs-20261013-f89f114716`
(`~/.local/share/verify-sources/receipts/<id>/receipt.json`): Crossref resolved the DOI to this article, and the
receipts' PDF (sha256 `5cbc8273…4158bc6`, 3 014 079 bytes, 16 pages) is the file in `source/`.

**Licence:** © 2018 Lee et al., open access under the Creative Commons Attribution License (CC BY), as stated on p. 1.

## Source files

| file | what it is |
|---|---|
| `source/lee2018_lasso.pdf` | the article, 16 pp. **Publisher version of record** (PLOS ONE typesetting, Arbortext/PDFlib, page footers "PLOS ONE \| https://doi.org/10.1371/journal.pone.0206172 October 23, 2018 n / 16"). Copied from `papers/lee2018/`, whose `SOURCE.txt` says: "lee2018_lasso.pdf: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0206172&type=printable (curl, 2026-10-13)". Born-digital; all five figures are embedded 300 ppi JPEG rasters (no vector plot data). |

`papers/lee2018/` also holds `lee2018_lasso.txt` / `.raw.txt` (earlier text extractions; not used).

**Not available (not in `papers/lee2018/`):** the two supporting files, *S1 Protocol* (fabrication protocol for
the TEM substrates, PDF) and *S1 Movie* (section pickup and placement, AVI). The Data Availability Statement says
"All relevant data are within the paper and its Supporting Information files"; no data set (tier-1 source) is named,
so there is none to fetch beyond these two files. Neither carries the plotted data, as far as their captions say.

**Cited works in our collection** (from `decompile_work/manifest.json`):
- ref. 5 (Lee WCA et al. 2016, Nature 532:370) = `lee2016` (the local PDF is the PMC author manuscript); also point [L] in Fig 1;
- ref. 6 (Zheng Z et al., bioRxiv 2017 May 22) = `zheng2018` (the local PDF is the bioRxiv version posted June 13, 2017, i.e. probably a later version than the one cited); also point [M] in Fig 1.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: title, authors, affiliations, the joint-senior and
  corresponding-author notes, abstract, the p. 1/p. 2 sidebar (citation, editor, dates, copyright, data
  availability, funding, competing interests; placed after the abstract), all sections, Eqs (1)–(7) and the two
  unnumbered equations as LaTeX math, the five figures with verbatim captions and figure DOIs, supporting-information
  list, acknowledgments, author contributions, 43 references. `\pdfpage{N}` marks every page start.
- `figures/`: `fig1.png` … `fig5.png` (whole figures, 200 dpi, `crop.py`); per plotted panel `<panel>.csv`,
  `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png`.
- `tables/`: empty. The paper has no tables.
- `tools/digitize_common.py`: copy of the shared helper (read-only copy, imported by the extract scripts via
  `sys.path.insert(0, <key>/tools)`).
- `decomp.sty`: copy, so `lualatex -interaction=nonstopmode -halt-on-error main.tex` compiles from this folder.
- `work/`: scratch (page renders, native figure images, overlays `*_overlay*.png`, side-by-side checks `cmp_*.png`,
  glyph crops, check JSON). May be deleted.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice) compiles without errors and without
missing characters; a few overfull lines from long URLs and the wide equation (2).

Re-run the data: `python3 -I -B figures/<panel>_extract.py` then `python3 -I -B figures/<panel>.py` (any working
directory; all paths are relative to the scripts). The extract scripts read the embedded images straight from
`source/lee2018_lasso.pdf` and write their overlays to `work/` (created if missing).

## Figures

No source data and no vector plot data exist (all figures are raster images), so every plotted panel is
**tier 3 (digitized)** from the embedded 300 ppi image, calibrated on the tick marks found in the image.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig 1 | scatter, log y (13 studies [A]–[M] + dashed line at 10⁻¹ mm³) | `figures/fig1.csv` | 3 | marker centroids; years come out within 0.02 yr of whole years |
| Fig 2a | schematic (traditional sectioning; hand, forceps, waterboat, grid inset) | – | – | description only |
| Fig 2b | schematic (LASSO robot; loop and substrate insets) | – | – | description only |
| Fig 3 | process schematic (7 cross-sections, colour key) | – | – | steps transcribed in `\alttext` |
| Fig 4 | 3D surface plot, yield(m, c), no colour bar | `figures/fig4.csv` | 3 | **outline of the surface only** (see below) |
| Fig 5a | photograph (4 substrates on a tray) | – | – | |
| Fig 5b | photograph (apertures, sections, loop) | – | – | |
| Fig 5c | TEM micrograph | – | – | |
| Fig 5d | TEM micrograph with red annotation | – | – | |
| Fig 5e | line plot, 2 ESF curves with bands | `figures/fig5e.csv` | 3 | per pixel column: line centre, band low/high; region boundaries in the header |
| Fig 5f | scatter + 2 marginal histograms + dashed box | `figures/fig5f.csv` | 3 | histograms complete; scatter only the 181 separable markers of 631 |
| Fig 5g | 2 overlapping histograms | `figures/fig5g.csv` | 3 | bins and counts of both series |

How the harder panels were done:
- **Fig 4.** In MATLAB's orthographic 3D view each boundary curve of the surface lies in a plane of the plot box
  (c = 80, m = 100, c = c_min, m = m_min), and a point in a known plane maps affinely to the image. The m and c axis
  lines were fitted to their pixels; the slanted tick marks were intersected with the axis lines (m = 0, 20;
  c = 0…80; z = 0…100); the outer contour of the coloured surface was split at its four corners and each piece
  inverted into its plane. The box corners come out at m ≈ 0.24 … 99.95 and c ≈ 1.15 … 80.19, i.e. the box spans
  m 0–100 and c 1–80 to within 2–3 px. The left outline (the yellow ridge) is read in the plane **m = 2** — an
  assumption from the caption ("we mandate at least two substrates per batch"); see the next section for why it fits.
  The interior of the surface is not given: the figure has no colour bar.
- **Fig 5f.** The top and right histograms have different bin widths (0.0230 and 0.0297 mm); bar ends were read at
  sub-pixel precision. The centroid markers overlap in a dense core that cannot be separated, so the scatter rows
  are incomplete (181 found by template matching; those in the core flagged).
- **Fig 5g.** The two semi-transparent histograms have different bin grids (2.17 s and 2.63 s). The taller bar of
  each column is the top of any grey; the lower one is the top of the darker overlap grey; heights were assigned to
  the two series so that every bar is flat across its bin (least squares over both grids). Where the two bins almost
  coincide the series of the taller bar was decided from its own solid or dashed vertical outline.

**Checks done:** every extraction draws its points back onto the source image (`work/fig1_overlay*.png`,
`fig4_overlay*.png`, `fig5e_overlay*.png`, `fig5f_overlay*.png`, `fig5f_ov_*.png`, `fig5g_overlay*.png`), and every
re-plot was put next to the original with `compare.py` (`work/cmp_fig1.png`, `cmp_fig4.png`, `cmp_fig5e.png`,
`cmp_fig5f.png`, `cmp_fig5g.png`). I looked at all of them: the points sit on the plotted markers, lines, bar tops
and outlines, and all series, ranges and scales match. Known gaps: Fig 5f core markers (see above); in Fig 5g a few
1–2-count bars are only 2–4 px tall.

### Cross-checks against numbers in the text (my computations from the CSVs)

| quantity | paper | from the digitized data |
|---|---|---|
| ESF slope, Luxel (blue), Fig 5e | −2.56 | −2.57 (linear segment of the blue line) |
| ESF slope, SiN (red), Fig 5e | −2.98 | −2.98 |
| centroids in Fig 5f histograms | 631 | x histogram sums to 631, y histogram to 630 |
| x centroid, mean ± s.d. | −20 ± 110 μm | −16 ± 98 μm (from binned counts) |
| y centroid, mean ± s.d. | 60 ± 150 μm | 53 ± 120 μm (from binned counts) |
| centroids inside the dashed box | 587/631 | dashed box at ±0.17 mm in x and y (x: 586 inside from the x histogram alone) |
| pickup time, Fig 5g dashed | 18.9 s ± 9.7 s | 18.4 ± 8.4 s (binned) |
| cycle time, Fig 5g solid | 43.5 s ± 11.7 s | 42.8 ± 9.9 s (binned) |
| counts in Fig 5g | ≤ 729 sections processed | the bars sum to 782 (pickup) and 756 (pickup and placement), more than 729: not explained by the paper |

**Fig 4 vs the paper's own model (my computation, not in the paper):** evaluating Eqs (1)–(3) with n = 25 000,
p′ = 0.01 (the text gives p = 0.01 for a section; p′ is not stated) and an integer number of batches
k = ⌈n/(c·m)⌉ reproduces the digitized outline: c = 80 edge, e.g. m = 72: 41.3 vs digitized 41.3, m = 99: 29.9 vs
29.4, m = 56: 50.3 vs 51.4; m = 100 edge: 29.3 / 21.6 / 15.9 / 11.7 / 6.3 / 3.4 / 1.4 vs digitized
29.4 / 21.6 / 15.8 / 11.0 / 6.5 / 3.7 / 1.3; left outline in the plane m = 2: c = 16: 92.3 vs 91.7, c = 52:
97.6 vs 97.4, c = 77: 98.3 vs 98.4. The same model gives 91.1 % at m = 4, c = 40 (text: "∼91%") and 91.8 %
failure for traditional sectioning (text: "≈ 92%"). This supports p′ = 0.01 and m_min = 2 as the figure's inputs,
but the paper does not state them.

## Text check (`tools/check_text.py` 2026-10-17j, no options)

`python3 -I -B …/tools/check_text.py main.tex source/lee2018_lasso.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 97.2 % | **98.5 %** (118 repeated tokens) | 98.7 % | 99.7 % | 2 runs (13 tokens, equation tokens) | 0 |

Every unmatched run (`--min-run 1`: 56 MISSING runs, 111 tokens; 15 EXTRA runs, 22 tokens) is explained:
- **boilerplate:** running header "Neuroanatomy using LASSO" + "PLOS ONE", page footers "October 23, 2018" and
  "n / 16" (repeated filter plus leftovers on single pages); three ORCID icons read as "ID" on p. 1;
- **equation tokens (p. 6–7):** the text layer of the TeX Computer Modern equation fonts gives "(" as "ð", ")" as
  "Þ", "=" as "¼", "[" as "½", subscripts glued to letters ("tload", "p0" for p′), and drops ∗, −, ≈ (see the glyph
  audit); the LaTeX math in `main.tex` gives different tokens (the EXTRA side: p, i, n, 1, losing, t, …). No prose
  word is among them;
- **"ffi" on p. 8:** the ≅ in "t_load time, traditional ≅ t_load time, LASSO" is stored as "ffi" in the text layer
  (written as ≅ from the page image);
- **real hyphens at line ends** joined by the tool: "Loop-based" (abstract), "end-effector" (p. 2);
- **reference 26:** its number is extracted at the end of p. 15 in the text layer; it is printed on p. 16.

Read-through against the page images (step 4): all equations, sub- and superscripts (mm³, 10³–10⁴, 10³ to 10⁵,
p_x = p_y, t_load time…), the superscript asterisk in "c*m" (p. 6, printed as c\*m with a raised asterisk), the
prime in p’, ±, μm, ∼ (written as U+223C), "95 ºC" (printed with the º ordinal-style degree sign, kept), ">> 3 mm",
"< 40 nm", "< 30 s", italics (scalability, consecutive, in silico, in situ, variables, caption italics), bold caption
titles, and the text order around the figures and the sidebar.

**Glyph audit** (`decompile_work/tools/glyph_audit.py source/lee2018_lasso.pdf --crops work/glyphs`): 24 hidden
glyphs, all in the equations on pp. 6–7 (TeX_CM_Maths_Symbols / Extension): 10 × U+0003 = ∗, 11 × U+0000 = −,
1 × U+0019 = ≈, 2 × U+0012/U+0013 = the big parentheses of Eq (5). All 24 crops were checked against `main.tex`;
every symbol is there.

## Errors and oddities in the paper

- Eq (3): the exponent of (P) is printed as *i* although the sum runs over *j* (kept, with a note in `main.tex`).
- Eq (4) has the subscript "pickup, traditional", the text right after it defines "t_pickup, manual".
- Conclusion: "two-sided Fisher test, p = .05"; Results: "(p < .05)". My two-sided Fisher exact test on
  727/729 vs 3649/3700 gives p = 0.008 (scipy; my computation), so "p = .05" is inaccurate.
- Abstract: "to access ssTEM scalability" (assess); "the probably of losing" (p. 6, probability); "number of section
  to be processed" (p. 7); "Consecutive sections are never placed on the same batch" (p. 4; elsewhere: the same
  substrate); "these specifics components", "these substrates could used with" (p. 12).
- Fig 1 caption: "(reference M Zheng, Z., *et. al.*, 207)": 207 for 2017; the legend has 2017.
- Fig 2: the label "Foreceps" (forceps) inside the drawing.
- Fig 4 caption: "1 < m < 100" but the lower bound is explained as "at least two substrates per batch" (and the
  plotted surface fits m starting at 2, see above); "0 < c < 80" while the plot box starts at c ≈ 1.
- Fig 5 caption: "Scale bar: 10 nm" for panel d has no closing period before "(e)"; "a 100 nm-thick silicon nitride
  support films".
- Fig 5g: the histogram bars sum to more than the 729 sections (above).
- References: refs 2 and 18 are the same paper (Gay & Anderson 1954), with different page ranges ("1071–3" vs
  "1071–1073"); "Lickthman" (ref 16), "Hazlettt" (ref 27), "Deveopment" (ref 35), "et. al.,." (ref 12),
  "Front Neuroanat.2015" (ref 29), "Mucciolo," without initials (ref 35).
- Acknowledgments: "Dol/IBC" (DoI/IBC), "not withstanding", "either expressed or implied, or IARPA" (of IARPA).

## Known problems

- Fig 5f scatter: only 181 of the 631 centroids are given (the dense core cannot be separated); use the histograms.
- Fig 4: only the outline; the left outline relies on the assumption m = 2; near the bottom-left corner
  (yield < ~25) the outline runs into a thin black line and is not reliable there.
- Fig 5g: totals exceed 729 (figure as printed); 1-count bars are 2 px tall.
- S1 Protocol and S1 Movie are not available locally.
