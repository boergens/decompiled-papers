# wildenberg2023: decompiled

Gregg Wildenberg\*†, Kevin Boergens†, Viktor Nikitin, Alex Deriy, Francesco De Carlo, Vincent De Andrade,
Xianghui Xiao, Narayan Kasthuri\* (\* corresponding, † equal contribution). "A Pipeline for a Primate Projectome:
mapping every individual myelinated axon across the whole brain." *bioRxiv* 2023.10.23.563679, **version 1**, posted
October 24, 2023 (the only version as of 2026-10-20; not peer reviewed).
DOI [10.1101/2023.10.23.563679](https://doi.org/10.1101/2023.10.23.563679).

**Licence (as printed on every page):** "The copyright holder for this preprint (which was not certified by peer
review) is the author/funder. All rights reserved. No reuse allowed without permission." No Creative Commons licence.
The copyright holder is the authors; Kevin Boergens, the owner of this collection, is the second author.

The citation above is taken from the PDF; it agrees with the task message and with `source/SOURCE.txt` (the PDF
prints "Narayan Kasthuri" on the title page, while references 14 and 24 write "Narayanan Kasthuri").

## Source files (`source/`)

| file | what it is |
|---|---|
| `wildenberg2023.pdf` | the preprint, bioRxiv version 1 (`2023.10.23.563679v1.full.pdf`), born-digital (LaTeX, xdvipdfmx 2023-10-24, embedded Times New Roman), 38 pp.: text pp. 1–14 (margin line numbers 1–489), Figures 1–6 on pp. 15–26, Supplementary Figures 1–6 on pp. 27–38 (each figure on one page with a bold "Figure N" label, its caption on the next page; line numbers 490–576 continue on the figure pages). bioRxiv stamp at the top of every page. |
| `SOURCE.txt` | fetch note (biorxiv.org, 2026-10-20). |

The task message said "Supplementary Figures 1–3"; the PDF has **Supplementary Figures 1–6**. All six are in `main.tex`.

**Not available (named by the paper, not in `source/`):**
- *Supplementary Movie 1* (bioRxiv `563679_file02.mov`, the only supplementary file on bioRxiv; cited in Results 3.2 for the blood vessel crossing two pillars). Not downloaded.
- *The x-ray data sets*: "All datasets are freely available for download at BosssBD (https://bossdb.org/)" (Data availability, p. 9; no project name or link is given). These would be the tier-1 source for the µXCT pillars (Figs. 3, 4, Suppl. Fig. 3), the 30 nm nXCT volume (Fig. 5) and the 100 nm nXCT volume (Fig. 6, Suppl. Figs. 4, 5). Not available here.
- *Code named in the Methods* (not in `source/`): tomopy-cli (https://github.com/tomography/tomopy-cli), Knossos (https://knossos.app/), webKnossos (https://webknossos.org/), the LSD segmentation code (https://github.com/funkelab/lsd), Kimimaro (https://zenodo.org/record/5539913), the xpress challenge (https://xpress.grand-challenge.org/). The paper's own gap-estimation, split-repair and gap-matching code (Methods 5.6–5.8) is not published, and no source data behind Fig. 5C or Suppl. Fig. 6 (the model curves) is given.
- All 53 cited references: none is in this folder.

## Contents

- `main.tex` / `main.pdf` (23 pp.): the bioRxiv stamp (once, because it carries the licence statement), title, authors with
  affiliation superscripts, affiliations, corresponding-author and equal-contribution lines, sections 1–7 (Abstract,
  Introduction, Results 3.1–3.4, Discussion with 4.1, Methods 5.1–5.9, Acknowledgements, References: the paper prints
  both a "7 References" section heading and a "References" bibliography heading, both kept), the two numbered lists of the
  Introduction and the one of the Discussion (as `hangpars`), the 53 references with their numbers, and Figures 1–6 and
  Supplementary Figures 1–6 where they are in the PDF (pp. 15–38), each with its bold page label, image, verbatim caption
  and `\alttext` description.
- `figures/`: every figure cropped from the PDF at 200 dpi (`fig1–6.png`, `sfig1–6.png`); for the two plotted panels the
  data, extraction and plotting scripts and replots: `fig5c.csv`, `fig5c_extract.py`, `fig5c.py`, `fig5c_replot.png`;
  `sfig6.csv`, `sfig6_extract.py`, `sfig6.py`, `sfig6_replot.png`.
- `tables/text_values.csv`: compiled by the decompiler (not a table of the paper): the key numbers about the tissue
  sectioning (slicers, species and tissue, section/pillar dimensions, the 697 nm gap estimate and how it was made, the
  computational kerfs and tracing accuracies, the SEM surface comparison), each with the printed wording and page.
  The paper has no tables of its own.
- `work/`: scratch (may be deleted): `build_main.py` (builds main.tex from the PDF text layer), `descriptions.py` (the
  decompiler's own text), page renders `pages/`, vector dumps `vd_*.json`, overlays `*_overlay.png`, side-by-side
  comparisons `cmp_*.png`, zooms `z_*.png`, `check_main.json`.

**Left out:** the bioRxiv stamp on pp. 2–38 (repeated), the page numbers, and the margin line numbers 1–576. Text printed
inside the figures (panel letters, labels, scale bars, axis labels) is in the `\alttext` descriptions.

**How the text was made:** `work/build_main.py` reads the PyMuPDF spans of every page, drops the stamp (Helvetica 8 pt),
the line numbers (LMSans8 6 pt) and the page numbers, and maps fonts to markup (Times Bold 17 pt = section, 14 pt =
subsection, bold 12 pt = `\textbf`, italic = `\emph`, LMMono = `\texttt`, Times < 10.5 pt = `\textsuperscript`, CMSY
glyphs ∼ ≈ × ≥ kept as Unicode, the raised circle (`\circ`) used as a degree sign written as °). Paragraphs are split at
indents and vertical gaps; line-end hyphens are removed when the next line starts with a lower-case letter (60 cases,
each printed by the script and checked; "hemi-brain", "synchrontron-source" and "Sub-cellular" kept their hyphen,
"Pro-Long" was joined to "ProLong", the product name; "Müller-Gerbl" is a real hyphen). Two exact fixes were needed where
the text layer drops a space after a symbol glyph: "180° with 0.3° angle" and "Fluoromyelin™ red" (both checked
against the page image). The result was proofread against the page images.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice) from this folder; no errors. The only
warnings: fontspec/DejaVu (no small caps; not used here) and one "Marginpar moved".

Re-run the data: `python3 -I -B figures/<panel>_extract.py` (reads `source/wildenberg2023.pdf` through
`/home/admin/ephemeral/oct_17_papers/tools/vector_dump.py`), then `python3 -I -B figures/<panel>.py`.

## Figures and data

Vector check (`vector_dump.py` on every figure page): Figures 1, 2, 4 are single raster images; Figures 3, 6 and
Supplementary Figures 1–5 are raster images with a few vector annotations (boxes, lines, labels); **Figure 5C** is a vector
dot plot with real text labels; **Supplementary Figure 6** is pure vector (223 paths, no raster image; its tick labels are
glyph outlines, so the axes were calibrated on the tick marks).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 | colour schematic of the pipeline (4 quadrants) | – | – | no data |
| Fig. 2A | schematic (cutting block A into A1, A2) | – | – | |
| Fig. 2B | two confocal (Fluoromyelin) images, A1 back / A2 front, numbered clusters, red boxes + insets, green ellipses | – | – | no scale bar printed |
| Fig. 3A | photograph of an embedded pillar, 1 mm bar, L1/V2/V1 labels | – | – | |
| Fig. 3B | three µXCT slices with coloured boxes, three 4× zoom-ins | – | – | |
| Fig. 3C | µXCT image of the pillar 1 / pillar 2 junction with a vessel | – | – | |
| Fig. 4A | two µXCT pillars with traced MAs, 1.5 mm bar | – | – | |
| Fig. 4B | zoom at the gap with ~20 coloured traces | – | – | |
| Fig. 4C | 3 rows: slice with red box and asterisk + zoom with one MA highlighted; 100 µm bar | – | – | |
| Fig. 5A | 30 nm nXCT image with shaded axons and the 50/100-slice boxes; 5 um bar | – | – | |
| Fig. 5B | skeleton traces, "Full" and "- 50 slices"; 10 um bar | – | – | |
| **Fig. 5C** | dot plot, accuracy (%) vs kerf size (slices / µm), 3 points | `figures/fig5c.csv` | **2 vector** | y from the grid lines (residual 0.3 %), x from the label centres (~1 slice) |
| Fig. 6A | 3D rendering of three neurons over nXCT slices | – | – | |
| Fig. 6B | nXCT slice with segmented MA cross sections; 10 um bar | – | – | |
| Fig. 6C | 3D rendering of segmented MAs | – | – | |
| Suppl. Fig. 1A | two low-magnification SEM images (vibratome, Compresstome); 1 mm bar | – | – | |
| Suppl. Fig. 1B | two surface SEM images; dotted circles, red arrows; 10 µm bar | – | – | |
| Suppl. Fig. 2A | photograph of the coronal slab with the V1/V2 box | – | – | |
| Suppl. Fig. 2B | pillar cartoon and bright-field photograph of the 2×4 pillars | – | – | |
| Suppl. Fig. 3 | µXCT montage of one MA over 2.2 mm, inset, zooms I–IV; 500 um bar | – | – | |
| Suppl. Fig. 4 | nXCT zoom, Node of Ranvier; 2.5 um bar | – | – | |
| Suppl. Fig. 5 | nXCT image with green/red/yellow match markers; 10 um bar | – | – | |
| **Suppl. Fig. 6** | line plot, No. MAs traced (log) vs distance (mm), 8 lines | `figures/sfig6.csv` | **2 vector** | 412 vertices, exact |

Panel counts by tier (plotted panels): tier 1: 0; tier 2: 2 (Fig. 5C, Suppl. Fig. 6); tier 3: 0; tier 4: 0.

**Figure 5C.** The three white markers sit at (−0.3, 99.7), (49.6, 96.8) and (100.4, 60.1) (slices, %); the orange line
joins their centres. y was calibrated on the four dotted grid lines, which are the labelled ticks 100/80/60/40: they are
not exactly equidistant (17.2, 17.9, 17.2 pt), so the fit residual is 0.27 %, which is the uncertainty given. There are
no x tick marks; x was calibrated on the centres of the labels 0/50/100 (residual 0.2 slices). The printed annotations
"(97)" and "(60)" and the text's 97 % / 60 % agree with the markers within that uncertainty.

**Supplementary Figure 6.** Axes from the tick marks: 10 x ticks at 0…90 mm (31.6 pt apart, residuals ≤ 0.006 mm, the
axis end at 99.99 mm) and the y major ticks 10¹…10⁴ plus the x axis line at 10⁰ (51.6 pt per decade, residuals ≤ 0.0004
decades, checked against the 40 minor ticks: max 0.0006). The eight series are stroked polylines (solid, or dash
patterns [1.85 1.85] / [4.03 4.03] for the dotted 2 mm lines): their vertices are the data, one per mm for the 1 mm
lines (x = 1.0, 2.0, …) and one per 2 mm for the 2 mm lines (x = 1.1, 3.1, …), clipped at the bottom of the axes box
(flag `clipped`). All eight lines extrapolate to about 7 × 10⁴ at 0 mm, and each line is consistent with
N = 7 × 10⁴ × P^(x/d) (P the success rate, d the pillar diameter): e.g. 0.99 solid reaches 2.6 × 10⁴ at 100 mm
(0.99¹⁰⁰ = 0.366), 0.50 solid reaches 1 at 16 mm. This formula is the decompiler's reading of the data; the paper gives
only P≈(Pseg×Pgap)^Ngap. The y axis also carries a second, finer set of unlabelled tick marks (a leftover axis in the
vector data, visible as small ticks on the upper half of the axis).

**Checks done:** both extractions were drawn back onto 4× renders of the source (`work/fig5c_overlay.png`: red crosses
on the marker centres and blue ticks at the calibrated 0/50/100 and 40–100 positions; `work/sfig6_overlay.png`: every
vertex as a small circle on its line, red ticks at the calibrated 0…100 mm and 10⁰…10⁴), and each replot was put next
to the original with `tools/compare.py` (`work/cmp_fig5c.png`, `work/cmp_sfig6.png`) and looked at: series, ranges,
log/linear scales and tick positions match.

## Text check (`tools/check_text.py`, version 2026-10-17j)

Options used: `--drop-line-numbers` (margin line numbers 1–576). No `--pages`, `--exclude` or `--figure-box`.

| file | PDF tokens | coverage | without repeated text | running text (also without in-figure text) | tex tokens in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|---|
| `main.tex` | 9508 | 95.6 % | 96.9 % (137 repeated tokens) | 97.5 % (54 in-figure tokens) | 99.1 % | 0 | 0 |

Without `--drop-line-numbers`: 10027 tokens, 90.6 % / 91.8 % / 92.3 % (the 519 extra tokens are the line numbers).

What the remaining 2.5 % is (`--min-run 1`: 104 runs, 232 tokens, every one looked at):
- the stamp's words "doi bioRxiv preprint", which the text layer gives in a different order on every page (3 × 38 = 114
  of the 137 "repeated" tokens; the stamp is in the .tex once, and its other words match on every page);
- the 38 page numbers (one token each);
- about 60 words hyphenated at a line end whose two halves the margin line number separates in the text layer ("compen 49
  sated", "beam 149 line", "Pro 247 Long", …): the tool cannot join them, so each counts as 2 missing tokens and 1 EXTRA
  token (the joined word); these are all the EXTRA singles;
- 4 line numbers that `--drop-line-numbers` did not drop (231, 441, 494, 513), and the section
  numbers "4", "5", "6", "7" of the Discussion/Methods/Acknowledgements/References headings, which the option drops from
  the PDF side because they sit at x = 72 pt, inside its 15 % margin band (so they are reported as EXTRA singles);
- text inside the figures (54 tokens counted by the tool, plus "1 mm" of Fig. 3A and "# um" scale bars that the tool
  lists as repeated): all in the `\alttext` descriptions;
- "Dogˇa" (references 25, 44), which the tokenizer splits as "dog a".

Read-through against the page images (step 4 of the spec) done for: the superscripts (affiliation numbers, cm³, nm³,
µm³, 10¹⁰, "(∼250 µm)³", the raised "Ngap"), ∼ ≈ × ≥ « °, the µ/μ characters as printed (the Fig. 3 caption uses both),
the italic phrases (*Rhesus macaque*, *relative to each other*, *whole brain*, *in vivo*, the caption lead-ins, the
journal names), the bold figure references, the URLs, the list numbering, the reference numbers and page ranges
(including "562–574" and "1637–1643", which are split at a line end in the PDF), and the order of the text around the
figures.

## Errors and oddities in the paper (kept verbatim; flagged with `\decompnote` where it matters)

- **Section thickness and species of the Fluoromyelin experiment (Fig. 2):** Results 3.1 says "We cut 300 µm thick
  serial slices of cortex brain tissue"; Methods 5.2 says the sections were "Paraformaldehyde fixed zebrafinch brain …
  cut into 200 µm thick serial sections", provided by Precisionary Instruments. The caption says "2-photon confocal
  microscopy", the Methods "a Leica Sp5 Confocal microscope".
- **Discussion formula:** "P≈(Pseg×Pgap)Ngap" with the subscripts typed as plain letters and the exponent raised, and
  "Pseg×Pgap ≥ 97.8" without a percent sign.
- **"«1%"** (Introduction) is printed with a guillemet; ≪ was presumably meant.
- **Fig. 5 title** "accurately traced across a computational kerf up to 1 µm" while the tested kerfs are 1.5 and 3 µm
  (97 % at 1.5 µm). Caption: "kerk".
- **Fig. 6 caption:** "Scale bar = 10 (B)" without a unit (the bar reads "10 um").
- **Suppl. Fig. 6 caption** swaps the axes ("x: the number of neurons … versus y: the total distance"); the plot has
  distance on x and the number of MAs on y.
- **Gap of "about 1 pixel of µXCT data"** (Results 3.3, 697 nm) while the Methods give a 0.345 µm pixel size and the
  Results "∼600 nm³ resolution".
- Typos kept as printed: "i..e", "subcortial", "tomogrpahy", "compatibly", "de-myleination", "theses repair",
  "within and across across the gap", "Supplementary Figure 3)and", "nano-xray", "127 accurately axons traced",
  "BosssBD" (BossDB), "manufacture's protocol", "University of at Chicago", "Knossos.Then", "shwon", "Individal",
  "synchrontron-source", "cab be", "compresstome,stained", unclosed parentheses in the Fig. 3 caption, "Fluoromyelin"
  vs "FluoroMyelin", "Jian-Qiang" (no surname), "Dogˇa" (caron after the g; ref. 23 writes "Doga"), "Narayan" vs
  "Narayanan Kasthuri", "mhc-tetramer", "nsls ii", lower-case journal/title words in several references.
- **Fig. 5C** plots 100 % at 0 slices, but the text only states that "100 percent of all MA" could be traced within the
  volume; the marker sits at 99.7 %.

## Notes for the spec / tools

- `--drop-line-numbers` also drops the section numbers printed at the left margin (x = 72 pt is inside the 15 % band),
  which then show up as EXTRA singles. Dropping only numbers set in a smaller font than the body (here LMSans8 6 pt vs
  Times 12 pt), or only numbers left of the text block's left edge, would avoid that.
- Words hyphenated at a line end next to a margin line number ("compen 49 sated") are not joined by the tool, so every
  such word costs 2 missing + 1 extra token (about 60 words here, 0.6 % of coverage). Skipping dropped line-number tokens
  before the hyphen join would fix it.
- `vector_dump.py` reports text spans with their bboxes; for this PDF the bboxes of rotated/scaled text (Fig. 5C's y
  labels, the scale-bar labels) are wrong (tall boxes), so label centres cannot be used for the y calibration there;
  the grid lines were used instead.
- The task message counted Supplementary Figures 1–3; the PDF has six.
