# Tension Register V3 + Milestone Workflow

## Purpose

Tension Register V3 tách conflict tracking thành state files rõ ràng, machine-readable fields, tag filtering, và consistency checks. Mục tiêu là giữ context cho agent chính xác theo task, giảm drift giữa files, và tránh archive decisions quá sớm.

## Core Problem

V2 dùng một file `TENSIONS.md` để chứa cả:

- tensions chưa quyết định
- tensions đã resolved nhưng vẫn còn tác dụng trong milestone hiện tại
- historical decisions

Cách này có 3 vấn đề:

- Agent phải parse free text như `Decision: RESOLVED ...` để suy ra state.
- Agent phải đọc nhiều tension không liên quan task.
- Resolved tension dễ bị archive quá sớm hoặc để lại quá lâu.

## V3 File Model

```text
.context/TENSIONS_OPEN.md
.context/TENSIONS_ACTIVE.md
.context/TENSIONS_HISTORY.md
```

Vai trò:

- `TENSIONS_OPEN.md`: chỉ chứa `Status: OPEN`.
- `TENSIONS_ACTIVE.md`: chỉ chứa `Status: RESOLVED_ACTIVE` của milestone hiện tại.
- `TENSIONS_HISTORY.md`: chỉ chứa `Status: ARCHIVED` từ milestone/version cũ.

`TENSIONS.md` cũ không còn là source of truth sau khi migrate.

## State Machine

```text
OPEN
  └─ human decision
       └─ RESOLVED_ACTIVE
            └─ human-approved milestone transition
                 └─ ARCHIVED
```

Rules:

- `OPEN` nằm trong `TENSIONS_OPEN.md`.
- `RESOLVED_ACTIVE` nằm trong `TENSIONS_ACTIVE.md`.
- `ARCHIVED` nằm trong `TENSIONS_HISTORY.md`.
- Agent không tự chuyển milestone.
- Agent không tự archive nếu human chưa approve.

## Tension Entry Format

```markdown
## [YYYY-MM-DD HH:MM] | [module]
Tension:    Short conflict
Context:    Current task or phase
Proposal:   What agent/human wanted to do
Constraint: Manual rule or invariant in conflict
Severity:   low | high
Tags:       tag-one, tag-two
Milestone:  V1 / 0.4.0
Status:     OPEN | RESOLVED_ACTIVE | ARCHIVED
Resolved:   YYYY-MM-DD hoặc empty
Decision:   Human-readable decision text
```

Agent không được parse `Decision` để suy ra state. Chỉ dùng `Status`.

## Tag Taxonomy

Current project tags:

```text
agent
blocks
milestone
multilingual
php
quote-flow
schema
slider
spam-protection
tailwind
theme
woocommerce
```

Khi cần tag mới, update taxonomy trong `AGENTS.md` trước khi dùng.

## Load Rules

Mỗi task load theo thứ tự:

```text
1. .context/GLOBAL.md
2. .context/MILESTONES.md
3. .context/TENSIONS_OPEN.md
4. .context/TENSIONS_ACTIVE.md
5. .context/<module>.md
```

Details:

- `TENSIONS_OPEN.md`: luôn đọc đầy đủ, không filter theo tag.
- `TENSIONS_ACTIVE.md`: đọc với tag filter.
- `TENSIONS_HISTORY.md`: không load mặc định.
- Nếu không chắc entry có liên quan hay không, đọc đầy đủ.

Tag filter cho `TENSIONS_ACTIVE.md`:

- Entry match task tag → đọc đầy đủ.
- Entry không match → chỉ đọc title/status/tags.
- `Status: OPEN` không bao giờ filter.

## Move Rules

### OPEN → RESOLVED_ACTIVE

Khi human resolve tension:

1. Move entry từ `TENSIONS_OPEN.md` sang `TENSIONS_ACTIVE.md`.
2. Set `Status: RESOLVED_ACTIVE`.
3. Set `Resolved: YYYY-MM-DD`.
4. Ghi `Decision`.

### RESOLVED_ACTIVE → ARCHIVED

Chỉ khi human approve milestone/version transition:

1. Move resolved active entries của milestone cũ từ `TENSIONS_ACTIVE.md` sang `TENSIONS_HISTORY.md`.
2. Set `Status: ARCHIVED`.
3. Update `MILESTONES.md`.
4. Keep completed milestone evidence in `docs/milestones/`.
5. Update current milestone trong `AGENTS.md`.

## Milestone Register

Milestone state được quản lý ở:

```text
.context/MILESTONES.md
.context/MILESTONE_ROADMAP.md
docs/milestones/
```

`MILESTONES.md` là source of truth cho:

- current milestone
- status
- checklist
- transition rule

`MILESTONE_ROADMAP.md` là detailed backlog. Agent chỉ promote một future milestone mỗi lần, không load hoặc implement nhiều future milestones cùng lúc.

`docs/milestones/` là implemented evidence: mỗi meaningful completed slice phải có hoặc update một milestone doc tương ứng.

`AGENTS.md` có current milestone summary nhưng phải match `MILESTONES.md`.

## Program Governance Root For Monorepos

In a monorepo or product suite, governance root and code module root are not the same thing.

If one repository contains many apps, packages, plugins, or services that still share product strategy, architecture constraints, release policy, or security policy, treat the repository as one program governance root.

Rules:

- Keep one milestone source of truth at root `.context/MILESTONES.md`.
- Keep one tension system at root `.context/TENSIONS_OPEN.md`, `.context/TENSIONS_ACTIVE.md`, and `.context/TENSIONS_HISTORY.md`.
- Do not create subproject milestone authority such as `apps/web/.context/MILESTONES.md`, `plugins/foo/.context/MILESTONES.md`, or `packages/api/MILESTONES.md`.
- Scope subproject work with `Area:` or tags such as `frontend`, `api`, `plugin-a`, `cross-project`, or `program`.
- Record conflicts that affect more than one subproject as root tensions with `Area: cross-project` or `Area: program`.
- A subproject may have an implementation checklist in its README or issue tracker, but it must point back to the root milestone and must not redefine roadmap authority.
- Only create separate milestone or tension systems after a subproject has been split into its own repository, or after explicit human approval of a governance split.

Recommended milestone fields for monorepos:

```markdown
Area: <subproject | package | app | cross-project | program>
Goal: <verifiable state>
Acceptance:
- <concrete check>
Out of scope:
- <scope boundary>
Dependencies:
- <shared contract, upstream milestone, runtime, or policy dependency>
```

Recommended tension fields for monorepos:

```markdown
Area: <subproject | cross-project | program>
Milestone: <current root milestone>
Tension: <specific governance or boundary conflict>
Constraint: <root invariant being protected>
Proposal: <recommended conservative path>
Severity: low | high
Decision: [human fill in]
```

`context-gen check-consistency .` checks for nested `.context/MILESTONES.md` and nested `.context/TENSIONS_*.md` under an existing root governance system. It reports these as errors because they create competing governance authority. Plain nested `MILESTONES.md` files are warnings so humans can decide whether they are harmless implementation checklists or accidental roadmaps.

## Out-of-Band Code Change Intake

Out-of-band changes are code, artifacts, or configuration updates made outside the active agent workflow, for example a hotfix from a phone terminal, a direct developer edit, or a Gutenberg artifact fix made after testing generated HTML/Tailwind output.

The agent cannot know the developer intent from the diff alone. It must reconcile the change before continuing work when the diff may create context debt.

### Trigger Signals

Run this intake when one or more are true:

- `git status --short` shows source, artifact, config, or docs changes that the current agent did not make.
- A change touches a module that has `.context/` or `.context/modules/` ownership notes.
- A fix changes behavior, generated markup, CSS contracts, editor behavior, security/data handling, or workflow assumptions.
- A fix appears outside the current milestone acceptance checklist or contradicts out-of-scope notes.
- A test artifact or debugging session reveals a rule future agents must remember.

Do not run the full intake for trivial typo fixes, formatting-only edits, generated files with no behavior impact, or changes already explained by an issue, commit message, or existing decision doc.

### Classification

Classify the change before writing docs:

```text
within milestone goal       -> update only the smallest relevant context/docs
outside checklist           -> document why it was needed; update milestone only if acceptance changed
scope expansion             -> ask human before changing milestone scope
conflict with invariant     -> write TENSIONS_OPEN.md before proceeding
production hotfix bypass    -> record evidence and follow-up verification
```

### Dev-Facing Questions

Ask only for information missing from the diff, issue, or test output:

1. What problem did this change fix?
2. Why did it happen outside the normal milestone or agent workflow?
3. What rule, constraint, or lesson should future agents and developers remember?
4. What evidence verifies the fix, such as artifact path, test result, screenshot, URL, or reproduction note?

These answers belong in human-readable docs when the change affects future decisions.

### Agent-Facing Updates

Keep agent-facing context short and operational:

- Update the owning `.context/<module>.md` or `.context/modules/<module>.md` when future agents must know the rule before editing that module.
- Update `.context/MILESTONES.md` only when acceptance criteria, milestone guardrails, or scope state changed.
- Update `.context/TENSIONS_OPEN.md` when the change remains unresolved or conflicts with an invariant.
- Update `.context/GLOBAL.md` only for project-wide rules or newly active docs that should be discovered during startup.

Do not copy long decision rationale into `.context/`. Put rationale, evidence, alternatives, and follow-up work in `docs/decisions/`, `docs/workflows/`, or `docs/testing/`.

### Future CLI/UI Contract

A future `context-gen` UI or CLI should model this intake as a structured reconciliation record:

```yaml
change_source: dev-direct | hotfix | artifact-test | external-agent | unknown
changed_paths:
  - path
classification: within-milestone | outside-checklist | scope-expansion | invariant-conflict | production-hotfix
problem_fixed: text
outside_workflow_reason: text
future_rule: text
evidence:
  - text
agent_context_targets:
  - .context/modules/<module>.md
dev_doc_targets:
  - docs/decisions/<topic>.md
tension_required: true | false
milestone_update_required: true | false
```

The UI should optimize for short questions and prefill from `git diff`, issue text, test output, and existing context. The agent should never invent missing developer intent.

## Version Naming Rule

For context-gen, `V0`, `V1`, `V2`, and `V3` are development milestone/phase codes. They are not official package versions.

SemVer (`MAJOR.MINOR.PATCH`) starts when packaging/release artifacts exist, planned for `V3 - Packaging And Distribution`.

Before V3:

- Do not assign `0.x.y` or `1.0.0` as an official package version.
- Use `Future Candidate` if a future release version is uncertain.
- Name milestone evidence by milestone code, for example `V1_001_milestone-source-protocol.md`.

At V3:

- Define package versioning in `pyproject.toml` or equivalent metadata.
- Document installed CLI version behavior.
- Keep development checkout usage separate from installed package usage.

## Milestone Source Priority

Khi xác định scope milestone, agent dùng thứ tự source:

```text
1. Latest explicit human instruction
2. .context/MILESTONES.md current milestone
3. .context/MILESTONE_ROADMAP.md promoted milestone
4. .context/*.md manual sections and .context/modules/*.md when present
5. docs/*.md architecture/workflow decisions
6. docs/milestones/*.md implemented evidence
7. code reality
```

Docs giải thích intent, nhưng implemented behavior và tests chứng minh điều đã hoạt động.

Khi promote milestone kế tiếp:

1. Đọc roadmap entry.
2. Đọc tất cả source docs trong entry đó.
3. So sánh source docs với code hiện tại và docs/milestones evidence.
4. Copy chỉ goal, acceptance, out-of-scope, source docs của milestone đó vào `.context/MILESTONES.md`.
5. Update current milestone trong `AGENTS.md`.
6. Hỏi human nếu acceptance mơ hồ, risky, hoặc conflict.

## Transition Rule

Chỉ chuyển milestone khi:

- Tất cả acceptance checklist của milestone hiện tại đã DONE.
- Runtime smoke test liên quan đã chạy.
- Human explicitly approve chuyển milestone.

Checklist/Gantt là trigger đề xuất, không phải trigger tự động.

## Consistency Check

`context-gen check-consistency .` dùng để detect drift.

Checks chính:

- `AGENTS.md` current milestone match `.context/MILESTONES.md`.
- `TENSIONS_OPEN.md` không chứa non-OPEN entries.
- `TENSIONS_ACTIVE.md` không chứa OPEN entries.
- `TENSIONS_HISTORY.md` chỉ chứa ARCHIVED entries.
- Active entries có milestone hợp lý với current milestone.

- Nested `.context/MILESTONES.md` or `.context/TENSIONS_*.md` files are not allowed under a root governance system.
- Nested `MILESTONES.md` files outside root `.context/` are warnings because they may be mistaken for separate roadmap authority.

Verification gate:

```bash
context-gen check-consistency .
```

## Current context-gen Status

context-gen uses the V3 split tension files:

```text
.context/TENSIONS_OPEN.md
.context/TENSIONS_ACTIVE.md
.context/TENSIONS_HISTORY.md
```

Current milestone state lives in:

```text
.context/MILESTONES.md
.context/MILESTONE_ROADMAP.md
```

Existing `RESOLVED_ACTIVE` entries from `V0` remain in `TENSIONS_ACTIVE.md` until human approves archival. `check-consistency` may report them as archive candidates while current milestone is `V1 - Governance And Milestone Workflow`.

## Key Principle

Resolved decision vẫn phải ở gần agent chừng nào milestone hiện tại còn cần nó.

Archive chỉ xảy ra khi context scope đổi qua human-approved milestone transition, không phải ngay khi decision được đưa ra.
