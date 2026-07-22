#!/usr/bin/env python3
"""Create a source map and bounded text chunks for a PDF or EPUB book."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


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


@dataclass
class Chunk:
    id: str
    title: str
    kind: str
    source_anchor: str
    word_count: int
    text_path: str


def slugify(value: str, fallback: str = "section") -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value[:80] or fallback


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def clean_text(text: str) -> str:
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n\n".join(lines)


def write_text(path: Path, title: str, body: str) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = clean_text(body)
    path.write_text(f"# {title}\n\n{text}\n", encoding="utf-8")
    return word_count(text)


def epub_manifest(source: Path, book_dir: Path) -> list[Chunk]:
    ebooklib = require("ebooklib")
    epub = __import__("ebooklib.epub", fromlist=["epub"])
    bs4 = require("bs4", "beautifulsoup4")
    BeautifulSoup = bs4.BeautifulSoup

    book = epub.read_epub(str(source))
    chunks: list[Chunk] = []
    chapter_dir = book_dir / "_work" / "chapter-text"

    index = 1
    for item in book.get_items():
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        soup = BeautifulSoup(item.get_content(), "html.parser")
        heading = soup.find(["h1", "h2", "h3"])
        title = clean_text(heading.get_text(" ")) if heading else Path(item.get_name()).stem
        text = soup.get_text("\n")
        if word_count(text) < 20:
            continue
        chunk_id = f"chapter-{index:03d}-{slugify(title)}"
        rel_path = Path("_work") / "chapter-text" / f"{chunk_id}.md"
        count = write_text(book_dir / rel_path, title, text)
        chunks.append(
            Chunk(
                id=chunk_id,
                title=title,
                kind="epub-document",
                source_anchor=item.get_name(),
                word_count=count,
                text_path=str(rel_path),
            )
        )
        index += 1

    return chunks


def pdf_manifest(source: Path, book_dir: Path, pages_per_chunk: int) -> list[Chunk]:
    pdfplumber = require("pdfplumber")
    chunks: list[Chunk] = []
    chunk_dir = book_dir / "_work" / "page-text"

    with pdfplumber.open(str(source)) as pdf:
        total_pages = len(pdf.pages)
        for start in range(0, total_pages, pages_per_chunk):
            end = min(start + pages_per_chunk, total_pages)
            parts = []
            for page_number in range(start, end):
                text = pdf.pages[page_number].extract_text(x_tolerance=1, y_tolerance=3) or ""
                parts.append(f"## PDF page {page_number + 1}\n\n{text}")
            title = f"PDF pages {start + 1}-{end}"
            chunk_id = f"pdf-pages-{start + 1:04d}-{end:04d}"
            rel_path = Path("_work") / "page-text" / f"{chunk_id}.md"
            count = write_text(book_dir / rel_path, title, "\n\n".join(parts))
            chunks.append(
                Chunk(
                    id=chunk_id,
                    title=title,
                    kind="pdf-page-range",
                    source_anchor=f"pages {start + 1}-{end}",
                    word_count=count,
                    text_path=str(rel_path),
                )
            )
    return chunks


def write_source_map(book_dir: Path, source: Path, source_type: str, chunks: Iterable[Chunk]) -> None:
    work = book_dir / "_work"
    work.mkdir(parents=True, exist_ok=True)
    chunks = list(chunks)
    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_name": source.name,
        "source_type": source_type,
        "chunk_count": len(chunks),
        "total_words": sum(chunk.word_count for chunk in chunks),
        "chunks": [asdict(chunk) for chunk in chunks],
    }
    (work / "source-map.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    lines = [
        "# Source Map",
        "",
        f"- Source type: {source_type}",
        f"- Source name: {source.name}",
        f"- Chunk count: {len(chunks)}",
        f"- Total extracted words: {data['total_words']}",
        "",
        "## Chunks",
        "",
    ]
    for chunk in chunks:
        lines.append(
            f"- `{chunk.id}` | {chunk.word_count} words | {chunk.source_anchor} | "
            f"[text]({chunk.text_path}) | {chunk.title}"
        )
    (work / "source-map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    log = work / "extraction-log.md"
    if not log.exists():
        log.write_text("# Extraction Log\n\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as handle:
        handle.write(
            f"- {datetime.now().isoformat(timespec='seconds')}: created source map "
            f"for {source.name} with {len(chunks)} chunks.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input PDF or EPUB")
    parser.add_argument("book_dir", type=Path, help="Output book folder, e.g. books/my-book")
    parser.add_argument("--pages-per-chunk", type=int, default=10, help="PDF pages per text chunk")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    book_dir = args.book_dir.expanduser().resolve()
    book_dir.mkdir(parents=True, exist_ok=True)
    (book_dir / "_work").mkdir(exist_ok=True)

    suffix = source.suffix.lower()
    if suffix == ".epub":
        chunks = epub_manifest(source, book_dir)
        source_type = "epub"
    elif suffix == ".pdf":
        chunks = pdf_manifest(source, book_dir, args.pages_per_chunk)
        source_type = "pdf"
    else:
        print("Only .epub and .pdf sources are supported by this helper.", file=sys.stderr)
        return 2

    write_source_map(book_dir, source, source_type, chunks)
    print(f"Created source map with {len(chunks)} chunks in {book_dir / '_work'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
