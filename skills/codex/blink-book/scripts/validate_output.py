#!/usr/bin/env python3
"""Validate the structure and permitted outputs of a Blink Book mode."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import validate_assessment
from validate_learner_quality import validate_book_quality


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def local_target(base: Path, raw: str) -> Path | None:
    target = raw.split("#", 1)[0].strip()
    if not target or "://" in target or target.startswith("mailto:"):
        return None
    return (base / target).resolve()


def has_navigation(text: str, index: int, count: int, expects_review: bool) -> bool:
    has_previous = "Previous:" in text
    has_next = "Next:" in text
    if count == 1:
        return has_next if expects_review else True
    if index == 1:
        return has_next
    if index == count:
        return has_previous and (has_next if expects_review else True)
    return has_previous and has_next


def validate_links(paths: list[Path], book_dir: Path, errors: list[str]) -> None:
    for path in paths:
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book_dir", type=Path, help="Book output folder")
    parser.add_argument("--mode", choices=("all", "blink", "assessment"), default="all")
    parser.add_argument("--assessment-mode", choices=("contextual", "generic", "recap"))
    parser.add_argument(
        "--context-file",
        type=Path,
        help="Context file whose approved sources contextual assessments may link in learner-facing related ideas.",
    )
    # Backwards-compatible aliases for previous skill versions.
    parser.add_argument("--assessment-standard", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--application-context", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    book_dir = args.book_dir.expanduser().resolve()

    if args.assessment_mode == "recap":
        args.assessment_mode = "generic"
    if args.assessment_standard and args.assessment_mode is None:
        args.assessment_mode = "contextual" if args.application_context else "generic"
    if args.application_context and args.assessment_mode != "contextual":
        parser.error("--application-context requires contextual assessment mode")
    if args.mode == "blink" and args.assessment_mode:
        parser.error("blink mode does not create assessments")
    if args.context_file and args.assessment_mode != "contextual":
        parser.error("--context-file requires contextual assessment mode")

    errors: list[str] = []
    warnings: list[str] = []
    required = ["metadata.yaml", "overview.md", "visuals", "_work"]
    if args.mode in ("all", "assessment"):
        required.extend(["review.md", "quizzes"])
    required.extend(
        [
            "_work/source-index.md",
            "_work/source-structure.md",
            "_work/source-evidence.md",
            "_work/key-idea-plan.md",
            "_work/idea-argument-packs",
        ]
    )
    for name in required:
        if not (book_dir / name).exists():
            errors.append(f"Missing required path: {name}")

    key_files = sorted(book_dir.glob("key-idea-*.md"))
    if not key_files:
        errors.append("No key-idea-*.md files found")

    expects_assessment_navigation = args.mode == "all"
    for index, path in enumerate(key_files, start=1):
        text = path.read_text(encoding="utf-8")
        if re.search(r"^## Source basis$", text, flags=re.MULTILINE | re.IGNORECASE) is None:
            errors.append(f"{path.name}: missing Source basis section")
        if "overview.md" not in text:
            errors.append(f"{path.name}: missing backlink to overview.md")
        if not has_navigation(text, index, len(key_files), expects_assessment_navigation):
            errors.append(f"{path.name}: missing expected previous/next navigation")
        if expects_assessment_navigation:
            expected_quiz = book_dir / "quizzes" / f"{path.stem}-comprehension.md"
            if expected_quiz.name not in text:
                errors.append(f"{path.name}: missing link to {expected_quiz.relative_to(book_dir)}")
            if not expected_quiz.exists():
                errors.append(f"{path.name}: linked quiz file missing: {expected_quiz.relative_to(book_dir)}")
        elif args.mode == "blink" and ("## Check understanding" in text or "quizzes/" in text or "review.md" in text):
            errors.append(f"{path.name}: blink mode must omit assessment links")

    overview = book_dir / "overview.md"
    if overview.exists():
        overview_text = overview.read_text(encoding="utf-8")
        for path in key_files:
            if path.name not in overview_text:
                errors.append(f"overview.md: missing link to {path.name}")
        if expects_assessment_navigation and "review.md" not in overview_text:
            errors.append("overview.md: missing review.md link")
        if args.mode == "blink" and ("quizzes/" in overview_text or "review.md" in overview_text):
            errors.append("overview.md: blink mode must omit assessment links")

    if args.mode in ("all", "assessment"):
        review = book_dir / "review.md"
        if review.exists() and "overview.md" not in review.read_text(encoding="utf-8"):
            errors.append("review.md: missing backlink to overview.md")

    paths = [overview, *key_files]
    if args.mode in ("all", "assessment"):
        paths.extend([book_dir / "review.md"])
        quiz_dir = book_dir / "quizzes"
        if quiz_dir.exists():
            paths.extend(sorted(quiz_dir.glob("*.md")))
    validate_links(paths, book_dir, errors)

    # Learner comprehension is a release requirement for work created in this
    # skill. Assessment-only mode must not demand new blink-phase artefacts.
    if args.mode in ("all", "blink"):
        errors.extend(validate_book_quality(book_dir))

    if args.assessment_mode:
        context_file = None
        if args.assessment_mode == "contextual":
            context_file = (args.context_file or Path.cwd() / "application-context.md").expanduser().resolve()
        validate_assessment.validate_assessment_standard(
            book_dir, errors, warnings, args.assessment_mode == "contextual", context_file
        )

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: Blink Book {args.mode} mode validates.")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
