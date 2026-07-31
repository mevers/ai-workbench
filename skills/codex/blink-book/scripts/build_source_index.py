#!/usr/bin/env python3
"""Create a deterministic index of source chunks and named-heading candidates."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


MARKER_RE = re.compile(r"^(Mechanism|The Solution):\s*(.*)$", re.IGNORECASE)
PAGE_RE = re.compile(r"^## (PDF page|Page) \d+", re.IGNORECASE)


def heading_at(lines: list[str], index: int, initial: str) -> str:
    parts = [initial.strip()] if initial.strip() else []
    for line in lines[index + 1 : index + 7]:
        text = line.strip()
        if PAGE_RE.match(text):
            continue
        if not text or text.startswith("#"):
            break
        if len(" ".join(parts + [text])) > 140:
            break
        parts.append(text)
    return " ".join(parts)


def page_anchor_at(lines: list[str], index: int, fallback: str) -> str:
    for line in reversed(lines[: index + 1]):
        match = PAGE_RE.match(line.strip())
        if match:
            return line.strip().removeprefix("## ")
    return fallback


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book_dir", type=Path, help="Blink Book output folder")
    args = parser.parse_args()
    book_dir = args.book_dir.expanduser().resolve()
    work_dir = book_dir / "_work"
    source_map_path = work_dir / "source-map.json"
    if not source_map_path.exists():
        parser.error(f"Missing source map: {source_map_path}")

    source_map = json.loads(source_map_path.read_text(encoding="utf-8"))
    candidates: list[dict[str, str]] = []
    lines = ["# Source Index", "", "## Chunks", "", "| Chunk | Source anchor | Text file |", "| --- | --- | --- |"]

    for chunk in source_map["chunks"]:
        text_path = work_dir.parent / chunk["text_path"]
        relative_path = text_path.relative_to(book_dir)
        work_relative_path = text_path.relative_to(work_dir)
        lines.append(f"| {chunk['id']} | {chunk['source_anchor']} | [{relative_path.name}]({work_relative_path}) |")
        if not text_path.exists():
            continue
        chunk_lines = text_path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(chunk_lines):
            match = MARKER_RE.match(line.strip())
            if not match:
                continue
            label = heading_at(chunk_lines, index, match.group(2))
            candidates.append(
                {
                    "kind": match.group(1).lower(),
                    "label": label or match.group(1),
                    "chunk_id": chunk["id"],
                    "source_anchor": page_anchor_at(chunk_lines, index, chunk["source_anchor"]),
                    "text_path": str(relative_path),
                }
            )

    lines.extend(["", "## Named-heading candidates", ""])
    if candidates:
        lines.extend(["| Type | Candidate | Source anchor |", "| --- | --- | --- |"])
        for candidate in candidates:
            lines.append(
                f"| {candidate['kind']} | {candidate['label']} | {candidate['source_anchor']} |"
            )
    else:
        lines.append("No named-heading candidates were found. Review the table of contents and headings manually.")

    lines.extend(
        [
            "",
            "## Use",
            "",
            "This is a deterministic discovery aid, not the source structure itself. Build `source-structure.md` from this index, the table of contents, introduction, conclusion, and source reading.",
        ]
    )
    (work_dir / "source-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (work_dir / "source-index.json").write_text(
        json.dumps({"candidates": candidates}, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Created source index with {len(candidates)} named-heading candidates in {work_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
