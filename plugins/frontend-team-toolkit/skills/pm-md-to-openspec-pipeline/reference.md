# pm-md-to-openspec-pipeline · 参考

与 **[SKILL.md](SKILL.md)** 配套：默认落盘路径、Change Spec → OpenSpec 映射、触发示例。

---

## 1. 全流程后的推荐目录树

`<工作区>` 默认为规格与变更的父目录（常见：仓库根，或团队约定的 `docs/requirements/`）。以 **目标仓库已有先例** 为准。

```text
<工作区>/
├── specs/<change-id>/
│   ├── 实操记录.md              # 阶段 A：切片 + 勘探
│   └── 变更规格-Change-Spec.md  # 阶段 A：Change Spec
└── openspec/changes/<change-id>/
    ├── proposal.md              # 若项目需要（可选）
    ├── design.md                # 阶段 B
    ├── tasks.md                 # 阶段 B
    └── specs/<capability>/
        ├── field-matrix.md      # 阶段 B（最先）
        └── spec.md              # 阶段 B
```

若目标仓 **仅** 使用 `openspec/changes/`、不设 `specs/` 平行目录，阶段 A 产物可落在：

```text
openspec/changes/<change-id>/
├── 实操记录.md
├── 变更规格-Change-Spec.md
├── design.md
├── tasks.md
└── specs/<capability>/
    ├── field-matrix.md
    └── spec.md
```

**规则**：不凭空搬迁路径；与仓内已有 `openspec` 变更 **照抄同仓 precedent**。

---

## 2. `change-id` 与 `capability`

| 字段 | 约定 |
|------|------|
| **change-id** | kebab-case；可与分支名、Ticket 对齐；未定时 Agent 提议 1 个并标注待确认 |
| **capability** | 默认 **1 变更 = 1 capability**，目录名可与 `change-id` 相同 |
| **多 capability** | 同一 `change-id` 下多个 `specs/<capability>/`，各一对 field-matrix + spec；共享或拆分 design/tasks 以团队惯例为准 |

---

## 3. Change Spec → OpenSpec 四文件映射

| Change Spec / 实操记录 | OpenSpec 文件 | 要点 |
|------------------------|---------------|------|
| §一 In/Out、验收 | `spec.md` Goals、验收标准 | 不扩 scope |
| §三 to-be（可验证描述） | `design.md` 策略与组件约束 | 切换/清空/提交/异常 |
| §六 接口与数据、实操 §五 矩阵草案 | `field-matrix.md` | **字段只进矩阵**；禁止「按图」 |
| §四 不变量 | `spec.md` + `design.md` 边界 | 带证据或 TBD |
| §七 风险、§八 对账 | `tasks.md` 实现任务 + Gate | Evidence 命令与 package.json 一致 |
| 全文 TBD | `spec.md` **Open Questions** | 与 tasks Gate 一致 |

阶段 B **不得脑补** PM MD 未出现且 Change Spec 未列的信息；一律进 Open Questions。

---

## 4. 用户一条消息示例

### 4.1 默认全流程（PM MD → Change Spec → OpenSpec）

```text
@skills/pm-md-to-openspec-pipeline/SKILL.md
@docs/prd/feature-x.md

请按 pm-md-to-openspec-pipeline 执行：阶段 A（步骤 1→2→3）→ 阶段 B（四文件）。
change-id 建议：feature-x-mvp-1
勘探范围：src/modules/feature-x/
API 文档：@README.md 中的链接 / @docs/api/...
禁止编造路径；TBD 保留至人工确认。
```

### 4.2 仅阶段 A（切片 + 勘探 + Change Spec）

```text
@skills/pm-md-to-openspec-pipeline/SKILL.md
@docs/prd/feature-x.md

仅阶段 A（change-spec-workflow 步骤 1→2→3），不要写 OpenSpec 四文件。
```

### 4.3 仅阶段 B（已有 Change Spec）

```text
@skills/pm-md-to-openspec-pipeline/SKILL.md
@openspec/changes/feature-x-mvp-1/
@specs/feature-x-mvp-1/变更规格-Change-Spec.md

仅阶段 B：按 openspec-contract-authoring 输出四文件。capability：feature-x。
```

### 4.4 Reconcile 模式（按 vN 重审）

```text
@skills/pm-md-to-openspec-pipeline/SKILL.md
@docs/prd/feature-x-vN.md
@specs/feature-x-mvp-1/
@openspec/changes/feature-x-mvp-1/

按 pm-md-to-openspec-pipeline 启用 Reconcile 编排（基准源文档 vN）：
- R0~R5：阶段 A 对齐分析 + 实操记录 / Change Spec 同步 + 阶段 B 四文件齐刷
- R6 暂不动代码（待我书面授权）
- 收尾标注"基准源文档版本：vN"
```

### 4.5 局部刷新（仅刷某契约文件）

```text
@skills/pm-md-to-openspec-pipeline/SKILL.md
@openspec/changes/feature-x-mvp-1/specs/feature-x/field-matrix.md

仅刷新 field-matrix（启用"局部刷新护栏"）：
- 列出受牵连的 design / spec / tasks 段落
- 输出"未同步文件清单 + 漂移风险声明"
- 不要齐刷其它文件，等我确认
```

将第一行换为 Cursor 中实际 @ 到的技能路径。

---

## 5. 闸门 G 快速核对表

| # | 检查项 |
|---|--------|
| G1 | 实操记录 §一 完整（含范围变更记录） |
| G2 | Change Spec 八块语义齐全（可 TBD） |
| G3 | change-id **已获用户确认**（或用户明确跳过确认） |
| G4 | 用户未要求「仅阶段 A」 |
| G5 | （建议）Owner 已确认 In/Out，或已有「跳过 Owner」书面记录 |
| G6 | 步骤 2 已输出 **易混淆模块对照表** + **跨端/跨角色/跨对象归属表** + **新旧轨道对照表** |
| G7 | Greenfield 场景已启用 **Greenfield 模式** / 常规场景闸门按代码证据判定 |
| G8 | 源文档若在工作区外，已提示复制入库、并将"未入库"登记为 TBD |
| G9 | **双根目录**（specs/ ↔ openspec/changes/）基准源文档版本号一致、无漂移 |

---

## 7. Reconcile 闸门 R7 快速核对表（按 vN 重审 / 全链同步后）

| # | 检查项 |
|---|--------|
| R7-1 | `<vN>-对齐分析.md` 三栏（应剔除 / 应新增 / 仍保留）已逐项 reconcile 到对应产物路径 |
| R7-2 | 实操记录、Change Spec、四文件契约**头部**均声明 `基准源文档版本：vN` |
| R7-3 | 四文件契约**互不残留** vN-1 误加项；保留的兼容字段已标"旧轨静默兼容" |
| R7-4 | `tasks.md` Gate 与 `spec.md` Open Questions 已同步 vN 增删 |
| R7-5 | 若 R6 改了代码：实操记录步骤 4 差异表已列、用户已书面授权 |
| R7-6 | 收尾 §七 首行已标注 `基准源文档版本：vN` + reconcile 日期 |

---

## 8. 局部刷新护栏快速核对表

| # | 检查项 |
|---|--------|
| L1 | 已输出"本次仅刷新 ＜文件＞，未同步文件清单"表，并征得用户"暂不同步"确认 |
| L2 | 局部刷新输出含「漂移风险声明」段，明确"四文件 Gate 未闭合，禁止宣称定稿" |
| L3 | 未悄悄勾选 Gate / Reconcile R7 |
| L4 | 若变更触及不变量 / 验收 / 接口契约 / Open Questions，已**主动建议**齐刷 |
| L5 | 收尾 §七 第二节合并"未同步文件清单"并标"漂移风险" |

---

## 6. 与子技能文档索引

| 技能 | 路径 |
|------|------|
| 变更规格全流程 | [`../change-spec-workflow/SKILL.md`](../change-spec-workflow/SKILL.md) |
| 变更规格模板 | [`../change-spec-workflow/reference.md`](../change-spec-workflow/reference.md) |
| OpenSpec 契约化 | [`../openspec-contract-authoring/SKILL.md`](../openspec-contract-authoring/SKILL.md) |
| 四文件模板 | [`../openspec-contract-authoring/reference.md`](../openspec-contract-authoring/reference.md) |

---

## 7. 安装与可发现性检查清单

若 `@pm-md-to-openspec-pipeline` 未出现在 Cursor Agent 自动技能列表中：

1. **确认 local plugin 已安装**：Cursor Settings → Features → Local Plugins → 检查 `frontend-team-toolkit` 路径
2. **Reload Cursor**：`Cmd+Shift+P` → `Developer: Reload Window`
3. **Rules 面板验证**：打开 Rules 面板，搜索 `pm-md-to-openspec-pipeline` / `change-spec-workflow` 是否出现
4. **Fallback**：若仍未加载，Agent 手动 `Read` 绝对路径：
   ```
   Read <repo>/plugins/frontend-team-toolkit/skills/pm-md-to-openspec-pipeline/SKILL.md
   ```
5. **`.cursor-plugin/marketplace.json`** 中 `skills` 字段须列出子技能路径

---

## 8. 技能执行反馈归档

优化技能后，执行反馈可归档至以下路径之一（以团队约定为准）：

- `specs/<change-id>/skill-execution-feedback.md`（跟业务 specs 同级）
- `docs/skill-retro/<change-id>.md`（团队集中反馈目录）
