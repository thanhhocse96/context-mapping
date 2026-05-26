# AGENTS.md — context-gen

> Protocol này áp dụng cho agent làm việc trên **context-gen tool itself**.
> Không nhầm với AGENTS.md của dự án *sử dụng* context-gen.

---

## Current Milestone

Current milestone: V1 - Governance And Milestone Workflow

Milestone source of truth: `.context/MILESTONES.md`.

Detailed milestone backlog: `.context/MILESTONE_ROADMAP.md`.

Version rule: `V0`, `V1`, `V2`, `V3` are development milestone codes, not package SemVer. Official SemVer starts when packaging/release artifacts exist, planned for V3.

---

## 0. Startup Protocol

### Tầng 1 — Always load, full
Đọc toàn bộ, không filter, mọi task.

```bash
cat .context/GLOBAL.md
cat .context/TENSIONS_OPEN.md
```

### Tầng 2 — Always load, filtered

```bash
# Chỉ đọc section current milestone
cat .context/MILESTONES.md

# Đọc theo tag filter:
# - Entry có tag match task keywords → đọc full
# - Entry không match → chỉ đọc Tension + Status
# - Exception: Status OPEN → luôn đọc full dù tag không match
cat .context/TENSIONS_ACTIVE.md
```

### Milestone source protocol

Agent không được invent roadmap scope từ memory. Build milestone scope theo thứ tự source này:

```text
1. Latest explicit human instruction
2. .context/MILESTONES.md current milestone
3. .context/MILESTONE_ROADMAP.md promoted milestone
4. .context/*.md manual sections and .context/modules/*.md when present
5. docs/*.md architecture/workflow decisions
6. docs/milestones/*.md implemented evidence
7. code reality
```

Dùng `.context/MILESTONES.md` là active checklist và `.context/MILESTONE_ROADMAP.md` là backlog. Không load hoặc implement nhiều future milestones cùng lúc.

Khi promote milestone kế tiếp:

```text
1. Read roadmap entry.
2. Read every source doc listed in that entry.
3. Compare source docs against current code and implemented milestone docs.
4. Copy only that milestone's goal, acceptance, out-of-scope, and source docs into .context/MILESTONES.md.
5. Update AGENTS.md current milestone line.
6. Ask human if acceptance is vague, risky, or conflicts with sources.
```

Ask before coding khi:

- Source docs conflict about behavior or priority.
- Acceptance cannot be verified with a concrete test.
- A live credential, paid service, browser install, or system package is required.
- A DB migration, destructive file operation, or cleanup touches user data.
- A decision would expand scope beyond the promoted milestone.

### Tầng 3 — Load on demand

```bash
# Load module match với task scope
python cli.py load <module_path> . --include-manual

# Load planning chỉ khi task liên quan scope/version/UX direction
cat .context/planning/<file>.md
```

### Không load mặc định
- `.context/TENSIONS_HISTORY.md`
- `.context/MILESTONE_ROADMAP.md` (except current/next milestone promotion)
- `.context/proposals/*`

Chỉ load khi human yêu cầu audit hoặc review proposal.

### Documentation protocol

Implemented milestone work belongs in `docs/milestones/`.

Rules:

- Milestone file names must match the milestone code from `.context/MILESTONES.md`, for example `V1_001_milestone-source-protocol.md`.
- `V0`, `V1`, `V2`, `V3` are milestone/phase codes, not package versions.
- Do not assign `0.x.y` or `1.0.0` official package versions before V3 packaging exists.
- Every meaningful completed slice must create or update a milestone doc.
- Milestone docs should start with workflow first, preferably Mermaid.
- Milestone docs must explain what was implemented, which files changed, which design pattern was used, how to verify it, and known limits.
- After adding, moving, or renaming a docs file, update `docs/README.md`.
- If the current milestone changes, update `.context/MILESTONES.md`, `AGENTS.md`, and docs naming together.

### Sau khi load xong — bắt buộc

```
1. Check TENSIONS_OPEN.md — có entry liên quan task không?
   → Nếu có → follow Tension Detection rules (Section 3) trước khi proceed

2. Check: TENSIONS.md có tồn tại song song với TENSIONS_OPEN.md không?
   → Nếu có → báo human: "TENSIONS.md chưa migrate sang V3.
     Bắt đầu migration session không?"
   → Không tự migrate
   → Nếu human từ chối → ghi note, tiếp tục task hiện tại

3. Nếu [manual] của module liên quan vẫn còn _Chưa có ghi chú._
   → DỪNG. Hỏi lại human trước khi implement.
```

### Skills

- Definition of Ready: `.context/skills/socratic-dor/SKILL.md`

---

## 0.1 Definition of Ready Protocol

Activate khi human message match một trong các trigger:

**Category 1 — Explicit brainstorm**
"brainstorm", "chưa rõ", "muốn thảo luận", "help me think"

**Category 2 — Reference-based (implicit vagueness)**
"như X", "giống X", "tương tự X" / "tạo cho tôi app/web/tool..." / "tôi muốn làm cái gì đó..."

**Category 3 — Scope quá lớn**
"toàn bộ", "cả hệ thống", "từ đầu đến cuối", "from scratch"

**Opt-out** — dừng ngay khi human nói:
"đủ rồi", "bắt đầu làm đi", "skip brainstorm"

→ Thực hiện theo `.context/skills/socratic-dor/SKILL.md`

---

## 0.2 Toolchain Installation Protocol

Trước mọi installation — trình bày plan, đợi human approve, rồi mới thực hiện.

**Ưu tiên môi trường:**
1. WSL2
2. Docker / Podman
3. Host machine

Exception — dùng host nếu: project đã có môi trường host setup và document,
dependency yêu cầu hardware access trực tiếp, hoặc human explicitly chọn.

**Template bắt buộc trước khi install:**

```
## Installation Plan — [tool name]

Environment:  [WSL2 / Docker / host — lý do chọn]
Location:     [path cụ thể]
Version:      [X.X.X — fetch latest stable, kèm link]
Dependencies: [list]
Conflicts:    [có thể conflict với gì đang có]
Rollback:     [uninstall bằng cách nào]

Approve? [Y/N]
```

**Rules:**
- Không install trước khi có human approval
- Fetch latest stable — không tự quyết version từ memory
- Nếu thực tế lệch plan giữa chừng → dừng, báo cáo, không improvise
- Rollback field bắt buộc — phải biết cách undo trước khi được install

---



### Plugin Registry

`cli.py` không biết ngôn ngữ nào tồn tại. Nó chỉ loop qua `REGISTRY`.

```
schema.REGISTRY
  ├── "rust"       ← registered bởi parsers/rust_parser.py
  ├── "typescript" ← registered bởi parsers/ts_parser.py
  └── "php"        ← registered bởi parsers/php_parser.py
```

**Thêm language mới**: tạo `parsers/<lang>_parser.py`, gọi `register_plugin()` ở cuối file, thêm `import parsers.<lang>_parser` vào `cli.py`. Không sửa gì khác.

**Không được**: thêm `if language == "..."` vào `cli.py`, `merger.py`, hoặc `schema.py`.

### Merge contract — invariant cốt lõi

```
merger.py chỉ replace vùng AUTO_START...AUTO_END.
Vùng MANUAL_START...MANUAL_END KHÔNG BAO GIỜ bị động vào.
```

Bất kỳ thay đổi nào trong `merger.py` phải verify lại invariant này bằng test.

### `load` command — stdout contract

```bash
python cli.py load <path> . --include-manual | <anything>
```

Stdout của `load` phải sạch tuyệt đối — chỉ có content của context file. Errors đi vào stderr. Không được print bất cứ thứ gì ra stdout trong code path của `load`.

---

## 2. Workflow bắt buộc cho mỗi task

```
1. Đọc .context/GLOBAL.md
2. python cli.py load <module> . --include-manual
3. Kiểm tra TENSIONS.md — có OPEN entry nào liên quan không?
4. Nếu [manual] còn template → DỪNG, hỏi human
5. Đừng viết những gì liên quan đến local environment 
6. Viết test FAIL trước
7. Implement cho đến khi test PASS
8. python cli.py build . --quiet   ← verify tool tự build được
9. Cập nhật .context/<module>.md [manual] nếu có decision mới
10. Nếu detect tension → ghi vào TENSIONS.md trước khi tiếp tục
```

---

## 2.1. Environment

### Local environment file

Nếu có file `.local/ENVIRONMENT.md`, agent phải đọc file đó trước khi chạy toolchain local, tạo venv, install dependency, hoặc chạy command phụ thuộc path máy hiện tại.

File `.local/ENVIRONMENT.md` là machine-local, đã được git ignore, và KHÔNG commit. File này có thể chứa path, command, version, hoặc thông tin riêng của máy hiện tại.

Nếu chưa có `.local/ENVIRONMENT.md` và task cần setup/toolchain local, agent phải hỏi human hoặc tạo file từ template sau khi được xác nhận:

```text
docs/templates/00_local-environment.example.md
```

Không ghi path máy cụ thể, credential, hoặc local-only command vào `.context/*.md` hoặc docs commit trừ khi đó là decision chung áp dụng cho mọi môi trường.

### WSL

Khi làm việc trên Windows và có Debian WSL, ưu tiên chạy toolchain Python trong WSL thay vì Windows Store `python.exe`.

Nếu repo nằm trên Windows filesystem, ví dụ:

```bash
/mnt/d/Github/context-mapping
```

KHÔNG tạo venv bên trong repo bằng:

```bash
python3 -m venv .venv
```

Lý do: venv trên `/mnt/<drive>` có thể fail với lỗi permission kiểu:

```text
Operation not permitted: '/mnt/d/Github/context-mapping/.venv/bin/activate.csh'
```

Phương án đúng: tạo venv trong Linux filesystem, rồi dùng nó khi đứng trong repo Windows mount.

```bash
mkdir -p ~/.venvs
python3 -m venv ~/.venvs/context-mapping
source ~/.venvs/context-mapping/bin/activate
cd /mnt/d/Github/context-mapping
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install tree-sitter-php watchdog
```

Mỗi session mới:

```bash
source ~/.venvs/context-mapping/bin/activate
cd /mnt/d/Github/context-mapping
```

Nếu `.venv` đã bị tạo dở trong repo Windows mount, có thể xóa nó trước khi tiếp tục:

```bash
rm -rf /mnt/d/Github/context-mapping/.venv
```

Phương án tốt nhất về lâu dài: clone repo vào Linux filesystem (`~/context-mapping`) và tạo `.venv` trong repo Linux đó.

---

## 3. Tension detection — khi nào ghi vào TENSIONS.md

Ghi tension khi agent nhận ra một trong những dấu hiệu sau, **trước khi** thực hiện action:

- Task yêu cầu sửa `cli.py`, `merger.py`, hoặc `schema.py` bằng cách thêm `if language == "..."` → tension với invariant registry
- Task yêu cầu print gì đó ra stdout trong `load` command → tension với stdout contract
- Task yêu cầu xóa hoặc overwrite `[manual]` section → tension với merge contract
- Task yêu cầu parser recursive scan → tension với "parse không recursive" invariant
- Task scope lớn hơn những gì `[manual] Behavior chưa implement` cho phép

**Format** (dùng cho tension do agent detect thủ công — ghi vào `.context/TENSIONS_OPEN.md`):

```markdown
## YYYY-MM-DD | <module>
Status:     OPEN
Tension:    <mô tả conflict cụ thể>
Context:    <đang làm task gì>
Proposal:   <agent muốn làm gì>
Constraint: <invariant nào bị conflict — trích dẫn từ [manual]>
Severity:   low | high
Tags:       <tag1, tag2> ← chọn từ taxonomy Section 3.1
Milestone:  <current milestone từ MILESTONES.md>
Decision:   [human fill in]
```

> **Lưu ý**: `tensions_writer.py` sinh staleness entries tự động vào `TENSIONS_OPEN.md`
> với cùng format structured fields ở trên.

**Load order mỗi task — bắt buộc:**

```
1. Đọc TENSIONS_OPEN.md     — luôn luôn, toàn bộ
2. Đọc TENSIONS_ACTIVE.md   — với tag filter:
     - Extract keywords từ task description
     - Đọc kỹ entries có tag match
     - Đọc chỉ Status + Tension của entries không match
3. KHÔNG đọc TENSIONS_HISTORY.md mặc định
     Chỉ đọc khi human yêu cầu audit hoặc task liên quan đến decision cũ
```

**Move rules:**

```
OPEN → RESOLVED_ACTIVE:
  Human điền Decision + Resolved date.
  Move entry từ TENSIONS_OPEN.md sang TENSIONS_ACTIVE.md.
  Đổi Status: RESOLVED_ACTIVE.

RESOLVED_ACTIVE → ARCHIVED:
  Chỉ khi human approve milestone transition.
  Move entries của milestone cũ sang TENSIONS_HISTORY.md.
  Agent KHÔNG tự archive.
```

**Routing**:
- `low` → ghi tension, tiếp tục theo hướng conservative nhất, human review sau
- `high` → ghi tension, **dừng task**, đợi human fill `Decision`

---

## 3.1 Tag Taxonomy

Khi viết tension entry mới, chọn tags từ danh sách này.

```
a11y            — Accessibility
agent           — Agent workflow/protocol decisions
blocks          — Gutenberg block development
cli             — cli.py changes
editor-governance — Custom block vs pattern/editor decisions
map             — Map integration (OpenStreetMap, etc.)
milestone       — Milestone transition decisions
multilingual    — Multilingual/i18n
patterns        — Gutenberg patterns
php             — PHP/WordPress plugin code
planning        — Planning snapshots, scope, version decisions
product-data    — WooCommerce product data modeling
quote-flow      — Quote/pricing flow feature
registry        — Plugin registry pattern
schema          — context-gen schema/parser
slider          — Slider component
spam-protection — Spam protection
staleness       — Staleness detection
tailwind        — Tailwind CSS integration
theme           — Theme development
woocommerce     — WooCommerce blocks/patterns
```

### Pending tags (chưa approved)
<!-- Agent thêm vào đây nếu phát sinh tag mới mid-task -->
<!-- Format: `tag-name` — proposed [YYYY-MM-DD], context: [mô tả ngắn] -->

### Tag rules
- Chỉ dùng tags trong taxonomy trên
- Phát sinh domain mới chưa có tag:
  1. Thêm vào section Pending tags với proposed name + date
  2. Hỏi human ngay trong turn đó — không đợi cuối task
  3. Human approve → move lên taxonomy, xóa pending
  4. Human reject → dùng tag gần nhất, xóa pending
  5. Không tự promote pending tag lên taxonomy khi chưa có human approval

---

## 4. Thêm parser mới — checklist

Khi được yêu cầu thêm language mới (ví dụ Python, Go, Vue):

Trước khi implement parser mới, dùng prompt template `docs/prompts/00_add-parser.md`. Agent phải chạy proposal phase trước, human approve rồi mới code.

```
□ Kiểm tra tree-sitter-<lang> có trên PyPI không
□ Probe AST node types trước khi viết parser
  python3 -c "... parser.parse(sample); walk(tree.root_node)"
□ Xác định "IPC bridge" tương đương cho language đó
  (tauri::command, add_action, URL endpoint, gRPC handler...)
□ Tạo parsers/<lang>_parser.py với register_plugin() ở cuối
□ Thêm import parsers.<lang>_parser vào cli.py (1 dòng duy nhất)
□ Thêm skip_dirs phù hợp với ecosystem
  (vendor/ cho PHP, __pycache__/ cho Python, target/ cho Rust...)
□ Viết .context/parsers_<lang>_parser.md với [manual] đầy đủ
□ Chạy: python cli.py build /tmp/test-<lang>-project .
□ Verify output trong .context/*.md đúng syntax
```

---

## 5. Files không được sửa nếu không có explicit instruction

| File | Lý do |
|------|-------|
| `.context/GLOBAL.md` [auto] section | auto-generated, sẽ bị overwrite |
| `.context/TENSIONS_OPEN.md` entries đã RESOLVED_ACTIVE | chỉ move sang ACTIVE, không sửa |
| `.context/TENSIONS_ACTIVE.md` entries đã ARCHIVED | chỉ move sang HISTORY, không sửa |
| `.context/TENSIONS.md` (nếu còn) | giữ đến khi human approve xóa sau migrate |
| `MANUAL_SECTION` template trong `schema.py` | agent dựa vào template để detect [manual] chưa điền |
| `AUTO_START` / `AUTO_END` markers trong `schema.py` | thay đổi markers = break toàn bộ merge logic |
| Hash trong `AUTO_START` marker của `.context/*.md` | metadata cho staleness detection, không phải lỗi format |

---

## 5.1 End-of-Session Checklist

Sau khi task hoàn thành, trước khi close session:

### Bắt buộc
```bash
python cli.py build . --quiet
```
- Check TENSIONS_OPEN.md — có tension mới phát sinh không? Nếu có → ghi vào
- Check Pending tags trong Section 3.1 — có tag chưa approved không? Nếu có → hỏi human ngay

### Nếu có quyết định kiến trúc trong session
- Update `[manual]` section của module liên quan
- Nếu quyết định resolve một tension → move từ TENSIONS_OPEN sang TENSIONS_ACTIVE

### Nếu có thay đổi scope hoặc milestone
```bash
python cli.py check-consistency .
```
- Update MILESTONES.md current milestone section

### Commit
```bash
git add .context/
git commit -m "context: session [date] — [1 dòng quyết định chính]"
```

---

## 6. Verification gate

Sau mỗi thay đổi, phải pass tất cả:

```bash
# Tool tự build được không bị crash
python cli.py build /tmp/test-project . --quiet

# Consistency check pass
python cli.py check-consistency .

# load stdout sạch (staleness warning đi stderr, không stdout)
python cli.py load /tmp/test-project/src . | python3 -c "
import sys
content = sys.stdin.read()
assert '<!-- AUTO_START -->' in content or len(content) > 0
assert 'WARN' not in content, 'stdout bẩn'
print('stdout OK:', len(content), 'chars')
"

# Registry đủ plugins
python3 -c "
import parsers.rust_parser, parsers.ts_parser, parsers.php_parser
from schema import REGISTRY
assert set(REGISTRY.keys()) == {'rust', 'typescript', 'php'}, REGISTRY.keys()
print('Registry OK:', list(REGISTRY.keys()))
"

# [manual] không bị xóa sau build
python cli.py build /tmp/test-project . --quiet
grep -q 'MANUAL_START' /tmp/test-project/.context/*.md && echo "MANUAL preserved OK"

# Staleness detection hoạt động
python cli.py build /tmp/test-project . --quiet
grep -q 'AUTO_START | hash:' /tmp/test-project/.context/*.md && echo "Hash injection OK"

# TENSIONS_OPEN chỉ chứa OPEN entries
python3 -c "
import re, pathlib
f = pathlib.Path('.context/TENSIONS_OPEN.md')
if f.exists():
    bad = re.findall(r'Status:\s+(?!OPEN)', f.read_text())
    assert not bad, f'Non-OPEN entries in TENSIONS_OPEN: {bad}'
    print('TENSIONS_OPEN OK')
"
```
