# Workflow Matrix — 三件套步骤映射

本文件是 `ai-coding-tri-kit` 的步骤 → 工具 → 产出物对照表。Agent 在每步执行前应快速核对。

**前置**：先 Read `environment-check.md` 确认环境；涉及外部 SDK 时 Read `external-dependency-check.md`。

## 工具能力判断（Step 5 并行前提）

**子 Agent 并行依赖工具能力**，执行前必须判断：

| 工具 | 并行支持 | 判断方法 | 建议模式 |
|------|----------|----------|----------|
| Claude Code | Agent 工具可创建子 agent | 检查 Agent 工具可用 | 可尝试并行，合并冲突需人工 |
| Cursor | Agent 模式 | 检查 Agent 面板 | 单线程更稳定 |
| Codex CLI | 待验证 | 查文档 | 默认单线程 |
| Windsurf | 待验证 | 查文档 | 默认单线程 |
| Copilot CLI | 无子 agent | — | executing-plans 单线程 |
| 其他 | 默认不支持 | — | executing-plans 单线程 |

### 降级触发条件

| 条件 | 降级动作 |
|------|----------|
| 工具不支持子 Agent 派发 | 使用 `executing-plans` 单线程 |
| 子 Agent 合并冲突超过 3 次 | 切换单线程，每 task 检查点 |
| 用户不熟悉多 Agent 操作 | 切换单线程 |
| 存在 BLOCKED 外部依赖 | 仅并行可执行部分，BLOCKED 渠道 Phase 2 |

### 单线程执行模式

```text
executing-plans（单线程）：
  Task 1 → 完成 → 检查点确认 → Task 2 → ...
  每完成一个 task，展示 diff + 测试结果，等待用户确认再继续。
```

## 关系模型

```text
OpenSpec（What）  →  Superpowers（How）  →  Agent Skills（Quality）
     ↓                      ↓                        ↓
proposal/spec/design   流程与任务编排            代码形态与量化门槛
```

## 8 步完整映射

| Step | 名称 | 主导 | 协作 | 关键命令/Skill | 产出物 | Exit Criteria |
|:----:|------|------|------|----------------|--------|---------------|
| 1 | 需求对齐 | OpenSpec | 人审 | `/opsx:propose`, `openspec validate` | proposal.md, spec.md, design.md, tasks.md | validate PASS 或人确认 |
| 2 | 需求澄清 | Superpowers | Agent Skills | brainstorming, req-clarify | design.md 更新 Decisions/OQ | 用户确认 |
| 3 | 分支隔离 | Superpowers | — | using-git-worktrees | 隔离 worktree + baseline 绿 | baseline 全绿 |
| 4 | 计划制定 | Superpowers | OpenSpec | writing-plans, req-breakdown | 细化计划（文件级） | tasks 全覆盖 |
| 5 | 并行开发 | Superpowers | Agent Skills | subagent-driven-development, code-structure, TDD | 代码 + tasks 勾选 | 无 CRITICAL 规格偏离 |
| 6 | 测试审查 | Superpowers | Agent Skills | TDD, requesting-code-review, test-coverage | 测试报告 + 审查分级 | 测试绿 + 无 CRITICAL |
| 7 | 安全检查 | Agent Skills | CI | security-secrets/deps/api | 扫描摘要 | 三项通过 |
| 8 | 验证收尾 | 三方 | 人决策 | verify, archive, finishing-branch, production-ready | 归档 + PR/merge 决策 | validate + 用户收尾 |

## 强度 × 步骤矩阵

| Step | Full | Standard | Lite |
|:----:|:----:|:--------:|:----:|
| 1 OpenSpec | ✅ 完整 4 件套 | ✅ 简化 proposal+spec | ⚪ 口头/Issue 描述 |
| 2 澄清 | ✅ brainstorming 3 轮内 | ✅ 关键 1–2 问 | ⚪ 跳过 |
| 3 worktree | ✅ | ⚪ 普通分支 | ⚪ 当前分支 |
| 4 计划 | ✅ 文件级 | ✅ 任务级 | ⚪ 内联 TODO |
| 5 子 Agent | ✅ 并行 | ⚪ 单线程 | ⚪ 直接改 |
| 6 TDD+审查 | ✅ 全 Scenario | ✅ 核心路径 | ✅ 至少 1 测试 |
| 7 安全 | ✅ 三项 | ✅ secrets | ✅ secrets |
| 8 verify+archive | ✅ | ✅ verify | ⚪ 可选 |

图例：✅ 必做 · ⚪ 可简化 · ❌ 跳过（Lite 下 Step 1/2/3/4/8 可 ⚪）

## OpenSpec 制品最小结构

```text
openspec/changes/<change-id>/
├── proposal.md
├── design.md
├── tasks.md
└── specs/<capability>/spec.md
```

### spec.md 语法要点

- 使用 `## ADDED Requirements` / `## MODIFIED Requirements`
- 每条 Requirement 含 `MUST` / `MUST NOT` 可验证语句
- 每个 Requirement 至少一个 `#### Scenario:`，含 **WHEN / THEN / AND**

## Superpowers 子链路（Step 2–6 内部顺序）

```text
brainstorming → using-git-worktrees → writing-plans
  → subagent-driven-development | executing-plans
  → test-driven-development → requesting-code-review
  → verification-before-completion → finishing-a-development-branch
```

## Agent Skills 推荐启用集

### 按阶段开关（省 token）

```bash
# 需求阶段
agent-skills on req-clarify req-breakdown

# 开发阶段（需求完成后可 off 上面两项）
agent-skills on code-structure code-documentation test-coverage test-quality

# 发布前
agent-skills on security-secrets security-dependencies security-api production-ready
```

### 与 Superpowers 分工

| 维度 | Superpowers | Agent Skills |
|------|-------------|--------------|
| 定位 | 流程与任务拆分 | 质量与局部规则 |
| 典型 | 先澄清再写大段代码 | 函数行数、覆盖率门槛 |
| 冲突时 | 以团队规范 + CI 为准 | 同上 |

## 输入输出衔接

```text
tasks.md (OpenSpec)
    ↓
writing-plans 细化计划 (Superpowers)
    ↓
subagent 按 task 实现 + spec 对照
    ↓
test-coverage / test-quality 量化 (Agent Skills)
    ↓
/opsx:verify 对照 Scenario (OpenSpec)
    ↓
/opsx:archive 更新主 spec (OpenSpec)
```
