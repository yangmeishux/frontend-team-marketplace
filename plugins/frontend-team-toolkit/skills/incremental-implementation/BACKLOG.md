# incremental-implementation · 迭代 Backlog

本文件汇总各项目执行 `incremental-implementation` 后的反馈与待办，供技能维护者排期改造。

**维护约定**：每次项目执行后，将运行反馈中的 P0～P3 建议追加到下方表格，并链接源反馈路径。

---

## Backlog 条目

| ID | 优先级 | 来源项目 | 来源反馈 | 问题摘要 | 建议改造 | 状态 |
|----|--------|---------|---------|---------|---------|------|
| BL-I001 | P1 | （待填） | — | Reconcile 上游未跑齐，直接进本技能导致分类依据不足 | 开工契约强化：缺 `<vN>-对齐分析.md` 时只输出待补充清单 | open |
| BL-I002 | P1 | （待填） | — | 实现映射与 tasks / 契约四文件版本号不一致 | 多产物版本对齐 Gate 自动化检测（脚本占位） | open |
| BL-I003 | P2 | （待填） | — | 局部代码更新后未列出未同步契约项 | 局部更新护栏模板已写入 reference §7；待实测 | partial |
| BL-I004 | P2 | （待填） | — | 「不变」项仍被误改 | P4 diff 自检增加不变项断言对照表 | open |

---

## 流程层 Open Questions（技能设计）

| ID | 问题 | 状态 |
|----|------|------|
| SQ-I1 | 上游 Reconcile R0~R5 未完成时，是否允许仅凭 tasks diff 做代码增量？ | open · 倾向允许但须标注「契约未同步风险」 |
| SQ-I2 | 实现映射反向建图（P0.5）是否每次 Reconcile 后强制重跑？ | open · 倾向仅 R1「应剔除/应新增」涉及锚点时增量更新 |
| SQ-I3 | 代码 R7 闸门闭合是否等价于可关闭 tasks Gate？ | open · 倾向否，契约 Gate 仍须 openspec-contract-authoring 核对 |

---

## 已交付改造（Changelog）

| 日期 | 条目 | 说明 |
|------|------|------|
| 2026-05-29 | v1.1.0 | 对齐 pipeline Reconcile / 局部刷新 / 版本对齐；新增 test-prompts.json + results.tsv baseline |

---

## 源反馈索引

| 项目 | change-id | 反馈文件 |
|------|-----------|---------|
| （待填） | | |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-29 | 初版：与 pipeline Reconcile / 局部刷新 / 版本对齐能力对齐 |
