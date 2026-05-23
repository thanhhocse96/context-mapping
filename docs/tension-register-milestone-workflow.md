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
4. Move milestone cũ sang `MILESTONES_HISTORY.md`.
5. Update current milestone trong `AGENTS.md`.

## Milestone Register

Milestone state được quản lý ở:

```text
.context/MILESTONES.md
.context/MILESTONES_HISTORY.md
```

`MILESTONES.md` là source of truth cho:

- current milestone
- status
- checklist
- transition rule

`AGENTS.md` có current milestone summary nhưng phải match `MILESTONES.md`.

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

Verification gate:

```bash
context-gen check-consistency .
```

## Migration Notes

SKVN đã migrate từ `TENSIONS.md` cũ sang:

```text
.context/TENSIONS_OPEN.md
.context/TENSIONS_ACTIVE.md
.context/TENSIONS_HISTORY.md
```

Current active decision:

- `product-grid / product-list`: `RESOLVED_ACTIVE`, V1 dùng WooCommerce native blocks/patterns; custom Product Grid/List hoặc style blocks để V2.

Current open tensions:

- quote-flow
- multilingual
- slider
- spam-protection

## Key Principle

Resolved decision vẫn phải ở gần agent chừng nào milestone hiện tại còn cần nó.

Archive chỉ xảy ra khi context scope đổi qua human-approved milestone transition, không phải ngay khi decision được đưa ra.
