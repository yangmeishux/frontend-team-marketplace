---
name: openspec-contract-authoring
description: >-
  将 OpenSpec 变更写成可验收契约：四文件（spec、field-matrix、design、tasks）、禁止「按图一致」、字段矩阵、Open Questions 闸门与 Evidence。
  当用户使用 OpenSpec、openspec/changes、field-matrix、按契约写需求、按 vN 同步四文件、或 openspec validate 时启用。以写文档与审阅为主；仅在用户明确要求按契约落地代码时追加实现前 Gate 核对。
  支持"局部刷新模式"：刷新单文件须输出"未同步文件清单 + 漂移风险声明"。四文件须共享同一基准源文档版本号，禁止四文件版本漂移。Gate 含"字段矩阵 vs 实现 diff"项。
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
- 「**同一套 X / 共用 / 复用 / 类似 / 与 Y 一致**」无明确指代物：须改为 design 边界（明确"共享何物：组件 / 接口 / 字段 / 配置"）或转入 `spec.md` Open Questions 等 Owner 裁决  
- "**新旧版本并存**" 而未标注双轨状态：须在 matrix / spec 显式注明每一项「新轨纳入 / 旧轨静默兼容 / 旧轨下线」

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
- [ ] 四文件 + 上游 Change Spec / 实操记录头部 **基准源文档版本号一致**；diff 中不得出现仅刷新部分文件而其它文件版本号未同步的"漂移 PR"  
- [ ] 全文检索无「同一套 / 共用 / 复用 / 类似」未指代物的模糊措辞，否则改写或转 Open Question  
- [ ] 含旧字段 / 旧 token 时，**显式**标注「旧轨静默兼容 / 旧轨下线」状态  
- [ ] 若 PR 仅刷新单文件，PR 描述含"未同步文件清单 + 漂移风险声明"

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

## 版本标识与漂移防护

每份契约文件（四文件 + 上游 Change Spec / 实操记录）**头部** 须含**基准源文档版本标识**，便于跨文件 / 跨目录的"版本一致性"核对。任一项即可，团队择一：

- 文件顶部 frontmatter / 元信息表声明：`基准源文档版本：vN`、`最近 reconcile 日期：YYYY-MM-DD`
- `<change-id>` 子目录下集中 `VERSION.md`，列出所有产物的基准版本

**漂移检测时机**：

- 进入"写作顺序"任一步之前
- 任何"局部刷新"前后
- Gate 核对时（见上方"四文件版本一致性"项）

**漂移发现的处置**：暂停四文件刷新，回退到上游编排（如 `pm-md-to-openspec-pipeline` 的 Reconcile 编排）拉齐版本后再续刷。

---

## 局部刷新模式（单文件 / 部分文件）

当用户**只**要求刷新四文件中某一个或某几个文件时，须启用以下护栏，**不**自动齐刷四文件，但**必须**显式输出未同步范围与漂移风险。

**刷新前**：

1. **影响面预扫**（不需完整执行，列出即可）：
   - 受刷文件的关键变更点（字段增删 / 边界变更 / Gate 项变更 等）
   - **受牵连的兄弟文件**（典型映射）：

| 受刷文件 | 受牵连兄弟文件（典型） |
|---------|------------------------|
| `field-matrix.md` | `design.md` 数据源 / 组件约束；`spec.md` §5 矩阵引用；`tasks.md` Gate |
| `design.md` | `spec.md` 验收 / 边界；`tasks.md` Evidence；`field-matrix.md` 备注 |
| `spec.md` | `tasks.md` Gate（Open Questions 变化）；`design.md` 边界（若验收边界变） |
| `tasks.md` | `spec.md` Open Questions（若 Evidence / Gate 变化倒推） |

2. 向用户输出 **「本次仅刷新 ＜文件＞，未同步文件清单」** 表；用户明确"暂不同步"才继续局部刷新

**局部刷新必须输出**：

```markdown
### 本次局部刷新
- 受刷文件：…
- 变更摘要：…

### 未同步文件（漂移风险）
| 文件 | 受牵连之处 | 当前是否已过时 | 处置建议 |
|------|-----------|---------------|----------|

### 漂移风险声明
> 本轮仅刷新上述文件；其余文件未同步至当前基准。**四文件 Gate 未闭合**，禁止据此宣称「文档已定稿」。
```

**触发齐刷的判据**（满足其一）：

- 用户明确「同步齐刷」「按 vN 齐刷四文件」
- 受刷文件的变更触及**不变量 / 验收 / 接口契约 / Open Questions**（非表述润色）
- 上游编排进入 Reconcile R5（须齐刷）

**禁止**：

- 局部刷新后悄悄勾 Gate
- 用"仅刷 ＜文件＞"绕过 Open Questions 闭合或 Evidence 一致要求

---

## Gate（tasks.md 须能勾选）

全部满足前，禁止宣称「文档已定稿 / 已实现」：

- [ ] **Open Questions** 已关闭或已批准例外并记录  
- [ ] **field-matrix** 无「按图」残留，表头与字段行完整  
- [ ] **design** 已写死组件、数据源、切换/清空策略、提交与异常策略  
- [ ] **spec** 含可验收流程与验收标准  
- [ ] **Evidence** 列表与项目实际命令一致（`openspec validate`、build、lint 等以仓库为准）  
- [ ] **四文件版本一致性**：四文件 + 上游 Change Spec / 实操记录头部声明的**基准源文档版本号**完全一致（如均为 `基于源文档 vN`），无漂移  
- [ ] **字段矩阵 vs 实现 diff**（若仓库已有对应实现）：matrix 字段集与实现侧（接口请求/响应、UI 字段、数据库列等）已逐项核对；不一致项已显式记录为 Open Question 或 design 边界  
- [ ] **新旧轨道显式标注**：matrix / spec 中如保留旧字段或旧 token，须标"旧轨静默兼容 / 旧轨下线"等明确状态，禁止与新轨并列暴露

---

## 校验命令（占位）

若项目启用 CLI：`openspec validate <change-id> --strict`（子命令与 flag **以项目 README / CONTRIBUTING 为准**，各仓可能不同）。**通过 validate 优先于**在文档中自夸「符合 OpenSpec」。

---

## 与 `reference.md` 的分工

| 文档 | 内容 |
|------|------|
| **本 SKILL.md** | 边界、甲乙、原则、禁止语、路径+兜底、PR 审阅摘要、proposal 摘要、顺序、Gate |
| **reference.md** | 目录树、四文件骨架、填空摘要、发布前自检、CLI、**§9 路径变体**、**§10 proposal 与生命周期**、**§11 PR 审阅扩展** |
