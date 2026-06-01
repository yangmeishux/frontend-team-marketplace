---
name: ai-coding-tri-kit
description: "编排 OpenSpec + Superpowers + Agent Skills 三件套 8 步工程化工作流。Use when 用户要做新功能/中等以上改动、要求可预测交付、提到三件套/OpenSpec+Superpowers、/opsx:propose 到 archive 全流程、或 AI 编程从碰运气变可复制；即使用户只说「按三件套走一遍」或「先对齐 spec 再开发」也应使用本 skill。"
license: MIT
metadata:
  version: "0.2.0"
  author: wechat-agents
  maturity: beta
  source_article: "AI 编程进阶：三件套 OpenSpec 定方向，Superpowers 带节奏，Agent Skills 守纪律"
---

# AI 编程三件套工作流（Ai Coding Tri-Kit）

> **铁三角**：OpenSpec 定方向（What）→ Superpowers 带节奏（How）→ Agent Skills 守纪律（Quality）  
> 输出契约：[`references/output-contract.md`](references/output-contract.md)  
> 步骤矩阵：[`references/workflow-matrix.md`](references/workflow-matrix.md)  
> 强度分级：[`references/intensity-tiers.md`](references/intensity-tiers.md)  
> 闸门与回退：[`references/gates-and-rollback.md`](references/gates-and-rollback.md)  
> 环境前置检查：[`references/environment-check.md`](references/environment-check.md)  
> 外部依赖检查：[`references/external-dependency-check.md`](references/external-dependency-check.md)  
> 降级方案：[`references/fallback-scenarios.md`](references/fallback-scenarios.md)

## When to Activate

- 用户发起 **新功能、重构、多文件改动**，希望需求不漂移、流程可控、质量可验
- 用户提到 **三件套、OpenSpec、Superpowers、Agent Skills** 组合使用
- 用户要使用 **`/opsx:propose` → 实现 → `/opsx:verify` → `/opsx:archive`** 完整链路
- 用户抱怨 AI **跳过 spec 直接写代码、不写测试、质量波动大**
- 团队希望把 **书面契约 + 工程流程 + 质量护栏** 串成一条可重复流水线

## When NOT to Use

- **单行 typo / <20 行 bugfix** 且用户明确要快修 → 见 [`intensity-tiers.md`](references/intensity-tiers.md) 的 Lite 模式，不必跑全套
- 用户 **只要写公众号/文档**，不涉及代码交付 → 用 content-writer 等，不用本 skill
- 仓库 **未初始化 git** 且用户拒绝初始化 → Step 3 worktree 不可执行，须 BLOCKED 或降级
- 用户 **只要 OpenSpec 提案**、不要实现 → 只执行 Step 1–2，在 Checkpoint 停住

## Prerequisites（执行前自检）

**前置**：先 Read [`references/environment-check.md`](references/environment-check.md)，确认环境可用后再进入步骤。

| 组件 | 最低要求 | 缺失时 |
|------|----------|--------|
| Node.js | ≥20.19.0 | 提示安装或降级手写方案 |
| git | 仓库已 init | 提示初始化或目录备份隔离（见 fallback-scenarios） |
| OpenSpec | `openspec/` 或 `openspec init` 已完成 | 手写四件套结构 |
| Superpowers | brainstorming / writing-plans / TDD 等 skill 在上下文 | 用本 skill 模拟流程 |
| Agent Skills | 核心 skill 已 enable（见 Step 映射） | 用本 skill 内嵌约束替代 |
| 网络 | npm registry 可达 | 离线手写方案（见 fallback-scenarios） |

**强度分级**：先 Read [`references/intensity-tiers.md`](references/intensity-tiers.md)，确定 Full / Standard / Lite，再进入对应步骤。

## Core Principle（不可违背）

```text
顺序执行，不可跳跃（Lite 模式除外）：
  OpenSpec 先说清楚 → Superpowers 走对流程 → Agent Skills 守质量

强度分层（见 workflow-matrix）：
  程序性强制 = CLI/编译/CI（openspec validate、测试、扫描）
  AI 行为约束 = Superpowers + Agent Skills（可能漏选，人可显式指定）
  流程惯例     = 团队共识 + 人审
```

**关键质量门槛必须落两层**：AI skill 引导 + CI/pre-commit 闸门（secrets、覆盖率等不可只交给 skill）。

---

## Workflow — 8 步主链路

执行时用下方 **Progress Checklist** 跟踪；每步完成须满足 **Exit Criteria** 才能进下一步。

### Progress Checklist

```text
- [ ] Step 1 需求对齐（OpenSpec）
- [ ] Step 2 需求澄清（Superpowers + req-clarify）
- [ ] Step 3 分支隔离（worktrees + baseline）
- [ ] Step 4 计划制定（writing-plans + req-breakdown）
- [ ] Step 5 子 Agent 并行开发（subagent-driven-dev + 结构/TDD 约束）
- [ ] Step 6 测试 + 审查（TDD + code review + coverage）
- [ ] Step 7 安全检查（security-*）
- [ ] Step 8 验证 + 收尾（openspec verify + production-ready + archive）
```

---

### Step 1：需求对齐 — OpenSpec 主导

**动作**：
1. **禁止写实现代码**
2. 读取 `openspec/project.md`、`openspec/AGENTS.md`（若存在）
3. 运行 `openspec list` 与 `openspec list --specs`（若 CLI 可用）
4. 创建变更目录 `openspec/changes/<change-id>/`，生成：
   - `proposal.md` — Why / What Changes / Impact
   - `specs/<capability>/spec.md` — ADDED Requirements + Scenario（WHEN/THEN/MUST）
   - `design.md` — Decisions + Open Questions
   - `tasks.md` — 可勾选实现清单
5. 运行 `openspec validate <change-id> --strict`（或 `npx @fission-ai/openspec validate <change-id>`）

**Exit Criteria**：validate 通过 **或** 用户书面确认「proposal/spec 可开发」  
**Checkpoint**：未确认前 **STOP** — 不得进入 Step 5 写生产代码

---

### Step 2：需求澄清 — Superpowers + Agent Skills

**前置**：涉及第三方 SDK/API 时，Read [`references/external-dependency-check.md`](references/external-dependency-check.md) 执行可行性检查。

**动作**：
1. 加载 **brainstorming**（Superpowers）：Socratic 式追问 spec/design 中的模糊词
2. 遵从 **req-clarify**（Agent Skills）：**最多 3 轮**澄清，超时则汇总 Open Questions 写入 `design.md`
3. **外部依赖检查**（新增）：
   - Q-ext-1: SDK/AppID/API Key 是否已申请？
   - Q-ext-2: SDK 官方维护状态？
   - Q-ext-3: 法务/隐私合规是否需审批？
   - Q-ext-4: 测试账号/沙箱是否就绪？
4. 将确认结论回填 `design.md` Decisions；未决项写入 Open Questions
5. **BLOCKED 渠道处理**：存在外部阻塞时，建议分阶段实现，记录 Phase 分割

**Exit Criteria**：`design.md` 含 Decisions + Open Questions；外部依赖状态明确；用户说「确认」  
**典型问题模板**（按需选用）：
- 模糊词（「后台运行」「尽快」）的可验证定义？
- 外部依赖/SDK/降级策略？
- 兜底文案、占位图、权限由谁审？

---

### Step 3：分支隔离 — Superpowers 主导

**动作**（Full/Standard 模式）：
1. 加载 **using-git-worktrees**
2. `git worktree add -b <branch> <path>` 创建隔离 workspace
3. 跑 **baseline**：项目标准测试/构建命令（如 `npm test`、`./gradlew test`）
4. baseline 必须绿；失败则先修基线或报告 BLOCKED

**Lite 模式**：普通 feature 分支即可，跳过 worktree  
**Exit Criteria**：隔离环境就绪 + baseline 全绿

---

### Step 4：计划制定 — Superpowers + OpenSpec 输入

**动作**：
1. Read OpenSpec `tasks.md`
2. 加载 **writing-plans**：每条任务细化到 **文件路径 + 预估时间 + 验收口径**
3. 加载 **req-breakdown**：每个任务 **可独立验证、可独立回滚**
4. 输出实现计划文档（可写入 `docs/plans/<change-id>.md` 或直接在对话中）

**Exit Criteria**：计划覆盖 `tasks.md` 全部条目，无「写一个 XX 功能」级模糊任务

---

### Step 5：子 Agent 并行开发 — Superpowers + Agent Skills

**动作**：
1. 加载 **subagent-driven-development**（或 **executing-plans** 若单线程）
2. 按 `design.md` Decisions 划分子任务；无依赖项 **可并行**派发子 Agent
3. 每个子 Agent **两阶段审查**：
   - 规格一致性：对照 `spec.md` MUST 条款
   - 代码质量：命名/结构/异常
4. 全程遵守 Agent Skills 约束（模型层）：
   - `code-structure`：文件 ≤500 行，函数 ≤50 行
   - `test-driven-development`：先 RED 再 GREEN
   - `code-documentation`：公开 API 有文档

**Exit Criteria**：`tasks.md` 全部 `[x]`；无 CRITICAL 级规格偏离

---

### Step 6：测试 + 审查 — Superpowers + Agent Skills 量化

**动作**：
1. **test-driven-development**：关键 Scenario 有失败测试 → 实现 → 全绿
2. **verification-before-completion**：宣称通过前必须跑过测试命令并贴输出摘要
3. **requesting-code-review**：按 🔴 CRITICAL / 🟡 WARNING / 🟢 INFO 分级
4. Agent Skills 量化：
   - `test-coverage`：分支覆盖 ≥80%（以报告为准）
   - `test-quality`：覆盖 spec 核心 Scenario

**Exit Criteria**：测试全绿 + 审查无 CRITICAL + 覆盖率达标（或用户接受豁免并记录）

---

### Step 7：安全检查 — Agent Skills 主导

**动作**（已 enable 时）：
- `security-secrets` — 无 token/密钥泄漏
- `security-dependencies` — 无 high/critical 漏洞
- `security-api` — API/URL 不携带敏感信息

**任意失败 → STOP**，修复后重跑；**CI 同步**才算不可绕过  
**Exit Criteria**：三项扫描通过或 CI 等价检查通过

---

### Step 8：验证 + 收尾 — 三方协作

**8a OpenSpec 验证**：
```bash
openspec validate <change-id> --strict
# 或 /opsx:verify — 逐条对照 spec Scenario
```

**8b Agent Skills — production-ready**：
- 单测/集成测全绿、覆盖率达标、无 secret 泄漏、feature flag/回滚方案（若适用）

**8c Superpowers — finishing-a-development-branch**：
- 提供 Merge / Create PR / Keep / Discard 选项；**默认不自动 merge**

**8d OpenSpec 归档**：
```bash
openspec archive <change-id> --yes
openspec validate --strict
```

**Exit Criteria**：validate 通过 + 用户选定收尾动作 + archive 完成（若用户要求归档）

---

## Checkpoints（必须暂停）

| 场景 | 动作 |
|------|------|
| Step 1 未确认 spec | STOP，不得写实现代码 |
| Open Questions 阻塞实现 | STOP，列出需产品/法务确认项 |
| baseline 失败 | STOP，不得归因于新代码 |
| 安全扫描失败 | STOP，不得进入 Step 8 发布 |
| 实现暴露 spec 缺口 | STOP，先更新 OpenSpec 产物再继续 |
| 用户未要求 merge/push | 不得自动 push 或 force 操作 |

---

## Output Contract

完整格式见 [`references/output-contract.md`](references/output-contract.md)。

每次会话至少输出：
1. **当前 Step** 与 Progress Checklist 勾选状态
2. **主导工具**（OpenSpec / Superpowers / Agent Skills）与本步 Exit Criteria
3. **证据摘要**（validate 输出、测试命令结果、覆盖率数字）
4. **闸门状态**（通过 / 阻塞 / 需人审）

---

## Skill Routing（步骤 → 外部 Skill）

详细映射见 [`references/workflow-matrix.md`](references/workflow-matrix.md)。

| Step | OpenSpec | Superpowers | Agent Skills |
|:----:|----------|-------------|--------------|
| 1 | propose, validate | — | — |
| 2 | 更新 design.md | brainstorming | req-clarify |
| 3 | — | using-git-worktrees | — |
| 4 | tasks.md 输入 | writing-plans | req-breakdown |
| 5 | spec 对照 | subagent-driven-development | code-structure, TDD, code-documentation |
| 6 | — | TDD, requesting-code-review, verification-before-completion | test-coverage, test-quality |
| 7 | — | — | security-* |
| 8 | verify, archive | finishing-a-development-branch | production-ready |

**AI 漏选 skill 时**：用户或本 skill 显式点名，例如「按 test-driven-development 先写 RED 测试」。

---

## Anti-patterns

| 跑偏 | 纠正 |
|------|------|
| 跳过 Step 1 直接写代码 | 回到 propose；至少补 proposal + spec |
| 把 skill 当系统钩子、宣称不可绕过 | 说明需 CI/pre-commit；见 gates-and-rollback |
| 澄清超过 3 轮仍发散 | req-clarify：强制汇总 Open Questions |
| 未跑测试宣称完成 | verification-before-completion：贴命令输出 |
| 单文件 2000 行 ShareCoordinator | code-structure：拆分 + CI lint |
| 安全失败仍 archive | Step 7 闸门：修复后重跑 |

---

## Eval & Upgrade

- 测试集：`evals/evals.json`（3 regression + 3 capability = 7）
- Fixtures：`fixtures/cap-case-*/`
- 真落盘 demo：`source/live-app-openspec-demo/openspec/changes/feat-dashboard-csv-export/`
- 问题池：`skill-issues.jsonl`
- 升级流程：仓库 `articles/skill-upgrade-sop.md`

## Bundled Resources

| 路径 | 何时读取 |
|------|----------|
| `references/environment-check.md` | 会话开始，确认环境可用性 |
| `references/external-dependency-check.md` | Step 2 涉及第三方 SDK/API 时 |
| `references/fallback-scenarios.md` | 环境受限或降级时 |
| `references/workflow-matrix.md` | 每步执行前确认工具分工 |
| `references/intensity-tiers.md` | 会话开始，确定 Full/Standard/Lite |
| `references/gates-and-rollback.md` | 闸门失败或用户问「卡住了怎么办」 |
| `references/output-contract.md` | 交付前自检 |
| `examples/feat-live-share-third-party-walkthrough.md` | Full 档位完整案例（直播分享第三方） |
| `examples/feat-dashboard-csv-export-walkthrough.md` | Standard 档位 Step 1–2 真落盘（capability eval） |
| `../live-app-openspec-demo/CHECKPOINT-feat-dashboard-csv-export.md` | **续跑入口** — Step 3–8 进度与待办 |
| `scripts/validate-output.sh` | 输出完成后（可选） |
