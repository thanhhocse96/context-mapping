# context-gen Milestone Roadmap

This file is the detailed milestone backlog. `.context/MILESTONES.md` remains the active milestone pointer and should load only the current milestone in full.

When starting a new milestone, promote exactly one milestone from this roadmap into `.context/MILESTONES.md` as `Current`, then update `AGENTS.md` if the current milestone name changes.

## How To Use This File

1. Read `.context/MILESTONES.md` first.
2. If the current milestone is already defined there, use that as the active checklist.
3. Use this roadmap only to understand upcoming work or promote the next milestone.
4. Before promotion, re-read the listed source docs and module contexts.
5. If source docs conflict, stop and ask the human which source wins.
6. If acceptance cannot be made concrete, ask the human before coding.

## Source Priority

Use this order when extracting milestone truth:

```text
1. Human's latest explicit instruction
2. .context/MILESTONES.md current milestone
3. .context/MILESTONE_ROADMAP.md promoted milestone
4. .context/*.md manual sections and .context/modules/*.md when present
5. docs/*.md architecture and workflow decisions
6. docs/milestones/*.md implemented evidence
7. code reality
```

Docs can explain intent, but implemented behavior and tests prove what already works.

## Version Naming Rule

`V0`, `V1`, `V2`, and `V3` are development milestone/phase codes. They are not package release versions.

SemVer (`MAJOR.MINOR.PATCH`) becomes meaningful only when context-gen has packaging/release artifacts, currently planned for `V3 - Packaging And Distribution`.

Before V3:

- Do not assign an official `0.x.y` or `1.0.0` package version.
- Use `Future Candidate` when a release version is uncertain.
- Keep milestone docs named by milestone code, for example `V1_001_...`.

At V3:

- Define package versioning in `pyproject.toml` or equivalent metadata.
- Document installed CLI version behavior.
- Keep development checkout usage separate from installed package usage.

## Completed Milestones

### V0 - Registry, Staleness, And Tension V3 Foundation

Status: completed.

Goal: establish the context-gen core contract and V3 governance foundation.

Source docs:

```text
.context/GLOBAL.md
docs/00_conceptual-model.md
docs/tension-register-milestone-workflow.md
docs/milestones/V1_001_milestone-source-protocol.md
```

Acceptance:

- [x] Registry-based parser dispatch.
- [x] Language-aware signatures.
- [x] Clean `load` stdout.
- [x] Manual section preservation.
- [x] Hash-based staleness detection.
- [x] Split tension files.
- [x] Consistency checker.

## Current Milestones

### V1 - Governance And Milestone Workflow

Status: active.

Goal: make milestone scope, promotion, documentation, and agent startup rules explicit for context-gen itself and for projects that use it.

Primary sources:

```text
AGENTS.md
docs/tension-register-milestone-workflow.md
docs/00_conceptual-model.md
docs/prompts/01_init-project-with-context-mapping.md
../ZeroClaw-Vbee-Automate/AGENTS.md
../ZeroClaw-Vbee-Automate/.context/MILESTONES.md
../ZeroClaw-Vbee-Automate/.context/MILESTONE_ROADMAP.md
```

Acceptance:

- [x] Active milestone pointer exists.
- [x] Roadmap/backlog exists.
- [x] Startup protocol reads milestone state before task scope decisions.
- [x] Promotion protocol requires source docs and human clarification for vague acceptance.
- [x] Implemented slice docs are stored under `docs/milestones/`.
- [x] Human reviews and archives old V0 active tensions.

Out of scope:

- Automatic milestone promotion.
- Automatic tension archival.
- Changing parser behavior.

## Backlog Milestones

### V2 - Parser Coverage And Self-Scan Hardening

Goal: make context-gen scan its own Python code correctly and avoid local environment artifacts such as `.venv/`.

Primary sources:

```text
.context/GLOBAL.md
docs/prompts/00_add-parser.md
docs/prompts/01_init-project-with-context-mapping.md
AGENTS.md
```

Acceptance:

- [ ] Python parser proposal is approved before coding.
- [ ] Parser registers through `register_plugin()`.
- [ ] `cli.py` receives only the parser import line.
- [ ] Python parser extracts functions, classes, imports, and relevant entrypoints.
- [ ] Parser discovery skips local environment directories such as `.venv/`, `venv/`, `__pycache__/`, and `.local/`.
- [ ] `python cli.py build . --quiet` does not generate context for local artifacts.
- [ ] `check-consistency` passes without milestone missing warning.
- [ ] V2 milestone doc and test report are created.

Out of scope:

- Go parser.
- PyPI packaging.
- Multi-language merge strategy.

Ask human before coding if:

- Parser scope needs decorators, CLI commands, or non-standard Python entrypoints.
- Dependency install requires network access.
- Existing `.context/*.md` manual sections are missing or stale.

### V3 - Packaging And Distribution

Goal: make context-gen easier to install and run from application projects without relying on ad hoc sibling paths.

Primary sources:

```text
README.md
docs/prompts/01_init-project-with-context-mapping.md
requirements.txt
```

Acceptance:

- [ ] Packaging proposal is approved before coding.
- [ ] `pyproject.toml` or equivalent packaging metadata exists.
- [ ] SemVer package versioning rule is defined.
- [ ] CLI entrypoint is documented.
- [ ] Install instructions distinguish development checkout from installed tool use.
- [ ] Existing sibling path workflow remains documented for local development.

Out of scope:

- Publishing to PyPI without human approval.
- Breaking current `python cli.py ...` usage.
