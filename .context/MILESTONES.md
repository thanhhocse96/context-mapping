# Milestones

Current: V1 - Governance And Milestone Workflow

Detailed roadmap source: `.context/MILESTONE_ROADMAP.md`.

This file is the active milestone pointer. Load the current milestone in full. Use `.context/MILESTONE_ROADMAP.md` as backlog, and promote only one future milestone at a time.

## Version Naming Rule

- `V0`, `V1`, `V2`, `V3` are development milestone/phase codes, not package release versions.
- SemVer (`MAJOR.MINOR.PATCH`) starts when context-gen has packaging/release artifacts, planned for `V3 - Packaging And Distribution`.
- Before V3, do not assign `0.x.y` or `1.0.0` as an official package version.
- If future release version is uncertain, write `Future Candidate` instead of inventing a SemVer.
- `MAJOR` will increase for architecture or product-scope breaks after package versioning exists.
- `MINOR` will increase for compatible feature additions after package versioning exists.
- `PATCH` will increase for fixes/hardening after package versioning exists.
- Do not change the current milestone or future package version without explicit human approval.

## Completed: V0 - Registry, Staleness, And Tension V3 Foundation

Goal: establish the context-gen core contract and V3 governance foundation.

Acceptance:

- [x] Parser registry dispatch replaces language-specific `if/elif` dispatch.
- [x] Rust, TypeScript/TSX, PHP, and PowerShell parser plugins register through `register_plugin()`.
- [x] `load` keeps stdout clean.
- [x] `[manual]` sections are preserved by merge logic.
- [x] Staleness hash is injected into `AUTO_START`.
- [x] Staleness entries write to `TENSIONS_OPEN.md`.
- [x] `check-consistency` validates split tension files.

Out of scope:

- PyPI packaging.
- Python parser.
- Go parser.
- Automatic archival of resolved tensions.
- Multi-language directory merge strategy.

## Current: V1 - Governance And Milestone Workflow

Goal: make milestone scope, promotion, documentation, and agent startup rules explicit for context-gen itself and for projects that use it.

Acceptance:

- [x] `.context/MILESTONES.md` exists as the active milestone pointer.
- [x] `.context/MILESTONE_ROADMAP.md` exists as the detailed backlog.
- [x] `AGENTS.md` declares the current milestone and milestone source protocol.
- [x] Documentation explains active checklist vs roadmap/backlog.
- [x] Implemented milestone evidence is stored under `docs/milestones/`.
- [x] `check-consistency` reports no missing milestone warning.
- [x] Remaining V0 active tensions are reviewed and archived after human approval.

Out of scope:

- Auto-promoting milestones.
- Auto-archiving tension entries.
- Rewriting historical tension decisions.
- Implementing new parser languages.

## Next: V2 - Parser Coverage And Self-Scan Hardening

Goal: make context-gen scan its own Python code correctly and avoid local environment artifacts such as `.venv/`.

Promotion source: `.context/MILESTONE_ROADMAP.md#V2 - Parser Coverage And Self-Scan Hardening`.

Before coding V2:

- [ ] Re-read `.context/GLOBAL.md`.
- [ ] Re-read `docs/prompts/00_add-parser.md`.
- [ ] Re-read `docs/prompts/01_init-project-with-context-mapping.md`.
- [ ] Promote V2 goal, acceptance, out-of-scope, and source docs from `.context/MILESTONE_ROADMAP.md`.
- [ ] Ask human to approve parser scope before implementation.
