#!/usr/bin/env python3
"""Validate the structure and permitted outputs of a Blink Book mode."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from validate_learner_quality import validate_book_quality


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
SOURCE_ID_RE = re.compile(r"^\|\s*([A-Za-z][A-Za-z0-9]*-\d+)\s*\|", re.MULTILINE)
QUESTION_RE = re.compile(
    r"^## (?P<heading>Quick recall|Apply|Deeper comprehension|Question \d+)\s*$"
    r"(?P<body>.*?)(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)
OPTION_RE = re.compile(r"^\*\*([A-D])\.\*\*\s+(.+)$", re.MULTILINE)
ANSWER_RE = re.compile(r"(?:Correct|Best answer):\s*\*\*([A-D])\*\*")
WORD_RE = re.compile(r"[\w’'-]+")


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


def approved_source_ids(context_file: Path, errors: list[str]) -> set[str]:
    if not context_file.is_file():
        errors.append(f"Contextual assessment requires an application context file: {context_file}")
        return set()
    source_ids = set(SOURCE_ID_RE.findall(context_file.read_text(encoding="utf-8")))
    if not source_ids:
        errors.append(f"{context_file}: no approved source IDs found")
    return source_ids


def references_section(text: str) -> str:
    match = re.search(r"^## References and evidence basis$", text, flags=re.MULTILINE)
    return text[match.end() :] if match else ""


def validate_context_reference(
    references: str, label: str, source_ids: set[str], path: Path, book_dir: Path, errors: list[str]
) -> None:
    match = re.search(rf"^- \*\*{re.escape(label)}:\*\*\s*(.+)$", references, flags=re.MULTILINE)
    if not match:
        errors.append(f"{path.relative_to(book_dir)}: missing evidence entry for {label}")
    elif not any(source_id in match.group(1) for source_id in source_ids):
        errors.append(f"{path.relative_to(book_dir)}: {label} must cite an approved context-source ID")


def review_option_quality(path: Path, book_dir: Path, warnings: list[str]) -> list[str]:
    answer_letters: list[str] = []
    text = path.read_text(encoding="utf-8")
    for match in QUESTION_RE.finditer(text):
        options = {letter: content for letter, content in OPTION_RE.findall(match.group("body"))}
        answer = ANSWER_RE.search(match.group("body"))
        if len(options) != 4 or answer is None:
            continue
        correct = answer.group(1)
        if correct not in options:
            continue
        answer_letters.append(correct)
        lengths = {letter: len(WORD_RE.findall(content)) for letter, content in options.items()}
        shortest = min(lengths.values())
        allowed_difference = min(4, max(1, round(shortest * 0.2)))
        if lengths[correct] > shortest + allowed_difference:
            warnings.append(
                f"{path.relative_to(book_dir)}: {match.group('heading')} correct option is "
                f"{lengths[correct]} words; shortest option is {shortest}. Review for a length or completeness tell."
            )
    return answer_letters


def warn_on_answer_concentration(answer_letters: list[str], warnings: list[str]) -> None:
    if len(answer_letters) < 4:
        return
    most_common = max(set(answer_letters), key=answer_letters.count)
    count = answer_letters.count(most_common)
    if count / len(answer_letters) > 0.5:
        warnings.append(
            f"Assessment set: {most_common} is correct in {count} of {len(answer_letters)} questions. "
            "Review answer-position variety."
        )


def validate_assessment_standard(
    book_dir: Path, errors: list[str], warnings: list[str], contextual: bool, context_file: Path | None
) -> None:
    key_files = sorted(book_dir.glob("key-idea-*.md"))
    quiz_dir = book_dir / "quizzes"
    source_ids = approved_source_ids(context_file, errors) if contextual and context_file is not None else set()
    answer_letters: list[str] = []
    expected = {f"{path.stem}-comprehension.md" for path in key_files}
    actual = {path.name for path in quiz_dir.glob("key-idea-*-comprehension.md")} if quiz_dir.exists() else set()
    for name in sorted(expected - actual):
        errors.append(f"quizzes: missing assessment file: {name}")
    for name in sorted(actual - expected):
        errors.append(f"quizzes: unexpected assessment file: {name}")

    for path in sorted(quiz_dir.glob("key-idea-*-comprehension.md")) if quiz_dir.exists() else []:
        text = path.read_text(encoding="utf-8")
        answer_letters.extend(review_option_quality(path, book_dir, warnings))
        if contextual:
            for heading in (
                "## Quick recall",
                "## Apply",
                "## Try this in your ",
                "## References and evidence basis",
            ):
                if heading not in text:
                    errors.append(f"{path.relative_to(book_dir)}: missing contextual assessment section: {heading}")
            if text.count("<details>") < 2:
                errors.append(f"{path.relative_to(book_dir)}: expected collapsed answers for recall and apply")
            if len(re.findall(r"\*\*[A-D]\.\*\*", text)) < 8:
                errors.append(f"{path.relative_to(book_dir)}: expected two four-option multiple-choice items")
            if source_ids:
                references = references_section(text)
                validate_context_reference(references, "Apply", source_ids, path, book_dir, errors)
                validate_context_reference(references, "Try this", source_ids, path, book_dir, errors)
        else:
            for heading in ("## Quick recall", "## Deeper comprehension"):
                if heading not in text:
                    errors.append(f"{path.relative_to(book_dir)}: missing generic assessment section: {heading}")
            if text.count("<details>") < 2:
                errors.append(f"{path.relative_to(book_dir)}: expected collapsed answers for two recap questions")
            if len(re.findall(r"\*\*[A-D]\.\*\*", text)) < 8:
                errors.append(f"{path.relative_to(book_dir)}: expected two four-option recap items")

    review = book_dir / "review.md"
    if not review.exists():
        errors.append("Missing required path: review.md")
        return
    text = review.read_text(encoding="utf-8")
    answer_letters.extend(review_option_quality(review, book_dir, warnings))
    question_count = len(re.findall(r"^## Question \d+", text, flags=re.MULTILINE))
    idea_count = len(key_files)
    expected_count = 5 if 5 <= idea_count <= 7 else 6 if idea_count >= 8 else idea_count
    if question_count != expected_count:
        errors.append(f"review.md: expected {expected_count} review questions, found {question_count}")
    if contextual and "## References and evidence basis" not in text:
        errors.append("review.md: missing References and evidence basis section")
    if contextual and source_ids:
        references = references_section(text)
        for question in range(1, expected_count + 1):
            validate_context_reference(references, f"Question {question}", source_ids, review, book_dir, errors)
    warn_on_answer_concentration(answer_letters, warnings)


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
        help="Context file whose approved source IDs contextual assessments must cite.",
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
        validate_assessment_standard(book_dir, errors, warnings, args.assessment_mode == "contextual", context_file)

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
