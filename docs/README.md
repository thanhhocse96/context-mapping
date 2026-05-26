# Documentation Index

Docs are split into four layers:

```text
docs/
  00_...                    # conceptual and governance overview
  tension-register-...      # workflow/governance details
  milestones/               # implemented milestone evidence
  prompts/                  # reusable agent prompts
  templates/                # committed examples for local-only files
```

## Naming Rules

General docs use numeric order:

```text
00_<name>.md
01_<name>.md
```

Milestone docs use:

```text
<milestone>_<sequence>_<name>.md
```

Example:

```text
V1_001_milestone-source-protocol.md
```

The milestone code must match `.context/MILESTONES.md`.

## Agent Rules

When an agent completes a meaningful implementation slice, it must create or update a milestone doc.

Milestone docs should start with workflow first, preferably Mermaid, then explain:

```text
what was implemented
files changed or added
design patterns used
verification commands or acceptance checks
known limits
```

After adding, moving, or renaming a docs file, update this index.

## Core Docs

1. [Conceptual Model](00_conceptual-model.md)
2. [FAQ](01_faq.md)
3. [Tension Register Milestone Workflow](tension-register-milestone-workflow.md)

## Prompts

1. [Add Parser Plugin](prompts/00_add-parser.md)
2. [Init Project With Context Mapping](prompts/01_init-project-with-context-mapping.md)

## Templates

1. [Local Environment Example](templates/00_local-environment.example.md)

## Implemented Milestone Docs

### V1 - Governance And Milestone Workflow

1. [Milestone Source Protocol](milestones/V1_001_milestone-source-protocol.md)
