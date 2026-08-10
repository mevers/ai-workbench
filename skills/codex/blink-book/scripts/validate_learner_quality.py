#!/usr/bin/env python3
"""Validate that each Blink Book key idea has an evidenced first-reader review.

The validator deliberately checks for review evidence, not prose style.  Clear
writing is a human judgement.  The gate therefore requires a source-blind reader
to document whether a key idea, its unfamiliar examples, and its terminology can
be understood from the learner-facing prose alone.
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


def validate_key_idea(path: Path, errors: list[str]) -> None:
    body = learner_body(path.read_text(encoding="utf-8"))
    draft_dir = path.parent / "_work" / "key-idea-drafts"
    draft_path = draft_dir / f"{path.stem}-full-draft.md"
    review_path = draft_dir / f"{path.stem}-first-reader-review.md"
    if not draft_path.is_file():
        errors.append(f"{path.name}: missing retained fuller draft: {draft_path.relative_to(path.parent)}")
    if not review_path.is_file():
        errors.append(f"{path.name}: missing source-blind first-reader review: {review_path.relative_to(path.parent)}")
        return

    review = review_path.read_text(encoding="utf-8")
    for heading in ("Review conditions", "Reader reconstruction", "Unfamiliar names and case examples", "Terms and labels", "Gate decision"):
        if section(review, heading) is None:
            errors.append(f"{review_path.name}: missing required section: {heading}")

    conditions = section(review, "Review conditions")
    if conditions is not None:
        for phrase in ("source-blind", "final learner-facing"):
            if phrase not in conditions.lower():
                errors.append(f"{review_path.name}: Review conditions must state that review was {phrase}")
        if not substantive(field(conditions, "Reviewer")):
            errors.append(f"{review_path.name}: Review conditions must identify the reviewer")
        if (field(conditions, "Writer and reviewer are different") or "").strip().lower() != "yes":
            errors.append(f"{review_path.name}: the writer may not approve their own prose")

    reconstruction = section(review, "Reader reconstruction")
    if reconstruction is not None:
        for label in ("Central conclusion", "Key mechanism", "Action or implication"):
            if not substantive(field(reconstruction, label)):
                errors.append(f"{review_path.name}: Reader reconstruction is missing a substantive '{label}' answer")
        if field(reconstruction, "Unresolved confusion") is None:
            errors.append(f"{review_path.name}: Reader reconstruction is missing an 'Unresolved confusion' answer")

    named_section = section(review, "Unfamiliar names and case examples")
    if named_section is not None:
        named_records = records(named_section)
        names = sorted({name.strip() for name in ITALIC_RE.findall(body) if len(name.split()) <= 8})
        for name in names:
            record = named_records.get(name)
            if record is None:
                errors.append(f"{review_path.name}: unfamiliar italicised reference '{name}' has no first-reader review")
                continue
            for label in ("What is it", "What happens", "Why it matters here", "Verdict"):
                if not substantive(field(record, label)):
                    errors.append(f"{review_path.name}: {name} is missing a substantive '{label}' answer")
            evidence = field(record, "Final-prose evidence")
            if not substantive(evidence) or normalise(evidence) not in normalise(body):
                errors.append(f"{review_path.name}: {name} must quote the final prose that supplies its context")
            if (field(record, "Verdict") or "").strip().upper() != "PASS":
                errors.append(f"{review_path.name}: {name} did not pass the first-reader case-context check")

    terms = section(review, "Terms and labels")
    if terms is not None:
        for label in ("Source-defined terms retained", "Non-source labels removed or rewritten"):
            if not substantive(field(terms, label)):
                errors.append(f"{review_path.name}: Terms and labels is missing '{label}'")

    decision = section(review, "Gate decision")
    if decision is None or not re.search(r"^Decision:\s*PASS\b", decision, re.MULTILINE):
        errors.append(f"{review_path.name}: Gate decision must explicitly be 'Decision: PASS'")


def validate_book_quality(book_dir: Path) -> list[str]:
    errors: list[str] = []
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
    print("OK: every key idea has a retained fuller draft and a passing source-blind first-reader review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
