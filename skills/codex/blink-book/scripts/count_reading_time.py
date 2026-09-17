#!/usr/bin/env python3
"""Count learner-facing summary words and estimate reading time."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_WPM = 135
DEFAULT_TARGET_MINUTES = 45


def strip_markdown_noise(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"<details>.*?</details>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#>*_\-|]+", " ", text)
    return text


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", strip_markdown_noise(text)))


def learner_files(book_dir: Path) -> list[Path]:
    files = [book_dir / "overview.md"]
    files.extend(sorted(book_dir.glob("key-idea-*.md")))
    return [path for path in files if path.exists()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book_dir", type=Path, help="Book output folder")
    parser.add_argument("--wpm", type=int, default=DEFAULT_WPM)
    parser.add_argument(
        "--target-minutes", "--limit-minutes", dest="target_minutes",
        type=int, default=DEFAULT_TARGET_MINUTES,
        help="Editorial target; exceeding it does not fail the check",
    )
    args = parser.parse_args()

    book_dir = args.book_dir.expanduser().resolve()
    if not book_dir.exists():
        print(f"Book folder not found: {book_dir}", file=sys.stderr)
        return 2

    rows = []
    total = 0
    for path in learner_files(book_dir):
        count = count_words(path.read_text(encoding="utf-8"))
        rows.append((path.relative_to(book_dir), count))
        total += count

    minutes = total / args.wpm if args.wpm else 0
    for rel_path, count in rows:
        print(f"{rel_path}: {count} words")
    print(f"Total learner-facing summary words: {total}")
    print(f"Estimated reading time at {args.wpm} wpm: {minutes:.1f} minutes")

    if minutes > args.target_minutes:
        print(
            f"NOTE: reading time exceeds the {args.target_minutes}-minute editorial target. "
            "Preserve explanation needed for understanding."
        )
    else:
        print("Reading time is within the editorial target.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
