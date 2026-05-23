# Visual Management & Status Dashboard

> Brainstorm document — chưa implement.
> Tập hợp các ý tưởng về visual management cho context system.
> Trigger để làm: khi modules/ có 5+ file và human bắt đầu hỏi
> "dự án đang ở đâu rồi" thay vì tự biết.

---

## Nguồn gốc

Từ Lean Manufacturing: Andon board — mọi thứ visible tại một chỗ,
ai nhìn vào cũng biết ngay trạng thái hệ thống mà không cần hỏi.

Vấn đề hiện tại: human mở `.context/` phải scan nhiều file để biết
project đang ở đâu. Không có single source of truth cho trạng thái.

---

## Ý tưởng 1 — STATUS.md (auto-generated)

File dashboard được `context-gen` tự generate, không viết tay.

```markdown
# Project Status — [auto-generated, do not edit]
Last updated: [timestamp]

Current milestone: V1 / 0.1.0
Open tensions:     3
Modules:           5 (2 có [manual] đầy đủ, 3 còn placeholder)
Last session:      [date] — [decision chính]
Pending tags:      2 (chờ human approve)
```

**Chưa làm vì:** cần `context-gen` support để auto-generate.
Không nên viết tay — sẽ drift ngay.

---

## Ý tưởng 2 — Tauri GUI cho context system

Vì context-gen core là Python và project chính dùng Tauri (Rust + React/TS),
Tauri gọi Python qua sidecar là pattern có sẵn và fit tự nhiên.

### Use case 1 — Read: Context Dashboard
- Hiển thị STATUS.md dạng visual
- Module list với indicator: [manual] đầy đủ / còn placeholder
- Tension list: OPEN / ACTIVE count
- Current milestone progress

### Use case 2 — Write: [manual] Editor
Hai hướng chưa quyết:

**Option A — Form-based editor**
Mỗi [manual] section là form có field rõ ràng:
- Design Decisions: list với add/edit/delete
- Invariants: list với add/edit/delete
- Behavior chưa implement: list với Phase tag

Ưu: structured, khó viết sai format
Nhược: rigid, không cover case [manual] cần free-form

**Option B — Raw markdown editor với guardrail**
Editor markdown thường, nhưng:
- Highlight AUTO section với warning "đừng edit"
- Block save nếu detect thay đổi trong vùng AUTO
- Diff view trước khi save

Ưu: flexible, human quen với markdown
Nhược: guardrail phức tạp hơn để implement đúng

### Open questions
- Option A hay B cho [manual] editor?
- STATUS.md nên load vào Tầng 1 hay Tầng 2 của startup protocol?
- GUI này là tool riêng hay tích hợp vào workflow hiện tại?

---

## Prerequisites trước khi làm

1. `context-gen check-consistency` phải stable
2. V3 migration (TENSIONS split) phải complete trên tất cả projects
3. STATUS.md spec phải được define rõ trước khi implement generator
4. Quyết định Option A vs B cho [manual] editor
