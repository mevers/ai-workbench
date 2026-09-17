#!/usr/bin/env python3
"""Validate learner prose and artefacts retained after independent review.

This checks deterministic prose prohibitions plus retained drafts and a
source-blind and source-aware PASS for every learner-facing file. It does not
prove that the prose is clear or that reviews were independent or valid.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


ITALIC_RE = re.compile(r"(?<![!*])\*([^*\n]+)\*(?!\*)")
NOT_BUT_RE = re.compile(
    r"\bnot(?:\s+(?:just|merely|simply|only))?\b[^.!?\n]{0,180}\bbut(?:\s+also)?\b",
    re.IGNORECASE,
)
NEGATION_RESET_RE = re.compile(
    r"\b(?:is|are|was|were|do|does|did|mean|means|meant)\s+not\b[^.!?\n]{0,160}[;:]\s*"
    r"(?:it|this|that|they|he|she|we|the\s+\w+)\s+"
    r"(?:is|are|was|were|do|does|did|mean|means|meant)\b",
    re.IGNORECASE,
)
CONTRACTION_RESET_RE = re.compile(
    r"\b(?:isn't|aren't|wasn't|weren't|doesn't|don't|didn't)\b[^.!?\n]{0,160}[;:]\s*"
    r"(?:it|this|that|they|he|she|we)(?:'s|\s+(?:is|are|was|were|do|does|did))\b",
    re.IGNORECASE,
)
INLINE_QUOTE_RES = (
    re.compile(r'"[^"\n]*"'),
    re.compile(r"“[^”\n]*”"),
    re.compile(r"‘[^’\n]*’"),
)


def normalise(value: str) -> str:
    return " ".join(value.replace("\\", "").split())


def learner_body(text: str) -> str:
    return re.split(r"^## Source basis\s*$", text, maxsplit=1, flags=re.MULTILINE | re.IGNORECASE)[0]


def mask_direct_quotations(text: str) -> str:
    """Mask clearly quoted text while preserving offsets and line numbers."""

    lines = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith(">"):
            lines.append("".join("\n" if char == "\n" else " " for char in line))
        else:
            lines.append(line)
    masked = "".join(lines)
    for pattern in INLINE_QUOTE_RES:
        masked = pattern.sub(lambda match: " " * len(match.group(0)), masked)
    return masked


def validate_learner_prose(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        return
    prose = mask_direct_quotations(learner_body(path.read_text(encoding="utf-8")))
    checks = (
        (re.compile(r"—|(?<=\s)--(?=\s)"), "em dash"),
        (NOT_BUT_RE, "not-X-but-Y contrast"),
        (NEGATION_RESET_RE, "not-X-it-is-Y contrast"),
        (CONTRACTION_RESET_RE, "not-X-it-is-Y contrast"),
    )
    for pattern, label in checks:
        for match in pattern.finditer(prose):
            line = prose.count("\n", 0, match.start()) + 1
            errors.append(f"{path.name}:{line}: prohibited {label} in authored learner prose")


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


def no_findings(value: str | None) -> bool:
    return bool(value is not None and value.strip() in {"None.", "None"})


def validate_review(
    review_path: Path, review_kind: str, learner_path: Path, errors: list[str]
) -> None:
    if not learner_path.is_file():
        errors.append(f"missing learner file for {review_kind} review: {learner_path}")
        return
    if not review_path.is_file():
        errors.append(f"missing {review_kind} review: {review_path}")
        return
    review = review_path.read_text(encoding="utf-8")
    required = ("Review conditions", "Reader reconstruction", "Blockers", "Advisories", "Gate decision")
    for heading in required:
        if section(review, heading) is None:
            errors.append(f"{review_path.name}: missing required section: {heading}")
    review_wave = field(review, "Review wave")
    if not re.fullmatch(r"[1-9][0-9]*", review_wave or ""):
        errors.append(f"{review_path.name}: Review wave must be a positive integer")
    if review_kind == "source-blind":
        style = section(review, "Plain-language and style")
        if style is None:
            errors.append(f"{review_path.name}: source-blind review is missing Plain-language and style")
        elif not style.strip():
            errors.append(f"{review_path.name}: Plain-language and style must be substantive")
    if review_kind == "source-aware":
        coverage = section(review, "Independent coverage baseline")
        if coverage is None:
            errors.append(f"{review_path.name}: source-aware review is missing Independent coverage baseline")
        elif not coverage.strip():
            errors.append(f"{review_path.name}: Independent coverage baseline must be substantive")
        if section(review, "Source terminology and fidelity") is None:
            errors.append(f"{review_path.name}: source-aware review is missing Source terminology and fidelity")
    if review_kind not in review.lower():
        errors.append(f"{review_path.name}: review record must identify it as {review_kind}")
    reconstruction = section(review, "Reader reconstruction")
    if reconstruction is None or not reconstruction.strip():
        errors.append(f"{review_path.name}: Reader reconstruction must be substantive")
    decision = section(review, "Gate decision")
    if decision is None or not re.search(r"^Decision:\s*PASS\b", decision, re.MULTILINE):
        errors.append(f"{review_path.name}: Gate decision must explicitly be 'Decision: PASS'")
    elif not no_findings(section(review, "Blockers")):
        errors.append(f"{review_path.name}: PASS review must record `None.` under Blockers")
    current_hash = hashlib.sha256(learner_path.read_bytes()).hexdigest()
    if current_hash.lower() not in review.lower():
        errors.append(
            f"{review_path.name}: review does not record the current SHA-256 for {learner_path.name}"
        )


def validate_key_idea(path: Path, errors: list[str]) -> None:
    draft_dir = path.parent / "_work" / "key-idea-drafts"
    draft_path = draft_dir / f"{path.stem}-full-draft.md"
    if not draft_path.is_file():
        errors.append(f"{path.name}: missing retained fuller draft: {draft_path.relative_to(path.parent)}")
    validate_review(
        draft_dir / f"{path.stem}-source-blind-review.md", "source-blind", path, errors
    )
    validate_review(
        draft_dir / f"{path.stem}-source-aware-review.md", "source-aware", path, errors
    )


def validate_book_quality(book_dir: Path) -> list[str]:
    errors: list[str] = []
    review_dir = book_dir / "_work" / "final-reviews"
    validate_learner_prose(book_dir / "overview.md", errors)
    overview_path = book_dir / "overview.md"
    validate_review(
        review_dir / "overview-source-blind-review.md", "source-blind", overview_path, errors
    )
    validate_review(
        review_dir / "overview-source-aware-review.md", "source-aware", overview_path, errors
    )
    for path in sorted(book_dir.glob("key-idea-*.md")):
        validate_learner_prose(path, errors)
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
    print("OK: learner prose passes deterministic style checks and required independent reviews contain current-hash PASS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
