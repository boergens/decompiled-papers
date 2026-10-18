#!/usr/bin/env python3
"""Dump the vector drawing commands and text spans inside a region of a PDF page.

Usage:
    python3 -I vector_dump.py <pdf> <page> [x0 y0 x1 y1] [--out file.json]

<page> is 1-based. The region is in PDF points (72 per inch), origin top left,
the same frame PyMuPDF uses; omit it for the whole page. Use --png to also
write a 4x render of the region for orientation.

Output (JSON):
  "paths": one entry per drawing: stroke/fill colour, line width, bounding box,
           and "items": each segment as ["l", [x,y], [x,y]] (line),
           ["c", p0, p1, p2, p3] (Bezier), ["re", [x0,y0,x1,y1]] (rectangle),
           ["qu", [4 points]] (quad).
  "text":  each text span with its bbox, origin and font size: tick labels,
           axis titles and legends. Fit the axis calibration from these.

Vector plots give the authors' plotted values exactly (up to the precision the
PDF stores, usually 0.01 pt or better). Convert page coordinates to data with a
linear (or log) map fitted to two or more tick marks per axis, and keep that
conversion script next to the CSV so it can be re-run.
"""
import json
import sys

import pymupdf


def pt(p):
    return [round(p.x, 3), round(p.y, 3)]


def main(argv):
    out = None
    png = False
    args = []
    i = 0
    while i < len(argv):
        if argv[i] == "--out":
            out = argv[i + 1]
            i += 2
            continue
        if argv[i] == "--png":
            png = True
            i += 1
            continue
        args.append(argv[i])
        i += 1
    if len(args) not in (2, 6):
        sys.exit(__doc__)
    doc = pymupdf.open(args[0])
    page = doc[int(args[1]) - 1]
    clip = pymupdf.Rect(*map(float, args[2:6])) if len(args) == 6 else page.rect

    paths = []
    for d in page.get_drawings():
        r0 = d["rect"]
        # Compare bounds directly: Rect.intersects() is False for zero-width or zero-height
        # rects, which would drop every horizontal and vertical line (axes, ticks, error bars).
        if r0.x1 < clip.x0 or r0.x0 > clip.x1 or r0.y1 < clip.y0 or r0.y0 > clip.y1:
            continue
        items = []
        for it in d["items"]:
            kind = it[0]
            if kind == "l":
                items.append(["l", pt(it[1]), pt(it[2])])
            elif kind == "c":
                items.append(["c"] + [pt(p) for p in it[1:5]])
            elif kind == "re":
                r = it[1]
                items.append(["re", [round(r.x0, 3), round(r.y0, 3), round(r.x1, 3), round(r.y1, 3)]])
            elif kind == "qu":
                q = it[1]
                items.append(["qu", [pt(q.ul), pt(q.ur), pt(q.lr), pt(q.ll)]])
        r = d["rect"]
        paths.append({
            "stroke": d.get("color"),
            "fill": d.get("fill"),
            "width": d.get("width"),
            "dashes": d.get("dashes"),
            "closePath": d.get("closePath"),
            "bbox": [round(r.x0, 3), round(r.y0, 3), round(r.x1, 3), round(r.y1, 3)],
            "items": items,
        })

    text = []
    for block in page.get_text("dict", clip=clip)["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                if not span["text"].strip():
                    continue
                b = span["bbox"]
                text.append({
                    "text": span["text"],
                    "bbox": [round(v, 2) for v in b],
                    "origin": [round(v, 2) for v in span["origin"]],
                    "size": round(span["size"], 2),
                    "dir": [round(v, 3) for v in line["dir"]],
                })

    images = []
    for info in page.get_image_info():
        r = pymupdf.Rect(info["bbox"])
        if not (r.x1 < clip.x0 or r.x0 > clip.x1 or r.y1 < clip.y0 or r.y0 > clip.y1):
            images.append({"bbox": [round(v, 2) for v in r], "width": info["width"], "height": info["height"]})

    result = {
        "pdf": args[0],
        "page": int(args[1]),
        "page_size": [page.rect.width, page.rect.height],
        "clip": [clip.x0, clip.y0, clip.x1, clip.y1],
        "n_paths": len(paths),
        "paths": paths,
        "text": text,
        "raster_images": images,
    }
    s = json.dumps(result, indent=1)
    if out:
        with open(out, "w") as f:
            f.write(s)
        print(f"{len(paths)} paths, {len(text)} text spans, {len(images)} raster images -> {out}")
    else:
        print(s)
    if png:
        target = (out or "region") .rsplit(".", 1)[0] + ".png"
        page.get_pixmap(clip=clip, matrix=pymupdf.Matrix(4, 4)).save(target)
        print("render ->", target)


if __name__ == "__main__":
    main(sys.argv[1:])
