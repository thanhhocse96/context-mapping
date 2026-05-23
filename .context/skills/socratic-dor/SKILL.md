---
name: socratic-dor
description: Activate when human request is vague, reference-based, or scope is too large for a single task. Guides agent through structured brainstorm using Socratic questioning to reach Definition of Ready, then captures output into project context or chat summary.
---

## When to Activate

Activate this skill when the human message matches any of these trigger categories:

**Category 1 — Explicit brainstorm request**
"brainstorm", "not sure", "help me think", "want to discuss", "still vague", "chưa rõ", "muốn thảo luận"

**Category 2 — Reference-based request (implicit vagueness)**
"like X", "similar to X", "something like X"
"create an app / web / tool..."
"I want to build something that..."

**Category 3 — Scope too large for one task**
"the whole system", "everything", "end to end", "from scratch"

**Opt-out keywords** — human can exit protocol at any point:
"that's enough", "let's start", "skip brainstorm", "đủ rồi", "bắt đầu làm đi"

---

## The Three DoR Slots

Track these internally throughout the session. Do not show them to the human until Phase 3.

```
Module:   [which part of the project / domain] — or "unclear"
Outcome:  [what must be true when done, expressed as behavior] — or "unclear"
Constraint: [known limits, rules, or invariants] — or "unclear"
```

---

## Phase 1 — Socratic Probe

One question per turn. Never ask all three DoR slots at once.

After each human response:
1. Summarize what you understood in 1–2 sentences
2. Ask one focused question based on the largest remaining gap

**Question type mapping — choose based on current gap:**

| Gap | Socratic type | Example |
|-----|--------------|---------|
| Outcome unclear | Clarification | "What would a user be able to do when this is done?" |
| Human describes implementation, not outcome | Assumptions | "What problem does that implementation solve?" |
| Reason behind request unclear | Evidence | "Why is this important right now?" |
| Scope seems too narrow or too wide | Perspective | "Is there another way to frame this problem?" |
| Consequences not considered | Implications | "If this works perfectly, what changes for the user?" |
| Direction feels arbitrary | Meta | "Why is this the right problem to solve first?" |

**Turn format:**

```
I understood: [1–2 sentence summary]
Question: [one focused question]
```

**Rules:**
- Never ask "what do you want?" — too broad
- If human answers with implementation → redirect to outcome
- If human answers with a problem → ask who has it and when
- Do not explain Socratic method unless human asks why you keep asking

---

## Phase 2 — Compress

Trigger automatically every ~3 turns. Do not wait for human to ask.

```
Here's what I've understood so far:

- Module:     [value or "still unclear"]
- Outcome:    [value or "still unclear"]
- Constraint: [value or "still unclear"]

Still open:
- [biggest remaining gap]

Next question: [one question targeting that gap]
```

Human confirms, corrects, or adds → return to Phase 1.

---

## Phase 3 — Definition of Ready Check

Agent self-detects when all three slots are sufficiently clear. Do not wait for human declaration.

Present to human:

```
I think we have enough to begin. Confirming:

- Module:      [X]
- Outcome:     [specific behavior, verifiable]
- Constraint:  [Y — from [manual] or human-confirmed]

Would you like to:
[ ] End brainstorm, capture to context, begin implementation
[ ] Continue clarifying
```

If human chooses to continue → return to Phase 1.
If human chooses to end → proceed to Phase 4.

---

## Phase 4 — Capture

### If `.context/GLOBAL.md` exists (project with context system)

```
Session summary — [date]

Module:      [X]
Outcome:     [behavior]
Constraint:  [Y]

Decisions made:
- [decision 1]
- [decision 2]

Open questions:
- [if any]

→ Write to: .context/modules/[X].md — [manual] section
→ If new constraint: TENSIONS_OPEN.md
→ If new tag needed: add to Pending tags in AGENTS.md, ask human to approve now
```

### If no context system detected

Output a summary block in chat:

```
Brainstorm Summary — [date]

Module / Domain: [X]
Outcome:         [behavior]
Constraint:      [Y]

Decisions:
- [decision 1]
- [decision 2]

Open questions:
- [if any]
```

Human decides what to do with this output.

---

## Invariants

- Never skip Phase 1 and go straight to implementation after trigger
- Never ask more than one question per turn
- Never explain Socratic method unsolicited
- Never auto-capture without human confirmation in Phase 3
- Always compress every ~3 turns even if human seems ready to proceed
- Opt-out keyword → stop protocol immediately, proceed with whatever is known
