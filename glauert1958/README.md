# glauert1958: decompiled

Audrey M. Glauert and R. H. Glauert. "Araldite as an Embedding Medium for Electron Microscopy."
*J. Biophysic. and Biochem. Cytol.*, 1958, Vol. 4, No. 2, pp. 191–194 and Plate 98. Received for publication
December 10, 1957. From the Strangeways Research Laboratory and the University Chemical Laboratory, Cambridge,
England. (Journal, volume, issue, year and pages are printed in the PDF: the journal line at the foot of p. 191
and the page numbers.)

**DOI:** none printed in the PDF and none given in `source/SOURCE.txt`. The PDF came from PMC as PMC2224339
(the id in the SOURCE.txt URL). *Background knowledge, not from the paper or the source note, unverified:* the
Journal of Cell Biology (successor of this journal) registers its back-file DOIs as `10.1083/jcb.<vol>.<issue>.<page>`,
which would make this `10.1083/jcb.4.2.191`.

**Licence:** no licence is printed in the PDF; it was fetched from NCBI's PMC Open Access bucket, whose metadata
gives no licence code.

**Redistribution basis (checked 2026-10-18 by the coordinator).** The PDF and its page at rupress.org print only
"Copyright, 1958, by The Rockefeller Institute", and PMC's open-access metadata gives no licence code. Rockefeller
University Press's policy, as stated in its 2013 editorial (Rossner, J. Cell Biol. 201:7, "New mandates? No problem for
The Rockefeller University Press", its own licence line): "We release all of our content six months after publication,
regardless of funding source" and "After six months it is available under a Creative Commons License
(Attribution–Noncommercial–Share Alike 3.0 Unported license)"; "All of RUP's content is available in the 'Open Access
Subset' of PMC six months after publication", which is where this PDF came from. RUP's current Permissions and Licensing
page (rupress.org/pages/permissions-and-licensing) lists CC BY-NC-SA 4.0 among its licence types and allows gratis reuse
with attribution "in an educational setting where it will not be sold for profit". This decompile is therefore mirrored
publicly as CC BY-NC-SA, with RUP's preferred attribution: ©1958 Glauert et al. Originally published in Journal of
Biophysical and Biochemical Cytology. https://doi.org/10.1083/jcb.4.2.191

**Version:** a scan of the printed journal pages, i.e. the published version of record (no preprint or manuscript
version exists for a 1958 paper).

## Source file (`source/`)

| file | what it is |
|---|---|
| `glauert1958.pdf` | 5 pages, letter size, 387 kB. A 2003 scan (Producer "PageGenie PDFGenerator", created 2003-10-10, document title "0191.tif"). `pdfimages -list`: one 2550 × 3300 px 1-bit CCITT image (300 ppi) per page, plus on page 5 an 805 × 987 px 8-bit JPEG (150 ppi) for the micrograph. `pdffonts`: 26 non-embedded TrueType substitutes (TimesNewRoman, CourierNew, Arial) and no embedded font, so the text layer is OCR; the page images are authoritative. The scan of page 1 sits 46.8 pt lower than the page box (image bbox y 46.8–838.8 pt); nothing of the article is lost. PDF pages 1–4 = journal pages 191–194, PDF page 5 = Plate 98. |
| `SOURCE.txt` | fetch note (PMC OA bucket, 2026-10-13). |

No supplement, data set or other file is named by the paper; nothing is missing.

## Method: tool-first transcript

The body text of `main.tex` was **not typed by the decompiler**. It was placed by a script from a fresh OCR and
then proofread against the page images:

1. **OCR:** Datalab API (Chandra model, "accurate" mode), run by the coordinator on 2026-10-18 on the PDF:
   `work/datalab/glauert1958.md` (markdown with `{n}----` page delimiters, headings, the two tables as markdown
   tables, the formulas and the plate as image files, italics and bold kept; `glauert1958.meta.json`: 5 pages, no
   failed pages, 3.75 cents). A tesseract 5.5 run at 300 dpi (`work/tess/p-1.txt` … `p-5.txt`) served as the second
   opinion, and the PDF's own 2003 text layer is `work/raw.txt`.
2. **Build:** `work/build_main.py` reads the markdown and writes `main.tex`: `{n}` delimiters → `\pdfpage{n+1}`
   (inline where a page starts mid-sentence), markdown headings → `\section*` (the small-capital headings) or
   `\subsection*` (the italic ones), the two markdown tables → the two tabulars (also `tables/*.csv`), the three
   image links → `figures/formula1.png`, `formula2.png`, `fig1.png` with the decompiler's `\alttext`, the `- `
   reference items → paragraphs in `hangpars`, `<sup>k</sup>` footnotes → `\footnote{}` at their marks, `*x*` /
   `**x**` / `<i>` / `$n$` / `$\times$` / quotes / `&` → LaTeX. The bibliographic block (journal line, title, authors,
   affiliation, Plate 98 and received lines, author footnote) and the plate page's header are the decompiler's
   constants in the script (verified on the page images), because Datalab dropped the journal line at the foot of
   p. 191 and the plate header of p. 5. `work/embed_blocks.py` is the one-off that copied the `\alttext` blocks and
   tabulars into the script from `work/main_summary.tex` (see History).
3. **Proofreading** against the page images: 300-dpi renders (`work/h-N.png`), 200-dpi half-page crops
   (`work/pr-N-top.png`, `pr-N-bot.png`) and 300-dpi zooms (`work/z*.png`, `zz_*.png`), word by word, with special
   attention to numbers, units, superscripts, chemical names, the two tables and the 20 places where the old text
   layer was wrong. Every Datalab/tesseract disagreement (`work/diff_ocr.py`, 182 tokens) was checked on the images.
   **Result: no word error in the Datalab text.** The corrections, all in the script's `CORRECTIONS` table
   (applied before the transformation, each asserted to match exactly once) or `JOINS` list:

| page | what | fix |
|---|---|---|
| 192 | `"nuclear"` with straight quotes | curly quotes like the other quotations (→ ``nuclear'') |
| 194 | `**Fig. 1**.` | the period belongs to the bold label: `\textbf{Fig. 1.}` |
| 191 | `the value of $n$ .` | stray space before the period |
| 192 | `(a) *Biological Specimens*.—` | the period is italic, as in `(b) *Other Specimens.*—` |
| 192 | paragraph broken at the column break ("to be reduced" / "to a value suitable") | joined (`JOINS`) |
| 192→193, 193→194 | paragraphs broken at the page breaks ("can be done at a" / "lower temperature"; "A" / "suitable choice") | joined, `\pdfpage` inline |
| 191, 5 | journal line and plate header missing | supplied from the bibliographic block |
| 191 | formula labels "(I)", "(II)" not in the text (inside Datalab's image crops) | in `figures/formula*.png` and `\alttext` |
| 193 | table dashes `1-2`, `2-3`, `4-6` | en dashes in the tabular / CSV (printed as short dashes) |

So the proofreading changed no word; it changed 4 formatting details, joined 3 split paragraphs and added 2 lines.

### How good were the three OCR outputs (for the engine choice)

`work/ocr_quality.py`, order-free: reference words (the proofread text, 2372 words) that each output failed to
produce, after rescuing words split at a line-end hyphen; reading order ignored.

| output | reference words not recognized | notes |
|---|---|---|
| Datalab (Chandra, accurate) | **0** | dropped 2 lines (journal line p. 191, plate header p. 5) and the formula labels; 1 straight-quote pair; hyphen-minus for the table's en dashes; a stray space; one italic period. Reading order, headings, footnotes, italics and bold all right; tables as tables. |
| tesseract 5.5, 300 dpi | **21** (16 distinct) in 2414 tokens (the script prints 31; 9 are the markdown list dashes and 1 a table-cell fragment of the reference, artefacts) | "Maalge" ×5 (the ø), "anv"/"PLaTE" (small capitals), footnote marks "araldite!" / "unstable.?", italic *n* read as "x" or dropped ("methyl/-butyl"), "(1)" for "(I)", "mi." ×2 for "ml.", "T.e." for "I.e.", "Fic." for "Fig.", "X" for ×, 4 dropped or changed periods/commas, 2 real hyphens dropped ("threedimensional", "glassstoppered"); table cells scrambled; running headers and the formula fragments appear as text. |
| PDF text layer (2003) | **≈ 61** (47 distinct; the script prints 71 incl. the 10 artefacts) in 2463 tokens, after 21 hyphen rescues | plus a reading-order problem that the count does not show: the two columns are interleaved line by line, so it is unusable as placed text. Word errors include all 5 "Maaløe", the journal line and "Plate 98", "1955" for 1956, "Nature"/"178" garbled, "Glanert", "Almqvlst", "typkimurium"/"typtdmurium", "103,030" for 100,000, "I t" ×7 for "It". |

The table of old-text-layer errors verified on the page images (kept from the first pass; they are what the
check_text EXTRA runs below consist of):

| OCR layer | page image (used) | where |
|---|---|---|
| `J'. B x o ~ s x c . AND Bzoc~z=. Crro~.` | J. Biophysic. and Biochem. Cytol. | journal line, p. 191 |
| `tle Uninersity` | the University | affiliation, p. 191 |
| `Pr~a~ 98` | Plate 98 | p. 191 |
| `1930%` | 1930's | p. 191 |
| `Maal¢e`, `Maalc~e`, `Maal~e`, `Maal~ie`, `Maal#e` | Maaløe (slashed o) | pp. 192, 194 |
| `aliphafic`, `typkimurium`, `typtdmurium` | aliphatic, typhimurium | pp. 192, 194 |
| `aralditet` | araldite¹ (footnote mark) | p. 192 |
| `unstable3` | unstable.² (footnote mark) | p. 192 |
| `I t` (several), `diificult`, `bc adequate`, `48QC`, `48"C` | It, difficult, be adequate, 48°C | pp. 192–193 |
| `I-2 hrs.` | 1–2 hrs. | table, p. 193 |
| `Specimcns`, `Etectron` | Specimens, Electron | headings, p. 193 |
| `Glauert and Brieger, 1955` | Glauert and Brieger, 1956 | Conclusions, p. 194 |
| `I~Iuxley`, `Glanert`, `Almqvlst`, `stradon` | Huxley, Glauert, Almqvist, -stration | references, p. 194 |
| `Ra~**ee, 1956, 1"/8, 803` | *Nature*, 1956, **178**, 803 | reference, p. 194 |
| `I956, 261` | 1956, 261 | reference, p. 194 |
| `Sowrces of Supt~ly` | Sources of Supply | p. 194 |
| `FIo. 1.` / `X 103,030` | Fig. 1. / × 100,000 | plate explanation, p. 194 |
| formula text `/o\ f CH=CHCH20 --ROCHL.= HCH~ .. (I) 0 /\ ROCHsCHCH2`, `CHs J CH~ (II)` | the drawings, see `\alttext` | p. 191 |

## What the folder contains

- `main.tex` / `main.pdf`: the whole article in reading order (journal line, title, authors, affiliation, Plate 98
  and received lines, author footnote, abstract, all sections with their two footnotes at the marks, the recipe
  list and the soaking-times table as tabulars, Sources of Supply, the five references in `hangpars`, the
  Explanation of Plate 98, the plate page with its header and footer lines, Fig. 1). Compile with
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` in this folder (decomp.sty is here); compiles without
  errors (run twice), 7 pages. Four overfull boxes: three of 0.8 pt from the `\alttext` frames, one of 18 pt in the
  last reference line, cosmetic.
- `figures/fig1.png`: the Plate 98 micrograph, cropped with `tools/crop.py` at the embedded image's exact bbox
  (page 5, 119.33 168.91 505.73 642.67 pt) at **150 dpi**, the half-tone's native resolution (806 × 988 px); 200 dpi
  would only upsample it. `figures/formula1.png`, `formula2.png`: structural formulas (I) and (II) from the page-1
  scan at 300 dpi (page 1, 104 615.5 311 691.3 pt and 340 404 510 460 pt), each with its printed label; in
  formula (I) the footnote separator rule (x 107.5–149.3, y 686.4–687.4 pt), which lies inside the rectangle 60 pt
  left of any formula ink, is painted white. Script: `work/make_figures.py` (re-runnable).
- `tables/table1.csv`: the soaking-times table (p. 193; the paper gives it no number or title).
  `tables/mixture.csv`: the recommended mixture (p. 192), printed as an untitled two-column list, not a numbered
  table; included because it is the paper's key recipe. Both carry the caption context in `#` lines and were
  checked cell by cell against the page.
- `work/`: `datalab/` (the Datalab markdown, its image crops and meta), `tess/` (tesseract text; the `.pgm`
  renders may be deleted), `raw.txt` (the PDF's text layer), `build_main.py` (re-runnable: rebuilds `main.tex`),
  `embed_blocks.py` (one-off, done), `main_summary.tex` (see History), `make_figures.py`, `diff_ocr.py`,
  `ocr_quality.py`, `ink.py`, `check_text.json`, page renders and zoom crops. Scratch except the scripts.

## Figures

No plotted panel in the paper: **0 panels in tiers 1–4, no CSV, no extraction or plotting script, no replot or
compare.py check**. The three images are a micrograph and two formula drawings.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 (Plate 98) | TEM micrograph, thin section of bovine tubercle bacilli in araldite, × 100,000, figure number "1" in the image | – | – | `figures/fig1.png`, native 150 ppi; described in `\alttext` |
| formula (I) | structural formula drawn in text characters (epoxy resin general formula, R and n) | – | – | `figures/formula1.png`; atoms, bonds and SMILES (n = 0, n = 1, repeat unit) in `\alttext` |
| formula (II) | structural formula (diphenyl propane unit R) | – | – | `figures/formula2.png`; SMILES of the divalent unit in `\alttext` |

*Background knowledge, not in the .tex:* formula (I) with R = (II) is the diglycidyl ether of bisphenol A type
resin; the paper does not use those names.

## Text check (`tools/check_text.py` 2026-10-17j)

Command (from this folder):
`python3 -I ../../tools/check_text.py main.tex source/glauert1958.pdf --figure-box 1:104,615.5,311,691.3 --figure-box 1:340,404,510,460`
(the two boxes are the formulas inside the page-1 scan; the page-5 micrograph is an embedded image and is found
automatically; 12 unmatched tokens were counted as in-figure).

| coverage of PDF tokens | without text repeated on ≥ 3 pages | running text (also without in-figure tokens) | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|
| **96.1 %** (2513 PDF tokens, 2425 tex tokens) | **96.1 %** (0 repeated tokens: the running heads differ page to page) | 96.5 % | 98.2 % | 3 runs, 23 tokens | 0 |

The check compares against the PDF's 2003 OCR layer, which is wrong in the places listed above; the page image is
authoritative, so these mismatches are expected and not fixable in the .tex.

- **MISSING ≥ 6 (3 runs):** `j bxo sxc and bzoc z crro` = the OCR's garbling of the journal line (the .tex has the
  real one); `191 192 araldite as embedding medium` = page numbers and running header (left out on purpose);
  `50 50 ethanol araldite araldite less accelerator araldite with accelerator` = the table's row labels, which the
  OCR reads as one run while the tabular has them row by row (all three are in the tabular).
- **MISSING at `--min-run 1` (39 runs, 87 tokens), all explained:** the 23 above; page numbers/running headers
  `193`, `194 araldite as embedding medium`; and OCR garbage for words the .tex has correctly: `tle uninersity`,
  `pr a`, `maal e` ×3, `maalc e`, `by maal ie`, `micro biology`, `al ready`, `amer ica`, `mix ture`, `metha erylate`,
  `demon stradon` (line-end hyphen splits the tool did not join), `aliphafic`, `typkimurium`, `typtdmurium`,
  `diificult`, `bc`, `qc`, `i` (from `I-2`), `t` (from `I t`), `1`, `3` (footnote marks), `specimcns`, `etectron`,
  `1955 i iuxley`, `sowrces of supt ly`, `almqvlst`, `glanert`, `ra ee`, `1 8`, `i 956`, `fio`, `x 103 030`.
- **EXTRA at `--min-run 1` (31 runs, 44 tokens; none ≥ 6), all explained:** the correct words for the garbage above
  (`j biophysic and biochem cytol`, `the university`, `plate`, `s` of 1930's, `maaloe` ×5, `typhimurium` ×2,
  `difficult`, `by`, `be`, `specimens`, `methacrylate`, `electron`, `1956` (OCR: 1955), `sources`, `supply`,
  `demonstration`, `almqvist`, `glauert`, `nature`, `178`, `fig`, `100 000`) and the table's row labels and the
  `1` of `1–2`, which the matcher sees out of order.

Read-through against the page images (SPEC step 4) done for: the bibliographic block, the recipe (10.0, 10.0, 1.0,
0.5 ml.), every cell of the soaking-times table, the five references (bold **178**, italic *Nature* and
*Salmonella typhimurium*, "Almqvist & Wiksell", "Birch-Andersen"), the ° and × signs, the superscript footnote
marks, the italic *n* and *i.e.*/*I.e.*, the em dashes after "medium:", "Specimens." (twice) and "Supply.", the
formula drawings atom by atom, and every number (2 per cent; 15 to 20 per cent; about 10 per cent; 48 hours at
48°C; 15/85; 50/50; 90 per cent; 50°C; 60°C; 0°C; × 100,000).

## Errors and oddities in the paper (kept verbatim)

- Abstract, last sentence: "electron microgram" where "micrograph" is meant (the Conclusions and the plate
  explanation print "micrograph"). Confirmed on a 300-dpi zoom (`work/zz_abstract_end.png`).
- p. 192: "compatability" (sic). British spellings "realised", "colour", "centre" and "stoichiometrical" are as
  printed, not errors.
- The reference list is unnumbered and alphabetical; the text cites by author and year. The soaking-times table has
  no number or title. The plate explanation (caption) is printed on p. 194, before the plate (PDF page 5); the .tex
  keeps that order.

## Not available

Nothing: the paper names no data set, supplement, video or source-data file.

## Known problems

- `figures/fig1.png` is at 150 dpi (native), not the SPEC's 200 dpi, on purpose.
- One 18-pt overfull line in the last reference (cosmetic).
- The hyphens in "three-dimensional" and "glass-stoppered" fall at line ends in the print; they are real hyphens
  and are kept (the tool's dehyphenation may join them when matching; it did not complain).

## History

The verbatim transcription by hand was cut off twice by the API's content filter (2026-10-17 and 2026-10-18;
nothing of those replies survived). A figures/data/summary form was then written (kept as `work/main_summary.tex`;
its `\alttext` blocks and tabulars are what `main.tex` now uses), and Kevin finally chose the tool-first transcript
above, which went through without any block.

## Time

About 55 minutes in the first two runs (reading brief/spec/example, page inspection with zooms, figure crops,
tables, the blocked verbatim attempt and its report), about 20 minutes for the summary form, and about 45 minutes
for the tool-first transcript (build script, proofreading pass over all pages, engine comparison, checks, README).
