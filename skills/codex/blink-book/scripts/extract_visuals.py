#!/usr/bin/env python3
"""Extract original source visuals from a PDF or EPUB and convert them to PNG."""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp"}


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


def slugify(value: str, fallback: str = "visual") -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value[:70] or fallback


def save_png(image_bytes: bytes, out_path: Path) -> tuple[int, int]:
    image_module = require("PIL.Image", "Pillow")
    with image_module.open(io.BytesIO(image_bytes)) as img:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, "PNG")
        return img.size


def extract_epub(source: Path, book_dir: Path) -> list[dict]:
    visuals = []
    visual_dir = book_dir / "visuals"
    work_dir = book_dir / "_work"

    # Map image path to first EPUB document that references it.
    refs: dict[str, str] = {}
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        BeautifulSoup = None

    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        if BeautifulSoup is not None:
            for name in names:
                if Path(name).suffix.lower() not in {".html", ".xhtml", ".htm"}:
                    continue
                soup = BeautifulSoup(archive.read(name), "html.parser")
                for img in soup.find_all("img"):
                    src = img.get("src")
                    if not src:
                        continue
                    candidate = str((Path(name).parent / src).as_posix())
                    refs.setdefault(candidate, name)
                    refs.setdefault(src, name)

        counter = 1
        for name in names:
            if Path(name).suffix.lower() not in IMAGE_EXTS:
                continue
            source_doc = refs.get(name, "")
            source_slug = slugify(Path(source_doc).stem, "epub") if source_doc else "epub"
            out_name = f"{source_slug}-image-{counter:03d}.png"
            out_path = visual_dir / out_name
            try:
                width, height = save_png(archive.read(name), out_path)
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
                    "source_document": source_doc or None,
                    "output": f"visuals/{out_name}",
                    "width": width,
                    "height": height,
                    "status": "ok",
                }
            )
            counter += 1

    write_visual_manifest(work_dir, visuals)
    return visuals


def extract_pdf(source: Path, book_dir: Path) -> list[dict]:
    fitz = require("fitz", "PyMuPDF")
    visuals = []
    visual_dir = book_dir / "visuals"
    work_dir = book_dir / "_work"

    doc = fitz.open(str(source))
    counter = 1
    for page_index in range(len(doc)):
        page = doc[page_index]
        images = page.get_images(full=True)
        for image_index, image in enumerate(images, start=1):
            xref = image[0]
            try:
                extracted = doc.extract_image(xref)
                image_bytes = extracted["image"]
                out_name = f"pdf-visual-{counter:03d}.png"
                out_path = visual_dir / out_name
                width, height = save_png(image_bytes, out_path)
                visuals.append(
                    {
                        "source_anchor": f"PDF page {page_index + 1}",
                        "xref": xref,
                        "output": f"visuals/{out_name}",
                        "width": width,
                        "height": height,
                        "status": "ok",
                    }
                )
                counter += 1
            except Exception as exc:
                visuals.append(
                    {
                        "source_anchor": f"PDF page {page_index + 1}",
                        "xref": xref,
                        "status": "failed",
                        "error": str(exc),
                    }
                )

    write_visual_manifest(work_dir, visuals)
    return visuals


def write_visual_manifest(work_dir: Path, visuals: list[dict]) -> None:
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "visuals-manifest.json").write_text(json.dumps(visuals, indent=2), encoding="utf-8")
    lines = ["# Visuals Manifest", ""]
    for item in visuals:
        if item.get("status") == "ok":
            anchor = item.get("source_document") or item.get("source_anchor") or item.get("source")
            lines.append(f"- `{item['output']}` | {item['width']}x{item['height']} | {anchor}")
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
            f"{ok_count} visuals as PNG.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input PDF or EPUB")
    parser.add_argument("book_dir", type=Path, help="Output book folder, e.g. books/my-book")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    book_dir = args.book_dir.expanduser().resolve()
    book_dir.mkdir(parents=True, exist_ok=True)
    (book_dir / "visuals").mkdir(exist_ok=True)
    (book_dir / "_work").mkdir(exist_ok=True)

    suffix = source.suffix.lower()
    if suffix == ".epub":
        visuals = extract_epub(source, book_dir)
    elif suffix == ".pdf":
        visuals = extract_pdf(source, book_dir)
    else:
        print("Only .epub and .pdf sources are supported by this helper.", file=sys.stderr)
        return 2

    ok_count = sum(1 for item in visuals if item.get("status") == "ok")
    print(f"Extracted {ok_count} visuals into {book_dir / 'visuals'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
