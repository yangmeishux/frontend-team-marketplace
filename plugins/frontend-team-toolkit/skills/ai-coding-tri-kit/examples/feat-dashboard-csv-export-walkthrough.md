# Walkthrough：feat-dashboard-csv-export（Standard 档位 · Step 1–2）

> Capability eval **004/005** 真落盘案例。制品路径：`source/live-app-openspec-demo/openspec/changes/feat-dashboard-csv-export/`

---

## 强度：Standard

- 1–3 文件、单一 Dashboard 模块
- 无外部 SDK → 不升 Full
- 需要 OpenSpec 四件套 + Step 2 澄清，可跳过 worktree（Step 3 可选）

---

## Step 1：需求对齐

**输入 fixture**：`fixtures/cap-case-csv-export/input-requirement.md`

**命令**：

```bash
cd source/live-app-openspec-demo
npx @fission-ai/openspec new change feat-dashboard-csv-export
# 写入 proposal / spec / design / tasks 后：
npx @fission-ai/openspec validate feat-dashboard-csv-export --strict
```

**结果**：`Change 'feat-dashboard-csv-export' is valid`，`Progress: 4/4 artifacts complete`

**spec 核心 Scenario**：

| Scenario | 要点 |
|----------|------|
| 用户导出选中数据 | N 行 → 下载 CSV，仅含 N 行 |
| 未选中任何记录 | Toast「请先选择要导出的数据」 |
| 大数据量导出 | >10000 → 进度条 |
| 特殊字符与 Excel | UTF-8 BOM + RFC 4180 escape |

---

## Step 2：需求澄清（≤3 轮）

**brainstorming 收敛表**（已写入 `design.md` → `## Clarifications`）：

| # | 问题 | 结论 |
|---|------|------|
| Q1 | UTF-8 vs BOM？ | UTF-8 BOM（Excel） |
| Q2 | 可配置列？ | 首版全部可见列 |
| Q3 | 特殊字符？ | RFC 4180 |
| Q4 | 必须 Worker？ | 首版分块+进度条即可 |

**Exit**：用户回复「确认可开发」→ Gate 1 PASS → 进入 Step 3/4

---

## 下一步（未在本 eval 范围）

- Step 4：`writing-plans` 细化 `tasks.md` → `src/utils/csv.ts` 等
- Step 5–8：TDD 实现 → 审查 → verify → archive

---

## 对照 Full 案例

| | feat-live-share（Full） | feat-dashboard-csv-export（Standard） |
|--|-------------------------|--------------------------------------|
| worktree | 必须 | 可选 |
| 子 Agent | 多渠道并行 | 单线程即可 |
| OpenSpec | 5 渠道 + 保活 MUST | 3 Scenario + 编码 |
| 澄清 | 微博 SDK Open Q | 编码/列/Worker 已收敛 |
