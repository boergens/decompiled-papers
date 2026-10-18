# mason1976: decompiled

Robert J. Mason, Jean Nellenbogen, and John A. Clements. "Isolation of disaturated phosphatidylcholine with
osmium tetroxide." *Journal of Lipid Research* Volume 17, 1976, *Notes on Methodology*, pp. 281–284.
Manuscript received 18 August 1975; accepted 2 February 1976. Cardiovascular Research Institute, University
of California Medical Center, San Francisco. DOI [10.1016/S0022-2275(20)36986-8](https://doi.org/10.1016/S0022-2275(20)36986-8).

Authors, title, journal, volume, year, pages and dates are printed in the PDF (pages 281–284 in the footers)
and agree with the task message. The DOI is **not printed on the pages**; it is in the PDF metadata (Subject:
"Journal Lipid Research, 17 (1976) 281-284. doi:10.1016/S0022-2275(20)36986-8") and in `SOURCE.txt`. The
issue number is not printed.

**Licence:** "This is an Open Access article under the CC BY license." This line is added by the publisher
as real text below the footer of p. 1 (the only licence statement in the PDF). `SOURCE.txt`: ScienceDirect,
open archive, "View PDF" in browser slot 0, 2026-10-17.

## Local and external

**In the local collection**
- Source files:
  - `papers/mason1976/1-s2.0-S0022227520369868-main.pdf` – 4 pp., scan of the printed journal pages
  - `papers/mason1976/SOURCE.txt` – fetch note
- Cited works decompiled here: korn1967 (`decompiled/korn1967/`), riemersma1968 (`decompiled/riemersma1968/`)

**External pull needed** (not on this machine)
- Nothing besides the references: the paper names no supplement, data set or source-data file (footnote 3 cites "unpublished observations").
- All other cited references: 23 entries in the reference list (1–25) without a [local: …] tag.

## Source files (`../../papers/mason1976/`)

| file | what it is |
|---|---|
| `1-s2.0-S0022227520369868-main.pdf` | 4 pp., **scan of the printed journal pages** (publisher's printed version, re-issued by Elsevier: PDF made 2003, modified 2020 with iTextSharp, which added the CC BY line). Pp. 1, 2, 4: one 1000 dpi bilevel CCITT image each; p. 3 (Table 2 and the Fig. 1 photograph): one 300 dpi greyscale JPEG. The text layer is OCR (embedded TimesNewRoman/Arial/Courier subsets). The upper half of p. 1 is blank in the scan (the article starts mid-page in the journal; whatever was above it was blanked). |
| `SOURCE.txt` | where the PDF came from. |

## Contents

- `main.tex` / `main.pdf`: the whole paper in reading order: footer line (given once), title, authors,
  affiliation, footnotes 1–2 (placed after the author list), Summary, key words, introduction, Methods
  (with Table 1 where it is printed, at the top of p. 2), Results and discussion (Table 2, footnote 3, Fig. 1
  with caption and `\alttext`), the grant note, received/accepted dates, the 25 references, and the CC BY line
  (printed on p. 1 below the footer; placed at the end, noted in the file). Left out: the repeated page
  footers and page numbers, and the journal's "JLR" end-mark glyph (noted).
- `figures/fig1.png`: the TLC photograph with its lane letters, 200 dpi (`tools/crop.py`, page 3, box
  316 314 562 556 pt). The embedded page image is 300 ppi.
- `tables/table1.csv`, `tables/table2.csv`: Tables 1 and 2 with caption and footnotes in `#` lines;
  Table 1's "mean ± SD" cells are split into mean and sd columns. Rows of Table 2 sum to 100.1, 99.7 and
  100.0 % (my check; "tr" counted as 0).
- **No plotted panels, so no figure CSVs.** Fig. 1 is a photograph of a TLC plate (no axes). For orientation,
  `work/lanes.py` measures the band positions on the embedded 300 ppi image (per-lane brightness profile,
  as fraction of the photo height from its bottom edge, about ±0.02); those numbers are in the `\alttext`.
  They are not Rf values: the plate's origin and solvent front are not marked.
- `work/`: scratch (page renders at 150 and 400 dpi, zooms, `zoom.py`, `lanes.py`, `check.json`, LaTeX log).
  Can be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex`. Compiles without
errors (run twice); a few overfull lines (Table 1 is slightly wider than the text block; long chemical names).

## The method as printed (quick reference; my arrangement, the paper's numbers)

| step | as printed | page |
|---|---|---|
| lipid extraction | chloroform–methanol 2:1 (v/v), filter, 0.1 M KCl phase split, Folch wash (19) | 1–2 |
| OsO₄ stock | OsO₄ (Electron Microscopy Sciences) in CCl₄, 100 mg/ml, dark, 4°C; "stable for at least two years" | 2 |
| reaction | 1 mg lipid, evaporated, redissolved in 0.5 ml CCl₄ containing 3.1 mg OsO₄; "darkens, presumably as osmium dioxide is formed (15)"; 15 min (reaction "complete in the time necessary to evaporate the sample") | 2 |
| column | evaporate, redissolve in chloroform–methanol 20:1; 0.8 g neutral alumina (100–200 mesh, Biorad, activated 1 hr at 110°C) in a 9-in Pasteur pipette on glass wool | 2 |
| elution | 10 ml chloroform–methanol 20:1 (neutral lipids), then 5 ml chloroform–methanol–7 M NH₄OH 70:30:2 (disaturated PC); ≈0.8 ml/min; "A dark residue remains at the top of the column" / "the black band should stay at the top" | 2 |
| result | recovery 90.7 ± 2.8 % and 92.5 ± 1.2 % (Table 1); 90.3 ± 3.1 % over 71 tissue extracts; >99 % saturated fatty acids (N = 30); TLC spot 93.9 ± 1.5 % of plate phosphorus (N = 3) | 2 |
| variants | chloroform–methanol 1:1 → recovery 75 %; acetic acid elutes excess phosphorus, black material and fatty acids; TLC on silica H with chloroform–methanol–7 M NH₄OH 70:30:3.5 for low-disaturated samples | 3–4 |

**Stoichiometry (my own arithmetic, not in the paper):** 3.1 mg OsO₄ (M ≈ 254.2 g/mol) is ≈ 12.2 μmol per
1 mg of total lipid, i.e. 31 μl of the 100 mg/ml stock. For a phospholipid of M ≈ 750–800 g/mol, 1 mg is
≈ 1.3 μmol, so OsO₄ is in roughly 9-fold molar excess per lipid molecule, enough for several double bonds each
(the paper says "One molecule of osmium tetroxide reacts with each double bond"). The molar masses are my
background knowledge.

## Figures

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 | photograph of a TLC plate under UV (lanes A–F) | – | – | band positions measured for the `\alttext` only (`work/lanes.py`) |
| Table 1 | table | `tables/table1.csv` | – | transcribed |
| Table 2 | table | `tables/table2.csv` | – | transcribed |

Plotted panels per tier: tier 1: 0, tier 2: 0, tier 3: 0, tier 4: 0.

## Text check (`tools/check_text.py`, version 2026-10-17f)

| | value |
|---|---|
| PDF tokens / tex tokens | 2981 / 2869 |
| coverage of PDF tokens | 95.9 % |
| coverage without text repeated on ≥ 3 pages (0 tokens) | 95.9 % |
| coverage of the running text (in-figure unmatched tokens left out: the tool found 0) | 95.9 % |
| tex tokens found in PDF | 96.9 % |
| MISSING runs ≥ 6 / ≥ 1 | 4 (43 tokens: 3 table runs, 1 lane-letter run) / 54 (123 tokens) |
| EXTRA runs ≥ 6 / ≥ 1 | 4 (35 tokens) / 46 (90 tokens) |

Every unmatched token is explained (`--min-run 1`); all are OCR problems, page furniture or tool artefacts:

- **Tables 1 and 2 (≈ 50 MISSING / ≈ 45 EXTRA tokens; three of the four MISSING runs ≥ 6 and all four EXTRA runs ≥ 6):** the OCR reads the table in a
  different cell order (column by column, header words split, "Prepara- tion") and garbles cells ("±" →
  "f"/"fr"/"2", "16:0" → "16:O", "16:1" → "16:l", "tr" → "t f", "14:0ᵇ" → "14:@"). Transcribed from the image.
- **Fig. 1 lane letters "A B C D E F" (6 tokens):** text in the photograph, described in `\alttext`. (The tool
  doesn't count them as in-figure, because every page is one full-page image.)
- **Page numbers 281–284 (4 tokens):** footers, left out.
- **Line-end hyphens dropped by the OCR** (word split in two): "isolat ing", "evapo rated", "chromatog raphy",
  "disatu rated", "hy droxide", "chloro form"; and spaced letters "o u r", "phosphatidylcho 1 ine".
- **OCR errors corrected against the page images** (MISSING = OCR text, EXTRA = my correction): superscript
  footnote marks 1, 2, 3 and table marks a, b, c (dropped or read as "'", "*", "@"); "8- lo" → 8–10;
  "type I1" → type II; "( 1 1)" → (11); "KC1" → KCl; "20:l" → 20:1; "pg" → μg (4×); "1-naphthalene" read as
  "l-"; "5 2 %" → ≤2%; ">IO%" → >10%; "C 10%" → <10%; "f"/"k" → ± (3×); "Februaq" → February; "0." → O.
  (Privett, Kuksis, Renkonen, Nutter: 4×); "182-135" → 132–135 (ref. 8); "Invavt" and "Inuest" → Invest.
  (refs 10, 15); "[ l , 2-14Cz]" → [1, 2-¹⁴C₂] (ref. 11); "5 1 1-524" → 511–524; "Biofhys. ilctu." →
  Biophys. Acta. (ref. 18); "chromatograph y.1. Bid." → chromatography. J. Biol. (ref. 20); "lung 11." →
  lung II. (ref. 21); "phosphatidylcholinewas" and similar run-together words split.
- **"166 669 675" (ref. 4, 3 tokens), MISSING and EXTRA at once:** the OCR puts "166: 669-675." in a separate
  text block, and the tool's moved-block matching doesn't pick up a 3-token block. Same text on both sides.
  This is a tool artefact.

Leaving out the table cells, lane letters and page numbers, ≈ 98 % of the PDF's tokens are matched. The rest
is OCR noise.

Read-through against the page images (step 4) done for: all table cells and footnote marks, ±, ≤/</>, °C,
μg, "v/v" ratios (2:1, 20:1, 70:30:2, 70:30:3.5, 100:50:14:7, 15:4), ¹⁴C and ³H superscripts and the C₂
subscript in ref. 11, en dashes in page ranges and in solvent names (chloroform–methanol), the em dash in
"Aquasol ...—water", italic journal names and bold volumes in the references, and ref. 18's partly italic title.

## Errors and oddities in the paper (kept verbatim)

- Three slightly different figures for the purity of the eluate: Summary "94%"; text "93.9 ± 1.5% (N = 3) of
  the phosphorus recovered from the plate"; Fig. 1 caption "94.9% of the phosphorus in lane D is in the
  phosphatidylcholine area". They may refer to different measurements; the paper doesn't say.
- Text: "The recoveries were 90% with 16 samples of rat lung"; Table 1's osmium rows are N = 10 at 90.7 % and
  N = 6 at 92.5 % (weighted mean ≈ 91.4 %, my arithmetic).
- Ref. 18: "and fixation of unsaturated" printed in italic (typesetting slip; noted in main.tex).
- Ref. 15: "Stoekenius"; the usual spelling is Stoeckenius (my background knowledge, not checked against the
  cited paper). "Nellenbogen" (second author) is reproduced as printed; I couldn't check it.
- "The limits of the resolution ... is 98%" (grammar, as printed).
- Fig. 1, from the image: lane D's single spot sits at about the height of lane A's highest bright standard
  band and of the upper part of lane C's region (positions in `\alttext`). The figure doesn't label which
  standard band is which.
