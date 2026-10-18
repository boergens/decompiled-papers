# hayworth2014: decompiled

Kenneth J. Hayworth, Josh L. Morgan, Richard Schalek, Daniel R. Berger, David G. C. Hildebrand, Jeff W. Lichtman.
"Imaging ATUM ultrathin section libraries with WaferMapper: a multi-scale approach to EM reconstruction of neural
circuits." *Frontiers in Neural Circuits* **2014**, 8:68 (Methods Article). DOI
[10.3389/fncir.2014.00068](https://doi.org/10.3389/fncir.2014.00068) (printed on p. 1 and in the citation block on p. 18).
Received 10 April 2014; accepted 05 June 2014; published online 27 June 2014. Edited by Benjamin R. Arenkiel;
reviewed by Julian Budd and Richard J. Weinberg.

The DOI is also confirmed by the verify-sources receipt `vs-20261013-3767fe775b`
(`web/checks/receipts/vs-20261013-3767fe775b.json`, Crossref record matched to this PDF; two more receipts for the
same DOI: `vs-20261013-6dcf06762b`, `vs-20261013-bf6f91c54e`).

**Licence:** © 2014 Hayworth, Morgan, Schalek, Berger, Hildebrand and Lichtman; open access under the Creative
Commons Attribution License (CC BY), as stated on p. 18.

## Source files

| file | what it is |
|---|---|
| `source/hayworth2014.pdf` | the article, 18 pp., **publisher version of record** (Frontiers typesetting, journal header on p. 1, running header and footer on every page; PDF producer Acrobat Distiller 8.0, created 27 June 2014). Copied from `papers/hayworth2014/hayworth2014.pdf`; `papers/hayworth2014/SOURCE.txt` says: "hayworth2014.pdf: https://www.frontiersin.org/articles/10.3389/fncir.2014.00068/pdf (curl, 2026-10-12)". |

Not copied: `papers/hayworth2014/hayworth2014.txt` and `.raw.txt` (earlier text extractions, not used).
The paper has no supplementary material, so there is no `supplement.tex`.

Cited works in our collection (from `decompile_work/manifest.json`): **denk2004** (Denk and Horstmann, 2004,
PLoS Biol. 2:e329). No other reference of this paper is in the manifest.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block, title, authors, affiliations, the
  editor/reviewer/correspondence block (printed in the left margin of p. 1), abstract, keywords, all sections
  (Introduction; Sample preparation; Imaging strategy and workflow; Implementation: WaferMapper; Example data;
  Future directions; Conclusion), Acknowledgments, the 12 references, conflict-of-interest statement, dates,
  citation line, copyright/licence. Figures 1–10 with verbatim captions, a description (`\alttext`) of every
  panel, and Table 1 as a `tabular`.
- `figures/fig1.png` … `fig10.png`: each figure rendered from the PDF at 200 dpi (embedded image bbox + 2 pt).
- `figures/fig8c_values.csv`, `fig8c_extract.py`, `fig8c.py`, `fig8c_replot.png`: the sixteen tile quality values
  printed on the montage of Fig. 8C (see below).
- `tables/table1.csv`: Table 1 (caption and footnote in `#` lines; one row per step, with its group heading).
- `decomp.sty`: copy of the shared macros, so `lualatex -interaction=nonstopmode -halt-on-error main.tex`
  compiles from this folder (run twice). It compiles without errors; the only warnings are ten 0.8 pt overfull
  boxes from the `\alttext` frames.
- `work/`: scratch (page renders, embedded images, zooms, draft text per page, `check.json`, comparison
  image `cmp_fig8c.png`); may be deleted. `work/scripts/` holds the two draft-text helpers I used
  (`draft.py`, `totex.py`: page text in column order with bold/italic markup and line-end hyphens resolved; the
  output was proofread, not used blindly).

## Figures

All ten figures are raster images (one 300 ppi JPEG per figure, 1417 px wide); the pages carry no vector plot
paths (`get_drawings()` finds only the header rule and the Table 1 rules). Image digests are all different (no
repeated plates). **No figure has a plotted panel with quantitative axes**, so there is no tier-1/2/3 data:
the figures are photographs, CAD renderings, schematics, a flow chart, program screenshots and SEM micrographs.

The only numbers printed inside a figure as data are the sixteen tile quality values of Fig. 8C. They are recorded
in `figures/fig8c_values.csv` (**tier 4, read by eye** from the 300 ppi JPEG, helped by a colour mask of the
green/red label pixels, `work/z8c_mask.png`); about half of the readings are marked "probable" with the
alternative reading, because the digits are ~12 px high and JPEG-blurred. `fig8c.py` redraws them as a 4 × 4
grid; I compared it side by side with the original panel (`work/cmp_fig8c.png`, made with `tools/compare.py`)
and looked at both. The screenshots of Fig. 4C show a grey colour key (0–0.9) of the program's correlation map;
it is part of a GUI screenshot, not a data panel, and is described in `\alttext` only.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A | photograph (ATUM on ultramicrotome in chamber) | – | – | |
| Fig. 1B | photograph (side view of ATUM) | – | – | |
| Fig. 1C, 1D | video frames (section collection) | – | – | |
| Fig. 1E | CAD rendering | – | – | |
| Fig. 1F | CAD rendering (zoom on knife boat) | – | – | |
| Fig. 1G | photograph (take-up reel) | – | – | |
| Fig. 1H | photograph (wafer with 10 tape strips) | – | – | |
| Fig. 1I | photograph (wafer box, 20 wafers) | – | – | |
| Fig. 2A | schematic (UTSL terms) | – | – | |
| Fig. 2B | block diagram | – | – | transcribed in `\alttext` |
| Fig. 2C | program screenshot (WaferMapper GUI) | – | – | |
| Fig. 3 | flow chart | – | – | transcribed box by box in `\alttext` |
| Fig. 4A | SEM montage (partial) + optical photograph | – | – | |
| Fig. 4B–D | program screenshots (thresholding, automap) | – | – | Fig. 4C colour key = GUI, not data |
| Fig. 5A | wafer images (mapped + optical) | – | – | |
| Fig. 5B | schematic (overview stack) | – | – | |
| Fig. 5C | 16 wafer image pairs | – | – | |
| Fig. 6A | SEM wafer montages | – | – | caption swaps left/right (see below) |
| Fig. 6B | schematic (overview stack) | – | – | |
| Fig. 6C | 11 SEM wafer montages | – | – | |
| Fig. 7A, 7B | program screenshots | – | – | |
| Fig. 8A | SEM image + schematic of kernel sampling | – | – | |
| Fig. 8B | schematic (3 × 3 contrast patterns) | – | – | all 8 patterns transcribed in `\alttext` |
| Fig. 8C | SEM montage with printed quality values | `figures/fig8c_values.csv` | 4 read by eye | printed numbers, no axes |
| Fig. 9A | program screenshot with zoom overlays | – | – | |
| Fig. 9B | SEM montages (3 sections), scale bar | – | – | |
| Fig. 9C | SEM micrographs (3 sections), scale bar | – | – | |
| Fig. 10A–C | SEM overview / zoom / micrograph, scale bars | – | – | |
| Fig. 10D | SEM image stack (every 10th image) | – | – | |

Tier counts: tier 1: 0, tier 2: 0, tier 3: 0, tier 4: 1 (Fig. 8C printed values; not a plotted panel).

Data sets named by the paper: none. The paper points to the WaferMapper source code and user's manual on a
Google Code SVN server (https://wafermapper.googlecode.com); that is software, not in `papers/`, and Google Code
has been shut down (decompiler's background knowledge, not checked here).

## Text check (`check_text.py` version 2026-10-17j, no options; also run with `--min-run 1`)

`python3 -I -B /home/admin/ephemeral/sep_28__osmium_chemistry/decompiled/tools/check_text.py main.tex source/hayworth2014.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | running text (also without in-figure text) | tex tokens found in PDF |
|---|---|---|---|---|
| `main.tex` | 99.4 % | **99.8 %** (51 repeated tokens) | 99.9 % (2 in-figure tokens) | 100.0 % |

Unmatched (`--min-run 1`):
- REPEATED: the running header "Hayworth et al." (17 pages); the other header/footer text is matched by the
  journal block given once on p. 1.
- MISSING: the page numbers 1–18 of the footer (one token per page), and "atumsem" on p. 17: a real hyphen at a
  line end ("ATUM-/SEM") that the checker's dehyphenation joins.
- EXTRA: "neural circuits" (2 tokens) — the "NEURAL CIRCUITS" text of the journal logo at the top left of p. 1,
  which lies among the vector drawings of the p. 1 header (logo, rule), so the checker counts the PDF side as
  in-figure text (the 2 in-figure tokens) and the transcription as unmatched; it is the paper's text and kept,
  with a note.

Read-through against the page images (step 4) done for: ∼, ×, µ, ±, ®, <, >, en and em dashes, quotes; the
counts of each of these characters in the PDF text layer and in the article text of `main.tex` agree
(e.g. 15 ∼, 23 ×, 16 µ, 4 ®, 18 >). Bold figure references, the italic *en bloc*, *(volume EM)*, *C. elegans*
and the italic journal names in the references were kept. Numbers printed with a math-mode thin space
("17, 000", "500, 000 × 600, 000", "12, 800 × 12, 800") are kept with the space as printed.

Hyphen decisions at line ends (the PDF has 160 line-end hyphens): kept as real hyphens "Tape-collecting",
"re-imaging", "multi-terabyte", "ATUM-SEM", "µm-thick"; joined all others (including "non-/destructive" →
"nondestructive", "pre-/defined" → "predefined", "sub-/region" → "subregion", which are ambiguous; the paper
spells "subregion" unbroken elsewhere).

## Errors and oddities in the paper (kept verbatim)

- **Fig. 6 caption, (A):** "Full wafer SEM montage of wafer 6 (right), same image with automapped positions of all
  sections labeled (left)" — in the printed panel it is the other way round: the unlabelled montage is on the left,
  the labelled one on the right (`\decompnote` in main.tex). (Fig. 5A's caption, optical image right / labelled
  image left, matches its panel.)
- Imaging section (p. 16): "Each title consisted of 12, 800 × 12, 800 pixels" — "tile" is meant (`\decompnote`).
- Fig. 10 caption: "(scale bar = 1 µ)" without the "m" (`\decompnote`).
- Typos kept without notes: "heterogenetity" (p. 4), "such a browsing" (Fig. 2 caption, for "such as"),
  "WaferMaper" (p. 14), "programing" (p. 6), "1 weeks" (p. 10), "Imaged Based Stage Correction" (Fig. 3 caption;
  "image-based stage correction" in the text), "checks its own work -making sure" and "layer IV -mapping out"
  (hyphen for a dash).
- Fig. 1 caption says 162 sections on the wafer of (H) with 10 strips; the handwriting on that wafer reads
  something like "YR1C W017" (hard to read). Not checked further.

## Known limitations of this decompilation

- The Fig. 8C quality values are only partly certain (see the CSV's `reading` column).
- Small GUI text in screenshots (Figs. 2C, 4B–D, 7A, 9A) was transcribed where legible; blurred values are
  marked approximate in `\alttext`.

## Time

About 45 minutes (reading the brief/spec ~5 min, figures and descriptions ~15 min, transcription ~15 min,
checks and README ~10 min).
