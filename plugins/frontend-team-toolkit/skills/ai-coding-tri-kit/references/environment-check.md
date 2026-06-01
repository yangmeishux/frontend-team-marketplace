# Environment Pre-check — 环境前置检查

执行三件套前必须确认环境可用性，避免执行中途阻塞。

## 检查清单

| 检查项 | 命令 | 最低要求 | 缺失处理 |
|--------|------|----------|----------|
| Node.js | `node --version` | ≥20.19.0 | 提示安装或手写方案 |
| git | `git status` | 已 init | 提示初始化或目录备份隔离 |
| OpenSpec CLI | `npx @fission-ai/openspec --version` | 可执行 | 手写四件套结构 |
| Superpowers | 检查 AGENTS.md / skill 列表 | skill 元数据注入上下文 | 用本 skill 模拟流程 |
| Agent Skills | `agent-skills list` | 核心技能 enable | 用本 skill 内嵌约束替代 |
| 网络（npm registry） | `ping registry.npmjs.org` 或 `curl -I https://registry.npmjs.org` | 可达 | 离线手写方案 |

## 缺失时的降级路径

```text
全部缺失 → Lite 档位 + 手写验收口径 + 直接改 + 测试底线 + secrets 检查
部分缺失 → Standard + 手写四件套 + 模拟 brainstorming + 普通 feature 分支
环境完整 → Full 标准流程（worktree + 子 Agent 并行 + CI 双保险）
```

## 降级模式对照

| 环境 | 推荐档位 | OpenSpec | Superpowers | Agent Skills | 隔离方式 |
|------|----------|----------|-------------|--------------|----------|
| 完整（全✅） | Full | CLI + validate | skill 自动加载 | enable 核心 | worktree |
| 部分（git/node ✅，其他 ⚠️） | Standard | 手写四件套 + 人审 | 模拟 brainstorming | 本 skill 内嵌约束 | feature 分支 |
| 最小（仅 git/node ⚠️） | Lite | 口头验收 | 跳过 | 仅测试/secrets底线 | 当前分支 |
| 无 git | Standard/Lite | 手写 | 模拟 | 本 skill 内嵌 | 目录备份 |
| 无网络 | Standard | 手写四件套 | 模拟 | 本 skill 内嵌 | 视 git 状态 |

## 会话开始时的输出格式

```markdown
## Environment Pre-check

| 检查项 | 状态 | 备注 |
|--------|------|------|
| Node.js | ✅ / ⚠️ / ❌ | 版本号或缺失 |
| git | ✅ / ⚠️ / ❌ | 已 init 或提示初始化 |
| OpenSpec CLI | ✅ / ⚠️ / ❌ | 可执行或手写方案 |
| Superpowers | ✅ / ⚠️ / ❌ | 已注入或模拟 |
| Agent Skills | ✅ / ⚠️ / ❌ | 核心 enable 或内嵌约束 |
| 网络 | ✅ / ⚠️ / ❌ | 可达或离线方案 |

**推荐档位**：Full / Standard / Lite（基于环境状态）
**缺失项处理**：[具体降级方案]

是否继续执行？[等待用户确认]
```

## 手写 OpenSpec 四件套结构

当 OpenSpec CLI 不可用时，手动创建以下目录结构：

```text
openspec/changes/<change-id>/（手动创建目录）
├── proposal.md   （手写内容模板见下）
├── specs/<capability>/spec.md （手写内容模板见下）
├── design.md     （手写内容模板见下）
└── tasks.md      （手写内容模板见下）
```

### proposal.md 手写模板

```markdown
# Change: <change-id>

## Why
[为什么要做这个变更，解决什么问题]

## What Changes
[要改什么，涉及哪些模块/文件]

## Impact
[影响面：用户、系统、其他模块]
```

### spec.md 手写模板

```markdown
# Spec: <capability>

## ADDED Requirements

### Requirement: <需求标题>
用户 MUST [可验证的行为]
系统 MUST [可验证的行为]

#### Scenario: <场景标题>
**WHEN** [触发条件]
**THEN** 系统 MUST [预期结果]
**AND** [补充条件]
```

### design.md 手写模板

```markdown
# Design: <change-id>

## Decisions
1. [决策项]
   - Decision：[具体决定]
   - Rationale：[决策理由]

## Open Questions
- [未决问题] —— 需 [谁] 确认
```

### tasks.md 手写模板

```markdown
# Tasks: <change-id>

## 1. [任务组]
- [ ] 1.1 [具体任务] —— 文件：[路径]
- [ ] 1.2 [具体任务] —— 验收：[标准]

## 2. [任务组]
- [ ] 2.1 [具体任务]
```

## 与 Output Contract 对齐

环境检查结果应写入会话首节的 **Session Summary** 或单独的 **Environment Pre-check** 节。

当环境不完整时，**Gate 0 Environment** 应标记为 `PASS_WITH_FALLBACK` 或 `BLOCKED`（严重缺失时）。