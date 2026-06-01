# Output Contract — ai-coding-tri-kit

本文件定义三件套编排 Skill 的 **会话交付物格式**。

## 必交付节（Must Have）

### 1. Session Summary

1–3 句：当前变更 ID、强度档位（Full/Standard/Lite）、所在 Step。

### 2. Progress Checklist

复制主 SKILL 中的 8 步清单，用 `[x]` / `[ ]` 标记。

### 3. Step Detail（当前步）

| 字段 | 内容 |
|------|------|
| Step N | 步骤名称 |
| 主导工具 | OpenSpec / Superpowers / Agent Skills |
| 本步动作 | 已执行的具体动作（命令、Read 的文件） |
| Exit Criteria |  met / not met |
| 证据 | validate 输出、测试命令摘要、覆盖率数字 |

### 4. Gate Status

```text
Gate 1 需求确认: PASS | BLOCKED | PENDING
Gate 2 代码评审: PASS | BLOCKED | PENDING | N/A
Gate 3 安全扫描: PASS | BLOCKED | PENDING | N/A
```

### 5. Assumptions & Open Questions

- 已做假设（含 Lite 降级、用户豁免）
- 未决 Open Questions（来自 design.md）

### 6. Next Steps

明确 **单一推荐下一步**（例如「请审阅 spec 并回复确认」）。

## 步骤完成时的附加节

### Step 1 完成后附加

- `change-id` 与制品路径列表
- `openspec validate` 输出摘要

### Step 8 完成后附加

- Scenario 对照表（✅/❌）
- 收尾决策（Merge / PR / Keep / Discard）
- archive 路径（若已执行）

## 禁止（Must NOT）

- 不得在未过 Gate 1 时输出「开始实现代码」
- 不得在无测试命令输出时宣称 Step 6 完成
- 不得编造 validate / 覆盖率 / 扫描结果
- 不得自动 push、merge、archive 除非用户明确要求
- 不得把 skill 约束描述为「系统级不可绕过」而不提 CI

## OK 形态示例（Step 1 刚完成）

```markdown
## Session Summary
变更 `feat-csv-export`，Standard 档位，已完成 Step 1 需求对齐，等待人审 spec。

## Progress Checklist
- [x] Step 1 需求对齐（OpenSpec）
- [ ] Step 2 …

## Step Detail
| Step | 1 — 需求对齐 |
| 主导工具 | OpenSpec |
| 本步动作 | 生成 proposal/spec/design/tasks；运行 validate |
| Exit Criteria | not met — 待人审 |
| 证据 | `Change 'feat-csv-export' is valid` |

## Gate Status
Gate 1: PENDING（待人确认 proposal/spec）

## Assumptions & Open Questions
- Assumption: UTF-8 BOM 编码待 Step 2 确认

## Next Steps
请审阅 `openspec/changes/feat-csv-export/specs/csv-export/spec.md` 并回复「确认可开发」。
```

## 与 Eval 对齐

| eval id | 本契约检查点 |
|---------|--------------|
| ai-coding-tri-kit-001 | 触发后输出含 Progress + Step Detail，不直接写代码 |
| ai-coding-tri-kit-002 | 缺输入时 BLOCKED + 最少追问 |
| ai-coding-tri-kit-003 | Full 流程会话含 8 步清单与 Gate Status |
