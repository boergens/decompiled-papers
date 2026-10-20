# kong2012: decompiled

Jian-Qiang Kong and George Y Kong (Greenville, NC). "Method and device for cutting fresh tissue slices."
US Patent 8,109,184 B2, granted Feb. 7, 2012. Appl. No. 12/310,519, PCT filed May 22, 2007 (PCT/US2007/012120,
WO2008/030279 published Mar. 13, 2008, § 371 date Feb. 27, 2009); provisional application 60/842,386 filed Sep. 6,
2006; prior publication US 2010/0175520 A1 (Jul. 15, 2010). 14 claims, 4 drawing sheets. All of this is printed on
the front page; the task message agrees. As the USPTO prints it: **US 8,109,184 B2**, "United States Patent, Kong et
al., Date of Patent: Feb. 7, 2012".

**DOI:** none (a patent). Document number US8109184B2.

**Licence:** this is a public USPTO patent document; the publication prints no copyright notice (USPTO patents carry
none; a patent owner may claim copyright in the drawings or specification only by a notice, and there is none here).
`source/SOURCE.txt` says the same.

**Version:** the granted patent as published by the USPTO (the B2 publication), an image-only PDF from the USPTO
full-text server.

## Source files (`source/`)

| file | what it is |
|---|---|
| `US8109184B2.pdf` | 11 pages, 748 kB, "USPTO PDF Builder". `pdfimages -list`: one 2560 × 3300 px 1-bit CCITT image per page; `pdffonts`: no fonts, i.e. **no text layer at all** (not even OCR). The PDF declares each page as a 2560 × 3300 pt box, so 1 pt = 1 scan pixel, and the physical letter page (8.5 × 11 in) is scanned at **300 ppi** (2550 px per 8.5 in plus the USPTO's 10-px frame). Page 1 front page, pages 2–5 drawing sheets 1–4, pages 6–11 the description and claims in columns 1–12. |
| `US8109184B2.google_patents.txt` | the text of the Google Patents page of the same document (HTML stripped), fetched by the coordinator the same day; the second opinion for the OCR. It contains the abstract, description and claims (and Google's metadata, classification and citation tables). |
| `US8109184B2.reference.txt` | **written here** by `work/diff_google.py --write-reference`: the Google text trimmed to the abstract, description and claims (6575 word tokens), the reference for `tools/check_text.py --reference-text`. |
| `SOURCE.txt` | the coordinator's fetch note (URLs, date, licence remark). |

No supplement, data set or other file is named by the patent; nothing is missing. The two patents it incorporates by
reference (US 7,146,895, the prior Kong "sliding blade microtome", and provisional 60/842,386) are not in `source/`.

## Method: tool-first transcript

The text of `main.tex` was **not typed by the decompiler**. It was placed by a script from an OCR and proofread:

1. **OCR:** Datalab API, accurate mode, run by the coordinator on 2026-10-20 on the PDF: `work/datalab/US8109184B2.md`
   (markdown with `{n}----` page delimiters, n = 0-based page index; headings; the two citation tables as markdown
   tables; the drawing sheets as image links followed by the reference numerals read inside them; bold and italics
   kept). `US8109184B2.meta.json`: 11 pages, no failed pages, 8.25 cents.
2. **Build:** `work/build_main.py` reads the markdown and writes `main.tex`: `{n}` delimiters → `\pdfpage{n+1}` (inline
   where a page begins mid-sentence), the front page's INID items → hanging paragraphs with its headings as
   `\section*`/`\subsection*` and the dotted leaders as `\dotfill`, the two citation tables → tabulars, the five image
   links → `figures/front_drawing.png` and `fig1.png`–`fig4.png` with the decompiler's `\alttext` (the numerals Datalab
   read inside the drawings are dropped from the text: every one of them is named in the `\alttext`), the sheet labels
   "FIG. N" kept as a line under each image, the column numbers (`# 1`, `## 2`, `###### 11`, `###### 12`, which Datalab
   emitted on two of the six text pages) dropped and replaced by one `\decompnote` per text page giving the column
   mapping and the first words of the right column, the seven paragraphs split at a column or page break inside a
   sentence joined (`JOINS`), Datalab's italic `*Z*` (its reading of the struck Z of the print) → `Z`, `$\mu$ m` → `μm`,
   markdown bold/italic/quotes → LaTeX. The reference numerals of the drawings are printed in bold in the description
   and the figure numbers from the Brief Description on, the claim numbers and "claim N" in the claims; Datalab bolded
   them on one page only, so the script applies the printed rule uniformly (`bold_numerals()`: a standalone integer
   from the set of 93 reference numerals, in the Description of the Preferred Embodiment; checked that the only
   standalone integers it leaves plain there are 20° and 80°, 1 mm and 7,146,895, all plain in print). The claims are a
   `hangpars` block; the indented elements of claims 1 and 3 get `\hspace*{1.5em}`.
3. **Proofreading:** every page image was viewed (300-ppi renders `work/pages/p-NN.png`, zooms `work/z_*.png`), and
   the Datalab text was compared word by word with the Google Patents text (`work/diff_google.py`): the two agree on
   every word of the abstract, description and claims except one ("accurately"/"accurally"), which was checked on a 2×
   zoom of the scan (`work/z_accurally.png`): the print says **accurally**. Google's own OCR-type artefacts ("O- ring",
   "Hall- Effect", "Z—-axis" for the struck Z) are not in the PDF and were ignored. The front page (bibliographic
   block, citation tables, abstract) and the sheet labels were proofread against the page image line by line.

The corrections, all in the script's `CORRECTIONS` table (applied before the transformation; each asserted to match
exactly once) or `JOINS` list:

| where | Datalab had | fix |
|---|---|---|
| col. 7, l. 19 | `accurately controllable` | **`accurally`** as printed (Datalab silently corrected the typo) |
| col. 10, claim 1 | the elements "attaching a specimen … holder;" and "supporting said specimen cutting blade …" merged into one paragraph | split into two elements as printed |
| sheet 2 | `FIG. 2` twice | once |
| cols 1→2, 3→4, 5→6, 7→8 | paragraphs broken at the column break | joined (`JOINS`) |
| pp. 7→8, 8→9, 9→10 | paragraphs broken at the page break | joined, `\pdfpage` inline |
| front page | `(10) Patent No.` and `(45) Date of Patent` as one paragraph (hard line break) | two items |
| whole text | `*Z*` (italic) for the struck Z | plain `Z`, said in the top `\decompnote` |
| cols 2, 2 | `$\mu$ m` | `μm` |
| embodiment, claims | reference numerals bold on one page only, claim numbers bold on one page only | bold throughout, as printed |

So the proofreading found **one word error** in 6575 words of running text, plus formatting. Datalab also dropped the
barcode number `US008109184B2` at the top of the front page (left out on purpose, see the top note), read all the
numerals inside the drawings (dropped; they are in the `\alttext`), and read the "19" of FIG. 3 as nothing (see
Errors).

## What the folder contains

- `main.tex` / `main.pdf`: the whole patent in reading order: front page (header, title, inventors, notice,
  application data, classification, references cited with the two tables, examiner, abstract, "14 Claims, 4 Drawing
  Sheets", the representative drawing), the four drawing sheets, the description with its headings, the claims 1–14 in
  `hangpars`, the closing asterisks. Compile with `lualatex -interaction=nonstopmode -halt-on-error main.tex` in this
  folder (`decomp.sty` is here); compiles without errors (run twice), 17 pages. Six overfull boxes: five of 0.8 pt from
  the `\alttext` frames, one of 18.9 pt in the description's title heading (the all-capitals title in the
  section font does not break), cosmetic.
- `figures/front_drawing.png`, `fig1.png`–`fig4.png`: `work/make_figures.py` (re-runnable) crops each drawing's ink
  box plus a 24-px margin with `tools/crop.py` and rotates the four sheets 90° clockwise so the numerals read upright
  (the sheets are printed sideways; the front-page drawing is upright and is not rotated). **Resolution:** the PNGs
  are at 200 ppi of the physical page, the SPEC's figure resolution, from the 300-ppi scan; because the PDF's page box
  is 1 pt per scan pixel, `crop.py`'s dpi argument has to be **48** (= 200/300 × 72) for that, not 200 (which would
  upsample the scan 2.8×). The crop boxes (PDF points = scan pixels): front drawing p. 1 670,2168–1842,3075; sheet 1
  p. 2 440,558–2016,2900; sheet 2 p. 3 638,515–2064,2911; sheet 3 p. 4 503,864–2015,2607; sheet 4 p. 5
  572,1077–2087,2413.
- `figures/fig4.csv`, `fig4_extract.py`, `fig4.py`, `fig4_replot.png`: the bar graph's data (below).
- `source/US8109184B2.reference.txt`: see Source files.
- `work/`: `datalab/` (the Datalab markdown, its five image crops, meta), `build_main.py` (rebuilds `main.tex`),
  `make_figures.py`, `diff_google.py` (the word-level comparison; `--write-reference` writes the reference text),
  `pages/` (300-ppi page renders), `z_*.png` (zooms used in proofreading), `fig4_overlay.png` (+ `_small`, `_crop`:
  the digitization overlay), `compare_fig4.png` (original beside the re-plot). Scratch except the scripts.

## Figures

One plotted panel (FIG. 4), tier 3 (digitized); the other four images are line drawings with a description only.

| figure | type | data | tier | notes |
|---|---|---|---|---|
| front page drawing | patent line drawing: the representative drawing = FIG. 1 upright, without the label, same 49 labels | – | – | `figures/front_drawing.png`; `\alttext` refers to FIG. 1 |
| FIG. 1 (sheet 1) | line drawing, front elevation view of the vibrating sliding-blade microtome 10; 49 labels (47 numerals, arrows B and C) | – | – | `figures/fig1.png`; every numeral named in `\alttext` with the description's wording |
| FIG. 2 (sheet 2) | line drawing, side elevation partly in section (bath, syringe tube with the reduced-diameter outlet lip 60, micrometer drive, blade holder with the glued blade); 43 labels (42 numerals, arc D) | – | – | `figures/fig2.png`; `\alttext` |
| FIG. 3 (sheet 3) | line drawing, top plan view of the micrometer drive assembly; 8 numerals and an arrow labelled "19" | – | – | `figures/fig3.png`; `\alttext` |
| FIG. 4 (sheet 4) | bar graph, live/dead cell ratio of two bars (206 invention, 208 prior vibrating microtome) with error bars and an asterisk | `figures/fig4.csv` | 3, digitized | values 6.15 ± 0.73 (cap) and 1.17 ± 0.19 (cap); uncertainty ± 0.1 (the printed ticks are unevenly spaced, residual 0.10 units of the linear fit over the five ticks) |

**FIG. 4 checks done:** `fig4_extract.py` works on the native 300-ppi bilevel page (rendered with PyMuPDF, rotated
upright with numpy), finds the y axis, its five ticks, the baseline, the two bars' extents, their top edges and the
error-bar caps by row coverage, and writes the CSV and the overlay `work/fig4_overlay.png` (magenta crosses on the
tick marks, bar tops and caps: all sit on the drawn lines; viewed, also as `fig4_overlay_small.png`). `fig4.py` reads
only the CSV and re-plots the two bars with their upper error bars, the asterisk and the 0–8 axis; `tools/compare.py`
put it beside the original (`work/compare_fig4.png`, viewed): same bars, heights, caps and axis range. The x axis has
no labels: the bars are categories (left 206, right 208). The patent gives no sample sizes, no statistics and no
definition of the error bars or the asterisk.

## Text check

`tools/check_text.py` (version 2026-10-20b) against the PDF alone reports **0 PDF tokens** (the PDF has no text
layer) and therefore 0 % coverage with the whole .tex as one EXTRA run; that output is meaningless for this document.
The checks that mean something:

**1. `check_text.py --reference-text`** (command from this folder):
`python3 -I ../../tools/check_text.py main.tex source/US8109184B2.pdf --reference-text source/US8109184B2.reference.txt`

| coverage of reference tokens | without text repeated on ≥ 3 pages | running text | tex tokens found in reference | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|
| **100.0 %** (6575 reference tokens, 6938 tex tokens) | 100.0 % (0 repeated) | 100.0 % | 95.1 % | 0 | 4 runs, 337 tokens |

The four EXTRA runs are exactly the parts of the patent that the reference (Google's abstract + description +
claims) does not contain: the front-page header `(12) United States Patent Kong et al. (10) Patent No. … (45) Date of
Patent Feb. 7, 2012 (54)` (24 tokens); the INID block from `(76) Inventors` to `Jul. 15, 2010` (98); the block from
`on Sep. 6, 2006 (51) Int. Cl.` through the classification, the References Cited tables, the examiner and attorney
lines (202); and `14 Claims, 4 Drawing Sheets FIG. 1 FIG. 2 FIG. 3 FIG. 4` (13: the sheet labels). Every one of these
was proofread against the page image (and the citation tables against Google's "Patent Citations" list: all 11
patent citations and the one non-patent citation agree). No MISSING run: every word of the reference is in the .tex.

**2. Own word-level comparison** (`python3 -I -B work/diff_google.py main.tex`, `difflib` on lower-case word tokens
of the three sections, the decompiler macros and LaTeX commands stripped):

| section | tex tokens | Google tokens | differing runs |
|---|---|---|---|
| abstract | 105 | 105 | 0 |
| description | 5870 | 5870 | 0 |
| claims | 600 | 600 | 0 |
| **total** | **6575** | **6575** | **0** |

Every token agrees, in order. (On the raw Datalab markdown the same script reported 6 differing runs: the column
numbers 2, 11, 12; `mu` from `$\mu$` twice, where Google has the character µ; and `accurately` vs `accurally`.)

Read-through against the page images (SPEC step 4) done for: the whole front page (every INID item, the two tables
cell by cell, the examiner lines, the abstract), the headings and their order, the nine struck Z's (cols 1–4; written
Z), "“zero —”" (col. 2, l. 2, an em dash inside the quotes, as printed), 15-35 degrees, 0.6 mm, 0.1 mm, 0.5 mm, 70 to
80 μm, 10 and 40 μm, 20° and 80°, 1 mm, 7,146,895 (four times), the bold reference numerals (spot-checked on every
text page), the claims' indentation, the closing `* * * * *`, and all 101 labels on the four sheets and the front
drawing (listed in the `\alttext` blocks and compared with Datalab's numeral lists: Datalab's FIG. 1 list has all 49,
its front-page list misses 172, its FIG. 3 list is empty).

## Errors and oddities in the patent (kept verbatim)

- col. 7, l. 19: "accurally controllable" (sic, for "accurately").
- col. 4, l. 64–65: "expressly incorporated herein be reference" ("be" for "by").
- col. 6, l. 43: "the reduced diameter outlet **tip** 60"; everywhere else (cols 5, 6, 9) the part 60 is the "reduced
  diameter outlet lip", and col. 9, l. 38 calls it the "decreased diameter lip 60".
- col. 2, l. 2: 'a so-called "zero —" technique': an em dash where a word is expected (the Google text has the same
  defect); the intended term is not recoverable from the document.
- col. 1, l. 46–47: "The horizontal oscillation of the blade, or its oscillation is a direction which is generally
  parallel to the longitudinal axis" ("is" where "in" reads naturally).
- col. 7, l. 62–63: "friction reducing elements, such as linear bearings, allow friction slide or other friction
  reducing components" ("allow" where "a low" reads naturally).
- col. 7, l. 20–21 "Hall-Effect sensors" (hyphenated, at a line break but Google's text has the hyphen too) vs "Hall
  Effect sensors" in cols 7, 9 and claim 6.
- FIG. 3: the double-headed arrow at the housing is labelled **19**, while col. 5, l. 56 says "the directions
  indicated by the arrow A in FIG. 3"; no part 19 exists in the description.
- FIG. 4: the y-axis label is defectively printed: "Live/" + a fragment, a gap, "l Cell Ratio" (the word "Dead" is
  missing but for its first and last strokes); the ticks 0, 2, 4, 6, 8 are unevenly spaced (up to 0.1 unit off a
  linear scale). The asterisk above bar 206 is not explained, and no sample size or statistic is given anywhere.
- Claim 7 introduces "a vibrating support drive motor"; claims 8 and 9 then refer to "said vibrating blade support
  drive motor" (no exact antecedent).
- The letter Z is set as a struck Z (Ƶ-like) in all nine occurrences of "Z-axis"/"Z axis" (cols 1–4), the drafting
  convention to distinguish it from 2; X and Y are plain. Written as Z in the .tex (said in the top note).
- Front page: "George Y Kong" has no period after the initial, as printed.

## Not available

Nothing: the patent names no data set, supplement or video. The two incorporated documents (US 7,146,895 and
provisional 60/842,386) are other publications, not parts of this one.

## Known problems

- The figure PNGs are rotated 90° from the printed orientation of the sheets (on purpose, for reading), and the
  rotated images are what `main.tex` includes; `crop.py`'s raw output is not kept.
- The struck Z is written as a plain Z (searchable); the form of the glyph is recorded in the top `\decompnote`.
- The printed line numbers (5, 10, …, 65) are left out, so citations by column and line need the page image; the
  column starts are given in the per-page notes.
- 18.9-pt overfull line in the description's title heading (cosmetic).
- Claims 1 and 3: the print indents the sub-elements of "said specimen holder including:" one level deeper than
  "providing a base …"; the .tex gives every claim element the same single indent (`\hspace*{1.5em}`).

## Time

About 45 minutes: reading brief, spec and example (5), page inspection and zooms (8), figures and the FIG. 4
digitization with its checks (10), the build script and the `\alttext` blocks (12), compile, checks, README (10).
