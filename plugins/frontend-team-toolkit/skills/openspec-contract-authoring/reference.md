# OpenSpec 契约化 · 参考手册

与 **`SKILL.md`** 配套：目录约定、四文件模板骨架、填空工作流摘要。**详细规则以项目内 OpenSpec 与 `openspec validate` 输出为准。** 路径兜底、proposal 生命周期与 PR 审阅扩展见 **§9–§11**。

---

## 1. 推荐目录树

```text
openspec/changes/<change-id>/
├── proposal.md                 # 若项目需要
├── design.md                   # 实现约束
├── tasks.md                    # 闸门 + 任务 + 证据
└── specs/<capability>/
    ├── spec.md                 # 需求主文档
    └── field-matrix.md         # 字段契约（最先填写）
```

---

## 2. `field-matrix.md` 骨架

表头固定；**每个字段一行**，无则写「无」。

```markdown
# 字段矩阵：<模块名>

| 字段（UI名称） | 控件类型 | 必填 | 显隐条件 | 默认值 | 限制 | 校验规则 | 文案 | 数据源/组件约束 |
|----------------|----------|------|----------|--------|------|----------|------|-----------------|
|  |  |  |  |  |  |  |  |  |
```

控件类型须明确（如 Input、Select、DatePicker、InputNumber、Cascader）；必填为 **是 / 否 / 条件** 并写明条件。

---

## 3. `design.md` 骨架

```markdown
# 实现约束：<功能名>

## 1. 组件约束
| 交互元素 | 必须使用 | 禁止 |
|----------|----------|------|
|  |  |  |

## 2. 数据源约束
| 数据 | 来源 | 禁止 |
|------|------|------|
|  |  |  |

## 3. 默认策略
- 切换类型清空策略：
- 提交策略（全量/增量/时机）：
- 错误处理策略：

## 4. 边界决策
- 加载态 / 空状态 / 只读 / 编辑 / 无权限 / 接口失败 / 重复提交：

## 5. 风控 / 权限 / 埋点（按需）
- 权限规则：
- 风控规则：
- 埋点事件：
```

策略材料未给出时写 **待确认**，并同步 **Open Questions**。

---

## 4. `spec.md` 骨架（节选）

须含：**TL;DR**、背景、Goals / Non-Goals、范围与影响、用户流程（含异常）、**§5 字段矩阵**（**引用** `field-matrix.md`，禁止仅写「按图」）、交互与校验细则、数据与接口（含清空策略）、**Open Questions**、验收标准（场景 + 验证方法）。

验收方法中列出项目约定命令，例如：

- `openspec validate <change-id> --strict`
- `pnpm run build` / `pnpm run lint`（以 `package.json` 为准）

---

## 5. `tasks.md` 骨架

```markdown
# 任务清单：<功能名>

## 闸门（Gate）——未完成前禁止宣称「已完成」
- [ ] 所有 Open Questions 已关闭（或已批准例外）
- [ ] `field-matrix.md` 已填写且无「按图/参考图」残留
- [ ] `design.md` 已写死组件、数据源、清空与提交策略
- [ ] `spec.md` 含可验收流程与标准

## 实现任务
- [ ] （按模块拆分）

## 证据（Evidence）
- [ ] `openspec validate <change-id> --strict`
- [ ] 构建 / 类型检查 / 测试（按项目）
- [ ] 关键交互截图或录屏 / 人工验收记录
```

---

## 6. 填空提示词（摘要）

对用户/Agent 的指令宜为 **「按模板填空」**，而非「帮我写需求」。规则要点：

1. 字段信息**只**写入 `field-matrix.md`。  
2. 策略**只**写入 `design.md`。  
3. 流程与验收写入 `spec.md`；任务与证据写入 `tasks.md`。  
4. **缺失信息不得脑补**，一律进 **Open Questions**。  
5. 输出四文件时可使用路径分隔符（如 `=== path ===`），**不省略章节**。  
6. 若与 `openspec validate --strict` 冲突，**以校验通过为最高优先级**（以项目为准）。

---

## 7. 发布前自检（文档侧）

- [ ] 四路径文件齐全或项目约定等价结构  
- [ ] `field-matrix` 表头齐全、无一词「按图」代替矩阵  
- [ ] `design` 含清空策略与组件/数据源约束  
- [ ] `spec` 中 Open Questions 与 tasks 闸门一致  
- [ ] `tasks` 中 Evidence 命令与仓库 package.json / CI 一致  

---

## 8. 与 CLI 的关系

OpenSpec 的安装、版本与 **strict 规则** 以各项目文档为准。本技能**不**假设全局已安装 `openspec`；写入 `tasks.md` 时使用项目实际可运行命令名。

**建议**：首次在陌生仓库落笔前，阅读根目录 **README、CONTRIBUTING、AGENTS.md**（若存在）中关于 `openspec validate` 的**示例命令**；参数（如 `--strict`、子命令名）可能因项目或 CLI 版本而异。

---

## 9. 路径变体与约定优先级（方案 A · 展开）

- **第一优先级**：目标仓库**已有**合并进主线的 `openspec` 目录结构（照抄同仓 precedent）。  
- **第二优先级**：仓库文档 declared 布局（CONTRIBUTING / 内部 Wiki 链接）。  
- **第三优先级**：本技能 **`SKILL.md` 中的常见路径表**（适用于尚未约定布局、**首次采用** OpenSpec 的仓库）。  
- **多 capability**：同一 `change-id` 下可有多个 `specs/<capability>/`；每个 capability 单独 `spec` + `field-matrix`，**共享或拆分 `design.md`/`tasks.md`** 以团队惯例为准，并在 `tasks` 中避免漏勾某一 capability。  
- **冲突处理**：若 `openspec validate` 报错指向另一路径，**以校验器期望路径修正文档**，不要只改文字不改文件位置（除非团队明确允许）。

---

## 10. `proposal.md` 与变更生命周期（方案 B）

| 话题 | 说明 |
|------|------|
| **是否必须 proposal** | 由团队流程决定：常见为「先 proposal 再开 change」或「直接 `changes/<id>`」。若仓内无 `proposal.md` 先例且无文档要求，**可不建**；若有模板则须遵守。 |
| **`proposal.md` 写什么** | 动机、范围边界、风险、与相关变更关系；**不**替代 `field-matrix` 中的字段契约。 |
| **`change-id` 命名** | 常与分支名、Ticket、RFC 号对齐；具体规则**以项目 CONTRIBUTING 为准**（如 kebab-case、禁止特殊字符等）。 |
| **合并之后** | 是否删除 `openspec/changes/<id>`、移至 `archive/`、或保留为只读历史——**团队约定**；本技能仅要求 **合并前** Gate 与 Evidence 成立。 |

---

## 11. PR / 文档审阅清单（方案 A · 扩展）

在 touches `openspec/` 的 PR 或文档评审中，除 **`SKILL.md` 摘要表**外可执行：

1. **全文检索**（在 diff 范围内）：`按图`、`参考图`、`原型`、`设计稿一致`、`差不多` → 要么已删除，要么**显式**注明「已由 field-matrix 第 x 行吸收」。  
2. **field-matrix**：新增/修改的 UI 是否**都有行**；显隐条件是否仍与 design 中组件约束一致。  
3. **spec ↔ tasks**：`Open Questions` 的每一项是否在 tasks「闸门」或「实现任务」中有**对应关闭条件**。  
4. **Evidence**：`pnpm`/`npm`/`yarn` 脚本名是否与目标分支 `package.json` `scripts` **一致**（避免复制别的仓库命令）。  
5. **design**：若 diff 更换了库或组件（如级联 → 树选择），**必须使用/禁止**表是否同步。

