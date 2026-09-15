#!/usr/bin/env python3
"""Exercise the compact assessment validator with meaningful invariants."""

from __future__ import annotations

import hashlib
import re

import validate_assessment
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "validate_output.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle_digest(book: Path) -> str:
    paths = [*sorted((book / "quizzes").glob("key-idea-*-comprehension.md")), book / "review.md"]
    manifest = "".join(f"{path.relative_to(book).as_posix()}\t{sha256(path)}\n" for path in paths)
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest()


def question(stem: str, answer: str = "A") -> str:
    return f"""{stem}

Select one answer.

**A.** Match the conclusion to the evidence.

**B.** Keep the conclusion and add a footnote.

**C.** Ask whether everyone agrees with it.

**D.** Remove the evidence from the report.

<details>
<summary>Answer</summary>

Correct answer: **{answer}**

The book's evidence rule supports A. A footnote does not repair a conclusion that is stronger than its evidence.

</details>"""


def plan_entry(context_excerpt: str = "None.", situation: str = "None.", distinction: str = "None.") -> str:
    return f"""**Source mechanism:** Conclusions should not be stronger than their evidence.
**Source anchor:** Key idea 1, evidence rule.
**Intended learner judgement:** Identify the conclusion supported by the evidence.
**Answer mode:** ONE_BEST
**Correct answers:** A
**Option rationales:** A applies the rule; B hides the mismatch; C substitutes agreement; D removes useful evidence.
**Context excerpt:** {context_excerpt}
**Proposed situation or practice:** {situation}
**Apply/Try-this distinction:** {distinction}
**Rejection risk:** The correct answer may be signalled by sounding more careful."""


def create_book(root: Path, contextual: bool) -> tuple[Path, Path]:
    book = root / "books" / "fixture-book"
    (book / "quizzes").mkdir(parents=True)
    (book / "visuals").mkdir()
    (book / "_work" / "idea-argument-packs").mkdir(parents=True)
    (book / "_work" / "assessment-reviews").mkdir()
    for name in ("source-index.md", "source-structure.md", "source-evidence.md", "key-idea-plan.md"):
        (book / "_work" / name).write_text("fixture\n", encoding="utf-8")
    (book / "metadata.yaml").write_text("title: Fixture\n", encoding="utf-8")
    (book / "overview.md").write_text("# Fixture\n\n[Key idea 1](key-idea-01.md)\n", encoding="utf-8")
    (book / "key-idea-01.md").write_text(
        "# Key idea 1\n\n## Source basis\n\nFixture source.\n\n[Back to overview](overview.md)\n",
        encoding="utf-8",
    )
    context = root / "application-context.md"
    excerpt = "Managers review an analyst's written report before a recommendation is shared."
    context.write_text(f"# Application context\n\n{excerpt}\n\nhttps://example.com/research\n", encoding="utf-8")
    context_digest = sha256(context)

    if contextual:
        plan = f"""# Assessment plan

**Assessment mode:** CONTEXTUAL
**Context path:** {context}
**Context SHA-256:** {context_digest}

## Key idea 1

**Route:** FULL
**Route reason:** The source supports recall and the context supplies a current report review.

### Quick recall

{plan_entry()}

### Apply

{plan_entry(excerpt, "A manager is deciding whether a report's conclusion matches its evidence.", "Apply asks for a judgement; Try this rehearses checking the report.")}

### Try this

**Source mechanism:** Conclusions should not be stronger than their evidence.
**Source anchor:** Key idea 1, evidence rule.
**Intended learner action:** Compare one conclusion with the evidence cited for it.
**Answer mode:** N/A.
**Correct answers:** N/A.
**Option rationales:** N/A.
**Context excerpt:** {excerpt}
**Proposed situation or practice:** Before sharing the report, compare one conclusion with its cited evidence so the wording can still be corrected.
**Apply/Try-this distinction:** Apply asks for a judgement; Try this rehearses checking the report.
**Rejection risk:** The action could become generic advice unless it names the report and present correction.

## Review question 1

{plan_entry(excerpt, "A manager is checking whether a recommendation follows from a written report.", "None.")}

Plan status: FROZEN
"""
        quiz = f"""# Key idea 1: Recall and apply

[← Back to key idea](../key-idea-01.md)

Commit to each answer before expanding its answer block.

## Quick recall

{question("What does the book's evidence rule require?")}

## Apply

{question("A manager is reviewing a written report. Which conclusion should the manager keep?")}

## Try this in your analysis environment

**When:** Before a written report is shared.

**Do:** Compare one conclusion with the evidence cited for it.

**Why now:** The wording can still be corrected before the recommendation is shared.

## Related ideas and further reading

- [Research](https://example.com/research): Evidence practice.
"""
        related = "\n## Related ideas and further reading\n\n- [Research](https://example.com/research): Evidence practice.\n"
    else:
        plan = f"""# Assessment plan

**Assessment mode:** GENERIC
**Context path:** None.
**Context SHA-256:** None.

## Key idea 1

**Route:** RECAP_ONLY
**Route reason:** Generic mode supports source-grounded recap only.

### Quick recall

{plan_entry()}

### Deeper comprehension

{plan_entry()}

## Review question 1

{plan_entry()}

Plan status: FROZEN
"""
        quiz = f"""# Key idea 1: Recall and deepen

[← Back to key idea](../key-idea-01.md)

Commit to each answer before expanding its answer block.

## Quick recall

{question("What does the book's evidence rule require?")}

## Deeper comprehension

{question("Which conclusion best respects the book's evidence rule?")}
"""
        related = ""

    (book / "_work" / "assessment-plan.md").write_text(plan, encoding="utf-8")
    (book / "quizzes" / "key-idea-01-comprehension.md").write_text(quiz, encoding="utf-8")
    (book / "review.md").write_text(
        f"""# End-of-book review

Commit to each answer before expanding its answer block.

## Question 1

{question("Which conclusion should remain in a report?")}
{related}
[← Back to overview](overview.md)
""",
        encoding="utf-8",
    )
    refresh_reviews(book, context if contextual else None)
    return book, context


def refresh_reviews(book: Path, context: Path | None, same_reviewer: bool = False) -> None:
    digest = bundle_digest(book)
    plan_digest = sha256(book / "_work" / "assessment-plan.md")
    context_digest = sha256(context) if context else "None."
    decisions = """### quizzes/key-idea-01-comprehension.md

**Findings:** None.

### review.md

**Findings:** None."""
    (book / "_work" / "assessment-reviews" / "source-aware-review.md").write_text(
        f"""# Source-aware assessment review

**Reviewer ID:** source-reviewer
**Writer and reviewer are different:** yes
**Review wave:** 1
**Plan SHA-256:** {plan_digest}
**Assessment bundle SHA-256:** {digest}

## File decisions

{decisions}

## Blockers

None.

## Advisories

None.

## Gate decision

Decision: PASS
""",
        encoding="utf-8",
    )
    language_id = "source-reviewer" if same_reviewer else "language-reviewer"
    (book / "_work" / "assessment-reviews" / "context-language-review.md").write_text(
        f"""# Context, language, and practice review

**Reviewer ID:** {language_id}
**Writer and reviewer are different:** yes
**Review wave:** 1
**Context SHA-256:** {context_digest}
**Assessment bundle SHA-256:** {digest}

## File decisions

{decisions}

## Blockers

None.

## Advisories

None.

## Gate decision

Decision: PASS
""",
        encoding="utf-8",
    )


def run(book: Path, context: Path | None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(VALIDATOR), str(book), "--mode", "assessment", "--assessment-mode", "contextual" if context else "generic"]
    if context:
        command.extend(["--context-file", str(context)])
    return subprocess.run(command, check=False, capture_output=True, text=True)


def require_failure(result: subprocess.CompletedProcess[str], message: str) -> None:
    if result.returncode == 0 or message not in result.stdout:
        raise AssertionError(f"Expected failure containing {message!r}:\n{result.stdout}\n{result.stderr}")


def use_format_two(book: Path, context: Path | None) -> None:
    plan = book / "_work" / "assessment-plan.md"
    text = plan.read_text()
    text = text.replace("# Assessment plan", "# Assessment plan\n\n**Assessment format:** 2", 1)
    text = text.replace("**Source mechanism:**", "**Learning target:**")
    text = text.replace("**Context excerpt:**", "**Context basis:**")
    text = text.replace("**Proposed situation or practice:**", "**Scenario facts:**")
    text = text.replace("**Option rationales:**", "**Reasoning:**")
    text = text.replace("**Intended learner action:**", "**Action and use:**")
    text = re.sub(r"^\*\*(?:Intended learner judgement|Apply/Try-this distinction|Rejection risk):\*\*.*\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\*\*(?:Answer mode|Correct answers|Reasoning):\*\* N/A\.\n", "", text, flags=re.MULTILINE)
    plan.write_text(text)
    refresh_reviews(book, context)
    learner = book / "_work" / "assessment-reviews" / "context-language-review.md"
    learner.write_text(learner.read_text().replace("## File decisions", """**Answers and explanations withheld until first pass saved:** yes

## First pass

The comparison of evidence with a conclusion determines the answer; practice asks for one check before sharing.

## Feedback check

The explanation distinguishes evidence from a footnote or agreement without adding facts.

## File decisions""", 1))


def check_format_two(root: Path) -> None:
    for contextual in (True, False):
        book, context = create_book(root / f"compact-{contextual}", contextual)
        context = context if contextual else None
        use_format_two(book, context)
        if (result := run(book, context)).returncode:
            raise AssertionError(f"Format 2 positive case failed:\n{result.stdout}")
        if contextual:
            plan = book / "_work" / "assessment-plan.md"
            valid = plan.read_text()
            plan.write_text(valid.replace("Managers review an analyst's written report before a recommendation is shared.", "Role: managers coach analysts on evidence and recommendations."))
            use_digest = sha256(plan)
            aware = book / "_work" / "assessment-reviews" / "source-aware-review.md"
            aware.write_text(re.sub(r"(\*\*Plan SHA-256:\*\*) .*", rf"\1 {use_digest}", aware.read_text()))
            if (result := run(book, context)).returncode:
                raise AssertionError(f"Context-consistent paraphrase should reach semantic review:\n{result.stdout}")
            plan.write_text(plan.read_text().replace("**Context basis:** Role: managers coach analysts on evidence and recommendations.", "**Context basis:** None.", 1))
            require_failure(run(book, context), "applied item requires Context basis")
        else:
            learner = book / "_work" / "assessment-reviews" / "context-language-review.md"
            valid = learner.read_text()
            learner.write_text(valid.replace("**Answers and explanations withheld until first pass saved:** yes", "**Answers and explanations withheld until first pass saved:** no"))
            require_failure(run(book, context), "staged blinding is not confirmed")
            learner.write_text(valid.replace("## First pass", "## Unrecorded first pass"))
            require_failure(run(book, context), "missing substantive First pass")

    original = question("Which conclusion fits the evidence?")
    blinded = validate_assessment.blind_assessment(original)
    assert "Which conclusion" in blinded and "**D.**" in blinded
    assert "Correct answer" not in blinded and "The book's evidence rule supports A" not in blinded
    assert "footnote does not repair" not in blinded
    for malformed in (original.replace("</details>", ""), original + "\nCorrect answer: **B**"):
        try:
            validate_assessment.blind_assessment(malformed)
        except ValueError:
            pass
        else:
            raise AssertionError("Blinding must reject an exposed answer or malformed block")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="blink-assessment-test-") as temp:
        root = Path(temp)
        check_format_two(root)
        contextual, context = create_book(root / "contextual", True)
        if (result := run(contextual, context)).returncode:
            raise AssertionError(f"Contextual positive case failed:\n{result.stdout}")

        quoted = root / "quoted-context"
        shutil.copytree(contextual.parent.parent, quoted)
        quoted_book = quoted / "books" / "fixture-book"
        plan = quoted_book / "_work" / "assessment-plan.md"
        excerpt = "Managers review an analyst's written report before a recommendation is shared."
        plan.write_text(plan.read_text().replace(excerpt, f"“{excerpt}”"), encoding="utf-8")
        refresh_reviews(quoted_book, quoted / "application-context.md")
        if (result := run(quoted_book, quoted / "application-context.md")).returncode:
            raise AssertionError(f"Quoted exact context should pass:\n{result.stdout}")

        generic, _ = create_book(root / "generic", False)
        if (result := run(generic, None)).returncode:
            raise AssertionError(f"Generic positive case failed:\n{result.stdout}")

        case = root / "pass-with-advisory"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        review = case_book / "_work" / "assessment-reviews" / "source-aware-review.md"
        review.write_text(
            review.read_text().replace(
                "## Advisories\n\nNone.",
                "## Advisories\n\nADVISORY: One optional explanation could be shorter.",
            ),
            encoding="utf-8",
        )
        if (result := run(case_book, case / "application-context.md")).returncode:
            raise AssertionError(f"PASS with an advisory should remain valid:\n{result.stdout}")

        case = root / "missing-plan"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        case_book.joinpath("_work/assessment-plan.md").unlink()
        require_failure(run(case_book, case / "application-context.md"), "Missing required assessment plan")

        case = root / "wrong-answer"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        quiz = case_book / "quizzes" / "key-idea-01-comprehension.md"
        quiz.write_text(quiz.read_text().replace("Correct answer: **A**", "Correct answer: **B**", 1), encoding="utf-8")
        refresh_reviews(case_book, case / "application-context.md")
        require_failure(run(case_book, case / "application-context.md"), "does not match the frozen assessment plan")

        case = root / "unsupported-context"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        plan = case_book / "_work" / "assessment-plan.md"
        plan.write_text(
            plan.read_text().replace(
                "Managers review an analyst's written report before a recommendation is shared.",
                "Managers hold a weekly decision meeting.",
                1,
            ),
            encoding="utf-8",
        )
        refresh_reviews(case_book, case / "application-context.md")
        require_failure(run(case_book, case / "application-context.md"), "Context excerpt is not an exact excerpt")

        case = root / "stale-review"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        quiz = case_book / "quizzes" / "key-idea-01-comprehension.md"
        quiz.write_text(quiz.read_text().replace("written report", "analysis report", 1), encoding="utf-8")
        require_failure(run(case_book, case / "application-context.md"), "stale review; assessment bundle digest does not match")

        case = root / "same-reviewer"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        refresh_reviews(case_book, case / "application-context.md", same_reviewer=True)
        require_failure(run(case_book, case / "application-context.md"), "reviewers must have distinct Reviewer IDs")

        case = root / "invalid-review-wave"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        review = case_book / "_work" / "assessment-reviews" / "source-aware-review.md"
        review.write_text(review.read_text().replace("**Review wave:** 1", "**Review wave:** 4"), encoding="utf-8")
        require_failure(run(case_book, case / "application-context.md"), "Review wave must be 1, 2, or 3")

        case = root / "pass-with-blocker"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        review = case_book / "_work" / "assessment-reviews" / "source-aware-review.md"
        review.write_text(
            review.read_text().replace(
                "## Blockers\n\nNone.",
                "## Blockers\n\nBLOCKER: The keyed answer is unsupported.",
            ),
            encoding="utf-8",
        )
        require_failure(run(case_book, case / "application-context.md"), "PASS review must record `None.` under Blockers")

        case = root / "obsolete-artifact"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        case_book.joinpath("_work/assessment-design").mkdir()
        require_failure(run(case_book, case / "application-context.md"), "Obsolete assessment-architecture artifact")

        case = root / "semantic-language-left-to-review"
        shutil.copytree(contextual.parent.parent, case)
        case_book = case / "books" / "fixture-book"
        quiz = case_book / "quizzes" / "key-idea-01-comprehension.md"
        quiz.write_text(quiz.read_text().replace("written report", "team readout"), encoding="utf-8")
        refresh_reviews(case_book, case / "application-context.md")
        if (result := run(case_book, case / "application-context.md")).returncode:
            raise AssertionError(f"Structural validator improperly judged semantic wording:\n{result.stdout}")

    print("OK: compact assessment validator tests pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
