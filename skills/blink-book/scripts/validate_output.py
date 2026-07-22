#!/usr/bin/env python3
"""Validate the folder structure and links for a Blink Book curriculum."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def local_target(base: Path, raw: str) -> Path | None:
    target = raw.split("#", 1)[0].strip()
    if not target or "://" in target or target.startswith("mailto:"):
        return None
    return (base / target).resolve()


def has_prev_next(text: str, index: int, count: int) -> bool:
    has_prev = "Previous:" in text
    has_next = "Next:" in text
    if count == 1:
        return True
    if index == 1:
        return has_next
    if index == count:
        return has_prev
    return has_prev and has_next


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book_dir", type=Path, help="Book output folder")
    args = parser.parse_args()
    book_dir = args.book_dir.expanduser().resolve()

    errors: list[str] = []
    required = ["metadata.yaml", "overview.md", "review.md", "quizzes", "visuals", "_work"]
    for name in required:
        if not (book_dir / name).exists():
            errors.append(f"Missing required path: {name}")

    key_files = sorted(book_dir.glob("key-idea-*.md"))
    if not key_files:
        errors.append("No key-idea-*.md files found")

    for idx, path in enumerate(key_files, start=1):
        text = path.read_text(encoding="utf-8")
        expected_quiz = book_dir / "quizzes" / f"{path.stem}-comprehension.md"
        if str(expected_quiz.relative_to(book_dir)) not in text and expected_quiz.name not in text:
            errors.append(f"{path.name}: missing link to {expected_quiz.relative_to(book_dir)}")
        if not expected_quiz.exists():
            errors.append(f"{path.name}: linked quiz file missing: {expected_quiz.relative_to(book_dir)}")
        if "## Source Basis" not in text:
            errors.append(f"{path.name}: missing Source Basis section")
        if not has_prev_next(text, idx, len(key_files)):
            errors.append(f"{path.name}: missing expected previous/next navigation")

    markdown_files = [book_dir / "overview.md", book_dir / "review.md", *key_files]
    markdown_files.extend(sorted((book_dir / "quizzes").glob("*.md")) if (book_dir / "quizzes").exists() else [])

    for path in markdown_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = local_target(path.parent, raw)
            if target is not None and not target.exists():
                errors.append(f"{path.relative_to(book_dir)}: broken link -> {raw}")
        for raw in IMAGE_RE.findall(text):
            target = local_target(path.parent, raw)
            if target is not None and not target.exists():
                errors.append(f"{path.relative_to(book_dir)}: missing visual -> {raw}")
            if target is not None and target.suffix.lower() != ".png":
                errors.append(f"{path.relative_to(book_dir)}: visual is not PNG -> {raw}")

    overview = book_dir / "overview.md"
    if overview.exists():
        overview_text = overview.read_text(encoding="utf-8")
        for path in key_files:
            if path.name not in overview_text:
                errors.append(f"overview.md: missing link to {path.name}")
        if "review.md" not in overview_text:
            errors.append("overview.md: missing review.md link")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK: curriculum structure, links, quizzes, navigation, and visuals validate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
