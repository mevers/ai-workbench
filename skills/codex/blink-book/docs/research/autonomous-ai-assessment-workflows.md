# Comparative research: autonomous AI assessment skills

## Research question

Which public AI skills or agent workflows can autonomously:

1. create an assessment from a specified source;
2. tailor it to a specified application context, such as the work of a data-science manager; and
3. plan, generate, review, repair, validate, and release the assessment using sound AI-skill design?

These requirements are cumulative. A quiz generator is not a complete match if it is not source-bound, context-grounded, and capable of running a controlled end-to-end workflow.

## Scope and evidence standard

The review was conducted on 27–28 August 2026. It covers assessment construction and review. Summarisation, source extraction, Blink prose, visuals, and key-idea generation are outside its scope.

Catalogue descriptions were used only to discover candidates. Findings were taken from published `SKILL.md` files and their supporting references, templates, validators, rubrics, and evaluation cases. The sample is broad but not exhaustive, and the review did not independently benchmark runtime performance.

### Search coverage

- Cross-platform catalogues: [VoltAgent Awesome Agent Skills](https://github.com/VoltAgent/awesome-agent-skills), [Skill Me](https://github.com/SkillMedev/skills), [GitHub Awesome Copilot](https://github.com/github/awesome-copilot), [ClawHub](https://clawhub.ai/skills), and [Awesome Claude Skills](https://awesomeclaude.ai/awesome-claude-skills).
- Education-focused libraries: [Education Agent Skills](https://github.com/GarethManning/education-agent-skills), [Anthropic K–12 Teacher Skills](https://github.com/anthropics/k12-teacher-skills), [Learning Commons Agent Skills](https://github.com/learning-commons-org/agent-skills), [Claude Skills for Intelligent Textbooks](https://github.com/dmccreary/claude-skills), [Claude for Education](https://github.com/lonj7798/claude-for-education), and [School Skills](https://github.com/Jellypod-Inc/school-skills).
- Focused assessment and tutoring repositories: [Learn Anything](https://github.com/Nar101/learn-anything), [Ask Me Paper](https://github.com/tuananhbui89/skills/blob/main/ask-me-paper/SKILL.md), [Tutor Skills](https://github.com/bevibing/tutor-skills), [MCQ Maker](https://github.com/hammadshakeelai/mcq-maker), the [Skillsmith repository](https://github.com/xiongxianfei/skillsmith) and its [Quiz Generator](https://github.com/xiongxianfei/skillsmith/blob/main/skills/quiz-generator/SKILL.md), and [Agent Skills Library: Quiz Developer](https://github.com/mcroitor/agent-skills-library/blob/main/education/quiz-developer/SKILL.md).

### Direct-comparator inclusion test

A candidate counted as a direct comparator only if it visibly implemented most of the following:

1. accepts or resolves supplied source material and keeps questions within an explicit source boundary;
2. defines the learning objective, mechanism, or evidence target before drafting;
3. adapts the assessment to a learner, role, domain, or application context;
4. provides concrete rules for ambiguity, distractors, rationales, transfer, or observable performance;
5. records source or design provenance at item level; and
6. performs a preflight, validation, independent review, or regression evaluation that can reject an item or run.

These are the criteria used in the original comparison. They are project evaluation criteria, not definitions supplied by one external source.

## Executive answer

No reviewed public AI skill meets the complete requirement.

[Learn Anything](https://github.com/Nar101/learn-anything/blob/main/SKILL.md) is the closest comparator. It combines supplied sources, an explicit application context, precommitted grading, assessment generation, differentiated mastery evidence, blocking preflight checks, and evaluation cases. It is an interactive tutor rather than a static assessment workflow, and assessment is mainly performed by the same tutor that created the learning experience.

The other candidates provide substantive components: source boundaries, quiz blueprints, misconception-based distractors, learner adaptation, transfer tasks, validators, or evaluation fixtures. None combines all of them into one enforced workflow with independent semantic review.

No first-party OpenAI skill specifically for source-grounded educational assessment was found in the reviewed public repository. OpenAI's contribution to the comparison is therefore skill architecture and evaluation guidance, not a first-party assessment method.

## AI-skill design evidence

### OpenAI and Codex

- OpenAI's [skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) separates concise workflow instructions from references and deterministic scripts and calls for validation on real tasks.
- OpenAI's [evaluate-skill](https://github.com/openai/plugins/blob/main/plugins/plugin-eval/skills/evaluate-skill/SKILL.md) separates structural findings from observed benchmark behaviour and builds benchmark scenarios before recommending a rewrite.
- [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/) describes skills as bundles of instructions, resources, and scripts for repeatable work.

The implication recorded in the original research is to keep semantic design rules in the skill, stable record formats in templates, and mechanically testable invariants in scripts; then test known good and known bad assessment cases. This favours explicit artefacts and executable checks over a larger collection of aspirational adjectives.

### Anthropic and Claude Code

- Anthropic's [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) evaluates representative prompts with and without the skill and converts observed failures into assertions.
- Anthropic's [skill-authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) emphasises concise, structured instructions and testing through real use. [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) recommends starting from observed capability gaps and using code where deterministic reliability is required.
- Anthropic's [agent-evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) recommends combining code, model, and human graders because they detect different failure classes.

The assessment implication recorded in the original research is to use code for structural parsing, a source-aware reviewer for fidelity and teaching value, and a source-blind reviewer for literal usability.

### GitHub Copilot

- GitHub's [Agent Skills documentation](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) treats skills as focused task instructions with optional scripts and examples.
- GitHub's guidance on [customising code review](https://docs.github.com/en/copilot/tutorials/customize-code-review) warns that vague instructions add noise and recommends short, direct rules.
- GitHub's [Exam Ready skill](https://github.com/github/awesome-copilot/blob/main/skills/exam-ready/SKILL.md) stays within supplied material and creates one practice question per syllabus topic. It demonstrates a source boundary, but not applied judgement, diagnostic distractors, contextual practice, or independent review.

The original research connects the code-review guidance directly to its observation that repeated “be concrete” gates had not reliably improved assessment writing.

## Direct comparator findings

### Learn Anything

[Learn Anything](https://github.com/Nar101/learn-anything/blob/main/SKILL.md) is a source-grounded adaptive tutor rather than a static book-assessment generator. Its assessment subsystem implements the most complete set of relevant controls found:

- It creates an observable mastery contract with `application_context` and `mastery_evidence`, separates source claims from tutor synthesis and learner-application assumptions, and maps key claims to sources.
- Its [assessment-integrity protocol](https://github.com/Nar101/learn-anything/blob/main/references/assessment-integrity.md) requires each question to record `source_claims`, the target node, answer or rubric, acceptable variants, rationale, common wrong answers, grading rules, and a hint ladder before delivery.
- Its [assessment template](https://github.com/Nar101/learn-anything/blob/main/templates/assessment.yaml) checks source sufficiency, an explicit target, a frozen answer or rubric, mutually exclusive options, realistic behaviour, and required prerequisites. Any failed field blocks delivery.
- Strategic, commercial, diagnostic, and creative judgement defaults to open response with a frozen rubric rather than an artificially unique multiple-choice answer. The skill also rejects scenarios in which a character unrealistically states a normally hidden judgement.
- It distinguishes `guided`, `independent`, `transferable`, and `durable` evidence, blocks progression after transfer failure, and does not count prompted success as independent mastery.
- Its [quality rubric](https://github.com/Nar101/learn-anything/blob/main/rubrics/tutor-quality-rubric.md) defines critical failures, pass thresholds, positive and adversarial evaluation cases, answer-consistency tests, and structural validation. Failed cases must be repaired and re-evaluated.

Its limitations are equally material: it is an interactive, stateful course runtime, not an assessment generator for an existing Blink; assessment is primarily performed by the tutor itself; and it does not use separate source-aware and source-blind reviewers. Its source-to-application separation and precommitted grading are stronger than in most reviewed quiz skills, while the project's independent semantic review remains an additional control.

### Other substantive comparators

| Skill or library | Controls observed | Gaps observed against the inclusion test |
| --- | --- | --- |
| [Skillsmith Quiz Generator](https://github.com/xiongxianfei/skillsmith/blob/main/skills/quiz-generator/SKILL.md) | Extracts objectives and a knowledge map; creates a blueprint before drafting; records cognitive level, difficulty, answer rationales, remediation feedback, and per-item source; rejects hidden context, unsupported advanced facts, ambiguity, shallow recall when transfer is intended, and redundant items. | Uses the generator's self-check. It has no independent assessment reviewer, frozen pre-delivery record, or executable semantic acceptance test. |
| [Ask Me Paper](https://github.com/tuananhbui89/skills/blob/main/ask-me-paper/SKILL.md) | Maps thesis, claims, evidence, definitions, assumptions, limitations, and implications; remains source-bound; uses misconception-based distractors and comparable option length and tone; corrects source misunderstandings before continuing. | Designed for conversational paper comprehension, not tailored workplace application or reusable static assessment. It has no item-level design record or independent review gate. |
| [Education Agent Skills](https://github.com/GarethManning/education-agent-skills) | Provides typed context inputs and explicit chaining. The [Assessment Validity Checker](https://github.com/GarethManning/education-agent-skills/blob/main/skills/curriculum-assessment/assessment-validity-checker/SKILL.md), [Hinge Question Designer](https://github.com/GarethManning/education-agent-skills/blob/main/skills/questioning-discussion/hinge-question-designer/SKILL.md), [Transfer Bridge](https://github.com/GarethManning/education-agent-skills/blob/main/skills/student-learning/transfer-bridge/SKILL.md), and [Assessment Design Orchestrator](https://github.com/GarethManning/education-agent-skills/blob/main/skills/original-frameworks/assessment-design-orchestrator/SKILL.md) cover construct validity, misconception-diagnostic distractors, immediate instructional decisions, near and far transfer, equity, and stop conditions. | These are modular teacher workflows, not one source-bounded pipeline. Most quality control is prompt self-check or teacher judgement; there is no per-item source record plus two independent review lenses. |
| [Intelligent Textbooks Quiz Generator](https://github.com/dmccreary/claude-skills/blob/main/skills/quiz-generator/SKILL.md) | Reads chapter content, course description, learning graph, and glossary; refuses or caps work when content is thin; records concept, source section, Bloom level, difficulty, and distractor quality; produces aggregate coverage and quality reports. | Its numeric quality score is generated largely by the workflow judging itself. Fixed Bloom distributions and answer-position balance do not establish contextual usefulness, and no independent reviewer checks applied or practice cases. |
| [MCQ Maker](https://github.com/hammadshakeelai/mcq-maker/blob/main/.claude/skills/mcq-maker/SKILL.md) | Converts a supplied document into MCQs, applies a detailed authoring guide, and runs a validator before building the quiz. The validator checks schema and detectable option-pattern defects; the skill requires plausible distractors and understanding rather than recognition. | Strong on packaging and mechanical validation, but it does not model application context, distinguish judgement from practice, or independently review semantic relevance. |
| [Tutor Skills](https://github.com/bevibing/tutor-skills/blob/main/skills/tutor/SKILL.md) | Builds a source-mapped study vault, reads relevant source notes before each round, uses domain misconceptions as distractors, tracks concept-level errors, and retests weak concepts in a new context. | The quiz stage has no required item-level source anchor, precommitted answer record, application payoff, or independent review. Proficiency percentages are state, not evidence of transfer or durable mastery. |
| [Claude for Education: Edu Quiz Generator](https://github.com/lonj7798/claude-for-education/blob/main/claude/agents/edu-creator/skills/edu-quiz-generator/SKILL.md) | Resolves explicit `source_refs`, maps questions evenly to chapter objectives, calibrates question form and hints to difficulty, derives distractors from related material, caps question count to source capacity, and asks advanced questions to differ from worked examples. | The wider system is context-rich and multi-agent, but the quiz step has no independent item reviewer or blocking preflight for vague, unrealistic, or contextually pointless practice. |
| [Agent Skills Library: Quiz Developer](https://github.com/mcroitor/agent-skills-library/blob/main/education/quiz-developer/SKILL.md) | Reviews objectives and source material, groups content domains, maps items to outcomes, balances difficulty, and checks clarity and coverage. | Its rules remain high-level. It lacks item-level source evidence, misconception records, realistic domain anchors, rejection cases, and independent review. |
| [Skill Me Quiz Generator](https://github.com/SkillMedev/skills/blob/main/skills/quiz-generator/SKILL.md) | Is portable across Claude Code, Codex, and other Agent Skills clients; declares a cognitive-level blueprint before drafting; maps every distractor to a named misconception; provides per-option rationales; and checks whether a prepared learner could defend another answer. | Not inherently source-bound and has no required application-context evidence, item-level source provenance, or independent second pass. |
| [GitHub Exam Ready](https://github.com/github/awesome-copilot/blob/main/skills/exam-ready/SKILL.md) | Refuses outside knowledge and restricts questions to supplied material and syllabus topics. | Produces one recall question per topic, without application design, distractor diagnostics, practice logic, or semantic quality assurance. |

## Evaluation architecture outside quiz generators

Two official education libraries provide relevant evaluation architecture but are not direct assessment-generation comparators:

- [Anthropic K–12 Teacher Skills](https://github.com/anthropics/k12-teacher-skills) publishes lesson-planning and differentiation skills alongside evaluation rubrics.
- [Learning Commons Agent Skills](https://github.com/learning-commons-org/agent-skills) publishes skills with separate model-judged rubrics for pedagogy, rigour, formatting, and scaffolding.

The observed pattern is separation between authoring instructions and reusable evaluation criteria. Neither repository is evidence for assessment-item rules it does not contain.

[Cold Read](https://github.com/cogpros/cold-read) is a non-education review pattern that freezes a rubric and uses cold reviewers plus reconciliation. It is not a direct assessment comparator; it supports only the narrower use of reviewers isolated from author intent.

## Conclusions supported by the comparison

The original comparative analysis reached these conclusions:

- The public sample contains many partial and several strong comparators. It does not contain the complete enforced workflow sought here.
- Useful implemented controls include source boundaries, blueprint-first generation, misconception-based distractors, transfer tasks, realistic-behaviour checks, source-capacity limits, precommitted answers or rubrics, validators, and adversarial evaluation cases.
- Learn Anything shows that item-level source claims, frozen grading, blocking preflight checks, transfer evidence, critical failures, repair, re-evaluation, and executable validation can coexist in one AI tutoring workflow.
- A checklist inside the generator remains self-review. In the reviewed architectures, a separate artefact or reviewer is required for a check that can independently fail an item, identify the evidence, and require another run.
- No reviewed public skill combines the project's fixed book source, separate application-context file, distinct Quick recall/Apply/Try this functions, item-level design records, present-usefulness constraints, source-aware and source-blind reviewers, mixed-review novelty checks, and deterministic positive and negative fixtures.

The final point describes the project's target combination. It is not a claim that every component is required for all autonomous assessment systems.

## Assessment-design evidence

- Carnegie Mellon's guidance on [alignment among objectives, assessment, and instruction](https://www.cmu.edu/teaching/assessment/basics/alignment.html) says an assessment task must reveal the specific learning objective. The original research uses this to support recording the intended judgement before drafting and rejecting questions that merely mention the topic.
- The American College of Surgeons' [multiple-choice item-writing guidelines](https://www.facs.org/for-medical-professionals/education/cme-resources/test-writing/) require one correct or best answer and grammatically consistent distractors. The NBME describes the same [focused one-best-answer structure](https://www.nbme.org/news/engaging-faculty-item-writing-workshops/). The original research uses these sources to support one decision point and a comparable option family.
- Roediger and Karpicke's study of [test-enhanced learning](https://pubmed.ncbi.nlm.nih.gov/16507066/) found that retrieval practice improves later retention. The original research uses this to support source-based recall while keeping it distinct from contextual application.
- Cardiff University's [authentic-assessment guidance](https://sites.cardiff.ac.uk/education-development-toolkit/key-principles/principle-5-assessment-as-learning/authentic-assessment/) asks whether assessment transfers into work resembling expert thought and action, with a recognisable product or performance. The original research uses this to support familiar, consequential domain situations rather than decorative context.
- The University of Oklahoma's [rubric guidance](https://www.ou.edu/assessment/resources/rubrics) requires observable, measurable, distinct, precise, and unambiguous criteria. The original research uses this to support review decisions tied to quoted evidence and named repairs.

These sources support individual assessment-design principles. They do not establish the complete autonomous AI workflow.

## Project-specific design decisions recorded in the original research

The original document adopted the following rules for the Blink Book assessment workflow. These are local design decisions informed by the comparison, not findings claimed by the external sources:

1. **Blueprint before prose.** Each key idea receives an assessment-design record containing the source anchor, tested mechanism, domain anchor, intended judgement, separate Apply and Try this functions, and rejection risks before drafting.
2. **One construct per item.** Quick recall retrieves one source idea; Apply tests one immediate judgement; Try this guides one distinct act of practice. A wrong response should diagnose a specific misconception or timing/trade-off error.
3. **Present usefulness.** A contextual situation should resemble a familiar decision for the configured role, and the action should improve the current conversation, decision, or work product. A future audience or recurrence cannot be its only rationale.
4. **Diagnostic distractors.** Map every wrong option to a misconception, incomplete application, or wrong trade-off; rewrite the item if another option is defensible.
5. **Reviewers cannot fill gaps.** A source-aware reviewer checks fidelity, mechanism, contextual relevance, component distinction, distractors, and case novelty. A source-blind reviewer checks literal language, defined terms, observable action, present payoff, and practical usability across every assessment component.
6. **Mixed graders.** Code checks file structure, required records, placeholders, answer syntax, and suspicious overlap. Independent reviewers judge semantic quality. Neither layer may claim the other's result.
7. **Repair and re-review.** Return failed components to the same reviewer after revision and require a fresh pass for every assessment file.
8. **Regression fixtures.** Positive and negative examples exercise assessment mode while Blink-mode commands and content-quality validation remain unchanged.

## Limits and exclusions

- The public sample is not exhaustive.
- Published instructions describe intended workflows; this review did not independently verify their runtime behaviour or output quality.
- Interactive tutors and static assessment generators address different products, even when their assessment controls overlap.
- Catalogue descriptions were not treated as evidence of implementation.
- Advice about ingestion, topic extraction, summarisation, lesson sequencing, diagrams, and explanatory prose was deliberately excluded because it falls outside assessment construction and review.

The original research therefore left existing Blink source processing and content-generation instructions unchanged.
