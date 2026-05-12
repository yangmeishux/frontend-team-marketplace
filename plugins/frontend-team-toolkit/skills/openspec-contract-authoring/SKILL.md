---
name: openspec-contract-authoring
description: >-
  将 OpenSpec 变更写成可验收契约：四文件（spec、field-matrix、design、tasks）、禁止「按图一致」、字段矩阵、Open Questions 闸门与 Evidence。
  当用户使用 OpenSpec、openspec/changes、field-matrix、按契约写需求或 openspec validate 时启用。以写文档与审阅为主；仅在用户明确要求按契约落地代码时追加实现前 Gate 核对。
---

# OpenSpec 契约化文档（甲：主路径）

## 技能边界

**主职责（甲）**：在仓库遵循 `openspec/changes/<change-id>/` 约定时，指导或审阅 **四份文档** 的**规范化写法**——把需求从描述性表述升级为 **字段矩阵 + 实现约束 + 可验证证据 + 闸门**，不替产品拍板业务取舍。

**不包含**：安装或版本选型 OpenSpec CLI（以项目文档为准）；不替代 YApi/Figma 等专用技能。

**可选扩展（乙，一句触发）**：当用户**明确**要求 **「按 OpenSpec / 按契约 / 按 field-matrix 实现或落地代码」** 时，在**批量修改业务源码前**，必须先核对 **`tasks.md` 中 Gate**：`field-matrix.md` / `design.md` 已定稿、**Open Questions** 已关闭或已书面记录例外；未满足则不得宣称「已按需求实现」。实现细节仍遵循项目代码规范与其它技能。

**勿滥用乙**：与 `openspec/changes` **无关**的普通重构、样式微调、非契约型需求，**不要**套用 Gate，以免增加无效流程。

---

## 三原则（须写入文档逻辑）

1. **Evidence > Claims**：「完成」须指向可复现命令、截图/录屏或逐步验收记录（见 `tasks.md` Evidence）。  
2. **Open Questions 是硬闸门**：未定项列入 `spec.md` Open Questions，且在关闭前禁止宣称「已对齐需求」。  
3. **禁止以图代契**：出现「按图 / 参考截图 / 与原型一致」时，**必须**改为 **`field-matrix.md` 表格化**；无矩阵则视为契约未完成。

---

## 禁止用语（契约未闭合信号）

以下表述不得作为**唯一**需求依据，须改写为矩阵行或 design 约束：

- 「按图 N 一致即可」「与设计稿一致」「差不多」  
- 无字段清单的「用级联 / 用日期组件」等（须写组件名、数据源、禁止项）

---

## 四文件职责与路径（常见约定）

相对仓库根（具体 `change-id`、`capability` 由变更决定）：

| 文件 | 路径约定 |
|------|-----------|
| 字段矩阵 | `openspec/changes/<change-id>/specs/<capability>/field-matrix.md` |
| 需求主规格 | `openspec/changes/<change-id>/specs/<capability>/spec.md` |
| 实现约束 | `openspec/changes/<change-id>/design.md` |
| 任务与证据 | `openspec/changes/<change-id>/tasks.md` |

内容分工：**字段类只进 field-matrix；组件/数据源/清空与提交/异常策略进 design；背景·目标·流程·验收进 spec；闸门·任务·Evidence 进 tasks。** 详见 **`reference.md`** 模板。

### 路径与项目差异（兜底 · 方案 A）

上表为**常见布局**。若目标仓库将 `design.md` / `tasks.md` 放在其它相对路径、或 **多 capability / monorepo** 分包，以 **该仓库已有 `openspec` 目录 + `CONTRIBUTING` / `AGENTS.md` / 内部 OpenSpec 说明** 为准；**不凭空搬迁路径**，但 **四文件职责**仍须落实。展开说明见 **`reference.md` §9**。

---

## PR / 变更审阅（甲 · 方案 A）

Review 已有文档或 **PR / diff** 时逐项核对：

- [ ] 变更范围内**无**以「按图 / 参考稿 / 原型一致 / 差不多」作为**唯一**契约（可全文搜索）  
- [ ] **`field-matrix.md`** 表头齐、字段行与 UI/接口范围一致  
- [ ] **`spec.md`** Open Questions：**无静默悬空**；未决项不得在 `tasks` Gate 标已闭  
- [ ] **`tasks.md`** Gate、Evidence 与 `spec` 一致；命令与 `package.json` / CI 一致  
- [ ] **`design.md`** 含切换/清空策略及组件 **必须使用 / 禁止**  

扩展步骤见 **`reference.md` §11**。

---

## proposal 与变更生命周期（方案 B）

是否必须先写 **`proposal.md`**、`change-id` 命名规则、合并后是否归档 `changes/<id>`，**以团队仓库约定为准**（见 **`reference.md` §10**）。本技能**不**规定分支模型；只要求契约四件套在**合入前**满足 Gate 与 Evidence。

---

## 写作顺序（必须）

1. **`field-matrix.md`**（先填，最易漏）  
2. **`design.md`**  
3. **`spec.md`**（第 5 节引用矩阵文件，不重复「按图」）  
4. **`tasks.md`**（Gate + Evidence）

---

## Gate（tasks.md 须能勾选）

全部满足前，禁止宣称「文档已定稿 / 已实现」：

- [ ] **Open Questions** 已关闭或已批准例外并记录  
- [ ] **field-matrix** 无「按图」残留，表头与字段行完整  
- [ ] **design** 已写死组件、数据源、切换/清空策略、提交与异常策略  
- [ ] **spec** 含可验收流程与验收标准  
- [ ] **Evidence** 列表与项目实际命令一致（`openspec validate`、build、lint 等以仓库为准）

---

## 校验命令（占位）

若项目启用 CLI：`openspec validate <change-id> --strict`（子命令与 flag **以项目 README / CONTRIBUTING 为准**，各仓可能不同）。**通过 validate 优先于**在文档中自夸「符合 OpenSpec」。

---

## 与 `reference.md` 的分工

| 文档 | 内容 |
|------|------|
| **本 SKILL.md** | 边界、甲乙、原则、禁止语、路径+兜底、PR 审阅摘要、proposal 摘要、顺序、Gate |
| **reference.md** | 目录树、四文件骨架、填空摘要、发布前自检、CLI、**§9 路径变体**、**§10 proposal 与生命周期**、**§11 PR 审阅扩展** |
