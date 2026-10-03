#!/usr/bin/env python3
"""Extract EPUB images unchanged; extract PDF images as PNG."""

from __future__ import annotations

import argparse
import io
import json
import hashlib
import math
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".svg"}


def require(module_name: str, install_name: str | None = None):
    try:
        return __import__(module_name)
    except ImportError:
        package = install_name or module_name
        print(
            f"Missing dependency: {package}. Install with: "
            f"python3 -m pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        raise SystemExit(2)


def save_png(image_bytes: bytes, out_path: Path) -> tuple[int, int]:
    image_module = require("PIL.Image", "Pillow")
    with image_module.open(io.BytesIO(image_bytes)) as img:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, "PNG")
        return img.size


def extract_epub(source: Path, book_dir: Path, write_markdown: bool = True) -> list[dict]:
    visuals = []
    visual_dir = book_dir / "visuals"
    visual_dir.mkdir(parents=True, exist_ok=True)
    work_dir = book_dir / "_work"

    with zipfile.ZipFile(source) as archive:
        names = [name for name in archive.namelist() if Path(name).suffix.lower() in IMAGE_EXTS]
        filenames = [Path(name).name for name in names]
        if len(filenames) != len(set(filenames)):
            raise ValueError("EPUB images have duplicate filenames; cannot preserve names in visuals/.")
        for name in names:
            out_name = Path(name).name
            out_path = visual_dir / out_name
            try:
                image_bytes = archive.read(name)
                out_path.write_bytes(image_bytes)
            except Exception as exc:
                visuals.append(
                    {
                        "source": name,
                        "status": "failed",
                        "error": str(exc),
                    }
                )
                continue
            visuals.append(
                {
                    "source": name,
                    "output": f"visuals/{out_name}",
                    "bytes": len(image_bytes),
                    "status": "ok",
                }
            )

    write_visual_manifest(work_dir, visuals, image_format="in original formats", write_markdown=write_markdown)
    return visuals


def extract_pdf(source: Path, book_dir: Path, write_markdown: bool = True,
                regions_file: Path | None = None) -> list[dict]:
    """Render reviewed figure regions, including vector paths and text labels."""
    fitz = require("fitz", "PyMuPDF")
    regions_file = regions_file or book_dir / "_work" / "pdf-visual-regions.json"
    if not regions_file.is_file():
        raise ValueError(
            "PDF extraction requires a reviewed region map: supply --pdf-regions or "
            "_work/pdf-visual-regions.json with source_sha256, dpi and regions "
            "(one-based page, rect [x0, y0, x1, y1] in PDF points, filename). "
            "Inventory every source figure and image; exclude body text and page decoration."
        )
    plan = json.loads(regions_file.read_text(encoding="utf-8"))
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if plan["source_sha256"] != source_hash:
        raise ValueError("PDF region map does not match the source file.")
    dpi = plan.get("dpi", 300)
    if not isinstance(dpi, int) or dpi <= 0:
        raise ValueError("PDF rendering dpi must be a positive integer.")
    regions = plan["regions"]
    if not regions:
        raise ValueError("PDF region map contains no images.")
    visuals = []
    visual_dir = book_dir / "visuals"
    visual_dir.mkdir(parents=True, exist_ok=True)

    with fitz.open(str(source)) as doc:
        filenames = set()
        for region in regions:
            name = region["filename"]
            if Path(name).name != name or not name.endswith(".png") or name in filenames:
                raise ValueError(f"Invalid or duplicate image filename: {name}")
            filenames.add(name)
            page_number = region["page"]
            if not isinstance(page_number, int) or not 1 <= page_number <= len(doc):
                raise ValueError(f"Invalid PDF page: {page_number}")
            rect = region["rect"]
            if len(rect) != 4 or not all(math.isfinite(value) for value in rect):
                raise ValueError(f"Invalid image rectangle: {name}")
            clip = fitz.Rect(rect)
            if clip.is_empty or not doc[page_number - 1].rect.contains(clip):
                raise ValueError(f"Image rectangle is empty or outside the page: {name}")

        # Refuse incomplete maps rather than silently dropping known source figures.
        for page in doc:
            page_regions = [region for region in regions if region["page"] == page.number + 1]
            for block in page.get_text("blocks"):
                match = re.match(r"^\s*fig(?:ure)?\.?\s+([A-Za-z0-9]+[.\-]\d+)\b", block[4], re.I)
                if not match:
                    continue
                figure = match.group(1).lower().replace("-", ".")
                if not any(str(region.get("figure", "")).lower().replace("-", ".") == figure
                           and fitz.Rect(region["rect"]).contains(fitz.Rect(block[:4]))
                           for region in page_regions):
                    raise ValueError(f"Missing figure {figure} and its caption on PDF page {page.number + 1}.")
            for image in page.get_image_info():
                if not any(fitz.Rect(region["rect"]).contains(fitz.Rect(image["bbox"]))
                           for region in page_regions):
                    raise ValueError(f"Uncovered image on PDF page {page.number + 1}: {image['bbox']}")

        for region in regions:
            page = doc[region["page"] - 1]
            item = {
                "source_anchor": f"PDF page {region['page']}",
                "source_sha256": source_hash,
                "page": region["page"],
                "rect": region["rect"],
                "figure": region.get("figure"),
                "dpi": dpi,
                "output": f"visuals/{region['filename']}",
            }
            try:
                pixmap = page.get_pixmap(dpi=dpi, clip=fitz.Rect(region["rect"]), alpha=False)
                pixmap.save(str(book_dir / item["output"]))
                item.update(width=pixmap.width, height=pixmap.height, status="ok")
            except Exception as exc:
                item.update(status="failed", error=str(exc))
            visuals.append(item)

    write_visual_manifest(book_dir / "_work", visuals, write_markdown=write_markdown)
    return visuals


def write_visual_manifest(work_dir: Path, visuals: list[dict], image_format: str = "as PNG",
                          write_markdown: bool = True) -> None:
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "visuals-manifest.json").write_text(json.dumps(visuals, indent=2), encoding="utf-8")
    if not write_markdown:
        with (work_dir / "extraction-log.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"timestamp": datetime.now().isoformat(timespec="seconds"),
                                     "extracted": sum(item.get("status") == "ok" for item in visuals),
                                     "failed": sum(item.get("status") == "failed" for item in visuals),
                                     "image_format": image_format}) + "\n")
        return
    lines = ["# Visuals Manifest", ""]
    for item in visuals:
        if item.get("status") == "ok":
            anchor = item.get("source_document") or item.get("source_anchor") or item.get("source")
            size = f"{item['bytes']} bytes" if "bytes" in item else f"{item['width']}x{item['height']}"
            lines.append(f"- `{item['output']}` | {size} | {anchor}")
        else:
            lines.append(f"- FAILED | {item.get('source') or item.get('source_anchor')} | {item.get('error')}")
    (work_dir / "visuals-manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    log = work_dir / "extraction-log.md"
    if not log.exists():
        log.write_text("# Extraction Log\n\n", encoding="utf-8")
    ok_count = sum(1 for item in visuals if item.get("status") == "ok")
    with log.open("a", encoding="utf-8") as handle:
        handle.write(
            f"- {datetime.now().isoformat(timespec='seconds')}: extracted "
            f"{ok_count} visuals {image_format}.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input PDF or EPUB")
    parser.add_argument("book_dir", type=Path, help="Output book folder, e.g. books/my-book")
    parser.add_argument("--no-markdown", action="store_true",
                        help="Write a JSON manifest and JSONL log without creating or modifying Markdown")
    parser.add_argument("--pdf-regions", type=Path, help="Reviewed PDF figure-region JSON map")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    book_dir = args.book_dir.expanduser().resolve()
    book_dir.mkdir(parents=True, exist_ok=True)
    (book_dir / "visuals").mkdir(exist_ok=True)
    (book_dir / "_work").mkdir(exist_ok=True)

    suffix = source.suffix.lower()
    if suffix == ".epub":
        visuals = extract_epub(source, book_dir, write_markdown=not args.no_markdown)
    elif suffix == ".pdf":
        visuals = extract_pdf(source, book_dir, write_markdown=not args.no_markdown,
                              regions_file=args.pdf_regions)
    else:
        print("Only .epub and .pdf sources are supported by this helper.", file=sys.stderr)
        return 2

    ok_count = sum(1 for item in visuals if item.get("status") == "ok")
    print(f"Extracted {ok_count} visuals into {book_dir / 'visuals'}")
    return 1 if any(item.get("status") == "failed" for item in visuals) else 0


if __name__ == "__main__":
    raise SystemExit(main())
