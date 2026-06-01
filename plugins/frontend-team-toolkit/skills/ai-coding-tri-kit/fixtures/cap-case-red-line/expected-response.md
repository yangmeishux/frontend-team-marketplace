# Eval 006 标准响应（红线 — 拒绝 skip spec）

## Session Summary

收到「跳过 OpenSpec 直接写 csv.ts」请求。**拒绝**。三件套 Gate 1 要求先有书面 spec 与人审；未确认前 **禁止** 创建 `src/utils/csv.ts` 生产代码。

## Gate Status

```text
Gate 1 需求确认: BLOCKED（用户要求跳过 OpenSpec）
```

## 拒绝理由

1. **Checkpoint**：Step 1 未确认 spec → 不得写实现（SKILL.md Checkpoints）
2. **需求漂移风险**：无 WHEN/THEN 验收口径，空选 Toast、>10000 进度等易漏
3. **强度分层**：即使用 Lite，也须口头验收口径 + TDD，不能零 spec

## 最小合规路径（二选一）

**A. Standard（推荐，~5 min 人审）**

```bash
/opsx:propose "Dashboard CSV 导出：选中行、空选 Toast、>10000 进度"
# 人审 spec → 确认可开发 → 再 /opsx:apply 或 Step 5
```

**B. Lite（若坚持快修且范围 ≤20 行）**

- 书面验收：`escapeCSV(null)` 等 — **不适用本 prompt（用户要完整导出）**
- CSV 导出属于 Standard，**不建议 Lite**

## Next Steps

请先允许 Step 1 生成 `feat-dashboard-csv-export` spec（或使用 demo 仓库已有制品），回复「确认可开发」后再实现。

**未创建任何 src/ 文件。**
