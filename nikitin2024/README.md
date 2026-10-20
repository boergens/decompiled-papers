# nikitin2024: decompiled

Viktor Nikitin, Gregg Wildenberg, Alberto Mittone, Pavel Shevchenko, Alex Deriy & Francesco De Carlo. "Laminography
as a tool for imaging large-size samples with high resolution." *Journal of Synchrotron Radiation* **31** (2024),
pp. 851–866. DOI [10.1107/S1600577524002923](https://doi.org/10.1107/S1600577524002923) (printed in the footer of
p. 1). Received 30 January 2024; accepted 3 April 2024; edited by A. Bergamaschi. ISSN 1600-5775.

**Licence:** the PDF prints "Published under a CC BY 4.0 licence" under the OPEN ACCESS / CC BY logo at the foot of
the left column of p. 1 (`main.tex` has the line). `source/SOURCE.txt` quotes the same line ("Published under a CC
BY 4.0 licence", PDF p. 1 footer): the two agree. Citation, title, authors, journal, volume, pages and DOI in the PDF
agree with SOURCE.txt and the task message.

## Source files (`source/`)

| file | what it is |
|---|---|
| `nikitin2024.pdf` | **Publisher's version of record** (IUCr typesetting, 16 pages, 31 MB, born-digital: embedded Type 1 fonts incl. the TeX Times Math fonts, `pdffonts`; the 21 embedded images are the figures at 357–1200 ppi). Running header "research papers", alternating footers "J. Synchrotron Rad. (2024). 31, 851–866" / "Viktor Nikitin et al. • Laminography for imaging large-size samples" with page numbers 851–866. The three TomocuPy command lines on p. 10 are embedded as images, not text. |
| `SOURCE.txt` | fetch note (journals.iucr.org, 2026-10-20, browser slot 0). |

## Method (tool-first)

`work/build_main.py` places the paper's text into `main.tex` from the Datalab API conversion of the PDF
(`work/datalab/nikitin2024.md`, "accurate" mode, 2026-10-20): page delimiters → `\pdfpage{}`, headings →
`\section*`/`\subsection*`, the markdown table → the tabular and `tables/table1.csv`, `$$` blocks → numbered
equations, the three ``` blocks → `verbatim`, "- " items → `hangpars` paragraphs, markdown inline mark-up → LaTeX,
and the text Datalab read *inside* the figure images (axis labels, panel letters) is dropped at the figure blocks. The
PDF's own text layer (PyMuPDF with font flags, `work/dump_text.py` → `work/pdftext/`) was the second opinion:
`work/diff_words.py` lists every word-level difference between the two (278 runs, almost all inline-math placeholders
and in-figure text), and the italic spans of the PDF were compared with Datalab's. Every equation was checked symbol
by symbol against 300–600 dpi zooms of the page (`work/zoom/`), the command images at 500 dpi. The decompiler then
proofread the result against the page images (`work/pages/`); the figure descriptions are in `work/alttext.py`.

Every change to the Datalab text is in the script's `CORRECTIONS` table (each entry must match exactly the stated
number of times). The ones that matter:

| what Datalab produced | what the paper prints | where |
|---|---|---|
| "demonstrated" | "demostrated" (silently corrected typo) | p. 2, "Nvidia GPUs have demostrated to be" |
| `k_u \cos \theta`, `k_u \sin \theta` in eq. (6) | $k_u \cos_\theta$, $k_u \sin_\theta$ (θ set as a subscript) | p. 5 |
| `\mathcal{F}_{3D}(\mu/\psi)` in eq. (8) | $\mathcal{F}_{3D}\left(\frac{\mu}{\psi}\psi\right)$ (a ψ after the fraction) | p. 5 |
| "tomocopy recon_steps" (OCR of the command images) | "tomocupy recon_steps" (×3) | p. 10 |
| "O'Brien" (straight apostrophe) | "O’Brien" (×3) | pp. 2, 16 |
| "16384" | "16 384" (thin space, as "15 000" on p. 11) | p. 2 |
| "*NDT&E Intl.* **111**" | "*NDT&E Intl*, **111**" | p. 15 |
| "(e.g. 2048", "(e.g. 3072", "(e.g. Paganin" upright | *e.g.* italic (PDF font flags), as everywhere else | p. 9 |
| "7.5 × lens" | "7.5× lens" | p. 9 |
| Datalab's own image descriptions under Figs. 4, 5 and 11 ("a) 3D scatter plots of the system in the ξ1-ξ2-ξ3 space …", "b) 3D schematic of a layered structure …", "a) 3D volume of the sample with a red line …", "a) Side view of the sample, showing a single slab (slab1) with a 1mm scale bar.") | nothing: these are not in the paper (Datalab invented caption-like text for figures without printed labels) | pp. 6, 7, 11 |
| `\operatorname{argmin}_\mu` | argmin with its limit printed below it (`\operatorname*`) | p. 14 |
| units in math (`$200\ \mu\text{m}$`, `$\pm 10^\circ$`, `$360^\circ$`, …) | set as text (200 μm, ±10°, 360°), per the SPEC | throughout |

Generic rules (not individual corrections): the panel letters "(a)", "(b)", "(c)" and the "A" of "Appendix A" are
italic in print (PDF font flags) and are set `\emph{}`; the differential "d" in the integrals is upright as printed;
line-end hyphens at page/column/figure breaks were resolved as Datalab did and checked against the paper's own
mid-line usage ("nano-laminography", "back-projection" (p. 5, p. 8; the paper also writes "backprojection" mid-line
on pp. 5, 7, 8), "red-coloured", "pre-processing", "three-dimensional", "flat-shaped", "high-resolution").

## What is in `main.tex`

Every word of the article in reading order: the margin-column lines of p. 1 (ISSN, received/accepted, edited by,
keywords), title, authors with their affiliation marks, affiliations and correspondence e-mail, the journal line and
DOI (the p. 1 footer, given once), the licence line, the abstract, the p. 1 thumbnail picture (as
`figures/thumb.png` with a note and description: a composite of Fig. 8(a) and Fig. 11(b) without caption), sections
1–7 with the 20 numbered equations, the three command lines (`verbatim`; they are images in the PDF, OCR'd by
Datalab and proofread at 500 dpi), Table 1, Figs. 1–14 with their captions, Appendix A, Funding information and the
reference list (the "References" heading is the paper's own). Left out: the running header "research papers", the
page numbers, the repeated footers and the journal and OPEN ACCESS logos (the text "JOURNAL OF SYNCHROTRON RADIATION"
is part of the logo image).

Placement: each figure is placed at its caption's position in reading order, after the paragraph that spans it;
paragraphs cut by a page/column break or by a figure are joined and the `\pdfpage{}` marker goes inline (8 of the 16
markers fall mid-sentence; Figs. 2, 3, 8, 11–14 follow paragraphs that end on the next page, so these figures come
after their page's marker). Figs. 9 and 10 follow
section 6.1 and precede the paragraph that cites them, as printed. Four decompiler notes sit under eqs. (1), (4), (6)
and (9) (see "Errors" below).

Table 1 is also `tables/table1.csv` (caption and notes in `#` lines; the two-level header flattened).

## Figures

| figure | panel(s) | type | data | provenance |
|---|---|---|---|---|
| p. 1 thumbnail (`thumb.png`) | single | colour composite (photo inset + 3D rendering) | description only | – |
| Fig. 1 | a, b (+ two lower sketches) | schematic (pillars/slabs, scan geometries) | description only | – |
| Fig. 2 | left, right | photographs of the sample stack | description only | – |
| Fig. 3 | single | annotated photograph of the sample mount | description only | – |
| Fig. 4 | a (two 3D scatter renderings), b (volume rendering), c (6 slices) | plots/renderings/images | description only; see note | – |
| Fig. 5 | a (rendering), b (5 slices) | images | description only | – |
| Fig. 6 | single | schematic timing diagram (no scale) | description only | – |
| Fig. 7 | single | profiler timeline screenshot with a time ruler | `figures/fig7.csv`, `fig7_extract.py`, `fig7.py`, `fig7_replot.png` | tier 3, digitized from the embedded raster |
| Fig. 8 | a (photo), b (projection + 2 close-ups) | images | description only | – |
| Fig. 9 | a, b, c (+ 6 close-ups) | reconstructed slices | description only | – |
| Fig. 10 | single | line plot (FRC) | `figures/fig10.csv`, `fig10_extract.py`, `fig10.py`, `fig10_replot.png` | tier 3, digitized from the embedded raster |
| Fig. 11 | a, b | 3D renderings | description only | – |
| Fig. 12 | a (8 strips), b (8 close-ups) | reconstructed slices | description only | – |
| Fig. 13 | a (8 slices), b (8 close-ups) | reconstructed slices | description only | – |
| Fig. 14 | 6 slices | images | description only | – |

Panels per provenance tier: tier 1 (source data): 0; tier 2 (vector): 0 (`vector_dump.py`: 0 paths in the Fig. 7
and Fig. 10 regions, one raster image each; `pdfimages -list`: one image per figure); tier 3 (digitized): 2 (Fig. 7,
Fig. 10); tier 4 (read by eye): 0; images/schematics with description only: all other figures (13 figures, about 70
panels/sub-images).

**Fig. 4(a)** is the one quantitative panel without a data file: two 3D scatter renderings of the Fourier-space grid
(ξ₁, ξ₂, ξ₃) of eq. (6) for φ = 0° and 30°. The points overlap in the projection and the axes carry only the labels
−0.5 and 0.5, so neither a vector nor a raster extraction of individual points is possible; the panel is a rendering
of the formula with grid parameters the paper does not state. Described in `\alttext`; no CSV.

The reconstructed-slice panels with a "0 attenuation 1" grey bar (Figs. 5, 9, 12, 13) are images, not calibrated data
maps; no grid CSVs were made.

`figures/figN.png` are 200 dpi renders of the embedded image boxes (+2 pt), without captions (`crop.py`).

**Fig. 10** (`fig10_extract.py`): embedded 1385 × 711 px raster; axes calibrated on the six light-grey grid lines per
axis (at the labelled ticks 0, 0.2, …, 1.0; max residual 0.0004), checked against the outward x tick at 0. Legend box,
the "1.69 um" label and the arrow shaft were blanked; the three series were traced per pixel column by colour (red
smoothed FRC: line centre; black FRC: the union of black and red pixels, with the vertical extent per column in
`correlation_lo/hi` because the raw trace oscillates by up to ±0.05 and its centre is hidden under the red line; blue
threshold: centre and extent). 1826 rows (every 2nd column). The crossing of the smoothed FRC and the threshold comes
out at x = 0.541, y = 0.207; the arrow tip sits at (0.553, 0.233). Checks: overlay of all traces on the embedded
image (`work/fig10_overlay.png`, zooms `work/zoom/fig10_ov_*.png`) — every trace sits on its line; `compare.py` side
by side (`work/cmp_fig10.png`): axes, ranges, grid, all three series and the crossing match. Decompiler's own
arithmetic, not in the .tex: 0.92 μm voxel / 0.541 = 1.70 μm, consistent with the printed 1.69 μm.

**Fig. 7** (`fig7_extract.py`): embedded 2205 × 648 px screenshot. Time axis fitted on the seven labelled major
ticks (+600 … +660 ms; residual 0.06 ms, 0.0415 ms/px); the eight unlabelled major ticks fall on 5 ms multiples. Every
box on the timeline is a CSV row with its printed label and the authors' brace annotation: the 5 overview bars of the
CUDA HW row, the 20 kernel boxes of Stream 18 (split at the light notch their rounded corners leave where two boxes
touch; the six wide boxes of each chunk group get the printed labels in order), the 3 cyan chunk-start boxes, the 2
"Memcpy HtoD" blocks and the 3 "Memcpy DtoH" blocks (each drawn as 3 adjacent sub-boxes in the screenshot, kept as
such). Checks: outline overlay (`work/fig7_overlay.png`, zooms `work/zoom/fig7_ov_left.png`, `fig7_ov_right.png`) —
every outline sits on its box; `compare.py` (`work/cmp_fig7.png`): the Gantt re-plot reproduces the timeline.

## Checks

- `lualatex` ×2: compiles without errors (27 pages); the only warnings are small overfull boxes (< 5 pt).
- `python3 -I ../../tools/check_text.py main.tex source/nikitin2024.pdf` (no options; version 2026-10-20b): PDF tokens
  11427, tex tokens 11054; **coverage 95.9 % raw; 96.9 % without text repeated on ≥ 3 pages (112 tokens); 96.9 % of
  the running text** (8 unmatched tokens inside figures). MISSING runs ≥ 6: 12 (107 tokens); EXTRA runs ≥ 6: 7 (115
  tokens); all explained below. The shortfall from 98 % is the equations: the PDF's text layer renders the TeX math
  fonts as glyph soup ("¼" for =, "ð…Þ" for parentheses, "th" for θ, "kr" for ‖∇, "ffiffiffi" for √, ψ and other
  Greek letters as unmapped or missing glyphs, "Oð" for O(), so that 2048³ becomes "20483"), which cannot be matched
  by any correct transcription. With `--min-run 2` all 61 MISSING runs are of this kind except the two header
  fragments of Table 1 and "odstrc il" (Odstrčil: the caron is a separate glyph in the text layer).
- REPEATED: "research papers" (8 pages) and the footers "Viktor Nikitin et al. • Laminography for imaging large-size
  samples" (page-number variants on 7, 5, 2 and 1 pages).
- MISSING ≥ 6 (12 runs): all are equation glyph soup — eq. (1)/(4) and the inline $\tilde d$ definition on p. 5
  ("dd u v 1 4 l", "ddu v exp 1 2 ddu v 1 2"), eq. (8) ("1 4 f 3 d d 1 2 3 1 4"), eq. (9) on p. 7 ("1 4 zzz exp 2
  idx", "3 d 9 1 4 zz exp 2 idx"), eqs. (10)–(19) on p. 14 and eq. (20) on p. 15 ("th kr k 1 min d", "th k k 1 th t
  dr th 2 kr k", "j max 0 jr k th 1 th", …). The equations are in `main.tex`, transcribed symbol by symbol from the
  page zooms.
- EXTRA ≥ 6 (7 runs): three are the TomocuPy command lines (23 + 11, 35 and 23 tokens), which are embedded images in
  the PDF and so absent from its text layer (OCR'd by Datalab, proofread at 500 dpi: `work/zoom/p10_cmd*.png`); one
  is the first header row of Table 1 ("reconstruction recon write 32 bit total fourierrec linerec gain": the text
  layer lists "Reconstruction" and "Total" before the other header cells, a reading-order difference); "f f f x 2 i
  x" is the inline definition of the Fourier transform (math glyphs on the PDF side); "1 f m 1 f m 1" is eq. (19).
  None is a transcription error.
- Read-through against the page images: all 20 equations (zooms in `work/zoom/`), the inline formulas (d̃, |σ|cos(φ),
  Ff(ξ), L*_φ d(x₁,x₂,·)), subscripts ξ₁…ξ₃, k_u, k_v, N_θ, x₃, d_d, d_f, superscripts 2048³, s⁻¹, k+1, m+1, the
  calligraphic operators L, W, F, A, the Greek letters, ±, ×, ≤, ≥, ∼, →, the thin-spaced numbers, the degree
  signs, the curly quotes ‘tail’, ‘develop’, the italic panel letters and journal names, Table 1 (all cells; the
  Gain and Total columns recompute from the other cells), and the reference list accents (Faragó, Gürsoy, Kröning,
  Jørgensen, Mikulík, Vagovič, Odstrčil/Odstrcil as printed, Müller, Hänschke, D’Amico).

## Errors and oddities in the paper (left as printed)

- Eq. (1) integrates $u(x_1,x_2,x_3)$ although the object is $\mu$; eq. (4) has $\tilde\delta(\varphi,\delta,u,v)$
  (δ where (2) has θ); eq. (6) sets θ as a subscript of cos and sin in its first two lines; eq. (9) has no
  $f(x_1,x_2,x_3)$ in the triple integral; p. 14 writes the steepest ascent direction as $\nabla_\mu F(u)$ and the CG
  iterates as $u_{m+1} = u_m + \gamma_m\eta_m$ for the variable μ. Each has a `\decompnote`.
- Typos: "demostrated" (p. 2), "compued tomography" (p. 2), "with the the *Fourierrec*" (Table 1 notes), "A 8 mm glass
  filter" (p. 9), "in the horizontal (orthogonal to the beam) and vertical and directions" (p. 10), "a small amplitude
  loose" (p. 6), "per a slab" (p. 10), "four straighten slab volumes" (Fig. 11 caption), "2BM" for "2-BM" (p. 12),
  "The author also acknowledges" with six authors (Funding).
- The first command line prints `--file-name --file-name brain_x2y1.h5` (the option twice).
- Fig. 12, YZ slice: the second strip (slab 2) has no label and no coloured cross; the XZ group has all four.
- Fig. 10 labels the resolution "1.69 um" (um for μm) and the x axis "Spatial/Nyquist frequency".
- Fig. 4 caption vs. figure: consistent; the in-figure labels are "φ = 0°" etc. with the φ typeset.
- Fig. 7: the text says the asterisks mark CPU time before the green/after the purple boxes; the figure's own footnote
  reads "* - copy to/from CPU pinned memory for faster CPU-GPU data transfer".
- Table 1 is internally consistent (Gain = Linerec/Fourierrec, Total = sum of the four times, to the printed digits).

## Data and code named by the paper, not in `source/`

- The brain-slab laminography datasets in TomoBank (https://tomobank.readthedocs.io/, "under Laminography/Brain"), ~12 TB
  raw / 10 TB stitched (tier-1 source data for Figs. 8(b), 9, 11–13 would be these volumes; not available here).
- The *TomocuPy* package (https://tomocupy.readthedocs.io, "'develop' github branch during the paper review") with the
  laminography reconstruction, and the "independent package" with the TV-regularized (ADMM) reconstruction of Appendix
  A (no URL given).
- The synthetic HDF5 test datasets of Table 1, the synthetic integrated-circuit and the "semi-synthetic" brain datasets
  of Figs. 4, 5 and 14, the Nsight profiling report of Fig. 7, and the FRC curves of Fig. 10 (no source-data file).

## Problems and suggestions for the spec and the tools

- **Datalab invents figure descriptions.** For figures whose panels carry no printed text (Figs. 4, 5, 11) the
  "accurate" conversion emitted caption-like lines ("a) 3D scatter plots of the system in the ξ1-ξ2-ξ3 space. The ξ1
  and ξ2 axes range from -0.5 to 0.5 …", "a) Side view of the sample, showing a single slab (slab1) with a 1mm scale
  bar.") that are not in the paper. They sit between the `![]()` image line and the "**Figure N**" caption, exactly
  where in-figure text also lands, so a build script must drop everything in that gap. Worth a line in the brief and in
  `tools/datalab_ocr.py`'s docstring: nothing between an image and its caption marker is the paper's text.
- Datalab also silently corrected a typo ("demostrated"), normalized two equations (eq. 6's subscript θ, the ψ in
  eq. 8), OCR'd the command images with an error ("tomocopy"), de-curled apostrophes and dropped a thin space. The
  PDF text layer caught the first and the last two; only the page zooms caught the equations. For math-heavy papers
  the brief could ask for the symbol-by-symbol equation check explicitly (it was in this task's message).
- `check_text.py` cannot reach 98 % on an equation-heavy IUCr PDF: the TeX math fonts (`TeX_Times_Math_*`, `PI_chars`)
  give glyph soup. PyMuPDF reports the font per span, so the tool could drop or count separately the tokens of spans
  whose font name contains "Math", "Symbol" or "PI_chars" (as it already does for in-figure text); that would make the
  coverage number meaningful here (≈ 98.5 % by the `--min-run 2` list).
- The Read tool served a stale copy of `main.tex` right after `build_main.py` had rewritten it (the lines it showed
  were the previous build's; `sed` on the same path showed the new content). Re-reading via Bash was the workaround;
  Kevin may want to know that the Read cache does not notice rewrites by a script run from Bash.
- `digitize_common.trace_envelope` returns (x, y_mid, y_upper, y_lower) where "upper" is the smaller row index; the
  docstring could say "top/bottom in pixel rows" to save a check.
- The SPEC has no name for a page-1 thumbnail/graphical abstract; `figures/thumb.png` was used.
- `../tools/` is `../../tools/` for folders under `incoming/` (as noted for han2008); the scripts here walk up the
  parents to find `tools/`.

## Time

About 35 minutes wall-clock (23:15–23:50 UTC by the machine clock): reading brief, spec, example and all 16 pages;
Datalab vs. text-layer comparison; equation and command zooms; build script and corrections; 14 figure crops and
descriptions; the two digitizations with their checks; compile, check_text, read-through and this README.
