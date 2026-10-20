# Decompiling a paper: the spec (oct_17_papers edition)

This is the osmium collection's SPEC (`docs/SPEC.osmium.md`, kept verbatim for reference) adapted to this
folder. Differences from the osmium layout, and nothing else:

- Each paper is a self-contained folder `<key>/` at the collection root. **Its source PDFs live in
  `<key>/source/`** (plus a `SOURCE.txt` saying where and how each was obtained), not in `../papers/`.
- Shared tools are in `tools/` at the collection root, so from inside `<key>/` they are `../tools/`.
  `decomp.sty` is also copied into each `<key>/` so `lualatex main.tex` works there without TEXINPUTS.
- The worked example is `li2024/` here (copied from osmium).
- Keys are `<firstauthor><year>` (lowercase; a letter suffix on collisions). Every paper gets a row in the root
  `README.md` index, its own git commit, and is pushed to the private GitHub repo (binaries via Git LFS, see
  `.gitattributes`). Issues are tracked with beads (`bd`).
- The coordinator (not the decompiling agent) obtains PDFs, with the browser slots where needed.

Everything below is the osmium text with paths rewritten.


This folder holds machine- and human-readable versions of scientific papers. Each paper is "decompiled": its text, tables and figure data are rebuilt
as LaTeX, CSV and Python, so they can be read, searched and re-used without the PDF. Making the
paper easy to ingest is the only goal. Reproducing the PDF's layout is not one.

The source PDFs are in `<key>/source/`. Each decompiled paper goes in `<key>/` here.
`li2024/` is the worked example: look at it (README, main.tex, a CSV and its scripts) before you start.
`<key>/source/` may also hold older `.txt`/`.raw.txt` text extractions; use them if they help.

## Folder layout

```
<key>/
  README.md              citation, DOI, licence, source files, which version the PDF is
                         (publisher's version of record, accepted manuscript, preprint version),
                         what is included or left out, check results, figure table (see below),
                         errors found in the paper, known problems
  main.tex               the article: every word of the main text, in reading order
  supplement.tex         supplementary text, figures and tables (one file per supplement PDF
                         if there are several: supplement.tex, supplement2.tex, ...)
  figures/
    fig1.png             the whole figure rendered from the PDF (tools/crop.py, 200 dpi)
    fig1b.csv            data of one plotted panel
    fig1b.py             re-plots fig1b.csv with matplotlib -> fig1b_replot.png
    fig1b_extract.py     how fig1b.csv was obtained (vector or raster extraction), re-runnable
    fig1b_replot.png
    sfig2a.csv ...       supplementary figures use an s prefix: sfig2.png, sfig2a.csv
  tables/
    table1.csv           every table, also as CSV (stable1.csv for supplementary tables)
  work/                  scratch (page renders, JSON dumps); may be deleted
```

## The .tex files

- Start with `\documentclass{article}` and `\usepackage{decomp}`, and compile with
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` from `<key>/` (decomp.sty is copied there; `TEXINPUTS=../tools:` also works).
  It must compile without errors. Write Unicode directly: μm, °C, ±, ≥, α, ä, č. Use
  `\ce{OsO4}` (mhchem) or `OsO$_4$` for formulas, and LaTeX math for equations.
- **Verbatim, complete, in reading order.** Title, authors, affiliations, the journal/DOI/dates
  block, the abstract, every section, the methods, footnotes, acknowledgments, author
  contributions, competing interests, data and code availability, and the full reference list
  with its original numbering. Do not paraphrase, shorten, modernize or correct. Remove only
  line-end hyphenation. An obvious typo stays, with a `\decompnote{}` if it matters.
- Leave out running headers and footers, page numbers, and publisher boilerplate ("Check for
  updates", reprint and permissions notes, journal ads). Keep the licence statement and the
  received/accepted/published dates.
- Take the citation (authors, title, journal, year, DOI, licence) from the PDF itself, not from the
  task message; if they differ, the PDF wins and the README says so. Old scans often print no
  journal, volume or DOI: take those from `<key>/source/SOURCE.txt` and say so in the README.
- A first or last page shared with another article (or with journal news): leave that text out, say
  so in a `\decompnote{}`, and give the coordinator the rectangle to exclude from the check (below).
- Supplementary figures or tables printed inside the main PDF stay in `main.tex`, at their page,
  named sfigN as usual. A caption that covers several figures is kept once, after the last of them.
- `\textsc` prints upright (DejaVu has no small caps); that is fine.
- Footnotes (affiliations, corresponding author, equal contribution) go right after the author
  list or where they are referenced. Structural headings the paper doesn't print (e.g. a
  "References" heading) are not allowed; use a `\decompnote{}` instead.
- Put `\pdfpage{N}` where page N of the PDF starts (at the first word of that page in reading
  order), so text can be cited by page. In a supplement, put `\sourcefile{<pdf name>}` at the top. Keep everything in a
  supplement, including a publisher cover page and a template title page with its own abstract.
- Reference lists and numbered steps the paper numbers itself: write the numbers as text inside
  `\begin{hangpars} ... \end{hangpars}` (from decomp.sty), not `enumerate`. If you roll your own
  `\everypar{\hangindent=..\hangafter=1}`, end it with `\relax`, or a paragraph starting with a
  digit loses it.
- Citations stay as the paper prints them ("^12", "[12]", "(Smith et al., 2010)"). Don't turn them
  into `\cite`.
- **Your own words go in the decompiler macros only:** `\alttext{}` (figure descriptions),
  `\figuredata{panel}{csv}{py}{provenance}`, and `\decompnote{}` (anything else: a missing part,
  an unreadable symbol, an uncertainty, an OCR correction). Nothing else in the file may be text
  that is not in the paper. `tools/check_text.py` enforces this.
- Tables: write each as a `tabular` (or `longtable`) where it appears, with its caption and
  footnotes verbatim, and also as `tables/tableN.csv` (header row, one row per table row; put the
  caption and footnotes in `#` comment lines at the top). A paper without tables whose key numbers
  sit in the running text may get `tables/text_values.csv` (value, printed wording, page), headed
  as compiled by the decompiler, not a table of the paper.
- Chemical structures: describe every atom, bond, charge and reagent in `\alttext`, with SMILES
  there where the drawing can be read atom by atom. Table cells holding structures become CSV
  columns `<name>_label`, `<name>_smiles`, `<name>_description`. `\ce{}` fails on a prime (′):
  write it outside `\ce`.
- Sideways figures: `\rotatebox[origin=c]{-90}{\includegraphics[width=...]{...}}`
  (`\includegraphics[angle=-90,...,keepaspectratio]` fails with "Division by 0").
- Keep `main.tex` self-contained: no `\input`.

## Figures

Every figure: main figures, Extended Data figures, figure supplements, supplementary figures.
Place it where it appears in the PDF, at the end of the paragraph that spans that point (don't
break a sentence; if that puts a later `\pdfpage{}` marker before an earlier one, that is fine, say so
in a `\decompnote{}`):

```latex
\begin{center}
\includegraphics[width=0.95\linewidth,height=0.55\textheight,keepaspectratio]{figures/fig1.png}
\end{center}
\noindent\textbf{Fig. 1 | Verbatim title.} Verbatim caption, all of it.
\alttext{Panel by panel description (see below).}
\figuredata{b}{figures/fig1b.csv}{figures/fig1b.py}{vector paths in the PDF, exact}
```

(Don't use a `figure` float: long captions break floats.) Crop the figure without its caption
text; the bbox of the embedded image (`page.get_image_info()`) plus a small margin is usually right.
Name panels by their printed letter (fig1b); a panel without a letter gets a position (sfig4top,
sfig4bottom) or, for a single-panel figure, no suffix (sfig2.csv).

### Descriptions (`\alttext`)

Write them for a reader who cannot see the image but wants everything a careful viewer would
take from it. Go panel by panel:
- what kind of image it is (TEM/SEM/SBEM micrograph, light micrograph, photograph, schematic,
  line plot, bar chart, spectrum, map), and the specimen and orientation where it is shown;
- everything printed in the panel: labels, annotations, arrows and what they point at, scale
  bars with their values, colour keys, insets;
- for micrographs: what is visible and how it looks (membranes dark and continuous, myelin
  rings, extraction holes, cracks, staining gradient from rim to core, ...), with positions
  ("upper left", "the arrowhead");
- for plots: axes (quantity, unit, range, linear or log), each series and its key, the shape
  of the data with approximate numbers (peaks, plateaus, crossings, the values at the ends),
  error bars, sample sizes and statistics marks;
- for schematics: the steps, quantities and arrows, transcribed.
Describe what is in the figure and its caption only. Don't add interpretation from elsewhere,
and say when something is hard to make out.

### Data of plotted panels (CSV + plotting code)

Any panel with quantitative axes (line plot, scatter, bars, histogram, spectrum, box plot,
calibrated colour map) gets a CSV, an extraction script and a plotting script. Use the best
source available, in this order, and state it in `\figuredata` and in the CSV header:

1. **source data**: the authors' own data file (eLife source data, Nature source data, a
   supplementary table). Cite the file.
2. **vector**: the plot is drawn as vector paths in the PDF. `tools/vector_dump.py` dumps the
   paths and the text (tick labels) of a page region. Fit the axis mapping from at least two
   ticks per axis (check a third), convert marker centres, line vertices, bar tops and error
   bar ends to data units. This is exact up to the PDF's precision; say so.
3. **digitized**: the plot is a raster image. Work on the embedded image at its native
   resolution (`tools/digitize_common.py`: `embedded_image()` applies the soft mask; frame and
   tick finders, axis fit, per-column trace, `trace_envelope()`, `overlay()`), calibrate on
   the ticks, and extract the series with colour masks (OpenCV) or by locating markers. For
   narrow peaks trace the top and bottom of the line in each pixel column, not one centre
   value, or peak heights come out low. Give the uncertainty in axis units (about one pixel of
   the source image, or more if the image is blurry). Import the helper with
   `sys.path.insert(0, "<abs path to decompiled/tools>")`; that is fine under `python3 -I`.
4. **read by eye**: last resort, when 3 is impossible (tiny, overlapping, low resolution).
   Give a generous uncertainty.

CSV format: `#` comment lines first (figure and panel, what each column is with its unit,
provenance tier and how it was obtained, uncertainty, anything odd), then one header row, then
tidy rows, e.g. `series,x,y,y_err_low,y_err_high`. Use the paper's series names. When an
axis has no numbers ("a.u." without ticks), give that coordinate as the fraction of the axis-box
height (0 = bottom frame, 1 = top frame) and say so; record any unlabelled tick positions. Read
CSVs in the plot scripts with `csv` (skip lines starting with `#`); `np.genfromtxt(names=True)`
mistakes the comment for the header. For a colour
map, a grid CSV (one row per pixel row, or x,y,value triples) sampled at the map's native
resolution and mapped through the colour bar.

The plotting script reads only the CSV and draws the panel with the same axes, scales, ranges
and series (looks don't matter: no need to match fonts or colours exactly). Run it, then check it two ways and
look at both images: draw the extracted points back onto the source image (`overlay()`; for
vector data, plot the points over `crop.py`'s render of the region), and put the original panel
and your re-plot side by side with `tools/compare.py`. Every series, range and scale must match;
fix the extraction until it does. Say in the README that you did these checks.

If the paper names a data set or source-data file (Zenodo, Dryad, figshare, source data) that is
not in `<key>/source/`, list it in the README as the tier-1 source that was not available, and
mention it in your final report.

Videos: if the PDF shows a still with a caption, treat it like a figure; list every video in the
README as not available. A grey or colour map without a colour bar: give the raw grey level (or
RGB) per cell and say plainly that it is uncalibrated. eLife PDFs print only the titles of figure
supplements; their images and legends come from the eLife API (`<key>/source/elife_figure_supplements/`).
The eLife "figures PDF" (figures and figure supplements with legends) goes into `supplement.tex`.
Full-page eLife figures put `\pdfpage` markers out of order; that is expected.

Category axes (evenly spaced labels that are not to scale, e.g. 5, 30, 100, 600 s): give each
point's position and its printed label. A measurement you take from a micrograph (an edge profile,
a width) may go in `figures/<fig>_<what>.csv` with a header saying it is your measurement, the
scale it assumes and where that scale comes from. Markers: the centre of a matched marker is the
centre of the template's ink, not of its box; JPEG colour subsampling shifts thin coloured markers
by about 1 px. NumPy 2 has no `ndarray.ptp`; use `np.ptp`.

Micrographs, photographs and schematics get a description and the PNG only. A paper with no
plotted panels at all gets no CSVs; say so in the README and skip the data checks. A schematic that
is really a table or timeline (protocol steps with times and temperatures) is also transcribed
into `\alttext` or a CSV.

## Checks before you finish

`check_text.py` is at version 2026-10-20a; the coordinator re-runs every check at the end
(`tools/audit.py`, which also OCRs scans afresh as a second opinion). Options for awkward PDFs:
`--pages A-B`, `--exclude P:x0,y0,x1,y1` (ignore another article's text on page P, PDF points),
`--figure-box P:x0,y0,x1,y1` (a figure inside a page scan). Report the options you used, so the
coordinator can put them into `tools/audit_checks.json`. Write a printed superscript used as a degree sign ("4⁰C") as `4\textsuperscript{0}C`.
Don't redirect lualatex's output to `<name>.out`: hyperref writes that file.

1. `lualatex` compiles every .tex without errors (run it twice).
2. `python3 -I ../tools/check_text.py main.tex source/<main>.pdf` (and the same for
   each supplement). Aim for coverage ≥ 98 % of the PDF's tokens once text repeated on 3 or more
   pages (headers, footers, download stamps) is left out; the tool prints both numbers, and a third
   one that also leaves out unmatched text printed inside figures (on an embedded image or among
   vector drawings: axis labels, scheme labels), which belongs in `\alttext`. Report all three. Known
   unavoidable mismatches: Symbol-font glyphs in the text layer (Φ read as "f"), subscripts glued
   to their letter, real hyphens at line ends. Every MISSING run must be
   explained (a header or footer, text inside a figure, boilerplate) and every EXTRA run must be
   fixed (a transcription error) or explained (a scanned PDF whose OCR layer is wrong: the page
   image is authoritative; list these corrections). Put the final numbers and explanations in
   the README.
3. Every plotted panel has CSV + extract script + plot script + replot, checked with
   `compare.py`.
4. Read through main.tex once against the page images for the things the token check can't
   see: equations, subscripts and superscripts, Greek letters, ±, units, table cells,
   minus signs, and the order of the text around figures and boxes.

## Rules

- Work only inside `<key>/`. Don't change other papers' folders, `tools/` or anything else.
- No network and no browser: everything needed is in `<key>/source/`. If a supplement or
  data file the paper mentions is not there, say so in the README; don't fetch it.
- Run Python with `python3 -I`. Available: numpy, scipy, matplotlib, OpenCV (cv2), PIL,
  PyMuPDF (`import pymupdf`), poppler (`pdftotext`, `pdfimages`, `pdftoppm`), tesseract,
  pandoc. Don't pip install anything. If a tool you need is missing, stop and say so.
- Read the PDF pages as images (the Read tool renders PDFs; or render PNGs with
  `tools/render_pages.sh`) as well as their text: the text layer alone misses figures, symbols
  and reading order.
- The README's figure table: one row per figure panel, with type, and for plotted panels the
  CSV and its provenance tier.
