---
name: pm-md-to-openspec-pipeline
description: >-
  薄封装编排：PM/规格 MD → change-spec-workflow（步骤 1→2→3）→ 闸门 → openspec-contract-authoring（四文件）。
  触发：pm-md-to-openspec-pipeline、PM 需求转 OpenSpec、需求切片转契约、源文档 vN 重审 / reconcile、仅刷新某契约文件、@ 本 SKILL + 源文档 MD 或规格根目录。
  须显式 @ 触发；不替代子技能细则。缺输入只出待补充清单。源文档版本演进走 Reconcile 编排（阶段 A→B→代码全链同步），单文件刷新触发"局部刷新护栏"；双根目录（specs/ 与 openspec/changes/）须共享版本号 / 日期戳，禁止漂移。
disable-model-invocation: true
---

# PM MD → OpenSpec 编排（薄封装）

## TL;DR（Agent 先读）

1. **本技能只做编排**：固定 **阶段 A → 闸门 → 阶段 B** 顺序；细则分别遵循同插件内两个子技能（须 **Read 全文** 后再执行对应阶段）。  
2. **阶段 A**：[`../change-spec-workflow/SKILL.md`](../change-spec-workflow/SKILL.md) 步骤 **1→2→3**（切片 → 勘探 → Change Spec）。  
3. **阶段 B**：[`../openspec-contract-authoring/SKILL.md`](../openspec-contract-authoring/SKILL.md) 四文件 **field-matrix → design → spec → tasks**。  
4. **缺 PM MD / 规格根目录 / 可读仓库** → 只输出 **待补充清单**，不虚构正文。  
5. 落盘路径与示例见 **[reference.md](reference.md)**。  
6. **源文档版本变化** / 用户说「按 vN 重审 / reconcile / 重新阶段 A」→ 启用 **Reconcile 编排**（见下方专节）：阶段 A R1~R5 + 阶段 B 同步刷新 + 实现代码核对，全链共享版本号；**不**从零重跑全部步骤。  
7. **单文件刷新请求**（如「只刷 field-matrix」）→ 默认启用 **局部刷新护栏**（见下方专节）：刷新前后须输出"未同步文件清单 + 风险"，禁止悄悄漂移。

### 阶段 A/B 产出与用户口令

| 阶段 | 产出 | 用户口令示例 |
|------|------|-------------|
| **A** | 实操记录（切片+勘探+易混淆模块表）+ Change Spec（八块） | `仅阶段 A` / `只切片` / `先出 Change Spec` |
| **B** | OpenSpec 四文件（field-matrix / design / spec / tasks） | `仅阶段 B` / `写契约` / `出 OpenSpec` |
| **A→B 全流程** | 以上全部 | `全流程` / `PM 需求转 OpenSpec`（默认） |

> **用户 @ 编排技能 = 人工触发，Agent 仍须 Read 子技能全文**（子技能 `disable-model-invocation: true` 不影响编排技能的手动触发链）。

---

## 技能边界

| 包含 | 不包含 |
|------|--------|
| 固定两阶段顺序与闸门 | 子技能全文规则（不复制粘贴替代 Read） |
| 输入契约与收尾三节格式 | OpenSpec CLI 安装/版本选型 |
| Change Spec → OpenSpec 路径映射 | YApi/Figma/蓝湖 对接 |
| 子阶段模式（仅 A / 仅 B） | 自动改业务源码（除非用户另请实现） |

**与子技能分工**：

- **`change-spec-workflow`**：执行顺序、勘探证据、Change Spec 八块。  
- **`openspec-contract-authoring`**：四文件契约化、矩阵、Gate、禁止「按图一致」。  
- **本技能**：把上述两者 **串成一条默认流水线**，避免跳过切片直接写 field-matrix。

---

## 开工前输入契约（缺则停）

进入 **阶段 A** 前须满足 **至少一项可读材料**：

1. **PM 需求 MD**（`@docs/prd/…` 或用户给定路径）；或  
2. **已有规格根目录**（`openspec/changes/<id>/`、`proposal`/`design`/`tasks` 等以仓库实际为准）。

**PRD 在工作区外**（如 `@/Users/.../Downloads/...`）：
- 材料**可读**但无法 `@` 进 repo，落盘 specs 与 PRD 源文件分离
- 步骤 1 开头输出：「⚠️ PRD 在工作区外，建议复制到 `docs/prd/<文件名>.md` 以便 `@` 引用」
- 继续执行但标记此风险为 TBD
- **禁止宣称「已按 vN 定稿 / 已完成 vN 对齐」**，除非 PRD 已复制入库，或团队书面允许外部 PRD 作为定稿基准（须在 Change Spec 顶部记录例外）

另须（缺则列入待补充清单，**可**在阶段 A 步骤 1 中由 Agent 提议默认值并标注「待确认」）：

- **`change-id`**：OpenSpec 变更目录名（kebab-case）；未给则步骤 1 末尾 **提议 1 个** 并 **强制停顿等用户确认** 后再落盘阶段 B。  
- **勘探范围**（大仓/monorepo）：模块名或路径前缀；未给则步骤 2 声明「外围 TBD」。  
- **目标仓库 `openspec` 布局**：以该仓已有 `openspec/` + CONTRIBUTING 为准（见 [reference.md §2](reference.md)）。
- **API 文档来源**（见下方 API 联动）：未给则接口章全 TBD。

**API 文档联动**（步骤 2 checklist 新增）：
1. `Read` 仓库 **README.md**，检索是否含 API 文档链接
2. 若 README 有 API 文档 URL → 访问并检索本期相关接口（如 `/<module>/<resource>/...`）
3. 若仓库已集成 `yapi-frontend-integration` 技能 → 可 `@` 该子流程获取接口定义
4. 无 API 来源时，接口章全标 **TBD**，并在实操记录中注明「需 @ API 文档 URL」

**工具不可读仓库**：说明限制，列需用户粘贴的路径/片段；**停止**编造文件内容。

---

## 固定流水线（必须按序）

```text
阶段 A  change-spec-workflow  步骤 1 → 2 → 3
          ↓
        闸门 G（见下）
          ↓
阶段 B  openspec-contract-authoring  field-matrix → design → spec → tasks
          ↓
        收尾 §七（三节）
```

### 阶段 A — change-spec-workflow（步骤 1→2→3）

**执行前**：`Read` [`../change-spec-workflow/SKILL.md`](../change-spec-workflow/SKILL.md) 全文；落盘骨架对照 [`../change-spec-workflow/reference.md`](../change-spec-workflow/reference.md)。

| 步骤 | 产出（默认路径，见 reference.md） |
|------|-----------------------------------|
| 1 切片 | `<工作区>/specs/<change-id>/实操记录.md` · §一（含范围变更记录） |
| 2 勘探 | 同上 · §二～§六 + **易混淆模块对照表** |
| 3 Change Spec | `<工作区>/specs/<change-id>/变更规格-Change-Spec.md` |

**步骤 2 强制输出 — 易混淆模块对照表**（防业务同名模块误导）：

| PRD 中名称 | 代码中候选模块 | 是否本期 | 备注 |
|------------|----------------|----------|------|
| | | ✅ / ❌ | |

- 搜索 PRD 关键词时，**所有命中但不出期的模块**必须列入此表并标 ❌
- 例：PRD 写「模块 X」→ 代码有 `module-x` 目录；写「功能 Y」→ 代码有 `feature-y` — 均须显式标注是否本期

**阶段 A 内禁止**：写 OpenSpec 四文件（`openspec/changes/.../field-matrix.md` 等）；矩阵细节可记在实操记录 §五，**完整契约留阶段 B**。

**步骤 2→3 闸门**：完全遵循 `change-spec-workflow` §四（证据不足时 to-be 段首套话、禁止对外承诺）。

### 闸门 G（阶段 A → 阶段 B）

**全部满足**才进入阶段 B；否则 **停在阶段 A**，收尾 §七 建议「补齐证据 / Owner 确认后再跑阶段 B」：

- [ ] 《实操记录》§一 In/Out、验收、TBD 已写（无整段空白）  
- [ ] Change Spec **八块语义**齐全（可 TBD，见 change-spec-workflow §四对照表）  
- [ ] **`change-id` 已确认**（用户确认或仓库既有目录）  
- [ ] 用户 **未**声明「仅要 Change Spec / 仅阶段 A」  
- [ ] （建议）Owner 已扫一眼切片 In/Out；若用户写「跳过 Owner、直接契约化」，须在 Change Spec 顶部记录 **书面例外**

### 阶段 B — openspec-contract-authoring（四文件）

**执行前**：`Read` [`../openspec-contract-authoring/SKILL.md`](../openspec-contract-authoring/SKILL.md) 全文；模板见 [`../openspec-contract-authoring/reference.md`](../openspec-contract-authoring/reference.md)。

**写作顺序（不可乱序）**：

1. `openspec/changes/<change-id>/specs/<capability>/field-matrix.md`  
2. `openspec/changes/<change-id>/design.md`  
3. `openspec/changes/<change-id>/specs/<capability>/spec.md`  
4. `openspec/changes/<change-id>/tasks.md`  

**内容来源映射**（细则见 [reference.md §3](reference.md)）：

- Change Spec **§6 接口与数据** → field-matrix  
- Change Spec **§3 to-be** + 实操记录 §五 → design  
- Change Spec **§1～§3、§8** → spec（§5 引用矩阵，禁止「按图」）  
- Change Spec 验收 + openspec Gate → tasks  

**`capability`**：默认与 `change-id` 同名的单 capability；多模块时见 reference.md §2。

**阶段 B 内禁止**：回改 PM MD；**不得**删除 Change Spec 中 TBD（可同步到 spec Open Questions）。

---

## 子阶段模式（用户首条指令）

| 模式 | 行为 |
|------|------|
| **默认** | 阶段 A（1→2→3）→ 闸门 G → 阶段 B |
| **仅阶段 A** / 「只切片勘探 Change Spec」 | 只跑 change-spec-workflow；**不**写 OpenSpec 四文件 |
| **仅阶段 B** | 须已有 Change Spec + 实操记录；跳过 1→2→3，直接四文件；缺材料则待补充清单 |
| **仅步骤 N** | 委托 change-spec-workflow 子步骤规则（N∈{1,2,3,4}）；**不**自动进入阶段 B |
| **裁剪模式** / 「仅核心模块」 | 跳过非核心章节的一页 checklist；接口章全 TBD（等 API 来源） |
| **Reconcile 模式** / 「按 vN 重审 / 重新阶段 A」 | 启用 **Reconcile 编排** R0~R5/R7（默认）或 R0~R7（全链）；不重跑全步骤；详见专节 |
| **局部刷新模式** / 「只刷某文件」 | 启用 **局部刷新护栏**：输出"未同步文件清单 + 风险声明"，禁止悄悄漂移；详见专节 |

用户指令矛盾时 **停下**问清；未答复前按 **较窄** 范围（通常「仅阶段 A」或「仅步骤 N」）。

---

## Reconcile 编排（源文档版本演进 / 重审）

**触发**：满足任一项：

- 源文档版本号 / 修订日期变化（如 vN-1 → vN）
- 用户说「按 vN 重审 / reconcile / 重新阶段 A / 剔除误加 / 新旧不能并存」
- 用户提供"剔除清单 / 新增清单"要求按某基准回溯

**编排顺序（不可乱序）**：

```text
R0 ❶ 锁定基准 vN（路径 + 版本号 + 入库状态）
    ↓
R1 ❷ 阶段 A · 子技能 R1 对齐分析 → <规格根>/<vN>-对齐分析.md
    （三栏：应剔除 / 应新增 / 仍保留）
    ↓
R2 ❸ 阶段 A · 实操记录 §一 范围变更记录 + In/Out 增量
    ↓
R3 ❹ 阶段 A · 增量勘探（仅 R1 影响范围；旧勘探可沿用并标注）
    ↓
R4 ❺ 阶段 A · Change Spec 受影响段重写（禁留 vN-1 残段）
    ↓
R5 ❻ 阶段 B · 四文件同步刷新（按 field-matrix → design → spec → tasks）
    ↓
R6 ❼ 实现代码核对（仅在用户书面要求时改代码；否则只列 diff 建议）
    ↓
R7 ❽ Reconcile 闸门：所有产物已剔 vN-1 误加项、已纳 vN 新增项、版本号一致
```

**Reconcile 子模式选择**：

| 用户口令 | 执行集 | 不做 |
|---------|--------|------|
| 「按 vN 重审」/「reconcile」（默认） | R0~R5 + R7 | R6（代码不动） |
| 「按 vN 全链同步」 | R0~R7 | — |
| 「只重审切片」 | R0~R3 + R7 部分 | R4~R6 |
| 「只刷契约」/「跳过 Change Spec」 | 须先有 R1~R4 产物；否则 **退回 R1** | — |

**禁止**：

- 跳 R1（对齐分析）直接刷阶段 B 文件
- 仅同步 specs/ 不同步 openspec/changes/（或反之），见下方"双根目录版本对齐"
- R7 未闭合就宣称「已按 vN 定稿 / 已对齐 vN」

**Reconcile 闸门（R7）核对清单**：

- [ ] R1 对齐分析三栏已逐项 reconcile 到对应产物路径
- [ ] 实操记录、Change Spec、四文件契约 **全部** 头部声明基准版本（如 `基于源文档 vN`）
- [ ] 四文件契约**互不残留** vN-1 误加项；如保留旧字段（兼容），须显式标"旧轨静默兼容，UI/契约不暴露"
- [ ] tasks.md Gate 与 spec.md Open Questions 已同步 vN 增删
- [ ] 若 R6 改了代码：实操记录步骤 4 差异表已列、用户已书面授权

---

## 双根目录版本对齐（阶段 A 产物 ↔ 阶段 B 产物）

当仓库同时存在两类落盘根（阶段 A 落 `<规格根>/specs/<change-id>/`、阶段 B 落 `openspec/changes/<change-id>/`），编排技能须**强制两侧共享同一版本标识**，避免一侧已升 vN、另一侧仍 vN-1 的"双根漂移"。

**版本标识规范**（任一项即可，团队择一）：

1. 每个核心文件**顶部 frontmatter / 元信息表** 含 `基准源文档版本：vN`、`最近 reconcile 日期：YYYY-MM-DD`
2. `<change-id>` 子目录下放 `VERSION.md`：列出当前基准 vN、上次 reconcile 日期、责任产物路径

**漂移检测**（每次进入阶段 B 之前必做）：

- [ ] 列出 `<规格根>/specs/<change-id>/` 与 `openspec/changes/<change-id>/` 下所有 md 的基准版本
- [ ] 不一致项标"漂移"，禁止在不一致状态下继续刷新阶段 B 任一文件
- [ ] 触发 Reconcile 编排 R1~R5 拉齐后再继续

**修复路径**（已发现漂移）：

1. 以**最新基准** vN 为准（除非用户明确指定基准）
2. 在 `<vN>-对齐分析.md` §五 同步任务勾选追加"修复双根漂移"条目
3. 修复完成后所有受影响文件版本标识统一更新

---

## 局部刷新护栏（单文件 / 部分文件刷新请求）

当用户**只**要求刷新阶段 B 中某一个或某几个文件（如「只刷 field-matrix」「只更新 design」），默认启用以下护栏，**不**自动齐刷四文件，但**必须**显式列出未同步范围与风险。

**刷新前**：

1. **影响面预扫**（不需要完整执行，列出即可）：
   - 受影响文件本次刷新的关键变更点（字段增删 / 规则变更 / 边界调整）
   - **受牵连的兄弟文件**：例如 field-matrix 字段增删 → design 数据源 / spec §5 矩阵引用 / tasks Gate；design 边界调整 → spec 验收 / tasks Evidence；spec Open Questions 关闭 → tasks Gate
2. 输出 **"本次仅刷新 ＜文件名＞，未同步文件清单"** 表，并询问用户是否一并刷新；用户明确说"暂不同步"才继续局部刷新

**局部刷新输出（必含）**：

```markdown
### 本次局部刷新
- 受刷文件：`openspec/changes/<id>/.../field-matrix.md`
- 变更摘要：……

### 未同步文件（漂移风险）
| 文件 | 受牵连之处 | 当前是否已过时 | 处置建议 |
|------|-----------|---------------|----------|
| `design.md` §x | | 是 / 否 / 待核对 | 同步刷新 / 用户确认暂不同步 / TBD |
| `spec.md` §5 | | | |
| `tasks.md` Gate | | | |

### 局部刷新风险声明
> 本轮**仅**刷新上述文件；其余文件**未**同步至当前基准。Reconcile 闸门 R7 **未闭合**，禁止据此宣称「已按 ＜版本＞ 定稿」。
```

**触发齐刷的判据**（满足其一）：

- 用户说「同步刷新所有受影响文件」「按 vN 齐刷四文件」
- 受刷文件的变更**改动了不变量 / 验收 / 接口契约**（不仅是表述润色），此时强烈建议齐刷并向用户确认
- 进入 Reconcile 编排 R5 阶段（Reconcile 流程内禁止局部刷新）

**禁止**：

- 局部刷新后悄悄勾选 Reconcile 闸门 / 阶段 B Gate
- 用「仅刷新 ＜文件＞」绕过 Change Spec 八块语义齐全的要求

---

## 如何触发

`disable-model-invocation: true` → 须 **显式 @** 本技能。

1. `@skills/pm-md-to-openspec-pipeline/SKILL.md`（以 Cursor 实际展示为准）  
2. 文中含 **`pm-md-to-openspec-pipeline`** 或 **「PM 需求转 OpenSpec」** + `@` 材料  
3. **同义**：需求 MD 切片并出 OpenSpec 契约、PM 稿转开发规格  

**推荐一条消息**（占位替换）见 [reference.md §4](reference.md)。

---

## Agent 自检（结束前）

- [ ] 是否 **Read** 两个子技能后再执行对应阶段？  
- [ ] 阶段 A 是否 **未**提前写 OpenSpec 四文件？  
- [ ] 闸门 G 未过是否 **未**进入阶段 B？  
- [ ] 阶段 B 是否按 **field-matrix → design → spec → tasks**？  
- [ ] spec / matrix 是否 **无「按图一致」** 作为唯一依据？  
- [ ] Change Spec 与 OpenSpec **TBD / Open Questions** 是否一致、未静默删除？  
- [ ] **§七 收尾三节**是否齐全？
- [ ] 步骤 1 后是否 **停顿等 change-id 确认**？
- [ ] 源文档在工作区外是否已 **提示复制入库**、并将"未入库"登记为 TBD？
- [ ] 步骤 2 是否输出 **易混淆模块对照表** + **跨端/跨角色/跨对象归属表** + **新旧轨道对照表**？
- [ ] 范围变更（用户收窄/扩大）是否已记录 **范围变更记录**？
- [ ] 是否检索了 **README API 链接** / API 文档来源？
- [ ] Greenfield 场景是否启用了 **Greenfield 模式**（as-is 引用模式库）？
- [ ] **Reconcile 触发条件**满足时（源文档版本变化 / 用户重审）是否启用 Reconcile 编排、产出 `<vN>-对齐分析.md`？
- [ ] **双根目录**（specs/ ↔ openspec/changes/）基准版本是否一致、无漂移？
- [ ] **局部刷新请求**是否触发"未同步文件清单 + 风险声明"，未悄悄勾闸门？
- [ ] Reconcile 闸门 R7 未闭合时，是否 **未**宣称「已按 vN 定稿 / 已对齐 vN」？

---

## 收尾输出格式（强制）

与 `change-spec-workflow` §七 相同，任务结束前须含 **三块**（不得合并成一段）：

1. **本轮写入或修改的路径**（含阶段 A / B；注明新建/覆盖/追加；若属 Reconcile 或局部刷新，**首行**显式标注「**基准源文档版本：vN**」与 reconcile 日期）  
2. **仍为 TBD**（每项 **问谁**；若 Reconcile 闸门 R7 未闭合，须显式列入；若局部刷新有"未同步文件清单"，须将清单合并到此节，标注「漂移风险」）  
3. **建议下一步**（如 Owner 审 Change Spec、`openspec validate`、仅阶段 B、齐刷未同步文件、Reconcile R6 代码核对、开发 Context Bundle）

若仅对话未 `Write` 任何文件，第一节写明 **「本轮未落盘」**。
