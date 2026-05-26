---
name: pm-md-to-openspec-pipeline
description: >-
  薄封装编排：PM/规格 MD → change-spec-workflow（步骤 1→2→3）→ 闸门 → openspec-contract-authoring（四文件）。
  触发：pm-md-to-openspec-pipeline、PM 需求转 OpenSpec、需求切片转契约、@ 本 SKILL + PM MD 或规格根目录。
  须显式 @ 触发；不替代子技能细则。缺输入只出待补充清单。
disable-model-invocation: true
---

# PM MD → OpenSpec 编排（薄封装）

## TL;DR（Agent 先读）

1. **本技能只做编排**：固定 **阶段 A → 闸门 → 阶段 B** 顺序；细则分别遵循同插件内两个子技能（须 **Read 全文** 后再执行对应阶段）。  
2. **阶段 A**：[`../change-spec-workflow/SKILL.md`](../change-spec-workflow/SKILL.md) 步骤 **1→2→3**（切片 → 勘探 → Change Spec）。  
3. **阶段 B**：[`../openspec-contract-authoring/SKILL.md`](../openspec-contract-authoring/SKILL.md) 四文件 **field-matrix → design → spec → tasks**。  
4. **缺 PM MD / 规格根目录 / 可读仓库** → 只输出 **待补充清单**，不虚构正文。  
5. 落盘路径与示例见 **[reference.md](reference.md)**。

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

另须（缺则列入待补充清单，**可**在阶段 A 步骤 1 中由 Agent 提议默认值并标注「待确认」）：

- **`change-id`**：OpenSpec 变更目录名（kebab-case）；未给则步骤 1 末尾 **提议 1 个** 并等用户确认后再落盘阶段 B。  
- **勘探范围**（大仓/monorepo）：模块名或路径前缀；未给则步骤 2 声明「外围 TBD」。  
- **目标仓库 `openspec` 布局**：以该仓已有 `openspec/` + CONTRIBUTING 为准（见 [reference.md §2](reference.md)）。

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
| 1 切片 | `<工作区>/specs/<change-id>/实操记录.md` · §一 |
| 2 勘探 | 同上 · §二～§六 |
| 3 Change Spec | `<工作区>/specs/<change-id>/变更规格-Change-Spec.md` |

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

用户指令矛盾时 **停下**问清；未答复前按 **较窄** 范围（通常「仅阶段 A」或「仅步骤 N」）。

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

---

## 收尾输出格式（强制）

与 `change-spec-workflow` §七 相同，任务结束前须含 **三块**（不得合并成一段）：

1. **本轮写入或修改的路径**（含阶段 A / B；注明新建/覆盖/追加）  
2. **仍为 TBD**（每项 **问谁**）  
3. **建议下一步**（如 Owner 审 Change Spec、`openspec validate`、仅阶段 B、开发 Context Bundle）

若仅对话未 `Write` 任何文件，第一节写明 **「本轮未落盘」**。
