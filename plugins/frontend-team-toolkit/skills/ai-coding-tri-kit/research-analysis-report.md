---
title: AI 编程三件套技能深度调研分析报告
date: 2026-05-31
author: PAI
status: draft
---

# 深度调研分析报告：ai-coding-tri-kit 技能

## 一、调研目标与范围

### 1.1 核心问题

1. 技能 `ai-coding-tri-kit` 与用户文章《AI 编程进阶：三件套》是否契合？
2. 技能设计是否合理？
3. 是否过于理想化？
4. 是否有不切实际的操作？
5. 若有问题，如何调整？具体改进方案与实践操作？

### 1.2 分析对象

| 对象 | 来源 |
|------|------|
| 用户文章 | `/Users/nathan/Documents/Obsidian Vault/2026年写的文章/AI 编程进阶：三件套...md` |
| 技能 SKILL.md | `source/skills/ai-coding-tri-kit/SKILL.md` |
| 技能参考文件 | `references/intensity-tiers.md`, `gates-and-rollback.md`, `workflow-matrix.md`, `output-contract.md` |
| 示例 walkthrough | `examples/feat-live-share-third-party-walkthrough.md`, `feat-dashboard-csv-export-walkthrough.md` |
| 测试验证 | `test-prompts.json`, `results.tsv`, `fixtures/` |
| 实际落盘制品 | `source/live-app-openspec-demo/openspec/changes/feat-dashboard-csv-export/` |

---

## 二、契合度分析：技能 vs 文章

### 2.1 核心理念对照

| 维度 | 文章表述 | 技能表述 | 契合度 |
|------|----------|----------|--------|
| **铁三角定位** | OpenSpec 定方向（What）→ Superpowers 带节奏（How）→ Agent Skills 守纪律（Quality） | 完全一致引用，首行即声明 | ✅ 100% |
| **问题诊断** | 需求漂移、流程失控、纪律缺失 | 同样三问题，触发条件映射 | ✅ 100% |
| **强度分层** | 程序性强制、AI行为约束、流程惯例 | `gates-and-rollback.md` 详细三层 | ✅ 100% |
| **8步主链路** | Step 1-8 完整流程图 + 闸门子图 | Progress Checklist + Exit Criteria | ✅ 95% |
| **强度分级** | 文章提及 Full/Standard（第六章跳过某些步骤） | `intensity-tiers.md` 三档完整定义 | ✅ 良好延伸 |
| **时间估算** | 40-65分钟（人10-15分钟） | walkthrough 附耗时表 | ✅ 一致 |

### 2.2 结构对照

| 文章章节 | 技能对应 | 契合判定 |
|----------|----------|----------|
| 第一章认识三位主角 | Prerequisites 表 + Skill Routing | ✅ 精简复刻 |
| 第二章三者结合 | workflow-matrix.md 关系模型 | ✅ 结构化表达 |
| 第三章完整工作流 | SKILL.md 8步 + walkthrough | ✅ 实操导向 |
| 第四章安装配置 | Prerequisites 缺失时提示 | ⚠️ 简化（合理） |
| 第五章实战案例 | walkthrough 示例 | ✅ 分档位案例 |
| 第六章进阶技巧 | intensity-tiers + gates | ✅ 分级 + 回退 |
| 第七章效率对比 | 未在技能中重复（文章内容） | ✅ 合理省略 |
| 第八章FAQ | Anti-patterns + 补救表 | ✅ 症状-补救映射 |

### 2.3 关键差异（非冲突，而是定位差异）

| 差异点 | 文章 | 技能 | 分析 |
|--------|------|------|------|
| **受众** | 教学向，完整讲解 | Agent 执行向，指令式 | ✅ 合理定位差异 |
| **Star数据** | 详细列出（43k/169k/24k） | 无（变化数据不适合固化） | ✅ 合理省略 |
| **安装命令** | 每平台详细命令 | Prerequisites 缺失时提示安装 | ⚠️ 可补充但不必要 |
| **竞品对比** | vs GitHub Spec Kit / AWS Kiro | 无 | ✅ 教学内容，技能不需要 |
| **Mermaid图** | 多个流程图 | 无图，纯表格 | ⚠️ 技能可补充简化图 |

**契合度总评**：**92% 高度契合**

技能精准提取了文章的**可执行内核**，省略了教学性内容（安装细节、竞品对比、Star数据），这是正确的 skill 设计决策。

---

## 三、合理性分析

### 3.1 合理的设计点（✅）

#### 3.1.1 强度分层是关键创新

技能的 `intensity-tiers.md` 是文章的有益延伸：

```markdown
| 维度 | Full | Standard | Lite |
|------|------|----------|------|
| OpenSpec | 完整 4 件套 | propose + spec | Issue/口头描述 |
| 澄清轮次 | brainstorming ≤3 轮 | 1–2 个关键问题 | 跳过 |
| Worktree | 必须 | 可选 | 跳过 |
```

这解决了"小改动也要跑全套？"的实际痛点。

#### 3.1.2 Checkpoint 阻断机制明确

```markdown
| 场景 | 动作 |
|------|------|
| Step 1 未确认 spec | STOP，不得写实现代码 |
| Open Questions 阻塞实现 | STOP，列出需产品/法务确认项 |
```

这是**防御性设计**，防止 AI 跳流程。

#### 3.1.3 Output Contract 可验证

`output-contract.md` 定义了每步必须输出的字段：

- Session Summary
- Progress Checklist（勾选状态）
- Step Detail（证据）
- Gate Status

这让技能执行**可审计**。

#### 3.1.4 红线测试设计

`fixtures/cap-case-red-line/skip-spec-trap.md` 测试用户要求"跳过 OpenSpec 直接写代码"时 Agent 是否拒绝。这是**关键防护测试**。

#### 3.1.5 实际落盘验证

`results.tsv` 显示 7/7 evals PASS，且有真落盘制品：
- `feat-dashboard-csv-export/` 四件套完整
- `feat-live-share-third-party/` 已存在

### 3.2 存疑的设计点（⚠️）

#### 3.2.1 前置依赖的可用性假设

技能假设 OpenSpec、Superpowers、Agent Skills 都已安装：

```markdown
| 组件 | 最低要求 | 缺失时 |
|------|----------|--------|
| OpenSpec | `openspec/` 或 `openspec init` 已完成 | Step 1 只能手写... |
| Superpowers | brainstorming 等在上下文 | 显式按本 skill 步骤模拟 |
```

**问题**：如果三者都缺失，"模拟"的可行性存疑。Agent 可能无法真正执行 brainstorming 的 Socratic 行为。

**实际测试情况**：`results.tsv` 显示在 `source/live-app-openspec-demo/` 环境下执行成功，但该环境已有 OpenSpec 初始化。

#### 3.2.2 子 Agent 并行的实际可行性

技能描述：

```markdown
子 Agent 切分：
| Agent-UI | 1.2, 1.3 面板+入口 | ✅ 并行 |
| Agent-WeChat | 2.2, 2.3 | ✅ 并行 |
```

**问题**：实际 AI 编码工具是否支持这种子 Agent 并行派发？

- Claude Code 支持 `Agent` 工具创建子 agent，但并行控制有限
- Cursor 的 Agent 模式并行能力待验证
- Codex CLI 的子 agent 支持程度不明

**建议**：技能应标注"子 Agent 并行依赖工具能力"，降级方案是 `executing-plans` 单线程。

#### 3.2.3 安全扫描的实际执行

```markdown
Step 7：安全检查
- security-secrets — 无 token/密钥泄漏
- security-dependencies — 无 high/critical 漏洞
```

**问题**：Agent Skills 的 `security-*` skills 是**AI 行为约束**，不是真正的扫描工具。它们提醒 AI 检查，但不会自动运行 `gitleaks` 或 `trivy`。

**技能已声明**："CI 同步才算不可绕过"，这是正确的诚实声明，但实际执行时可能被误解。

---

## 四、理想化程度分析

### 4.1 过度理想化的点（❌ 需改进）

#### 4.1.1 时间估算可能过于乐观

文章声称："人真正需要投入的时间：约 10-15 分钟"

**现实挑战**：

1. **Step 2 澄清**：用户回答问题需要思考，5-10分钟可能不够
2. **Step 5 子 Agent**：SDK 接入、ROM 兼容的实际调试时间未计入
3. **Step 6 审查**：人审阅代码的时间与改动规模正相关

**改进建议**：区分"AI推理时间"与"实际工程时间"，明确标注不含：
- 真机回归
- SDK 联调/鉴权申请
- CI 排队
- 跨团队审批

#### 4.1.2 Superpowers skill 自动加载假设

技能假设 Superpowers 的 brainstorming 等会"按上下文主动选用"：

```markdown
AI 在加载 `brainstorming` skill 后主动进入 Socratic 模式
```

**现实情况**：

- Claude Code 需用户显式触发或 skill 元数据正确注入
- AI 可能"漏选" skill，需要人显式指定

**技能已处理**："AI 漏选 skill 时人要显式指定"，但这对用户要求较高。

#### 4.1.3 测试覆盖率的实际达成

技能要求"分支覆盖率 ≥80%"：

```markdown
test-coverage：分支覆盖 ≥80%（以报告为准）
```

**现实挑战**：

- 首版实现可能只有 60-70%
- 达到 80% 需要补边界测试，增加时间
- CI 门禁配置需团队事先完成

**技能已声明**："不达标禁止提交需把覆盖率门槛配置到 CI"，但实际执行时可能成为阻塞点。

### 4.2 合理现实的点（✅）

#### 4.2.1 强度分级务实

Lite 模式承认小改动不必跑全套：

```markdown
| Lite 档位 | 保留 TDD + secrets 底线，跳过完整 propose/worktree |
```

这是务实的妥协，避免了"银弹"陷阱。

#### 4.2.2 Skill ≠ 系统强制

技能明确声明：

```markdown
关键质量门槛必须落两层：AI skill 引导 + CI/pre-commit 闸门
```

这是诚实的边界声明，没有夸大 skill 的强制能力。

#### 4.2.3 不可自动 merge

```markdown
不得自动 push、merge、archive 除非用户明确要求
```

这是正确的安全底线。

---

## 五、不切实际操作分析

### 5.1 可能不切实际的点

#### 5.1.1 worktree 在非 git 仓库

```markdown
Step 3：分支隔离
git worktree add -b <branch> <path>
```

**现实问题**：很多项目未初始化 git，或使用 SVN/其他 VCS。

**技能已处理**："仓库未初始化 git 且用户拒绝初始化 → Step 3 跳过 worktree，改普通分支"

但"普通分支"在非 git 仓库也不可行。应补充：无 git 时使用目录备份/复制隔离。

#### 5.1.2 openspec CLI 的全局可用性

技能频繁引用：

```bash
npx @fission-ai/openspec validate <change-id>
```

**现实问题**：

- 需要网络访问 npm registry
- 需要 Node.js ≥20.19.0
- 中国网络可能有访问限制

**改进建议**：补充离线/手动方案（手写四件套结构，人审确认）。

#### 5.1.3 多 SDK 并行接入的实际复杂度

walkthrough 示例涉及微信/QQ/微博三个 SDK：

```markdown
Agent-WeChat | 2.2, 2.3 微信+朋友圈（同一 SDK）
Agent-QQ | 2.4 QQ + QQ 空间
```

**现实挑战**：

- 微信 SDK 需要企业认证、AppID 申请
- QQ SDK 需要腾讯开放平台注册
- 微博 SDK 可能已停更或法务问题

这些**非技术门槛**未在技能中体现，可能导致 Step 5 阻塞时间远超预期。

**改进建议**：在 Step 2 澄清阶段增加"外部依赖可行性检查"问题。

---

## 六、改进方案

### 6.1 结构性改进

#### 6.1.1 增加前置环境检查清单

**改进内容**：

```markdown
## Environment Pre-check（新增）

执行 Step 1 前必须确认：

| 检查项 | 命令/方法 | 缺失处理 |
|--------|----------|----------|
| Node.js ≥20 | `node --version` | 提示安装或用替代方案 |
| git init | `git status` | 提示初始化或用目录备份 |
| OpenSpec CLI | `npx @fission-ai/openspec --version` | 手写四件套 |
| Superpowers | 检查 skill 列表 | 用本 skill 模拟流程 |
| Agent Skills | `agent-skills list` | 用本 skill 内嵌约束 |
| 网络 | `ping registry.npmjs.org` | 离线手写方案 |
```

#### 6.1.2 时间估算分层

**改进内容**：

```markdown
## Time Estimate（修订）

| 时间类型 | Full | Standard | Lite |
|----------|------|----------|------|
| **AI推理+命令** | 30-40 min | 15-25 min | 5-10 min |
| **人审阅决策** | 10-15 min | 5-8 min | 1-2 min |
| **不含** | SDK联调、真机回归、CI排队、跨团队审批 | - | - |
| **阻塞风险** | SDK鉴权、ROM兼容、法务确认 | 编码/Worker | 无 |

**时间口径说明**：上表仅计 AI 会话内可执行部分。外部依赖导致的阻塞不计入。
```

#### 6.1.3 外部依赖可行性检查

**改进内容**（加入 Step 2）：

```markdown
### Step 2 增加检查项

**brainstorming 必问**（涉及外部 SDK/API 时）：

| # | 问题 | 阻塞级别 |
|---|------|----------|
| Q-ext-1 | 第三方 SDK 是否已注册/有 AppID？ | BLOCKED 若无 |
| Q-ext-2 | SDK 官方支持状态（维护/停更）？ | 需记录 |
| Q-ext-3 | 法务/隐私合规是否需审批？ | Open Questions |
| Q-ext-4 | 测试账号/沙箱环境是否就绪？ | 影响时间估算 |

**写入 design.md Open Questions**：
- SDK 鉴权未就绪 → 标记 BLOCKED，建议分阶段实现（先 UI mock，后 SDK 接入）
```

### 6.2 操作性改进

#### 6.2.1 子 Agent 并行的降级方案

**改进内容**：

```markdown
### Step 5 执行模式选择

**判断工具能力**：

| 工具 | 并行支持 | 建议 |
|------|----------|------|
| Claude Code | Agent 工具可创建子 agent | 可尝试并行，但合并冲突需人工 |
| Cursor | Agent 模式 | 单线程更稳定 |
| Codex CLI | 待验证 | 默认单线程 |
| 其他 | 默认不支持 | 使用 executing-plans 单线程 |

**降级触发条件**：
- 子 Agent 合并冲突超过 3 次
- 工具不支持并行派发
- 用户不熟悉多 Agent 操作

**降级执行**：按 executing-plans 单线程执行，每完成一个 task 让用户检查点确认。
```

#### 6.2.2 无 git 环境的替代方案

**改进内容**：

```markdown
### Step 3 非 git 仓库替代方案

**当 git 不可用时的隔离方式**：

| 方案 | 操作 | 适用场景 |
|------|------|----------|
| 目录复制 | `cp -r project project-backup` | 小项目 |
| 分支模拟 | 在子目录创建 `backup/` | 临时隔离 |
| 容器/虚拟环境 | Docker/venv 隔离 | Python/容器化项目 |
| Feature flag | 配置开关 + 条件编译 | 增量发布项目 |

**Exit Criteria 调整**：隔离方案就绪 + 基线验证（测试/构建）绿。
```

#### 6.2.3 离线/受限环境方案

**改进内容**：

```markdown
### Step 1 离线替代方案

**当 npm registry 不可达时**：

1. **手写四件套结构**：

```text
openspec/changes/<change-id>/（手动创建目录）
├── proposal.md   （手写：Why/What/Impact）
├── specs/<cap>/spec.md （手写：ADDED Requirements + Scenario）
├── design.md     （手写：Decisions + Open Questions）
└── tasks.md      （手写：勾选清单）
```

2. **人审代替 validate**：用户审阅四件套，回复"确认可开发"作为 Gate 1 PASS。

3. **归档时手动移动**：完成后手动移动到 `archive/` 目录。
```

### 6.3 技能结构优化

#### 6.3.1 建议新增文件

| 文件 | 内容 |
|------|------|
| `references/environment-check.md` | 前置环境检查清单 |
| `references/time-estimate.md` | 分层时间估算 |
| `references/fallback-scenarios.md` | 各种受限环境的降级方案 |
| `references/external-dependency-check.md` | SDK/API 可行性检查 |

#### 6.3.2 建议修订现有文件

| 文件 | 修订内容 |
|------|----------|
| `intensity-tiers.md` | 增加时间估算分层、阻塞风险标注 |
| `gates-and-rollback.md` | 增加外部依赖 BLOCKED 场景 |
| `workflow-matrix.md` | 增加工具能力判断 |
| `SKILL.md` | 增加 Environment Pre-check 节 |

---

## 七、改进后的具体实践操作

### 7.1 Full 档位完整实践（修订版）

#### Phase 0: 环境检查（新增）

```text
[PAI]: 在开始三件套流程前，检查环境：
- Node.js: ✅ v22.1.0
- git: ✅ 已初始化
- OpenSpec: ✅ 已安装（npx 可用）
- Superpowers: ⚠️ 未确认，将用本 skill 模拟
- 网络: ⚠️ npm registry 可达但较慢

是否继续？[用户: 继续]
```

#### Step 1: 需求对齐（修订）

```text
[PAI]: 确认强度档位：
- 变更涉及：多渠道 SDK（微信/QQ/微博）→ Full
- 外部依赖：SDK 鉴权、AppID → 需 Step 2 检查

执行 /opsx:propose "直播间分享到第三方..."

产出：
├── proposal.md ✅
├── specs/third-party-live-share/spec.md ✅
├── design.md ✅
├── tasks.md ✅

验证：openspec validate PASS

Gate 1: PENDING（待人审 spec）
```

#### Step 2: 需求澄清（修订）

```text
[PAI]: brainstorming（≤3 轮）：

Q1. 「后台运行」= 进程不被杀 / 禁止发停止指令？
Q2. 微信 SDK AppID 是否已申请？[新增检查]
Q3. 微博 SDK 官方支持状态？[新增检查]
Q4. 法务对第三方分享是否有合规要求？[新增检查]

用户回答：
- Q1: 禁止发停止指令
- Q2: 微信 AppID 已申请，QQ 待申请
- Q3: 微博 SDK 官方已停更，建议降级 ACTION_SEND
- Q4: 需法务审批分享文案模板

design.md 更新：
## Decisions
- 保活策略：禁止调用直播停止 API
- 微博降级：使用 ACTION_SEND

## Open Questions
- QQ AppID 待申请 → BLOCKED 渠道 2.4
- 法务审批分享文案 → BLOCKED 标题兜底模板

Gate 1: PASS（部分渠道 BLOCKED，建议分阶段实现）
```

#### Step 3: 分支隔离（修订）

```text
[PAI]: 检查 git 可用 → ✅

创建 worktree：
git worktree add -b feat/live-share ../app-live-share

baseline:
./gradlew test → ✅ 42 tests passing

Exit: 隔离就绪 + baseline 绿
```

#### Step 5: 子 Agent 并行（修订）

```text
[PAI]: 检查工具能力 → Claude Code Agent 工具可用

但部分渠道 BLOCKED：
- Agent-QQ: BLOCKED（无 AppID）
- Agent-Weibo: 降级方案待法务确认

建议调整并行策略：
| Agent | 任务 | 状态 |
|-------|------|------|
| Agent-UI | 1.2, 1.3 | ✅ 可并行 |
| Agent-WeChat | 2.2, 2.3 | ✅ 可并行 |
| Agent-QQ | 2.4 | ⚠️ BLOCKED |
| Agent-Weibo | 2.5 | ⚠️ 待降级方案 |
| Agent-Payload | 3.1, 3.2 | ✅ 可并行 |

用户选择：
1. 先实现 UI + 微信 + Payload，QQ/微博后续迭代
2. 等待 QQ AppID 申请完成再并行

[用户: 选择 1]
```

### 7.2 Lite 档位实践（修订版）

```text
[PAI]: 确认 Lite 档位：
- fix escapeCSV null 处理
- 约 5 行改动

跳过：OpenSpec propose、worktree、完整澄清
保留：测试底线 + secrets 检查

执行：
1. 先写 RED 测试
   @Test fun `escapeCSV handles null`() { ... } → FAIL ❌

2. 写实现（5 行）
   fun escapeCSV(input: String?): String = input ?: ""

3. 跑测试 → PASS ✅

4. secrets 意识检查：无密钥改动 ✅

Output:
- Lite 档位
- 测试证据：1 test PASS
- secrets 检查：✅
- 建议提交：fix(csv): handle null input
```

---

## 八、总结与建议

### 8.1 总体评价

| 维度 | 评分 | 说明 |
|------|------|------|
| **契合度** | 92% | 高度契合，精准提取可执行内核 |
| **合理性** | 85% | 核心设计合理，部分前置假设存疑 |
| **理想化程度** | 70% | 时间估算偏乐观，依赖加载假设理想化 |
| **实践可行性** | 75% | 在理想环境可行，受限环境降级方案不足 |
| **测试覆盖** | 90% | 7/7 evals PASS，红线测试设计优秀 |

### 8.2 核心改进建议

| 优先级 | 改进项 | 预期效果 |
|--------|--------|----------|
| P0 | 增加环境前置检查 | 减少执行阻塞 |
| P0 | 增加外部依赖可行性检查 | 提前发现 SDK/审批阻塞 |
| P1 | 修订时间估算为分层 | 用户有合理预期 |
| P1 | 增加工具能力判断 | 子 Agent 并行降级有依据 |
| P2 | 增加离线/受限环境方案 | 扩大适用场景 |
| P2 | 增加非 git 环境替代方案 | 消除 git 强依赖 |

### 8.3 不需要改进的点

- 强度分层设计（Full/Standard/Lite）务实有效
- Checkpoint 阻断机制防御性好
- Output Contract 可审计性强
- 红线测试覆盖关键防护
- Skill ≠ 系统强制声明诚实正确

### 8.4 最终结论

`ai-coding-tri-kit` 技能与用户文章**高度契合**（92%），设计**核心合理**。主要问题在于：

1. **环境前置假设过于理想**：假设 OpenSpec/Superpowers/Agent Skills 都已就绪
2. **时间估算偏乐观**：未计入外部依赖阻塞时间
3. **受限环境降级方案不足**：无 git、无网络场景覆盖不全
4. **子 Agent 并行可行性依赖工具能力**：未明确判断标准

建议按优先级实施改进方案后，技能的**实践可行性可从 75% 提升至 90%+**。

---

## 附录：改进文件模板

### A. environment-check.md（新增模板）

```markdown
# Environment Pre-check

执行三件套前必须确认环境可用性。

## 检查清单

| 检查项 | 命令 | 最低要求 | 缺失处理 |
|--------|------|----------|----------|
| Node.js | `node --version` | ≥20.19.0 | 提示安装或手写方案 |
| git | `git status` | 已 init | 提示初始化或目录备份 |
| OpenSpec CLI | `npx @fission-ai/openspec --version` | 可执行 | 手写四件套 |
| Superpowers | 检查 AGENTS.md | skill 元数据注入 | 用本 skill 模拟 |
| Agent Skills | `agent-skills list` | 核心技能 enable | 用本 skill 内嵌约束 |
| 网络 | `ping registry.npmjs.org` | 可达 | 离线手写方案 |

## 缺失时的降级路径

```text
全部缺失 → Lite 档位 + 手写验收 + 直接改 + 测试底线
部分缺失 → Standard + 手写四件套 + 模拟流程
环境完整 → Full 标准流程
```
```

### B. external-dependency-check.md（新增模板）

```markdown
# External Dependency Check

涉及第三方 SDK/API 时必做的可行性检查。

## Step 2 增加问题

| # | 问题 | 阻塞级别 | 缺失处理 |
|---|------|----------|----------|
| Q-ext-1 | SDK AppID/鉴权是否已申请？ | BLOCKED | 分阶段实现或等待 |
| Q-ext-2 | SDK 官方维护状态？ | WARN | 记录降级方案 |
| Q-ext-3 | 法务/隐私合规审批？ | BLOCKED | Open Questions |
| Q-ext-4 | 测试账号/沙箱环境？ | WARN | 影响时间估算 |

## BLOCKED 渠道处理

1. 标记 design.md Open Questions
2. 建议分阶段：先实现可执行渠道，BLOCKED 渠道后续迭代
3. 时间估算调整为"不含 BLOCKED 渠道"
```