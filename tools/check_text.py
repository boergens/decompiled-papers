#!/usr/bin/env python3
"""Check a decompiled .tex against its source PDF(s): is every word there, and nothing added?

Usage:
    python3 -I check_text.py <file.tex> <source.pdf> [<more.pdf> ...] [--min-run N] [--json out.json]
                             [--pages A-B] [--drop-line-numbers]
                             [--exclude P:x0,y0,x1,y1 ...] [--figure-box P:x0,y0,x1,y1 ...]

--reference-text F uses the plain-text file F (an OCR or publisher text) instead of the PDF's text layer (scans without one);
--pages A-B checks only those pages of each PDF (a supplement printed inside the main PDF);
--drop-line-numbers ignores bare numbers in the outer 15 % of the page width (preprint line numbers);
--exclude P:x0,y0,x1,y1 ignores PDF text whose line centre lies in that rectangle of page P (1-based,
  PDF points, origin top left), e.g. the neighbouring article sharing the first or last page;
--figure-box P:x0,y0,x1,y1 marks that rectangle of page P as a figure area, for scanned pages where
  the figures are part of the page image and cannot be found automatically. Both may be repeated;
  with several PDFs, P counts pages across all of them in order.

Both sides are reduced to a stream of lower-case word tokens (accents and
punctuation dropped, letters and digits split, ligatures and line-end hyphens
undone). The decompiler's own additions (\\alttext, \\decompnote, \\figuredata,
comments, the preamble) are removed from the .tex first.

Reports:
  coverage   share of the PDF's tokens found in the .tex, in order or as a
             moved block (e.g. a caption placed elsewhere);
  REPEATED   text missing on 3 or more pages (running headers, footers, stamps), reported once;
  in-figure  unmatched text printed inside figures (on an embedded image, or within a cluster of
             vector drawings: labels, axes, schemes) is counted
             separately and not listed; describe it in \\alttext instead;
  MISSING    runs of >= N PDF tokens found nowhere in the .tex, with the PDF page;
             these are text you left out (fine for running headers, page
             numbers, publisher boilerplate, text inside figures; say so in the
             paper's README) or dropped by mistake (fix it);
  EXTRA      runs of >= N .tex tokens found nowhere in the PDF: words that are
             not the paper's. These are usually transcription errors. Fix them,
             or move your own text into \\decompnote / \\alttext.
"""
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher

import pymupdf

# Bump on every change; it is printed with the results so READMEs can say which version they used.
# 2026-10-17i: ignore \\localother too.
# 2026-10-17h: drop page-sized merged figure boxes (strip-scanned pages).
# 2026-10-17g: ignore the \\localcopy / \\externalonly collection markers.
# 2026-10-17f: optional --pages and --drop-line-numbers (defaults unchanged).
# 2026-10-17e: keep \\item[...] labels; drop \\hspace*{}, \\name=<length> assignments. FROZEN for this run.
# 2026-10-17d: repeats need >= 2 word tokens per 5-gram; verbatim/lstlisting tokenised literally.
# 2026-10-17c: superscript split, joined/split word matching, figure-area text, number-blind repeats.
# 2026-10-17j: read glyphs without a Unicode map as their codes (TEXT_CID_FOR_UNKNOWN_UNICODE; before, such
#              PDFs came out as U+FFFD, e.g. low1998); Springer "Ligature" font W/X/V/Y = fi/fl/ff/ffi;
#              1-bit page images >= 50 % of the page are scans, not figures; short repeated lines
#              (footers with page numbers) count as repeated; \\rotatebox/\\scalebox arguments
#              dropped; --exclude and --figure-box.
VERSION = "2026-10-20b"

LIG = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "ß": "ss", "æ": "ae", "œ": "oe",
       "ø": "o", "ł": "l", "đ": "d", "ð": "d", "þ": "th", "ı": "i"}
TOKEN = re.compile(r"[a-z]+|[0-9]+")


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(LIG.get(c, c) for c in s if not unicodedata.combining(c))
    return s.lower()


def tokens(s):
    return TOKEN.findall(norm(s))


def merge_boxes(boxes, gap):
    out = [pymupdf.Rect(b) for b in boxes]
    changed = True
    while changed:
        changed = False
        res = []
        for b in out:
            for i, o in enumerate(res):
                if b.x0 <= o.x1 + gap and o.x0 <= b.x1 + gap and b.y0 <= o.y1 + gap and o.y0 <= b.y1 + gap:
                    res[i] = pymupdf.Rect(min(o.x0, b.x0), min(o.y0, b.y0), max(o.x1, b.x1), max(o.y1, b.y1))
                    changed = True
                    break
            else:
                res.append(pymupdf.Rect(b))
        out = res
    return out


def vector_figure_boxes(page, gap=6.0, min_paths=15, min_area=3000.0):
    """Bounding boxes of clusters of vector drawings (plots, schematics): drawings closer than
    `gap` pt are merged; clusters with at least `min_paths` paths and `min_area` pt^2 count."""
    rects = []
    for d in page.get_drawings():
        r = pymupdf.Rect(d["rect"])
        if r.width > 0.9 * page.rect.width:
            continue  # full-width rules
        rects.append([r.x0, r.y0, r.x1, r.y1, 1])
    merged = True
    while merged:
        merged = False
        out = []
        for r in rects:
            for o in out:
                if r[0] <= o[2] + gap and o[0] <= r[2] + gap and r[1] <= o[3] + gap and o[1] <= r[3] + gap:
                    o[0], o[1], o[2], o[3] = min(o[0], r[0]), min(o[1], r[1]), max(o[2], r[2]), max(o[3], r[3])
                    o[4] += r[4]
                    merged = True
                    break
            else:
                out.append(list(r))
        rects = out
    return [pymupdf.Rect(r[:4]) for r in rects
            if r[4] >= min_paths and (r[2] - r[0]) * (r[3] - r[1]) >= min_area]


LIGATURE_FONT = str.maketrans({"W": "fi", "X": "fl", "V": "ff", "Y": "ffi"})


FIG_MARGIN = 20.0  # pt around each figure box within which unmatched text counts as printed inside the figure


def pdf_tokens(paths, pages_sel=None, drop_line_numbers=False, exclude=None, figure_box=None):
    """Tokens of the PDFs in reading order, the page of each, whether it is text printed inside a
    figure (a line whose centre lies on an embedded image that is not a page scan), and a line id."""
    toks, pages, infig, lineid = [], [], [], []
    exclude, figure_box = exclude or {}, figure_box or {}
    nline = 0
    gpage = 0  # page number counted across all PDFs, for --exclude / --figure-box
    for path in paths:
        doc = pymupdf.open(path)
        for i, page in enumerate(doc):
            gpage += 1
            if pages_sel and not (pages_sel[0] <= i + 1 <= pages_sel[1]):
                continue
            area = page.rect.width * page.rect.height
            bpc = {im[0]: im[4] for im in page.get_images(full=True)}
            figs = []
            for im in page.get_image_info(xrefs=True):
                r = pymupdf.Rect(im["bbox"])
                big = r.width * r.height >= 0.8 * area
                scan = r.width * r.height >= 0.5 * area and bpc.get(im.get("xref")) == 1  # bilevel page scan
                if not big and not scan and r.width > 20 and r.height > 20:
                    figs.append(r)
            figs += vector_figure_boxes(page)
            figs = merge_boxes(figs, gap=12.0)  # panels of one figure, with the labels between them
            # A page scanned as many image strips merges into one page-sized box: that is the page,
            # not a figure, so drop it (otherwise every unmatched word counts as figure text).
            figs = [r for r in figs if r.width * r.height < 0.8 * area]
            figs += figure_box.get(gpage, [])
            d = page.get_text("dict", flags=pymupdf.TEXT_DEHYPHENATE | pymupdf.TEXT_CID_FOR_UNKNOWN_UNICODE)
            for block in d["blocks"]:
                for line in block.get("lines", []):
                    # A space between spans of clearly different size, so superscripts and
                    # subscripts (affiliation letters, citation numbers) don't glue onto words.
                    main = max((sp["size"] for sp in line["spans"]), default=0)
                    text = ""
                    for sp in line["spans"]:
                        small = sp["size"] < 0.85 * main
                        st = sp["text"].translate(LIGATURE_FONT) if sp["font"] == "Ligature" else sp["text"]
                        text += (" " + st + " ") if small else st
                    t = tokens(text + " ")
                    x0, y0, x1, y1 = line["bbox"]
                    if drop_line_numbers and text.strip().isdigit() and (
                            x1 < 0.15 * page.rect.width or x0 > 0.85 * page.rect.width):
                        continue  # margin line numbers (preprints)
                    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                    if any(r.x0 <= cx <= r.x1 and r.y0 <= cy <= r.y1 for r in exclude.get(gpage, [])):
                        continue
                    # in-figure: the line's box overlaps a figure box grown by FIG_MARGIN (axis labels and rotated
                    # y labels sit up to ~17 pt outside the raster; measured on xu2021 p.2, pesce2022 p.3, 2026-10-20)
                    f = any(x0 <= r.x1 + FIG_MARGIN and x1 >= r.x0 - FIG_MARGIN and y0 <= r.y1 + FIG_MARGIN and y1 >= r.y0 - FIG_MARGIN for r in figs)
                    toks += t
                    pages += [f"{path.rsplit('/', 1)[-1]} p.{i + 1}"] * len(t)
                    infig += [f] * len(t)
                    lineid += [nline] * len(t)
                    nline += 1
    return toks, pages, infig, lineid


def drop_braced(s, cmd, nargs):
    """Remove \\cmd{...}{...} (nargs balanced groups), with optional [..] args."""
    out, i = [], 0
    pat = re.compile(r"\\" + cmd + r"(?![A-Za-z])")
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:])
            break
        out.append(s[i:m.start()])
        j = m.end()
        for _ in range(nargs):
            while j < len(s) and s[j] in " \t\n":
                j += 1
            if j < len(s) and s[j] == "[":
                j = s.find("]", j) + 1
                while j < len(s) and s[j] in " \t\n":
                    j += 1
            if j >= len(s) or s[j] != "{":
                break
            depth = 0
            while j < len(s):
                if s[j] == "\\":
                    j += 2
                    continue
                if s[j] == "{":
                    depth += 1
                elif s[j] == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
        i = j
    return "".join(out)


# letter accents (\\c, \\t, \\b, ...) must be followed by "{" or a space, otherwise
# \\ce{..}, \\textsuperscript, \\textbf, \\bigskip were eaten as accent + letter ("e", "extsuperscript", ...).
ACCENT = re.compile(r"\\(?:[`'^\"~=.]\s*|[uvHcdbtk](?:\s+|(?=\{)))\{?([A-Za-z])\}?")


def tex_text(path):
    s = open(path, encoding="utf-8").read()
    if "\\begin{document}" in s:
        s = s.split("\\begin{document}", 1)[1]
    s = s.split("\\end{document}", 1)[0]
    verb = []
    def keep(m):
        verb.append(m.group(2))
        return f" DECOMPVERBATIM{len(verb) - 1} "
    s = re.sub(r"\\begin\{(verbatim\*?|lstlisting|Verbatim)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}", keep, s, flags=re.S)
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = re.sub(r"\\(hspace|vspace)\*?\s*\{[^}]*\}", " ", s)
    # drop tabular column specs and \\[2pt]-style line-break options before the generic rules
    s = re.sub(r"\\begin\{(tabular|longtable|array)\*?\}(\[[^\]]*\])?\{(?:[^{}]|\{[^{}]*\})*\}", " ", s)
    s = re.sub(r"\\\\\s*\[[^\]]*\]", " ", s)
    s = re.sub(r"\\cmidrule\s*(\([^)]*\))?\s*\{[^}]*\}", " ", s)
    for cmd, n in [("alttext", 1), ("decompnote", 1), ("figuredata", 4), ("sourcefile", 1),
                   ("pdfpage", 1), ("localcopy", 1), ("localother", 1), ("externalonly", 2), ("includegraphics", 1), ("label", 1), ("ref", 1),
                   ("eqref", 1), ("hypertarget", 1),
                   ("setlength", 2), ("addtolength", 2), ("vspace", 1), ("hspace", 1),
                   ("begin", 1), ("end", 1), ("multicolumn", 2), ("multirow", 2),
                   ("cmidrule", 1), ("rule", 2), ("raisebox", 1), ("resizebox", 2), ("rotatebox", 1), ("scalebox", 1),
                   ("bibitem", 1), ("thebibliography", 1)]:
        s = drop_braced(s, cmd, n)
    s = re.sub(r"\\href\s*\{[^{}]*\}", " ", s)  # \href{url}{text}: keep the text
    s = re.sub(r"\\url(?![A-Za-z])", " ", s)  # \url{...}: keep the URL, it is printed
    s = re.sub(r"\\item\s*\[([^\]]*)\]", r" \1 ", s)  # \item[1.]: the label is printed
    s = re.sub(r"\\[A-Za-z]+\s*=\s*-?[0-9.]+\s*(em|ex|pt|cm|mm|in|bp)\b", " ", s)  # \hangindent=3em
    s = re.sub(r"\\[A-Za-z]+\s*=\s*-?[0-9]+\b", " ", s)  # \hangafter=1
    s = ACCENT.sub(r"\1", s)
    s = s.replace("\\ss", "ss").replace("~", " ").replace("\\\\", " ")
    s = re.sub(r"\\(ce|textsubscript|textsuperscript|emph|textbf|textit|textrm|textsc|mathrm|mathit|text|mbox|section|subsection|subsubsection|paragraph|caption|title|author|footnote|item|textsf|texttt|underline|mathbf|mathsf|operatorname|SI|si|num)(?![A-Za-z])\*?(\[[^\]]*\])?", " ", s)  # (?![A-Za-z]) so \\sigma is not read as \\si + "gma"
    s = re.sub(r"\\[A-Za-z]+\*?", " ", s)  # remaining command names (\alpha, \times, \mu ...)
    s = re.sub(r"DECOMPVERBATIM(\d+)", lambda m: " " + verb[int(m.group(1))] + " ", s)
    return s


def runs(flags, min_run):
    out, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            if i - start >= min_run:
                out.append((start, i))
            start = None
    return out


def ngrams(t, n):
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}


def present_elsewhere(seg, grams, n):
    if len(seg) < n:
        return False
    g = [tuple(seg[i:i + n]) for i in range(len(seg) - n + 1)]
    return sum(x in grams for x in g) >= 0.9 * len(g)


def main(argv):
    min_run, jout, files, pages_sel, dln = 6, None, [], None, False
    exclude, figure_box = {}, {}
    reference_text = None  # --reference-text <file>: a plain-text reference (e.g. Google Patents text, a fresh OCR) used instead of the PDF's text layer
    i = 0
    while i < len(argv):
        if argv[i] in ("--exclude", "--figure-box"):
            pg, _, xy = argv[i + 1].partition(":")
            r = pymupdf.Rect(*[float(v) for v in xy.split(",")])
            (exclude if argv[i] == "--exclude" else figure_box).setdefault(int(pg), []).append(r)
            i += 2; continue
        if argv[i] == "--min-run":
            min_run = int(argv[i + 1]); i += 2; continue
        if argv[i] == "--pages":
            a, _, b = argv[i + 1].partition("-"); pages_sel = (int(a), int(b or a)); i += 2; continue
        if argv[i] == "--drop-line-numbers":
            dln = True; i += 1; continue
        if argv[i] == "--json":
            jout = argv[i + 1]; i += 2; continue
        if argv[i] == "--reference-text":
            reference_text = argv[i + 1]; i += 2; continue
        files.append(argv[i]); i += 1
    if len(files) < 2:
        sys.exit(__doc__)
    tex, pdfs = files[0], files[1:]
    if reference_text:
        rt = open(reference_text, encoding="utf-8", errors="replace").read()
        p = tokens(norm(rt)); pages = [1] * len(p); infig = [False] * len(p); lineid = list(range(len(p)))
        print(f"reference text: {reference_text} ({len(p)} tokens) used instead of the PDF text layer")
    else:
        p, pages, infig, lineid = pdf_tokens(pdfs, pages_sel, dln, exclude, figure_box)
        if not p:
            print("WARNING: the PDF has no text layer (0 tokens): OCR it, or pass --reference-text <file> with an OCR or publisher text to check against")
    t = tokens(tex_text(tex))
    sm = SequenceMatcher(None, p, t, autojunk=False)
    p_ok, t_ok = [False] * len(p), [False] * len(t)
    for a, b, size in sm.get_matching_blocks():
        if size >= 2 or (size == 1 and len(p[a]) > 3):
            for k in range(size):
                p_ok[a + k] = True
                t_ok[b + k] = True
    N = 5
    tg, pg = ngrams(t, N), ngrams(p, N)
    missing, extra = [], []
    # mark moved text 5-gram by 5-gram instead of all-or-nothing per unmatched run.
    # A moved block (affiliations, a caption placed elsewhere) is usually glued to an adjacent running
    # header/footer in the unmatched run, which pushed the whole run below the 90 % threshold and
    # reported the moved block as MISSING.
    for ok, seq, grams in ((p_ok, p, tg), (t_ok, t, pg)):
        for a, b in runs([not x for x in ok], 1):
            for k in range(max(0, a - N + 1), b):
                if tuple(seq[k:k + N]) in grams:
                    for j in range(k, min(k + N, len(seq))):
                        ok[j] = True
    # Words split on one side and joined on the other ("reduced osmium" vs "reducedosmium" from a
    # real hyphen at a line end, "formamide a" vs "formamidea" from a glued superscript): match an
    # unmatched token against two adjacent unmatched tokens of the other side.
    for ok_a, seq_a, ok_b, seq_b in ((p_ok, p, t_ok, t), (t_ok, t, p_ok, p)):
        joined = {}
        for k in range(len(seq_b) - 1):
            if not ok_b[k] and not ok_b[k + 1]:
                joined.setdefault(seq_b[k] + seq_b[k + 1], []).append(k)
        for k, x in enumerate(seq_a):
            if not ok_a[k] and joined.get(x):
                j = joined[x].pop()
                ok_a[k] = ok_b[j] = ok_b[j + 1] = True
    # Text missing on 3 or more pages is almost always a running header, footer or download
    # stamp. Find it 5-gram by 5-gram with numbers blanked (page numbers differ), report each
    # such text once, and give the coverage without it as well.
    from collections import defaultdict
    blank = ["#" if x.isdigit() else x for x in p]
    gram_pages = defaultdict(set)
    def wordy(g):  # at least two word tokens: runs of bare numbers (tick labels) are not headers
        return sum(x != "#" for x in g) >= 2
    for k in range(len(p) - N + 1):
        g = tuple(blank[k:k + N])
        if not any(p_ok[k:k + N]) and wordy(g):
            gram_pages[g].add(pages[k])
    rep = [False] * len(p)
    for k in range(len(p) - N + 1):
        g = tuple(blank[k:k + N])
        if not any(p_ok[k:k + N]) and wordy(g) and len(gram_pages[g]) >= 3:
            for j in range(k, k + N):
                rep[j] = True
    # Short lines (running footers like "PRECISION ENGINEERING 58") are too short for the 5-grams:
    # a whole unmatched line of <= 8 tokens whose number-blanked text recurs on 3 or more pages.
    line_toks = defaultdict(list)
    for k, li in enumerate(lineid):
        line_toks[li].append(k)
    line_pages = defaultdict(set)
    for li, ks in line_toks.items():
        g = tuple(blank[k] for k in ks)
        if len(ks) <= 8 and any(x != "#" for x in g) and not any(p_ok[k] for k in ks):
            line_pages[g].add(pages[ks[0]])
    for li, ks in line_toks.items():
        g = tuple(blank[k] for k in ks)
        if len(line_pages.get(g, ())) >= 3 and not any(p_ok[k] for k in ks):
            for k in ks:
                rep[k] = True
    rep_tokens = sum(rep)
    repeated = defaultdict(set)
    for a, b in runs(rep, 1):
        repeated[" ".join(blank[a:b])[:300]].add(pages[a])
    fig_missing = sum(1 for x, r, f in zip(p_ok, rep, infig) if not x and not r and f)
    for a, b in runs([not x and not r and not f for x, r, f in zip(p_ok, rep, infig)], min_run):
        missing.append({"where": pages[a], "n": b - a, "text": " ".join(p[a:b])[:400]})
    for a, b in runs([not x for x in t_ok], min_run):
        ctx = " ".join(t[max(0, a - 6):a])
        extra.append({"after": ctx, "n": b - a, "text": " ".join(t[a:b])[:400]})
    repeated_list = sorted(({"pages": len(w), "text": txt} for txt, w in repeated.items()),
                           key=lambda r: -r["pages"])
    cov = sum(p_ok) / max(1, len(p))
    prec = sum(t_ok) / max(1, len(t))
    print(f"check_text.py version {VERSION}")
    print(f"{tex}: PDF tokens {len(p)}, tex tokens {len(t)}")
    print(f"coverage {cov:.1%} of PDF tokens found in tex; {prec:.1%} of tex tokens found in PDF")
    cov_x = sum(p_ok) / max(1, len(p) - rep_tokens)
    print(f"coverage without text repeated on >= 3 pages ({rep_tokens} tokens): {cov_x:.1%}")
    cov_r = sum(p_ok) / max(1, len(p) - rep_tokens - fig_missing)
    print(f"coverage of the running text (also without {fig_missing} unmatched tokens printed inside figures): {cov_r:.1%}")
    print(f"REPEATED (missing on >= 3 pages; '#' = any number): {len(repeated_list)} text(s), {rep_tokens} tokens")
    for r in repeated_list[:30]:
        print(f"  [{r['pages']} pages] {r['text']}")
    print(f"MISSING runs >= {min_run}: {len(missing)} ({sum(m['n'] for m in missing)} tokens)")
    for m in missing:
        print(f"  [{m['where']}] ({m['n']}) {m['text']}")
    print(f"EXTRA runs >= {min_run}: {len(extra)} ({sum(m['n'] for m in extra)} tokens)")
    for m in extra:
        print(f"  (after '{m['after']}') ({m['n']}) {m['text']}")
    if jout:
        json.dump({"version": VERSION, "tex": tex, "pdfs": pdfs, "coverage": cov, "coverage_without_repeated": cov_x, "coverage_running_text": cov_r, "unmatched_in_figure_tokens": fig_missing, "precision": prec,
                   "missing": missing, "repeated": repeated_list, "extra": extra}, open(jout, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
