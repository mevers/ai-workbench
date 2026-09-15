#!/usr/bin/env python3
"""Validate deterministic invariants of the Blink assessment subsystem."""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path


FIELD_RE_TEMPLATE = r"^{label}\s*(.+?)\s*$"
OPTION_RE = re.compile(r"^\*\*([A-D])\.\*\*\s+(.+)$", re.MULTILINE)
ANSWER_RE = re.compile(r"^Correct answer(s?):\s+\*\*([A-D](?:\s*,\s*[A-D])*)\*\*\s*$", re.MULTILINE)
URL_RE = re.compile(r"https?://[^\s)>]+")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
QUESTION_FIELDS = (
    "**Source mechanism:**",
    "**Source anchor:**",
    "**Intended learner judgement:**",
    "**Answer mode:**",
    "**Correct answers:**",
    "**Option rationales:**",
    "**Context excerpt:**",
    "**Proposed situation or practice:**",
    "**Apply/Try-this distinction:**",
    "**Rejection risk:**",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assessment_bundle_digest(paths: list[Path], book_dir: Path) -> str:
    manifest = "".join(
        f"{path.relative_to(book_dir).as_posix()}\t{sha256_file(path)}\n"
        for path in sorted(paths, key=lambda item: item.relative_to(book_dir).as_posix())
    )
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest()


def field_value(text: str, label: str) -> str | None:
    match = re.search(FIELD_RE_TEMPLATE.format(label=re.escape(label)), text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def markdown_section(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else None


def substantive(value: str | None) -> bool:
    return bool(value and value not in {"None.", "N/A.", "<none>"} and not value.startswith("<"))


def split_sections(text: str, heading_re: re.Pattern[str]) -> list[tuple[str, str]]:
    matches = list(heading_re.finditer(text))
    return [
        (match.group(1), text[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(text)])
        for index, match in enumerate(matches)
    ]


def answer_letters(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return ()
    return tuple(part.strip() for part in raw.split(",") if part.strip())


def unquote_excerpt(raw: str | None) -> str:
    value = (raw or "").strip()
    for opening, closing in (("“", "”"), ('"', '"'), ("`", "`")):
        if value.startswith(opening) and value.endswith(closing):
            return value[len(opening) : -len(closing)].strip()
    return value


def blind_assessment(text: str) -> str:
    """Remove complete answer blocks before the learner review."""
    blinded = re.sub(r"<details\b[^>]*>.*?</details\s*>", "", text, flags=re.DOTALL | re.IGNORECASE)
    if re.search(r"Correct answers?:|</?details\b", blinded, flags=re.IGNORECASE):
        raise ValueError("Cannot blind assessment: answer text or an incomplete answer block remains")
    return blinded


def validate_compact_context(body: str, label: str, contextual: bool, applied: bool, errors: list[str]) -> None:
    basis = field_value(body, "**Context basis:**")
    facts = field_value(body, "**Scenario facts:**")
    if facts is None or not facts.strip():
        errors.append(f"{label}: Scenario facts must list additions or use None.")
    if applied:
        if not contextual:
            errors.append(f"{label}: generic assessment cannot contain contextual application")
        if not substantive(basis):
            errors.append(f"{label}: applied item requires Context basis")
    elif basis not in {"None.", "None"} or facts not in {"None.", "None"}:
        errors.append(f"{label}: recap question must use `None.` for context fields")


def validate_question_plan(
    body: str,
    label: str,
    contextual: bool,
    context_text: str,
    applied: bool,
    errors: list[str],
    format_version: int = 1,
) -> tuple[str | None, tuple[str, ...]]:
    fields = ("**Learning target:**", "**Source anchor:**", "**Context basis:**", "**Scenario facts:**", "**Answer mode:**", "**Correct answers:**", "**Reasoning:**") if format_version == 2 else QUESTION_FIELDS
    for field in fields:
        if field_value(body, field) is None:
            errors.append(f"{label}: missing plan field {field}")

    mode = field_value(body, "**Answer mode:**")
    answers = answer_letters(field_value(body, "**Correct answers:**"))
    if mode not in {"ONE_BEST", "SELECT_ALL"}:
        errors.append(f"{label}: Answer mode must be ONE_BEST or SELECT_ALL")
    elif mode == "ONE_BEST" and len(answers) != 1:
        errors.append(f"{label}: ONE_BEST requires exactly one correct answer")
    elif mode == "SELECT_ALL" and len(answers) not in {2, 3}:
        errors.append(f"{label}: SELECT_ALL requires two or three correct answers")
    if any(letter not in {"A", "B", "C", "D"} for letter in answers):
        errors.append(f"{label}: Correct answers must use A-D")

    if format_version == 2:
        for field in ("**Learning target:**", "**Source anchor:**", "**Reasoning:**"):
            if not substantive(field_value(body, field)):
                errors.append(f"{label}: plan field is not substantive: {field}")
        validate_compact_context(body, label, contextual, applied, errors)
        return mode, answers

    for field in ("**Source mechanism:**", "**Source anchor:**", "**Intended learner judgement:**", "**Option rationales:**", "**Rejection risk:**"):
        if not substantive(field_value(body, field)):
            errors.append(f"{label}: plan field is not substantive: {field}")

    excerpt = unquote_excerpt(field_value(body, "**Context excerpt:**"))
    situation = field_value(body, "**Proposed situation or practice:**")
    distinction = field_value(body, "**Apply/Try-this distinction:**")
    if applied:
        if not contextual:
            errors.append(f"{label}: generic assessment cannot contain contextual application")
        if not substantive(excerpt) or excerpt not in context_text:
            errors.append(f"{label}: Context excerpt is not an exact excerpt from application-context.md")
        if not substantive(situation):
            errors.append(f"{label}: applied item requires a proposed situation")
    elif any(value not in {"None.", "None"} for value in (excerpt, situation, distinction)):
        errors.append(f"{label}: recap question must use `None.` for context fields")
    return mode, answers


def validate_try_plan(body: str, label: str, context_text: str, errors: list[str], format_version: int = 1) -> None:
    if format_version == 2:
        for field in ("**Learning target:**", "**Source anchor:**", "**Action and use:**"):
            if not substantive(field_value(body, field)):
                errors.append(f"{label}: plan field is not substantive: {field}")
        validate_compact_context(body, label, True, True, errors)
        return
    fields = (
        "**Source mechanism:**",
        "**Source anchor:**",
        "**Intended learner action:**",
        "**Answer mode:**",
        "**Correct answers:**",
        "**Option rationales:**",
        "**Context excerpt:**",
        "**Proposed situation or practice:**",
        "**Apply/Try-this distinction:**",
        "**Rejection risk:**",
    )
    for field in fields:
        if field_value(body, field) is None:
            errors.append(f"{label}: missing plan field {field}")
    for field in ("**Source mechanism:**", "**Source anchor:**", "**Intended learner action:**", "**Proposed situation or practice:**", "**Apply/Try-this distinction:**", "**Rejection risk:**"):
        if not substantive(field_value(body, field)):
            errors.append(f"{label}: plan field is not substantive: {field}")
    for field in ("**Answer mode:**", "**Correct answers:**", "**Option rationales:**"):
        if field_value(body, field) not in {"N/A.", "N/A"}:
            errors.append(f"{label}: Try this must use `N/A.` for {field}")
    excerpt = unquote_excerpt(field_value(body, "**Context excerpt:**"))
    if not substantive(excerpt) or excerpt not in context_text:
        errors.append(f"{label}: Context excerpt is not an exact excerpt from application-context.md")


def validate_plan(
    book_dir: Path,
    key_files: list[Path],
    contextual: bool,
    context_file: Path | None,
    errors: list[str],
) -> tuple[Path, dict[str, str], dict[str, list[tuple[str | None, tuple[str, ...]]]], list[tuple[str | None, tuple[str, ...]]]]:
    path = book_dir / "_work" / "assessment-plan.md"
    routes: dict[str, str] = {}
    specs: dict[str, list[tuple[str | None, tuple[str, ...]]]] = {}
    review_specs: list[tuple[str | None, tuple[str, ...]]] = []
    if not path.is_file():
        errors.append("Missing required assessment plan: _work/assessment-plan.md")
        return path, routes, specs, review_specs

    text = path.read_text(encoding="utf-8")
    context_text = context_file.read_text(encoding="utf-8") if context_file and context_file.is_file() else ""
    format_label = field_value(text, "**Assessment format:**")
    if format_label not in {None, "2"}:
        errors.append("_work/assessment-plan.md: unsupported Assessment format")
    format_version = 2 if format_label == "2" else 1
    expected_mode = "CONTEXTUAL" if contextual else "GENERIC"
    if field_value(text, "**Assessment mode:**") != expected_mode:
        errors.append(f"_work/assessment-plan.md: Assessment mode must be {expected_mode}")
    if "Plan status: FROZEN" not in text:
        errors.append("_work/assessment-plan.md: plan is not FROZEN")

    recorded_digest = field_value(text, "**Context SHA-256:**")
    if contextual:
        if context_file is None or not context_file.is_file():
            errors.append(f"Contextual assessment requires an application context file: {context_file}")
        elif recorded_digest != sha256_file(context_file):
            errors.append("_work/assessment-plan.md: Context SHA-256 does not match application-context.md")
        if not substantive(field_value(text, "**Context path:**")):
            errors.append("_work/assessment-plan.md: contextual plan requires Context path")
    elif field_value(text, "**Context path:**") not in {"None.", "None"} or recorded_digest not in {"None.", "None"}:
        errors.append("_work/assessment-plan.md: generic plan must use `None.` for context path and digest")

    key_sections = split_sections(text, re.compile(r"^## Key idea (\d+)\s*$", re.MULTILINE))
    expected_numbers = {str(index) for index in range(1, len(key_files) + 1)}
    actual_numbers = {number for number, _ in key_sections}
    if actual_numbers != expected_numbers:
        errors.append(f"_work/assessment-plan.md: key-idea plan sections must be {sorted(expected_numbers)}")

    for number, body in key_sections:
        key_name = f"key-idea-{int(number):02d}"
        label = f"_work/assessment-plan.md: Key idea {number}"
        route = field_value(body, "**Route:**")
        if route not in {"FULL", "RECAP_ONLY"}:
            errors.append(f"{label}: Route must be FULL or RECAP_ONLY")
            continue
        if not contextual and route != "RECAP_ONLY":
            errors.append(f"{label}: generic assessment must use RECAP_ONLY")
        if not substantive(field_value(body, "**Route reason:**")):
            errors.append(f"{label}: Route reason is not substantive")
        routes[key_name] = route

        components = dict(split_sections(body, re.compile(r"^### (Quick recall|Apply|Try this|Deeper comprehension)\s*$", re.MULTILINE)))
        expected = {"Quick recall", "Apply", "Try this"} if route == "FULL" else {"Quick recall", "Deeper comprehension"}
        if set(components) != expected:
            errors.append(f"{label}: expected plan components {sorted(expected)}, found {sorted(components)}")
            continue
        item_specs = [validate_question_plan(components["Quick recall"], f"{label} Quick recall", contextual, context_text, False, errors, format_version)]
        if route == "FULL":
            item_specs.append(validate_question_plan(components["Apply"], f"{label} Apply", contextual, context_text, True, errors, format_version))
            validate_try_plan(components["Try this"], f"{label} Try this", context_text, errors, format_version)
        else:
            item_specs.append(validate_question_plan(components["Deeper comprehension"], f"{label} Deeper comprehension", contextual, context_text, False, errors, format_version))
        specs[key_name] = item_specs

    expected_review_count = 5 if 5 <= len(key_files) <= 7 else 6 if len(key_files) >= 8 else len(key_files)
    review_sections = split_sections(text, re.compile(r"^## Review question (\d+)\s*$", re.MULTILINE))
    if [int(number) for number, _ in review_sections] != list(range(1, expected_review_count + 1)):
        errors.append(f"_work/assessment-plan.md: expected Review question 1-{expected_review_count}")
    for number, body in review_sections:
        context_field = "**Context basis:**" if format_version == 2 else "**Context excerpt:**"
        excerpt = unquote_excerpt(field_value(body, context_field))
        applied = excerpt not in {"None.", "None", None}
        review_specs.append(validate_question_plan(body, f"_work/assessment-plan.md: Review question {number}", contextual, context_text, applied, errors, format_version))
    return path, routes, specs, review_specs


def question_sections(text: str, pattern: str) -> list[tuple[str, str]]:
    return split_sections(text, re.compile(pattern, re.MULTILINE))


def validate_question_block(
    body: str,
    label: str,
    planned: tuple[str | None, tuple[str, ...]] | None,
    errors: list[str],
    warnings: list[str],
) -> str | None:
    options = OPTION_RE.findall(body)
    if [letter for letter, _ in options] != ["A", "B", "C", "D"]:
        errors.append(f"{label}: expected exactly four options A-D")
    answers = ANSWER_RE.findall(body)
    if len(answers) != 1:
        errors.append(f"{label}: expected one Correct answer(s) line")
        return None
    plural, raw = answers[0]
    letters = answer_letters(raw)
    mode = "SELECT_ALL" if plural else "ONE_BEST"
    instruction = "Select all that apply." if mode == "SELECT_ALL" else "Select one answer."
    if instruction not in body:
        errors.append(f"{label}: missing `{instruction}`")
    if mode == "ONE_BEST" and len(letters) != 1:
        errors.append(f"{label}: singular answer line must contain one letter")
    if mode == "SELECT_ALL" and len(letters) not in {2, 3}:
        errors.append(f"{label}: plural answer line must contain two or three letters")
    if "<details>" not in body or "</details>" not in body:
        errors.append(f"{label}: answer must be inside a details block")
    if planned and (mode, letters) != planned:
        errors.append(f"{label}: learner answer does not match the frozen assessment plan")

    lengths = [len(text.split()) for _, text in options]
    if len(lengths) == 4 and min(lengths) and max(lengths) / min(lengths) >= 1.8:
        warnings.append(f"{label}: option lengths differ substantially; review for answer signalling")
    return letters[0] if mode == "ONE_BEST" and letters else None


def validate_links(text: str, label: str, contextual: bool, approved_urls: set[str], errors: list[str]) -> None:
    external = {target.rstrip(".,") for target in LINK_RE.findall(text) if target.startswith(("http://", "https://"))}
    if not contextual and external:
        errors.append(f"{label}: generic assessment cannot contain external related-idea links")
    for url in sorted(external - approved_urls):
        errors.append(f"{label}: external URL is not present in application-context.md: {url}")


def validate_review_record(
    path: Path,
    assessment_paths: list[Path],
    book_dir: Path,
    bundle_digest: str,
    errors: list[str],
) -> str | None:
    if not path.is_file():
        errors.append(f"Missing required independent assessment review: {path.relative_to(book_dir)}")
        return None
    text = path.read_text(encoding="utf-8")
    label = str(path.relative_to(book_dir))
    reviewer = field_value(text, "**Reviewer ID:**")
    if not substantive(reviewer):
        errors.append(f"{label}: Reviewer ID is missing")
    if field_value(text, "**Writer and reviewer are different:**") != "yes":
        errors.append(f"{label}: writer/reviewer independence is not confirmed")
    review_wave = field_value(text, "**Review wave:**")
    if review_wave not in {"1", "2", "3"}:
        errors.append(f"{label}: Review wave must be 1, 2, or 3")
    if field_value(text, "**Assessment bundle SHA-256:**") != bundle_digest:
        errors.append(f"{label}: stale review; assessment bundle digest does not match")
    blockers = markdown_section(text, "Blockers")
    if blockers is None:
        errors.append(f"{label}: missing required section: Blockers")
    if markdown_section(text, "Advisories") is None:
        errors.append(f"{label}: missing required section: Advisories")
    if not re.search(r"^Decision:\s+PASS\s*$", text, flags=re.MULTILINE):
        errors.append(f"{label}: final Decision must be PASS")
    elif blockers is None or blockers.strip() not in {"None.", "None"}:
        errors.append(f"{label}: PASS review must record `None.` under Blockers")
    for assessment in assessment_paths:
        heading = f"### {assessment.relative_to(book_dir).as_posix()}"
        if heading not in text:
            errors.append(f"{label}: missing file decision for {assessment.relative_to(book_dir)}")
    return reviewer


def validate_learner_review_stages(text: str, errors: list[str]) -> None:
    label = "_work/assessment-reviews/context-language-review.md"
    if field_value(text, "**Answers and explanations withheld until first pass saved:**") != "yes":
        errors.append(f"{label}: staged blinding is not confirmed")
    for heading in ("First pass", "Feedback check"):
        section = markdown_section(text, heading)
        if not substantive(section.strip() if section else None):
            errors.append(f"{label}: missing substantive {heading}")


def validate_assessment_standard(
    book_dir: Path,
    errors: list[str],
    warnings: list[str],
    contextual: bool,
    context_file: Path | None,
) -> None:
    key_files = sorted(book_dir.glob("key-idea-*.md"))
    plan_path, routes, specs, review_specs = validate_plan(book_dir, key_files, contextual, context_file, errors)
    for obsolete in (
        book_dir / "_work" / "assessment-design",
        book_dir / "_work" / "assessment-reviews" / "context-grounding-review.md",
        book_dir / "_work" / "assessment-reviews" / "source-aware-design-review.md",
        book_dir / "_work" / "assessment-reviews" / "source-blind-language-review.md",
    ):
        if obsolete.exists():
            errors.append(f"Obsolete assessment-architecture artifact must be removed: {obsolete.relative_to(book_dir)}")

    context_text = context_file.read_text(encoding="utf-8") if context_file and context_file.is_file() else ""
    approved_urls = {url.rstrip(".,") for url in URL_RE.findall(context_text)}
    quiz_dir = book_dir / "quizzes"
    expected_names = {f"{path.stem}-comprehension.md" for path in key_files}
    actual_names = {path.name for path in quiz_dir.glob("key-idea-*-comprehension.md")} if quiz_dir.is_dir() else set()
    for name in sorted(expected_names - actual_names):
        errors.append(f"quizzes: missing assessment file: {name}")
    for name in sorted(actual_names - expected_names):
        errors.append(f"quizzes: unexpected assessment file: {name}")

    assessment_paths = sorted(quiz_dir.glob("key-idea-*-comprehension.md")) if quiz_dir.is_dir() else []
    answer_positions: list[str] = []
    for path in assessment_paths:
        text = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(book_dir))
        if "Commit to each answer before expanding its answer block." not in text:
            errors.append(f"{relative}: missing commit-before-reveal instruction")
        key_name = path.stem.removesuffix("-comprehension")
        route = routes.get(key_name)
        expected_components = ["Quick recall", "Apply"] if route == "FULL" else ["Quick recall", "Deeper comprehension"]
        blocks = question_sections(text, r"^## (Quick recall|Apply|Deeper comprehension)\s*$")
        if [name for name, _ in blocks] != expected_components:
            errors.append(f"{relative}: expected question sections {expected_components}")
        for index, (name, body) in enumerate(blocks):
            planned = specs.get(key_name, [])[index] if index < len(specs.get(key_name, [])) else None
            position = validate_question_block(body, f"{relative}: {name}", planned, errors, warnings)
            if position:
                answer_positions.append(position)
        if route == "FULL":
            if "## Try this in your " not in text:
                errors.append(f"{relative}: FULL route requires Try this")
            for field in ("**When:**", "**Do:**", "**Why now:**"):
                if field_value(text, field) is None:
                    errors.append(f"{relative}: Try this is missing {field}")
        elif "## Try this in your " in text:
            errors.append(f"{relative}: RECAP_ONLY must not contain Try this")
        if not contextual and "## Related ideas and further reading" in text:
            errors.append(f"{relative}: generic assessment must not contain related ideas")
        validate_links(text, relative, contextual, approved_urls, errors)

    review_path = book_dir / "review.md"
    if not review_path.is_file():
        errors.append("Missing required path: review.md")
        return
    assessment_paths.append(review_path)
    review_text = review_path.read_text(encoding="utf-8")
    if "Commit to each answer before expanding its answer block." not in review_text:
        errors.append("review.md: missing commit-before-reveal instruction")
    review_blocks = question_sections(review_text, r"^## (Question \d+)\s*$")
    expected_review_count = 5 if 5 <= len(key_files) <= 7 else 6 if len(key_files) >= 8 else len(key_files)
    if len(review_blocks) != expected_review_count:
        errors.append(f"review.md: expected {expected_review_count} review questions")
    for index, (name, body) in enumerate(review_blocks):
        planned = review_specs[index] if index < len(review_specs) else None
        position = validate_question_block(body, f"review.md: {name}", planned, errors, warnings)
        if position:
            answer_positions.append(position)
    if not contextual and "## Related ideas and further reading" in review_text:
        errors.append("review.md: generic assessment must not contain related ideas")
    validate_links(review_text, "review.md", contextual, approved_urls, errors)

    bundle_digest = assessment_bundle_digest(assessment_paths, book_dir)
    review_dir = book_dir / "_work" / "assessment-reviews"
    aware_path = review_dir / "source-aware-review.md"
    language_path = review_dir / "context-language-review.md"
    aware_id = validate_review_record(aware_path, assessment_paths, book_dir, bundle_digest, errors)
    language_id = validate_review_record(language_path, assessment_paths, book_dir, bundle_digest, errors)
    if aware_id and language_id and aware_id == language_id:
        errors.append("Assessment reviewers must have distinct Reviewer IDs")
    if aware_path.is_file() and plan_path.is_file():
        text = aware_path.read_text(encoding="utf-8")
        if field_value(text, "**Plan SHA-256:**") != sha256_file(plan_path):
            errors.append("_work/assessment-reviews/source-aware-review.md: stale review; plan digest does not match")
    if language_path.is_file():
        text = language_path.read_text(encoding="utf-8")
        expected_context_digest = sha256_file(context_file) if contextual and context_file and context_file.is_file() else "None."
        if field_value(text, "**Context SHA-256:**") != expected_context_digest:
            errors.append("_work/assessment-reviews/context-language-review.md: stale review; context digest does not match")
        if plan_path.is_file() and field_value(plan_path.read_text(encoding="utf-8"), "**Assessment format:**") == "2":
            validate_learner_review_stages(text, errors)

    if len(answer_positions) >= 4:
        letter, count = Counter(answer_positions).most_common(1)[0]
        if count / len(answer_positions) > 0.5:
            warnings.append(f"Assessment set: {letter} is correct in {count} of {len(answer_positions)} one-best questions; review answer-position variety")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book_dir", type=Path, nargs="?")
    parser.add_argument("--blind-file", type=Path, help="Print a learner copy with complete answer blocks removed")
    parser.add_argument("--print-bundle-digest", action="store_true")
    args = parser.parse_args()
    if args.blind_file:
        if args.book_dir or args.print_bundle_digest:
            parser.error("--blind-file cannot be combined with book arguments")
        try:
            print(blind_assessment(args.blind_file.read_text(encoding="utf-8")))
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
        return 0
    if args.book_dir is None:
        parser.error("provide book_dir or --blind-file")
    book_dir = args.book_dir.expanduser().resolve()
    paths = sorted((book_dir / "quizzes").glob("key-idea-*-comprehension.md"))
    review = book_dir / "review.md"
    if review.is_file():
        paths.append(review)
    if not paths:
        parser.error("no assessment files found")
    if args.print_bundle_digest:
        print(assessment_bundle_digest(paths, book_dir))
        return 0
    parser.error("use scripts/validate_output.py for full assessment validation")


if __name__ == "__main__":
    raise SystemExit(main())
