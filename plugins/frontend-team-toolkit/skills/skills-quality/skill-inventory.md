# Skill Inventory

## 质量状态分级

| 等级 | 含义 |
|------|------|
| L2 | 使用中人工复盘优化 |
| L3 | 已有 eval 资产，可跑 baseline |
| L4 | 每次改动前后都跑回归门禁 |
| L5 | Darwin / autoresearch 式自动多轮优化 |

## 核心链路

| Skill | 定位 | 上游 | 下游 | 核心输出 | 当前状态 | 下一步 |
|------|------|------|------|----------|----------|--------|
| `pm-md-to-openspec-pipeline` | PM MD -> Change Spec -> OpenSpec 的薄封装编排器 | PM 需求 MD、已有规格根目录、源文档版本 | `change-spec-workflow`、`openspec-contract-authoring` | 阶段 A 产物、闸门 G、阶段 B 四文件、收尾三节 | L3 ready | 跑 `pipeline-*` baseline，重点看子技能读取、阶段闸门、Reconcile、局部刷新 |
| `change-spec-workflow` | 需求切片、影响面勘探、Change Spec、实现后核对 | PM/规格材料、可读仓库、勘探范围 | `pm-md-to-openspec-pipeline` 阶段 A、后续契约技能 | 实操记录、Change Spec、差异表 | L3 ready | 补跑现有 id 1-6 baseline；后续扩充真实失败案例 |
| `openspec-contract-authoring` | OpenSpec 四文件契约化与审阅 | Change Spec、实操记录、OpenSpec 变更目录 | 实现前 Gate、PR 审阅、Evidence | `field-matrix.md`、`design.md`、`spec.md`、`tasks.md` | L3 ready | 跑 `openspec-*` baseline，重点看四文件漂移、Open Questions、按图一致 |

## 必须守住的高风险能力

| 风险 | 覆盖 Skill | Eval 来源 |
|------|------------|-----------|
| 缺输入仍编造正文 | `pm-md-to-openspec-pipeline`、`change-spec-workflow` | `pipeline-002`、`change-spec-workflow` id 2 |
| 阶段 A 闸门未过却进入阶段 B | `pm-md-to-openspec-pipeline` | `pipeline-005` |
| 源文档 vN 重审不走 Reconcile | `pm-md-to-openspec-pipeline`、`change-spec-workflow` | `pipeline-006` |
| 单文件刷新导致四文件漂移 | `pm-md-to-openspec-pipeline`、`openspec-contract-authoring` | `pipeline-007`、`openspec-004` |
| 四文件版本号不一致仍宣称 Gate 通过 | `pm-md-to-openspec-pipeline`、`openspec-contract-authoring` | `pipeline-008`、`openspec-005` |
| Open Questions 未关闭却宣称定稿 | `openspec-contract-authoring` | `openspec-003` |
| 用「按图一致」替代字段契约 | `openspec-contract-authoring` | `openspec-001` |
