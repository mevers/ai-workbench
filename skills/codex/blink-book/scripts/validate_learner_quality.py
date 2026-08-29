#!/usr/bin/env python3
"""Validate the artefacts for the independent dual-review gate.

This is deliberately a structural check. It verifies retained drafts and a
passing source-blind and source-aware review for every learner-facing file; it
does not assess prose quality or overrule either independent reviewer.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ITALIC_RE = re.compile(r"(?<![!*])\*([^*\n]+)\*(?!\*)")


def normalise(value: str) -> str:
    return " ".join(value.replace("\\", "").split())


def learner_body(text: str) -> str:
    return re.split(r"^## Source basis\s*$", text, maxsplit=1, flags=re.MULTILINE | re.IGNORECASE)[0]


def section(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL
    )
    return match.group("body") if match else None


def records(text: str) -> dict[str, str]:
    return {
        match.group(1).strip(): match.group("body")
        for match in re.finditer(r"^###\s+(.+?)\s*$\n(?P<body>.*?)(?=^###\s+|\Z)", text, re.MULTILINE | re.DOTALL)
    }


def field(record: str, label: str) -> str | None:
    match = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.+)$", record, re.MULTILINE)
    return match.group(1).strip() if match else None


def substantive(value: str | None) -> bool:
    return bool(value and value.lower() not in {"none", "n/a", "tbd", "todo"})


def validate_review(review_path: Path, review_kind: str, errors: list[str]) -> None:
    if not review_path.is_file():
        errors.append(f"missing {review_kind} review: {review_path}")
        return
    review = review_path.read_text(encoding="utf-8")
    required = ("Review conditions", "Reader reconstruction", "Concerns and required repairs", "Most vulnerable passage", "Gate decision")
    for heading in required:
        if section(review, heading) is None:
            errors.append(f"{review_path.name}: missing required section: {heading}")
    if review_kind == "source-aware" and section(review, "Source terminology and fidelity") is None:
        errors.append(f"{review_path.name}: source-aware review is missing Source terminology and fidelity")
    if review_kind not in review.lower():
        errors.append(f"{review_path.name}: review record must identify it as {review_kind}")
    reconstruction = section(review, "Reader reconstruction")
    if reconstruction is None or not reconstruction.strip():
        errors.append(f"{review_path.name}: Reader reconstruction must be substantive")
    decision = section(review, "Gate decision")
    if decision is None or not re.search(r"^Decision:\s*PASS\b", decision, re.MULTILINE):
        errors.append(f"{review_path.name}: Gate decision must explicitly be 'Decision: PASS'")


def validate_key_idea(path: Path, errors: list[str]) -> None:
    draft_dir = path.parent / "_work" / "key-idea-drafts"
    draft_path = draft_dir / f"{path.stem}-full-draft.md"
    if not draft_path.is_file():
        errors.append(f"{path.name}: missing retained fuller draft: {draft_path.relative_to(path.parent)}")
    validate_review(draft_dir / f"{path.stem}-source-blind-review.md", "source-blind", errors)
    validate_review(draft_dir / f"{path.stem}-source-aware-review.md", "source-aware", errors)


def validate_book_quality(book_dir: Path) -> list[str]:
    errors: list[str] = []
    review_dir = book_dir / "_work" / "final-reviews"
    validate_review(review_dir / "overview-source-blind-review.md", "source-blind", errors)
    validate_review(review_dir / "overview-source-aware-review.md", "source-aware", errors)
    for path in sorted(book_dir.glob("key-idea-*.md")):
        validate_key_idea(path, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book_dir", type=Path, help="Blink Book output folder")
    args = parser.parse_args()
    errors = validate_book_quality(args.book_dir.expanduser().resolve())
    if errors:
        print("Learner-quality validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("OK: overview and every key idea have passing independent source-blind and source-aware reviews.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
