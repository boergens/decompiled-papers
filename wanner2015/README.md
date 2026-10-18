# wanner2015: decompiled

A.A. Wanner, M.A. Kirschmann & C. Genoud. "Challenges of microtome-based serial block-face scanning
electron microscopy in neuroscience." *Journal of Microscopy* **259**(2), 137–142 (2015).
DOI [10.1111/jmi.12244](https://doi.org/10.1111/jmi.12244) (printed on p. 1).
Received 15 September 2014; accepted 11 February 2015. Friedrich Miescher Institute for Biomedical Research, Basel.

**DOI check:** verify-sources receipts `vs-20261013-b51672bfc9` (also `-30bc8ce460`, `-325b0de8d3`, `-63cba7f5e6`,
`-5e0f32bfcd`, `-7b5ce5c3f1`, cited in the whitepaper's References) resolved the DOI at Crossref (Wanner, Kirschmann,
Genoud; J. Microsc. 259(2):137–142, 2015; not retracted) and matched it to this exact PDF (same SHA-256,
`63685e08…8d65`).

**Licence:** open access under the Creative Commons Attribution License (CC BY), "© 2015 The Authors / Journal of
Microscopy © 2015 Royal Microscopical Society", as printed in the p. 1 footer. A p. 1 footnote says the copyright
line was changed on June 17, 2015 after original online publication.

**Version:** publisher's version of record (Wiley typesetting, journal page numbers 137–142, PhotinaMT fonts,
PDF created 2015-07-09, after the copyright-line change), born-digital with a usable text layer. Not a scan.

## Source files

| file | what it is |
|---|---|
| `source/wanner2015.pdf` | the article, 6 pp., copied from `papers/wanner2015/wanner2015.pdf`. `papers/wanner2015/SOURCE.txt`: "Fetched 2026-10-13 by the lead session (oct-12-epoxy-cutting) from NCBI's PMC Open Access bucket: https://pmc-oa-opendata.s3.amazonaws.com/PMC4745002.1/PMC4745002.1.pdf (%PDF checked)." |

`papers/wanner2015/` also holds `wanner2015.txt`, an earlier text extraction (not used, not copied). The paper has
no supplement and names no data set, source data or video.

**Cited works in our collection** (keys from `decompile_work/manifest.json`): `denk2004` (Denk & Horstmann 2004,
PLoS Biol.), `hayworth2014` (Hayworth et al. 2014, Front. Neural Circuits), `titze2013` (Titze & Denk 2013,
J. Microsc. 250).

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block, title, authors, affiliation, the p. 1
  footnotes (copyright-line change, correspondence) and the p. 1 copyright/licence footer (placed after the
  author block, noted in the file), key words, Summary, the four sections, the Conclusion and the 41 references (unnumbered, alphabetical, as printed).
  `\pdfpage{N}` markers at the first word of each page in reading order.
- `figures/fig1.png`, `figures/fig2.png`: the two figures rendered at 200 dpi (the native resolution of both
  embedded JPEGs) from the embedded-image bbox plus a 3 pt margin, without caption.
- `decomp.sty`: copied from the osmium `tools/`, so `lualatex -interaction=nonstopmode -halt-on-error main.tex`
  compiles from this folder.
- `work/`: scratch (page renders, 600 dpi zooms of Fig. 1, check JSON, `scripts/draft.py` which dumped the
  text layer with font styles to find italics/bold). May be deleted.
- No `tables/`: the paper has no tables. No CSVs: see Figures.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (run twice): no errors, 6 overfull-box
warnings from long URLs and unbreakable lines.

## Figures

Neither figure has quantitative axes, so there are **no plotted panels, no CSVs and no data checks**
(`vector_dump.py`: 0 vector paths on pp. 4–5; each figure is one embedded 200 ppi JPEG; image digests differ, no
duplicate). Every panel has an `\alttext` description.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A | schematic: resin box with sectioned pyramid, planes labelled z = n −1 … n+2 | – | – | |
| Fig. 1B1 | schematic: 6 unaligned tiles with a magnified overlap showing matched feature dots (7 arrows) | – | – | caption calls it (B) |
| Fig. 1B2 | schematic: the 6 tiles after registration, continuous blue outline | – | – | caption calls it (B) |
| Fig. 1C | schematic: three stacked tile mosaics with blue outlines of increasing size | – | – | |
| (Fig. 1D) | – | – | – | described in the caption, **not printed** |
| Fig. 2 | 3D rendering: consolidated neuron skeletons (6 mitral cells red, 8 interneurons blue) over an SBEM image plane, translucent blobs, 10 µm scale bar | – | – | single panel |

## Text check (`check_text.py` version 2026-10-17j, no options)

`python3 -I -B /home/admin/ephemeral/sep_28__osmium_chemistry/decompiled/tools/check_text.py main.tex source/wanner2015.pdf`

| measure | value |
|---|---|
| coverage of PDF tokens (raw) | 97.2 % (4647 PDF tokens, 4742 tex tokens) |
| without text repeated on ≥ 3 pages (58 tokens) | **98.5 %** |
| also without unmatched in-figure text (0 tokens) | 98.5 % |
| tex tokens found in PDF | 94.9 % |
| MISSING runs ≥ 6 | 2 (13 tokens): the odd-page running header "CHALLENGES OF SBEM IN NEUROSCIENCE 139/141" (on 2 pages only, so the repeat filter misses it) |
| EXTRA runs ≥ 6 | 18 (186 tokens), all explained below |

Explanation of everything unmatched (`--min-run 1`: 42 MISSING runs / 71 tokens, 36 EXTRA runs / 242 tokens):

- **Glued text-layer lines (all 18 EXTRA runs ≥ 6 and most short ones).** In tightly justified lines the PDF's
  text layer has no space characters, so the checker reads a whole line as one token
  ("thesemchambersputteringathinconductivelayeraftereach", "tbstoragespaceafterimagepreprocessing", …) that
  cannot match the spaced words of `main.tex`. I checked all 40 glued tokens of 12+ letters: every one is a
  letter-for-letter substring of `main.tex` (with markup removed), so these are a text-layer artefact, not
  transcription errors. (pdftotext's layout analysis puts the spaces back; PyMuPDF's does not.)
- **Repeated / boilerplate:** page footer "© 2015 The Authors / Journal of Microscopy © 2015 Royal Microscopical
  Society, 259, 137–142" (pp. 2–6), even-page header "A.A. WANNER *ET AL.*" + page number, odd-page header
  "CHALLENGES OF SBEM IN NEUROSCIENCE" + page number (pp. 3, 5); left out on purpose.
- **"c" (7 × 1 token):** the © sign is set as a "C" plus a combining enclosing circle in the text layer; `main.tex`
  writes ©, which is not a token.
- **"re search" (p. 1), "ham precht" (p. 6):** line-end hyphens ("Re-search" in the correspondence footnote,
  "Ham-precht" in Maco et al. 2013) that the checker did not join; `main.tex` has "Research", "Hamprecht".
- Real hyphens at line ends kept as hyphens in `main.tex` (the paper uses the hyphenated form elsewhere or it is
  a compound): tape-collecting, labour-intensive, block-face, single-beam, centimetre-sized,
  osmium-thiocarbohydrazide-osmium, maximum-a-posteriori, As-rigid-as-possible.

Read-through against the page images (step 4) done for: superscripts (pixel⁻¹, s⁻¹, mm², 10¹⁴), ×, <, >, µm, en
dashes in ranges, italics (*et al.*, *in situ*, *en bloc*, *in silico*, *x*, *y*, *z*-direction, journal names),
bold volume numbers in the references (Lowe 2004's "60" is not bold in the paper; kept), paragraph breaks, and the
text order around both figures (Fig. 1 after the paragraph spanning pp. 3–4; Fig. 2 after the paragraph that
begins p. 5 under the figure, before the right column).

## Errors and oddities in the paper (kept verbatim)

- **Fig. 1 caption describes a panel (D)** ("Tiles are stitched into a mosaic optimizing the global overlap for each
  section") that is **not printed**; the printed panels are (A), (B1), (B2), (C), and the caption's (B) covers
  B1 and B2. Flagged with `\decompnote` in `main.tex`.
- "OTO (osmium-thiocarbohydrazide-osmium, rOTO …": the parenthesis after OTO is never closed; "lead
  citrate/asparte" (aspartate meant). Flagged with `\decompnote`.
- Smaller slips left without notes: "This allows to reliable cut thousands" (p. 1), "allows now to scan" ("now"
  twice, p. 2), "results in a significantly reduction" (p. 3), "electrodense molecules. (Martell et al., 2012)."
  (full stop before the citation, p. 3).
- Lowe (2004) (SIFT) is cited among software "for computer-assisted, semiautomated large-scale annotation and
  segmentation" (p. 5); as printed.
- Reference Hayworth et al. (2014): "Front Neural Circ. 68, 1–18". *Not from this PDF:* the collection's fetch
  note for `hayworth2014` gives the DOI 10.3389/fncir.2014.00068, i.e. volume 8, article 68; "68" in the volume
  position looks like the article number.
- Reference Eberle et al. (2015) has no volume or pages ("J Microsc."), as printed.

## Known problems

- None affecting content. The odd-page running header slips past the checker's repeat filter (it appears on only
  2 pages), as the brief predicts.

## Time

About 25 minutes.
