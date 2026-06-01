# Capability Eval 004 — 期望产物说明

**Eval ID**: `ai-coding-tri-kit-004`  
**类型**: capability · real_usage · Step 1 真落盘

## 输入

- Fixture: `fixtures/cap-case-csv-export/input-requirement.md`
- 目标仓库: `source/live-app-openspec-demo/`

## 期望落盘路径

```text
openspec/changes/feat-dashboard-csv-export/
├── proposal.md
├── design.md
├── tasks.md
└── specs/dashboard-csv-export/spec.md
```

## Pass 判据

1. `openspec validate feat-dashboard-csv-export --strict` → valid
2. spec 含 ≥3 个 Requirement，各含 Scenario
3. 覆盖：选中导出、空选 Toast、>10000 进度
4. Step 1 阶段无 `src/` 实现代码（本 eval 仅测 spec 落盘）

## Baseline（2026-05-31）

- validate: **PASS**
- artifacts: 4/4 complete
- 执行方式: Agent 真写文件 + CLI 校验
