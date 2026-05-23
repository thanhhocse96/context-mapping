# Governance Methodology

> Decision log — không phải proposal, không phải documentation.
> Ghi lại các quyết định phương pháp làm việc được hình thành từ thực tế.
> Audience: human. Agent không load file này mặc định.
> Đọc file này để hiểu tại sao hệ thống hoạt động như vậy.

---

## Quyết định 1 — Folder Structure vs Agent Protocol

**Context hình thành:**
Dự án bắt đầu gom nhiều loại file vào `.context/` mà không phân loại.
Planning snapshots, governance files, module context, proposals nằm chung một chỗ.
Human mở folder cảm thấy overwhelmed. Có câu hỏi: restructure folder có giải quyết được không?

**Quyết định:**
Folder structure và agent startup protocol là hai thứ tách biệt, phục vụ hai mục đích khác nhau.

**Lý do:**
- Folder structure phục vụ human — giảm visual noise khi mở editor
- Startup protocol phục vụ agent — định nghĩa load order và priority
- Agent không học priority từ folder depth. Agent học từ AGENTS.md.
- Restructure folder mà không update protocol = clean folder + broken agent behavior

**Áp dụng:**
- Conservative structure: giữ governance files flat, group modules/ planning/ proposals/
- AGENTS.md là source of truth cho agent behavior, không phải folder layout
- Không move governance files mà không update protocol đồng thời

---

## Quyết định 2 — Startup Protocol 3 Tầng

**Context hình thành:**
Startup protocol cũ load theo file type, không theo relevance.
Agent load TENSIONS_ACTIVE.md toàn bộ dù task không liên quan đến phần lớn nội dung.
Signal/noise ratio giảm khi project lớn lên.

**Quyết định:**
Tách startup protocol thành 3 tầng theo tần suất và depth của load.

**Lý do:**
- Tầng 1 (Always full): file nhỏ, luôn relevant — GLOBAL.md, TENSIONS_OPEN.md
- Tầng 2 (Always filtered): file lớn, chỉ đọc phần liên quan — TENSIONS_ACTIVE.md, MILESTONES.md
- Tầng 3 (On demand): chỉ load khi task liên quan — modules/, planning/
- Separation of concerns theo tần suất đọc, không chỉ theo loại file

**Áp dụng:**
- TENSIONS_OPEN.md luôn đọc full — không filter
- TENSIONS_ACTIVE.md đọc theo tag match với task
- Status OPEN trong bất kỳ file nào → luôn đọc full, bất kể tag
- Sau load xong → check TENSIONS_OPEN trước khi proceed

---

## Quyết định 3 — Tag Taxonomy + Pending Rule

**Context hình thành:**
Agent tự infer tag từ task description → inconsistent giữa các session.
Taxonomy có nhưng chưa có rule xử lý khi phát sinh domain mới mid-task.

**Quyết định:**
Tag taxonomy cố định trong AGENTS.md. Tag mới phải được human approve trước khi dùng.
Pending tags có section riêng ngay dưới taxonomy. Agent hỏi human ngay trong turn phát sinh, không để nợ.

**Lý do:**
- Taxonomy là implicit documentation về domain structure của project
- Pending tag để cuối task → thường bị skip
- "Hỏi ngay" là enforce của nguyên tắc không để nợ

**Áp dụng:**
- Agent chỉ dùng tags trong taxonomy hiện tại
- Phát sinh tag mới → thêm vào Pending section + hỏi human ngay turn đó
- Human approve → promote lên taxonomy, xóa pending
- Human reject → dùng tag gần nhất, xóa pending

---

## Quyết định 4 — Definition of Ready Protocol

**Context hình thành:**
Human thường giao task ở dạng mơ hồ — "làm app như Shopee", "fix cái form đó".
Đây là biểu hiện của System 1 thinking (Think Fast and Slow).
Agent làm theo → implement đúng yêu cầu nhưng sai vấn đề.
3 câu hỏi thẳng không đủ vì human chưa biết họ muốn gì trước khi nói.

**Quyết định:**
Dùng Socratic questioning để dẫn human đến Definition of Ready qua brainstorm có cấu trúc.
4 giai đoạn: Probe → Compress → DoR Check → Capture.
Tách thành skill reusable (socratic-dor/SKILL.md).

**Lý do:**
- Socratic method externalize System 1 thinking thành System 2 output
- 1 câu hỏi mỗi turn tránh overwhelm human
- Compress mỗi ~3 turn giữ human oriented
- Agent tự detect khi đủ DoR — không đợi human tuyên bố

**Nguồn gốc framework:**
- TDD: viết test (outcome) trước implement
- Agile: Definition of Ready — task chưa rõ outcome thì chưa làm
- Lean: define value trước, eliminate waste sau

**Áp dụng:**
- Trigger: explicit request / reference-based ("như Shopee") / scope quá lớn
- Opt-out: human dùng keyword → dừng ngay, proceed với những gì đã có
- Capture: branch theo có/không có context system

---

## Quyết định 5 — Toolchain Installation Protocol

**Context hình thành:**
Agent tự cài toolchain vào môi trường sai (host thay vì WSL) mà không hỏi.
Destructive action, khó rollback.

**Quyết định:**
Trước mọi installation: trình bày plan theo template cố định, được human approve mới thực hiện.
Ưu tiên môi trường ảo hóa. Nếu thực tế lệch plan → dừng, báo cáo, không improvise.

**Lý do:**
- Installation là irreversible action — phải có human approval gate
- Template chuẩn giúp human scan nhanh và approve/reject rõ ràng
- Rollback field bắt buộc — agent phải biết cách undo trước khi được install
- "Lệch plan → dừng" là instance của Test First: plan là spec, thực tế là test

**Template bắt buộc:**
```
Environment:  [WSL2 / Docker / host — lý do chọn]
Location:     [path cụ thể]
Version:      [X.X.X — source: link, fetch latest stable]
Dependencies: [list]
Conflicts:    [có thể conflict với gì đang có]
Rollback:     [uninstall bằng cách nào]

Approve? [Y/N]
```

---

## Quyết định 6 — TENSIONS.md Migration Detection

**Context hình thành:**
Sau khi migrate sang TENSIONS_OPEN/ACTIVE/HISTORY, các project cũ vẫn còn TENSIONS.md cũ.
Không có gì nhắc nhở việc migrate.

**Quyết định:**
Startup protocol detect nếu TENSIONS.md tồn tại song song với TENSIONS_OPEN.md.
Agent báo human và hỏi có muốn migrate không. Agent không tự migrate.

**Lý do:**
- Migration cần human judgment: classify status, assign milestone
- Silent wrong migration tệ hơn chưa migrate
- Agent là người nhắc, không phải người quyết

---

## Để làm sau — Visual Management

**Context hình thành:**
Khi `.context/` có nhiều file, human không có cách nhanh để biết trạng thái project.
Tauri GUI được đề xuất như interface cho context system (đọc + edit [manual]).

**Chưa làm vì:**
- Cần context-gen support để auto-generate
- Tauri GUI cần thiết kế interaction model rõ hơn
- Out of scope cho milestone hiện tại

**Open questions:**
- Edit [manual] bằng form có field rõ ràng, hay raw markdown editor với guardrail?
- STATUS.md nên auto-generate hay human-maintained?

**Trigger để làm:** khi modules/ có 5+ file và human bắt đầu hỏi "dự án đang ở đâu rồi".
