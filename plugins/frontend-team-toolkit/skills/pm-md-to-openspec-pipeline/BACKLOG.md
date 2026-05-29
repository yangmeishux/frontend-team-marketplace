# pm-md-to-openspec-pipeline · 迭代 Backlog

本文件汇总各项目执行 `pm-md-to-openspec-pipeline` 后的反馈与待办，供技能维护者排期改造。

**维护约定**：每次新项目执行后，将 `skill-execution-feedback.md` 中的 P0～P3 建议条目追加到下方表格，并链接源反馈路径。

---

## Backlog 条目

| ID | 优先级 | 来源项目 | 来源反馈 | 问题摘要 | 建议改造 | 状态 |
|----|--------|---------|---------|---------|---------|------|
| BL-001 | P0 | customer-assistant | [skill-execution-feedback.md](file:///Users/win-yingyangxing/Documents/yunxiao/customer-assistant/specs/wecom-customer-assistant-mvp-1/skill-execution-feedback.md) · P1 | 技能未出现在 Agent 自动技能列表 | 在 SKILL.md / reference.md 强化安装检查；推荐各业务仓 AGENTS.md fallback | **done**（customer-assistant 已加 AGENTS.md） |
| BL-002 | P0 | customer-assistant | 同上 · P2 | PRD 在工作区外无法 reconcile | 步骤 1 增加「复制 PRD 到 docs/prd/」可执行提议或脚本模板 | **done**（customer-assistant 已入库 + Reconcile） |
| BL-003 | P1 | customer-assistant | 同上 · P3 | 双源文档冲突依赖 Agent 自行裁决 | 步骤 1 强制「基准文档版本号」输入；首跑也产出简版对齐/冲突表 | open |
| BL-004 | P1 | customer-assistant | 同上 · P4 | 步骤 1 切片未落盘，change-id 停顿偏晚 | 明确：§一 可先落盘，change-id 确认前禁止阶段 B | open |
| BL-005 | P1 | customer-assistant | 同上 · P5 | README 无 API 时未追问 YApi | API 联动 checklist 增加「已询问/用户未提供」记录；Greenfield 预设 OAuth/待办/签单必看三问 | open |
| BL-006 | P2 | customer-assistant | 同上 · P6 | 跨仓库 PRD scope 易膨胀 | 开工输入增加「交付仓库 + 姐妹仓库 Out」；实操记录模板增加对应节 | **partial**（customer-assistant 实操已加；技能模板待改） |
| BL-007 | P2 | customer-assistant | 同上 · P7 | 首次 OpenSpec 无双根 precedent | 首跑询问单根/双根；默认创建 VERSION.md | **partial**（customer-assistant 已建 VERSION；技能待改） |
| BL-008 | P2 | management-community-operations | （历史）crm-todo-admin-mvp-1 反馈 | 同类 pipeline 问题 | 与 BL-003～BL-007 合并改造 | open |
| BL-009 | P3 | customer-assistant | 同上 · P8 | OpenSpec CLI 未配置时 tasks 仍引用 validate | tasks 模板：无 CLI 时默认移除 validate 项 | open |
| BL-010 | P3 | customer-assistant | 同上 · P9 | 原型 HTML 过大全量 Read | reference 注明只读 PRD §十 panel 导航表 | open |
| BL-011 | P3 | customer-assistant | 同上 · SQ-3 | 「继续下一步」口令歧义 | reference 口令表补充映射 | open |

---

## 流程层 Open Questions（技能设计）

| ID | 问题 | 状态 |
|----|------|------|
| SQ-1 | 阶段 B 在 Open Questions 未关闭时是否允许落盘？ | open · 倾向允许落盘但禁止宣称定稿 |
| SQ-2 | Greenfield 下步骤 2→3 闸门是否自动满足？ | open |
| SQ-3 | 「继续下一步」是否等价跳过 Owner 确认？ | open · 建议写入口令表 |
| SQ-4 | 跨仓库 change-id 命名规范？ | open |

---

## 已交付改造（Changelog）

| 日期 | 条目 | 说明 |
|------|------|------|
| 2026-05-29 | BL-001 | `customer-assistant/AGENTS.md` 技能触发与 fallback |
| 2026-05-29 | BL-002 | `customer-assistant/docs/prd/` + Reconcile R1 |
| 2026-05-29 | BL-006/007 partial | customer-assistant 实操/VERSION；技能 SKILL 待跟进 |

---

## 源反馈索引

| 项目 | change-id | 反馈文件 |
|------|-----------|---------|
| customer-assistant | `wecom-customer-assistant-mvp-1` | `specs/wecom-customer-assistant-mvp-1/skill-execution-feedback.md` |
| management-community-operations | `crm-todo-admin-mvp-1` | `specs/crm-todo-admin-mvp-1/skill-execution-feedback.md`（若存在） |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-29 | 初版：合并 customer-assistant 首次执行反馈 |
