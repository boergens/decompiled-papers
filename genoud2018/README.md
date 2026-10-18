# genoud2018: decompiled

Christel Genoud, Benjamin Titze, Alexandra Graff-Meyer, Rainer W. Friedrich. "Fast Homogeneous En Bloc
Staining of Large Tissue Samples for Volume Electron Microscopy." *Frontiers in Neuroanatomy* **2018**,
12:76 (Methods article). DOI [10.3389/fnana.2018.00076](https://doi.org/10.3389/fnana.2018.00076).
Received 20 June 2018; accepted 29 August 2018; published 28 September 2018.

**Licence:** Copyright © 2018 Genoud, Titze, Graff-Meyer and Friedrich; open access under the Creative
Commons Attribution License (CC BY), as stated on p. 8.

## Local and external

**In the local collection**
- Source files:
  - `papers/genoud2018/fnana-12-00076.pdf` – the article, 8 pp., publisher's version of record
  - `papers/genoud2018/fnana-12-00076.txt`, `papers/genoud2018/fnana-12-00076.raw.txt` – earlier text extractions (not used)
  - `papers/genoud2018/SOURCE.txt` – fetch note
- Cited works decompiled here: hua2015 (`decompiled/hua2015/`), mikula2015 (`decompiled/mikula2015/`), seligman1966 (`decompiled/seligman1966/`)

**External pull needed** (not on this machine)
- Supplementary Data S1 (movie of an image stack from the adult zebrafish brain, fBROPA protocol) – https://www.frontiersin.org/articles/10.3389/fnana.2018.00076/full#supplementary-material – the paper's only supplement; a movie, no plot data
- All other cited references: 17 entries in the reference list (20 unnumbered, alphabetical entries) without a [local: …] tag.

## Source files (`../../papers/genoud2018/`)

| file | what it is |
|---|---|
| `fnana-12-00076.pdf` | the article, 8 pp. **Publisher's version of record**: Frontiers typesetting with journal header ("METHODS / published: 28 September 2018 / doi"), "Check for updates" button, running header "Genoud et al. / En Bloc Staining of Large Tissue Samples" and footer "Frontiers in Neuroanatomy \| www.frontiersin.org \| n \| September 2018 \| Volume 12 \| Article 76". PDF metadata: created 2018-09-22, modified 2018-09-24 (dvips + Ghostscript). `SOURCE.txt`: fetched from frontiersin.org (curl, 2026-10-12). Born-digital; the text layer is good. |
| `fnana-12-00076.txt`, `.raw.txt` | earlier text extractions (not used). |

**Not available:** *Supplementary Data S1* (a movie of an image stack from the adult zebrafish brain,
"Field of view is 8 × 8 µm². Original voxel size is 10 × 10 × 30 nm³"), on the Frontiers article page
(https://www.frontiersin.org/articles/10.3389/fnana.2018.00076/full#supplementary-material). It is not in the
source folder and was not fetched (no network). It is a movie, not plot data. The paper names no data set or
source-data file, so no tier-1 data is missing.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block, title, authors, affiliations,
  the left-margin block of p. 1 (OPEN ACCESS, editor, reviewers, correspondence, dates, citation; placed after
  the author list, noted in the file), abstract, keywords, Introduction, Results (with the numbered list 1–8 and
  Day 1–4), Discussion, Materials and Methods (Reagents, the 20-step fBROPA protocol, Imaging), Author
  Contributions, Funding, Acknowledgments, Supplementary Material (with the Data S1 legend), the 20 references
  (author–year, unnumbered, in printed order), Conflict of Interest Statement, copyright/licence statement.
  `\pdfpage{1..8}` marks where each PDF page starts. Numbered lists are written as paragraphs with their
  printed numbers, so the numbers are part of the text.
- `figures/fig1.png` … `fig4.png`: each figure cropped from the PDF at 200 dpi (embedded image bbox + 3 pt),
  without its caption.
- `tables/`: not created; the paper has no tables.
- `work/`: scratch (page renders `pages/`, text-block dump `blocks.txt`, `draft.py`/`draft.tex` = text-layer
  draft with bold/italic markup used as the transcription base, vector dumps `vec_p*.json`, zooms `z_*.png`,
  `check_text_fixed.py` and check JSON). May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (run twice); compiles
without errors, a few slightly overfull lines (long URL, sidebar lines).

## Figures

All four figures are greyscale electron micrographs (embedded 600 ppi raster images, one per figure). There is
**no plotted panel** (no axes, no charts), so there are no CSVs, extraction or plotting scripts, and no
`compare.py` checks were needed. I checked for vector content anyway: `get_drawings()` finds 6 paths on each
figure page, all of them the figure's frame box and the header/footer rules; panel letters and scale-bar labels
are part of the raster images (no text spans in the figure areas).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A | EM micrograph, zebrafish telencephalon, 2-week protocol | – | – | scale bar 10 µm |
| Fig. 1B | EM micrograph, zebrafish telencephalon, 5-day protocol without lead aspartate | – | – | scale bar 10 µm; charging artifacts |
| Fig. 2A | low-magnification EM micrograph, coronal section of telencephalon with silver-particle resin | – | – | scale bar 100 µm |
| Fig. 2B | EM micrograph, neuropil near surface | – | – | scale bar 2 µm |
| Fig. 2C | EM micrograph, neuropil 300 µm below surface | – | – | scale bar 2 µm |
| Fig. 3A | EM mosaic (6 × 6 tiles), whole tectum cross-section with locations B, C, D marked | – | – | scale bar 200 µm |
| Fig. 3B | EM micrograph, neuropil at location B | – | – | scale bar 2 µm |
| Fig. 3C | EM micrograph, neuropil at location C | – | – | no scale bar printed |
| Fig. 3D | EM micrograph, neuropil at location D | – | – | no scale bar printed |
| Fig. 3E | four EM close-ups of synapses | – | – | scale bar 500 nm (first image only) |
| Fig. 4 | EM micrograph, two-cell organoid, with inset | – | – | scale bar 2 µm; no panel letter; inset without scale bar |

Panels per provenance tier: tier 1: 0, tier 2: 0, tier 3: 0, tier 4: 0 (no plotted panels).

## Text check (`tools/check_text.py`)

| run | coverage (raw) | coverage without repeated text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|
| stock tool | 97.7 % | 97.7 % (0 tokens detected as repeated) | 99.9 % | 8 runs, 122 tokens | 0 |
| `work/check_text_fixed.py` (one fix, see below) | 97.7 % | 99.4 % (96 tokens repeated) | 99.9 % | 2 runs, 26 tokens | 0 |

The stock tool's "without repeated" number equals the raw one here because the running footer contains the
page number, so it is never the same text on 3 pages (see Problems). All MISSING runs (`--min-run 1`, 128 tokens
in total) are explained:

- 125 tokens: the running footer on pp. 1–8 ("Frontiers in Neuroanatomy | www.frontiersin.org | n | September
  2018 | Volume 12 | Article 76") and the "Genoud et al." part of the running header on pp. 2–8 (the rest of the
  header, "En Bloc Staining of Large Tissue Samples", is matched against the title). Left out on purpose.
- 3 tokens: "highquality", "highcontrast", "opensource": real hyphens at line ends ("high-quality",
  "high-contrast", "open-source") that the tool's dehyphenation joins.

Without the header/footer, the article's own text is covered at 5494 / 5497 tokens ≈ 99.9 %.

EXTRA (`--min-run 1`, 8 tokens): the same three hyphenated words split on the tex side (6 tokens), and "OPEN
ACCESS" (2 tokens), printed in the left margin of p. 1 but drawn as graphics, not in the text layer
(transcribed from the page image; noted in main.tex).

Read-through against the page images (step 4) done for: superscripts (nm³, mm³, e⁻/nm², nm², µm², author
affiliation numbers and the asterisk), subscripts (ddH₂O, OsO₄, K₄Fe(CN)₆), ×, ∼, ≤, >, °C, µm/µs/µl,
the em dashes in "osmium—thiocarbohydrazide—osmium", en dashes in ranges and in "lipid–containing" /
"tetroxide–fixed" (ref. Seligman), the minus sign in "50% resin−50%", bold figure citations and bold durations
in protocol steps 4, 5, 7, 9, 12, italics (en bloc, *SBEMimage*, journal names, "bioRxiv 207472"), and the
reference list punctuation (kept as printed, including "541–546.doi:").

## Errors and inconsistencies in the paper (kept verbatim)

Flagged in main.tex with `\decompnote`:
- Reagents, Fixative: "Sigma **CO250**" is printed with a letter O (checked at 400 dpi); probably C0250 (digit
  zero) is meant. Not checked against a catalogue.
- Reagents, OsO₄/K₄Fe(CN)₆ solution: "2.5 M formamide" but "1.125 ml of formamide" in 10 ml. By my arithmetic
  (45.04 g/mol, ≈1.13 g/ml) 1.125 ml gives ≈2.8 M; 1.125 **g** (≈1.0 ml) gives 2.5 M. Probably g/ml mixed up.
  The other amounts check out: 0.147812 g K₄Fe(CN)₆ = 35 mM in 10 ml for the trihydrate (422.4 g/mol);
  2.5 ml of 4 % OsO₄ in 10 ml ≈ 39 mM; 40.35 g pyrogallol in 250 ml = 1.28 M; 8.56 g sodium cacodylate
  trihydrate in 100 ml = 0.4 M; 0.040 g aspartic acid / 0.066 g lead nitrate in 10 ml = 30 mM / 20 mM.
- Fig. 3 caption: panel E "(5 nm pixel size)", but the Imaging section says the 10 × 10 nm² pixel size was
  used for "all high-resolution images from the zebrafish brain".

Not flagged in main.tex (minor):
- Protocol step 9: "Stain in in OsO₄ solution B" (doubled word).
- Results: the paragraph on the 2-week protocol cites "(Figure 1B)" for the large empty spaces and poor
  conductivity, but the Fig. 1 caption says 1B is the 5-day protocol without lead aspartate; the large empty
  spaces are visible in 1A.
- Results says "FEI Quanta 200 FEG", Methods says "Quanta 200 VP-FEG".
- Abstract: voxel size 10 × 10 × 25 nm³; Supplementary Data S1: original voxel size 10 × 10 × 30 nm³ (may be
  different stacks).
- Fig. 4 caption: "Insert" for "inset". Abstract: "Homogenous" (elsewhere "Homogeneous").
- References: Deerinck et al. (2017) author list "…, and Peltier, S. T., Ellisman, M. H." (misplaced "and");
  Mikula and Denk (2015) "541–546.doi:" (no space); Zhu et al. (2012) "neuronalactivity" (no space).

## Problems with the spec and tools (found while doing this paper)

1. **`vector_dump.py` drops all horizontal and vertical lines.** It filters paths with
   `d["rect"].intersects(clip)`, and PyMuPDF's `Rect.intersects` is False for an empty (zero-height or
   zero-width) rect. On this paper's figure pages it reports `n_paths: 0` for the whole page, while
   `get_drawings()` returns 6 paths (all straight lines). In a real vector plot this would silently drop axis
   lines, tick marks, gridlines, horizontal error-bar caps and vertical error bars. Fix: test the bbox with a
   tolerance, e.g. `r = d["rect"]; if r.x1 < clip.x0 or r.x0 > clip.x1 or r.y1 < clip.y0 or r.y0 > clip.y1:
   continue` (or `pymupdf.Rect(r.x0-0.5, r.y0-0.5, r.x1+0.5, r.y1+0.5).intersects(clip)`).
2. **`check_text.py`'s repeated-text exclusion misses running footers with page numbers.** It groups MISSING
   runs by exact text, so a footer that contains the page number is never "repeated on ≥ 3 pages"; here the
   "without repeated" coverage stayed at 97.7 % (0 tokens excluded). `work/check_text_fixed.py` groups runs by
   their text with digit-only tokens removed (marked `FIX`), which catches 6 of the 8 footer runs (99.4 %); the
   footers on pp. 1 and 8 still differ because the header next to them is missing there. A sturdier fix: count
   5-grams of missing tokens across pages and drop any 5-gram (digits removed) missing on ≥ 3 pages.
3. **Spec suggestion:** a custom list environment using `\everypar{\hangindent=..\hangafter=1}` (the pattern of
   li2024's `reflist`) swallows a paragraph's leading number: "1. Dissection…" was typeset as ". Dissection…",
   because TeX reads `\hangafter=11`. The token check cannot see it (it reads the .tex source). Fix: end the
   assignment with `\relax` (`\hangafter=1\relax`), and mention it in the spec or put a ready list environment
   into `decomp.sty`. (Also: the name `numlist` clashes with siunitx's `\numlist`.)
4. **Spec gap:** for a paper with no plotted panels, the spec's step 3 and the figure-table columns are moot; one
   sentence saying "if there are no plotted panels, say so and skip CSV/compare" would help.
