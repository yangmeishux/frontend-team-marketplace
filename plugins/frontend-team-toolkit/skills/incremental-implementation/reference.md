# incremental-implementation · 模板与参考

本文件提供落盘模板与核对表，SKILL.md 引用此处。所有路径以仓库实际 `change-id` 替换占位符。

---

## §1 `实现映射.md` 模板

落盘路径：`specs/<change-id>/实现映射.md`

作用：把每个开发任务锚定到具体代码位置，使「已提交代码」成为可追溯的事实源。
首次使用本技能时，若该文件不存在，先用 P0.5「反向建图」从现有代码回填。

```markdown
# 实现映射 · <change-id>

| 字段 | 值 |
|------|-----|
| change-id | `<change-id>` |
| 基准源文档版本 | vN |
| 最近 reconcile 日期 | YYYY-MM-DD |
| 当前基线 commit | `<短哈希>` |

> 说明：本表是「任务 ↔ 代码」唯一锚点。代码即事实源；文档变更须经 Reconcile 对齐分析 + 本表落成最小 diff。

## 锚点表

| 任务 ID | 任务摘要 | 状态 | 实现锚点（文件 / 关键符号） | 关联契约项 | 最近变更 commit |
|---------|---------|------|------------------------------|------------|-----------------|
| T1-1 | 列表页分页与筛选 | 已实现 | `src/modules/<module>/ListView.vue` · `useListQuery` | field-matrix §2 | `a1b2c3d` |
| T2-3 | 详情页只读展示 | 已实现 | `src/modules/<module>/DetailView.vue` | spec §3 | `a1b2c3d` |
| T3-2 | 配置弹窗字段校验 | 部分实现 | `src/modules/<module>/ConfigDialog.vue`（GAP-1） | tasks T3-2 | `e4f5g6h` |
| T4-1 | 导出接口对接 | 锚点待确认 | TBD（需反向建图） | spec §5 | — |

## 状态枚举

- `未实现` / `部分实现` / `已实现` / `已废弃`（删除后保留一行存档，标 commit）
- `锚点待确认`：反向建图时无法定位，须人工确认，**禁止臆造路径**

## 修订记录

| 日期 | 摘要 |
|------|------|
| | |
```

---

## §2 变更分类表模板（P1 / IC-R3 产出）

对照 Reconcile `<vN>-对齐分析.md` 三栏（应剔除 / 应新增 / 仍保留）逐项归类。

```markdown
### 本轮变更分类（基准源文档 vN）

| 序 | 变更项 | 类别 | 依据（对齐分析栏 / 字段） | 现有锚点 | 备注 |
|----|--------|------|--------------------------|----------|------|
| 1 | 列表新增「状态」列 | 修改 | 仍保留·字段变更 | `ListView.vue` | 改列定义+类型 |
| 2 | 新增批量操作入口 | 新增 | 应新增 | 复用 `useBatchActions` | 不另起并行模块 |
| 3 | 移除某对外 API | 删除 | 应剔除 | `api/module.js#complete` | 删实现+引用+映射 |
| 4 | 详情页布局 | 不变 | 仍保留·无变化 | `DetailView.vue` | **本轮不动** |

> 「不变」项必须逐条列出并断言不动，作为防误改护栏。
```

---

## §3 影响定位表模板（P2 / IC-R3 产出）

仅对【新增/修改/删除】项展开。

```markdown
### 影响定位

| 变更项 | 受影响文件 | 关键符号 / 行为 | 调用点 / 测试 | 编辑方式 |
|--------|-----------|-----------------|---------------|----------|
| 列表新增「状态」列 | `ListView.vue`, `types/module.ts` | 列配置 + 类型 | 列表 API 映射 | StrReplace 最小补丁 |
| 批量操作入口 | `ListView.vue`, `useBatchActions.js` | 新增 action | `api/module.js` | 新增方法，复用现有 api |
| 移除某 API | `api/module.js`, `DetailView.vue` | 删方法 + 删调用 | 路由/按钮守卫 | 定点删除 + 清引用 |
```

---

## §4 推荐执行口令（用户一条消息触发）

### 4.1 默认 · Reconcile 代码同步

```text
@skills/incremental-implementation/SKILL.md
@specs/<change-id>/<vN>-对齐分析.md
@specs/<change-id>/实现映射.md

请按 incremental-implementation 执行 Reconcile 代码编排（IC-R0~IC-R7）：
在现有代码基础上做增量迭代，禁止 greenfield 重跑。
change-id：<change-id>
基准源文档版本：vN
要求：git 基线 → 多产物版本检测 → 变更分类（四类齐全）→ 最小编辑 → 回写映射与 tasks。
```

### 4.2 接力 pipeline R6（文档已 reconcile，只改代码）

```text
@skills/incremental-implementation/SKILL.md
@specs/<change-id>/<vN>-对齐分析.md
@openspec/changes/<change-id>/tasks.md

接力 pm-md-to-openspec-pipeline R6：按对齐分析「应剔除/应新增」在旧代码上最小 diff。
默认 IC-R4~IC-R7；文档侧已 R0~R5 完成，勿回改契约语义。
```

### 4.3 局部代码更新

```text
@skills/incremental-implementation/SKILL.md
@specs/<change-id>/实现映射.md

仅局部更新：删除 `src/modules/<module>/api.js` 中的 `<symbol>` 及相关 UI 引用。
启用局部代码更新护栏：列出未同步的 field-matrix / tasks / 映射项，暂不同步文档等我确认。
```

### 4.4 映射缺失 · 先反向建图

```text
@skills/incremental-implementation/SKILL.md
change-id：<change-id>

请先执行 P0.5 反向建图：扫描已实现 tasks.md，从现有代码回填 specs/<change-id>/实现映射.md。
锚点无法定位的标「锚点待确认」，不要臆造路径。建完图后停下来等我确认再进入增量。
```

---

## §5 tasks.md 状态约定（可选增强）

若希望 `tasks.md` 自身也带锚点，可在每条任务下追加一行（与 `实现映射.md` 二选一或并存）：

```markdown
- [x] T1-1 列表页分页与筛选
  → 实现：src/modules/<module>/ListView.vue（commit a1b2c3d）
```

推荐「单独建 `实现映射.md` 集中管理」；`tasks.md` 保持勾选 + 可选指向映射。

---

## §6 Reconcile 代码编排 · IC-R7 快速核对表

| # | 检查项 |
|---|--------|
| IC-R7-1 | 对齐分析「应剔除」在代码中已无实现与悬挂引用 |
| IC-R7-2 | 对齐分析「应新增」在代码中已有锚点，或标 TBD + 问谁 |
| IC-R7-3 | 「仍保留 / 不变」项经 `git diff` 确认未被误改 |
| IC-R7-4 | `实现映射.md` 已废弃项标 `已废弃` + commit，未静默删除行 |
| IC-R7-5 | 多产物 `基准源文档版本：vN` 一致（映射 / tasks / 契约四文件） |
| IC-R7-6 | IC-R6 matrix vs 代码 diff 已列；不一致未静默忽略 |
| IC-R7-7 | 收尾首行已标 vN + 基准 commit + reconcile 日期 |

---

## §7 局部代码更新护栏 · 快速核对表

| # | 检查项 |
|---|--------|
| L-I1 | 已输出「本次仅改 ＜模块/文件＞，未同步产物清单」表 |
| L-I2 | 用户已确认「暂不同步文档」或已触发全链同步 |
| L-I3 | 输出含「局部更新风险声明」，明确 IC-R7 未闭合 |
| L-I4 | 未悄悄勾选 tasks Gate / 宣称「已按 vN 对齐」 |
| L-I5 | 删除类变更已同步更新 `实现映射.md` 对应锚点状态 |

**局部更新必含输出模板**：

```markdown
### 本次局部代码更新
- 受改路径：…
- 变更摘要：…

### 未同步产物（漂移风险）
| 产物 | 受牵连之处 | 是否已过时 | 处置建议 |
|------|-----------|-----------|----------|
| `field-matrix.md` §x | | 是 / 否 / 待核对 | 回 pipeline 齐刷 / 用户确认暂不同步 |
| `实现映射.md` T2-x | | | |
| `tasks.md` Gate | | | |

### 局部更新风险声明
> 本轮**仅**改上述代码；契约 / 映射 / tasks **未**同步至当前基准。IC-R7 **未闭合**。
```

---

## §8 多产物版本漂移检测表（IC-R2）

进入 P3 之前填写：

```markdown
| 产物路径 | 声明的基准版本 | 与目标 vN 一致？ |
|----------|---------------|-----------------|
| specs/<change-id>/实现映射.md | | ✅ / ❌ 漂移 |
| specs/<change-id>/变更规格-Change-Spec.md | | |
| openspec/changes/<change-id>/tasks.md | | |
| openspec/changes/<change-id>/specs/<cap>/field-matrix.md | | |
| … | | |

**处置**：存在 ❌ 时暂停改代码 → 建议 pipeline Reconcile R0~R5 或用户书面指定基准。
```

---

## §9 与 pm-md-to-openspec-pipeline 的分工索引

| 阶段 | 技能 | 产出 |
|------|------|------|
| 文档 Reconcile R0~R5 | `pm-md-to-openspec-pipeline` | `<vN>-对齐分析.md`、Change Spec、四文件契约 |
| 文档 R6（默认） | `pm-md-to-openspec-pipeline` | 代码 diff **建议**，不改代码 |
| 代码 Reconcile IC-R0~IC-R7 | **本技能** | 最小代码 diff + 回写映射 / tasks |
| 契约 Gate | `openspec-contract-authoring` | Open Questions / Evidence 闭合 |

---

## §10 安装与可发现性（Fallback）

若 `@incremental-implementation` 未出现在 Agent 技能列表：

1. 确认 `frontend-team-toolkit` 插件已安装并重载 Cursor
2. Fallback：`Read <repo>/plugins/frontend-team-toolkit/skills/incremental-implementation/SKILL.md`
3. 业务仓 `AGENTS.md` 可追加本技能路径与触发词

---

## §11 技能执行反馈归档

优化技能后，执行反馈可归档至：

- `specs/<change-id>/skill-execution-feedback.md`
- 或本目录 **[BACKLOG.md](BACKLOG.md)** 追加条目
