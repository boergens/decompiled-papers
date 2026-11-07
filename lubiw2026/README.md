# lubiw2026: decompiled

Anna Lubiw and Marcus Schaefer. "Recognizing Penny and Marble Graphs is Hard for Existential Theory of the Reals."
arXiv:2508.10136v3 [cs.CG], 9 Sep 2026 (stamp on p. 1). 41 pages. Affiliations as printed: University of Waterloo; DePaul University.

**Version.** The PDF is the **arXiv preprint, version 3**. There is no journal version here, so this PDF is the reference.
It prints no journal, DOI or received/accepted dates. Under the authors it prints "September 11, 2026". The source sets no
date, so that is the compile date, two days after the stamp. The citation agrees with the task message and with `source/SOURCE.txt`.

**Text follows** the authors' TeX source of v3, checked against the v3 PDF (numbers below). No wording difference between the
two was found.

**Licence:** CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/), per the arXiv abstract page, checked 2026-11-07 by the
coordinator (`source/SOURCE.txt`). The PDF itself prints no licence line. Fig. 3's two raster insets are public-domain drawings
from Wikimedia Commons (see Fig. 3 under Figures).

**Section 1.1, "History and Background"** (the section the hexagon-clink project cites) starts on printed p. 4 and ends on printed
p. 5. Printed page numbers equal PDF page numbers throughout. It was compared word by word with the PDF text and read against the
page images of pp. 4 and 5, with no difference. Its citations are [31], [26, 9], [22], [25], [11], [10], [28], [14], [39], [38],
[8], [16], [17], [5], [19], [27], [24], [33], [2], [20], [47], [13], [48], [41], [36].

## Source files (`source/`)

| file | what it is |
|---|---|
| `lubiw2026.pdf` | arXiv v3, 41 pages, 42 587 455 bytes, born-digital (LaTeX, arXiv GenPDF; embedded Computer Modern Type 1 fonts). The text layer is the typesetter's, not OCR. |
| `arXiv-2508.10136v3.tar.gz` | the authors' source of the same version, 35 329 431 bytes: `main.tex`, `penny.bib`, `figures/` (53 files, all used), `anc/GeogebraGadgets.7z`, `00README.json`. No `.bbl`. Unpacked by the coordinator in `work/arxiv/`, read as text. |
| `SOURCE.txt` | fetch notes, licence, SHA-256 of both files. |

## Method (tool first)

`work/build_main.py` writes `main.tex` from `work/arxiv/main.tex`. It removes the authors' `%` comments (their editing notes
are not printed and are not in `main.tex`), writes out their macros, and types in the printed numbers of sections, theorems,
equations, figures, tables and citations. Details:

- Label numbers come from a draft `pdflatex -no-shell-escape` run of the source (`work/compile/arxiv.aux`). They agree with the PDF.
- The reference list comes from the PDF's text layer, because the archive has no `.bbl` and `plainurl.bst` is not installed here.
  Fonts give the italics, the PDF's link annotations give the link targets, and line-end hyphens are undone. Cite keys are mapped to
  printed numbers by finding each cited title in the printed list (`work/cite_map.json`).
- Floats stand at the end of the paragraph in which the PDF prints them. Moved against the source order: Figs. 5, 10, 12, 13, 16,
  17, 20, 21, 22, 24, 30, Tables 1 and 2 (`MOVE_BEFORE` in the script). The `\pdfpage` markers stay in order. The marker for p. 40
  falls inside a formula on the page break, so that inline formula is split in two around it.
- The decompiler read all 41 page images against the source text and the reference list, and spot-checked the compiled `main.pdf`
  (pages with displays, tables, floats and references). No text correction was needed beyond the script's rules.
- Figure descriptions are in `work/alttext.tex`. Tables as CSV: `work/build_tables.py`.

Left out: the page numbers at the foot of each page. Kept once, with a note: the arXiv stamp in the left margin of p. 1. The
authors' e-mail footnotes of p. 1 stand right after the author block. Theorem heads are written out in bold with italic statements,
as printed.

## Check results

Compiled twice with `lualatex -interaction=nonstopmode -halt-on-error main.tex`: no errors, no missing glyphs, 45 pages.
There are 36 overfull boxes, nearly all under 2 pt. The largest are 40 pt and 15 pt (refs. [4] and [19], links that cannot break) and 11 pt; they change no text.

`check_text.py` version 2026-10-20b, `python3 -I -B ../tools/check_text.py main.tex source/lubiw2026.pdf`, no options:

| measure | value |
|---|---|
| PDF tokens / tex tokens | 17218 / 17077 |
| coverage, raw | 98.9 % |
| coverage without repeated text (0 tokens repeated) | 98.9 % |
| coverage of running text (13 unmatched tokens inside figures left out) | 98.9 % |
| tex tokens found in the PDF | 99.6 % |
| MISSING runs of 6 or more | 1 (6 tokens) |
| EXTRA runs of 6 or more | 0 |

The one MISSING run (p. 40, "2 1 y 2 1 x") is a text-layer order: the PDF gives a superscript before its subscript, `y_1^2`.
A run with `--min-run 1` (`work/check_text_min1.txt`: 113 MISSING runs, 185 tokens; 40 EXTRA runs, 70 tokens) was read through
in full, and every run is one of these:

- page numbers at the foot of the page, and footnote marks, which LaTeX prints from `\footnote`;
- CM accents split in the text layer ("Hlin ě n ý", "Ji ř í", "J é r é my");
- `ℓ` in the PDF against `\ell` in the source, which the tool strips;
- sub/superscript order and sum limits (`\bigwedge_{i=1}^{n-1}`, `y_1^2`);
- real hyphens at line ends ("channel-restricting", "non-crossing", "∃R-complete", "degree-3-flexible-vertex");
- a tool artefact: `\alpha = 85` and `\alpha = 114` on p. 23 are removed by the tool as TeX register assignments (see Problems).

Text inside figures (labels, bar lengths, angles) is transcribed in `\alttext`.

## Figures

30 figures with 46 panels, plus 7 small drawings in Table 1. Every panel has a description. All 53 images are the authors' own files,
copied unchanged from `work/arxiv/figures/`, not cropped from the PDF. 25 of them are the authors' one-page PDFs (Quartz or Keynote
exports; nearly all hold a raster image, and `fig3.pdf` also holds vector lines and text), the others PNG. None has active PDF content
(no JavaScript, embedded files or open actions, by a string scan).

"Match" is the normalised correlation between the file, rendered at its printed size, and the printed page (`work/compare_figs.py`,
150 dpi, slightly blurred). The lowest is 0.974. The 8 lowest were looked at side by side with the print (`work/compare_figs_sheet.png`),
and all show the same picture. So every author's file matches what is printed.

The source names `figures/ufo.png` for Fig. 25, while the archive holds `figures/UFO.png`. TeX's file search here finds it anyway,
by its case-insensitive fallback (`kpsewhich figures/ufo.png` gives `UFO.png`, `texmf_casefold_search = 1`), and the printed Fig. 25 matches `UFO.png`.

**Possibly taken from another source: Fig. 3.** The two graph drawings labelled "Petersen graph" and "Möbius-Kantor graph" are
raster insets (1920 px square-ish, transparent background) inside an otherwise vector Keynote drawing. Their own vertices are coloured
(red; red and blue), and black dots are painted over them. The paper gives no credit. **Checked by the coordinator, 2026-11-07:**
both insets are Wikimedia Commons files, both released into the public domain by their authors (`{{PD-self}}` on each file page):
the Petersen inset is "File:Petersen graph, unit distance.svg" by David Benbennick ("I release all rights to it"), the
Möbius-Kantor inset is "File:Möbius–Kantor unit distance.svg" by David Eppstein (2007, "Redrawn from a figure in Coxeter (1950)").
The insets (pulled from `work/arxiv/figures/unit-distance.pdf`, objects 9 and 11, composited onto white) and Commons' 960 px
renders of the two SVGs, scaled to the same size, differ by a mean of 0.2 grey levels out of 255; the aspect ratios match too
(1920 × 1830 against 1035 × 986; 1920 × 1920 against 480 × 480). Nothing in them stops the figure from going into the public
mirror. No other figure looks taken from elsewhere: the photographs (Figs. 1, 2, 23,
24, 25, 30) show the same kinds of coins and rod models throughout, the rest are GeoGebra drawings with the paper's own labels,
and none carries a credit line.

Panels per provenance tier: tier 1 (source data) 0; tier 2 (vector) 0; tier 3 (digitized) 1; tier 4 (by eye) 0; description only 45,
plus the 7 Table 1 drawings. These are gadget drawings and photographs, so CSV digitising does not apply to them; the table says so
per panel. The bar lengths, angles and heights printed in the drawings are transcribed in `\alttext`, not as CSV, because they are
labels of a construction rather than data on axes.

Fig. 28 is the one panel with numbered axes that carry a 2D scale, a construction on a GeoGebra grid. It gets `figures/fig28.csv`,
`figures/fig28_extract.py`, `figures/fig28.py` and `figures/fig28_replot.png`. Checks done and looked at: the extracted points and
circles drawn over the source (`work/fig28_overlay.png`), and original beside re-plot with `compare.py` (`work/fig28_compare.png`).
Points, circles, axes and ranges agree. One oddity: the top end of the blue triangle side merges into the dark slope line and
reads low, noted in the CSV. Figs. 26 and 27 also show numbered axes, but these are axes of a 3D scene seen in projection, with no
plotted data.

| panel | page | type | copied as | author's file | match | data |
|---|---|---|---|---|---|---|
| Fig. 1 | 1 | photograph of four coins | `figures/fig1.png` | `K4me.png` | 0.996 | no axes, no CSV |
| Fig. 2 left | 2 | photograph of coins | `figures/fig2left.png` | `grid4x4.png` | 0.995 | no axes, no CSV |
| Fig. 2 middle | 2 | photograph of coins | `figures/fig2middle.png` | `grid4x4pert.png` | 0.999 | no axes, no CSV |
| Fig. 2 right | 2 | photograph of coins | `figures/fig2right.png` | `grid_braced4x4.png` | 0.999 | no axes, no CSV |
| Fig. 3 | 3 | schematic: containment diagram with sample graphs (see Figures below) | `figures/fig3.pdf` | `unit-distance.pdf` | 0.997 | no axes, no CSV |
| Fig. 4 left | 8 | GeoGebra linkage drawing | `figures/fig4left.pdf` | `A-frame-1-new.pdf` | 0.998 | no axes, no CSV |
| Fig. 4 middle | 8 | GeoGebra linkage drawing | `figures/fig4middle.pdf` | `A-frame-2-new.pdf` | 0.997 | no axes, no CSV |
| Fig. 4 right | 8 | GeoGebra linkage drawing | `figures/fig4right.pdf` | `A-frame-3-new.pdf` | 0.997 | no axes, no CSV |
| Fig. 5 left | 9 | GeoGebra linkage drawing | `figures/fig5left.pdf` | `half-to-two-simple-1.pdf` | 0.988 | no axes, no CSV |
| Fig. 5 right | 9 | GeoGebra linkage drawing | `figures/fig5right.pdf` | `half-to-two-simple-2.pdf` | 0.977 | no axes, no CSV |
| Fig. 6 | 10 | schematic: grid of channels and gadget boxes | `figures/fig6.pdf` | `overall-new.pdf` | 0.991 | no axes, no CSV |
| Fig. 7 left | 11 | GeoGebra linkage drawing | `figures/fig7left.pdf` | `exact-interval-new-1.pdf` | 0.990 | no axes, no CSV |
| Fig. 7 middle | 11 | GeoGebra linkage drawing | `figures/fig7middle.pdf` | `exact-interval-new-2.pdf` | 0.979 | no axes, no CSV |
| Fig. 7 right | 11 | GeoGebra linkage drawing | `figures/fig7right.pdf` | `exact-interval-new-3.pdf` | 0.994 | no axes, no CSV |
| Fig. 8 left | 12 | GeoGebra gadget schematic | `figures/fig8left.pdf` | `turning.pdf` | 0.991 | no axes, no CSV |
| Fig. 8 right | 12 | GeoGebra gadget schematic | `figures/fig8right.pdf` | `crossing.pdf` | 0.995 | no axes, no CSV |
| Fig. 9 | 13 | GeoGebra gadget schematic | `figures/fig9.pdf` | `crossing-same.pdf` | 0.988 | no axes, no CSV |
| Fig. 10 | 14 | GeoGebra gadget schematic | `figures/fig10.pdf` | `adding-new.pdf` | 0.979 | no axes, no CSV |
| Fig. 11 | 15 | GeoGebra gadget schematic | `figures/fig11.pdf` | `inverting-4-setup.pdf` | 0.985 | no axes, no CSV |
| Fig. 12 left | 16 | GeoGebra construction with shaded triangles | `figures/fig12left.pdf` | `inverting-4-1.pdf` | 0.984 | no axes, no CSV |
| Fig. 12 right | 16 | GeoGebra construction with shaded triangles | `figures/fig12right.pdf` | `inverting-4-2.pdf` | 0.991 | no axes, no CSV |
| Fig. 13 left | 17 | GeoGebra gadget schematic | `figures/fig13left.pdf` | `inverting-4-detail-1.pdf` | 0.988 | no axes, no CSV |
| Fig. 13 right | 17 | GeoGebra gadget schematic | `figures/fig13right.pdf` | `inverting-4-detail-2.pdf` | 0.988 | no axes, no CSV |
| Fig. 14 left | 18 | GeoGebra penny drawing | `figures/fig14left.png` | `barAB.png` | 0.987 | no axes, no CSV |
| Fig. 14 right | 18 | GeoGebra penny drawing | `figures/fig14right.png` | `barABwithangles2.png` | 0.991 | no axes, no CSV |
| Table 1 pic, 90° | 19 | small drawing of a vertex type | `figures/table1_angle_90.png` | `angle_90.png` | 0.982 | no axes, no CSV |
| Table 1 pic, 120° | 19 | small drawing of a vertex type | `figures/table1_angle_120.png` | `angle_120.png` | 0.989 | no axes, no CSV |
| Table 1 pic, 150° | 19 | small drawing of a vertex type | `figures/table1_angle_150.png` | `angle_150.png` | 0.985 | no axes, no CSV |
| Table 1 pic, 90, 90° | 19 | small drawing of a vertex type | `figures/table1_angle_90_90.png` | `angle_90_90.png` | 0.988 | no axes, no CSV |
| Table 1 pic, 90, 120° | 19 | small drawing of a vertex type | `figures/table1_angle_90_120.png` | `angle_90_120.png` | 0.984 | no axes, no CSV |
| Table 1 pic, 150, 30° | 19 | small drawing of a vertex type | `figures/table1_angle_150_30.png` | `angle_150_30.png` | 0.986 | no axes, no CSV |
| Table 1 pic, 60, 90, 30° | 19 | small drawing of a vertex type | `figures/table1_angle_60_90_30.png` | `angle_60_90_30.png` | 0.994 | no axes, no CSV |
| Fig. 15 left | 20 | GeoGebra linkage drawing with angle values | `figures/fig15left.pdf` | `A-frame-angles-1.pdf` | 0.980 | no axes, no CSV |
| Fig. 15 right | 20 | GeoGebra linkage drawing with angle values | `figures/fig15right.pdf` | `A-frame-angles-2.pdf` | 0.984 | no axes, no CSV |
| Fig. 16 left | 21 | GeoGebra closeup with angle values | `figures/fig16left.pdf` | `inverting-4-detail-closeup-1.pdf` | 0.991 | no axes, no CSV |
| Fig. 16 right | 21 | GeoGebra closeup with angle values | `figures/fig16right.pdf` | `inverting-4-detail-closeup-2.pdf` | 0.999 | no axes, no CSV |
| Fig. 17 | 22 | GeoGebra penny drawing | `figures/fig17.png` | `vx_uni_fix_new.png` | 0.993 | no axes, no CSV |
| Fig. 18 | 22 | GeoGebra penny drawing | `figures/fig18.png` | `vx2_flex_uni.png` | 0.985 | no axes, no CSV |
| Fig. 19 left | 23 | GeoGebra penny drawing | `figures/fig19left.png` | `vx3_flex_180_20.png` | 0.996 | no axes, no CSV |
| Fig. 19 right | 23 | GeoGebra penny drawing | `figures/fig19right.png` | `vx3_flex_180_100.png` | 0.996 | no axes, no CSV |
| Fig. 20 left | 24 | GeoGebra penny drawing | `figures/fig20left.png` | `panto_closed.png` | 0.998 | no axes, no CSV |
| Fig. 20 right | 24 | GeoGebra penny drawing | `figures/fig20right.png` | `panto_open.png` | 0.983 | no axes, no CSV |
| Fig. 21 | 25 | GeoGebra penny drawing | `figures/fig21.png` | `new_apex_stand.png` | 0.998 | no axes, no CSV |
| Fig. 22 | 25 | GeoGebra penny drawing | `figures/fig22.png` | `new_apex_kneel.png` | 0.998 | no axes, no CSV |
| Fig. 23 | 27 | photograph of a rod-and-ball model | `figures/fig23.png` | `smallUFO2.png` | 0.980 | no axes, no CSV |
| Fig. 24 | 27 | photograph of a rod-and-ball model | `figures/fig24.png` | `3arm.png` | 0.984 | no axes, no CSV |
| Fig. 25 | 28 | photograph of a rod-and-ball model | `figures/fig25.png` | `UFO.png` | 0.974 | no axes, no CSV |
| Fig. 26 | 28 | GeoGebra 3D rendering | `figures/fig26.png` | `vgag.png` | 0.994 | scene axes of a 3D view, not data: no CSV |
| Fig. 27 | 29 | GeoGebra 3D rendering, top view | `figures/fig27.png` | `vgagtop.png` | 0.998 | scene axes of a 3D view, not data: no CSV |
| Fig. 28 | 32 | GeoGebra construction on numbered axes | `figures/fig28.png` | `Treestwodisks.png` | 0.985 | `figures/fig28.csv`, tier 3 (digitized) |
| Fig. 29 left | 38 | GeoGebra linkage drawing | `figures/fig29left.pdf` | `A-frame-proof.pdf` | 0.985 | no axes, no CSV |
| Fig. 29 right | 38 | GeoGebra linkage drawing | `figures/fig29right.pdf` | `A-frame-proof-2.pdf` | 0.982 | no axes, no CSV |
| Fig. 30 | 41 | two photographs of a rod-and-ball model, one image | `figures/fig30.png` | `smallUFOrigid.png` | 0.983 | no axes, no CSV |

## Tables

Table 1 and Table 2 (both p. 19) stand in `main.tex` as `tabular` and in `tables/table1.csv` and `tables/table2.csv`. The printed tables merge the degree
cell across rows; in `main.tex` the number stands in the first row of its group, and the CSVs repeat it. Table 1's picture cells
are `pic_file` and `pic_description` in the CSV, the description being the decompiler's. Partial row rules are written `\cmidrule`,
not the source's `\cline` (see Problems).

## Data and files the paper names

- No Zenodo, Dryad or source-data files, no supplement, no videos.
- 12 GeoGebra applets, named in the captions and available "through the arxiv version": `Hart's-A-frame.ggb`, `flex-gadget.ggb`,
  `flex-gadget-range-constrained.ggb`, `cross-over-gadget-different-variables.ggb`, `cross-over-gadget-same-variable.ggb`,
  `addition-gadget.ggb`, `inversion-setup.ggb`, `inversion-detail.ggb`, `degree-2-flexible-vertex.ggb`,
  `degree-3-flexible-vertex.ggb`, `degree-4-flexible-vertex.ggb`, `3d-marble-arms.ggb`. **The archive carries them** in
  `anc/GeogebraGadgets.7z` (393 614 bytes). It was **not unpacked**, as instructed; its listing (`7z l`) shows exactly these 12 names.
- Ref. [24] names only the whole volume (Guy and Woodrow, eds.), while the text cites Harborth's "Match Sticks in the Plane" in it;
  the printed entry gives no chapter or pages.
- Cited works the decompiler noticed in this collection, to be tagged by `tools/mark_local.py`: ref. [33] is `lavollee2023` (the
  journal version; that folder's text follows arXiv v2) and ref. [25] is `reutter1974`.

## Errors found in the paper

All kept as printed. Pages are printed pages. Items marked (reading) are the decompiler's reasoning, not something the paper says.

Words and punctuation:
- p. 4 (Section 1.1): "the problems of recognizing intersection or contact graphs of disks is `NP`-hard": number disagreement.
- p. 3: "Schaefer [41] showed that ... to recognize [41]": the same citation twice in a sentence.
- p. 11, proof of Claim 5: "(see Figure 7(right)))": one closing parenthesis too many.
- p. 16, proof of Claim 10: "range (12, 16.97])": stray closing parenthesis.
- p. 18: "the following five gadgets", then six are listed.
- p. 25, Fig. 21 caption: "less than 11 gadgets thick"; p. 24 says "11 pennies thick".
- p. 28: "To keep the spinners vertical this arrangement we create": garbled.
- p. 29: "gadgets of top of this realization" ("on top"); Fig. 27 caption ends "of the mast in red)." with no opening parenthesis.
- p. 32: "Kachiyan and Porkolab [30]"; ref. [30] spells "Khachiyan".
- p. 33: "see Remark 4", but the Remark on p. 26 is unnumbered; the 4 is the section number LaTeX gives its label.
- p. 38: "isoceles" (spelt "isosceles" in step (3)). p. 41: "bipyraminds" (p. 40: "bipyramids").
- References: five DOIs print a literal `\_` (refs. [5], [8], [27], [38], [41]); their link targets are right.

Mathematics (reading):
- p. 24: "an embedding D′ from (L, D)": everywhere else the linkage's embedding is Λ and the graph's is D, so (L, Λ) and D seem meant.
- p. 29: "form an angle greater than 60 degrees", then "the ≥ 60° gap" in the same paragraph; Fig. 27's caption has arms at "less than 60 degrees". Two edges of a triangle in a penny graph form exactly 60°.
- p. 33: "ρ = 2^(-2^(n^c))" for radii in [1, ρ], which needs ρ ≥ 1; probably 1 + 2^(-2^(n^c)).
- pp. 39-40, Appendix B: indices mixed. f has n components, but g is called (g_i) for i in [d+2], "the first d of them homogeneous", with g_{d+1}, g_{d+2} added after i in [n]. Also "(x_1, ..., x_n, y_1, y_2, y_3)" for x_d; "V(G)" for V(g); "f(p_k) = 0" for g(p_k) = 0, since p_k has d+3 coordinates; "y_{k,2} = Σ x_i² = 0" without the k; and B^d, B_d, B_2 for the same kind of ball.

## Known problems and notes

- `main.pdf` is 42 MB because three photographs are 7-9 MB PNGs (Figs. 23, 24, 25), copied as they are.
- Fig. 28's source image is only 417 x 284 px.
- `work/` holds scratch and may be deleted, but `work/build_main.py` needs `work/arxiv/` and `work/compile/arxiv.aux`.
- Problems with the tools (reported to the coordinator): `check_text.py` treats `\alpha = 85` as a register assignment and removes it; it also reads the
  argument of `\cline{2-4}` as printed digits.

## Facts from background knowledge, not from the paper

None in the text of the paper. Fig. 3's Wikimedia Commons sources were found and checked by the coordinator (Commons file pages
and images, 2026-11-07), as stated there. The match to `reutter1974` and `lavollee2023` comes from
the collection's root `README.md`.
