# Gates & Rollback — 闸门与回退

三件套的真实强度分层。Agent 必须向用户正确传达：**skill 是行为约束，CI/CLI 才是不可绕过**。

## 强度三层

| 等级 | 表现 | 由谁保证 | 本工作流示例 |
|------|------|----------|--------------|
| **程序性强制** | 命令失败即中断 | CLI / 编译器 / CI | `openspec validate`, `./gradlew test`, gitleaks |
| **AI 行为约束** | 模型主动遵守，可能漏选 | Skill 元数据 | brainstorming, TDD, code-structure |
| **流程惯例** | 文档与共识 | 团队 + 人审 | PR Reviewer、覆盖率口头约定 |

## 三大闸门子图

### 闸门 1：需求确认（Step 1 后）

```text
/opsx:propose → 人审 spec/design → 确认可开发？
  ├─ 是 → Step 2
  └─ 否 → 更新文档 / 重跑 propose → 回到 propose
```

**阻断条件**：validate 失败、用户未确认、Open Questions 阻塞核心 Scenario

### 闸门 2：代码评审（Step 6 后）

```text
TDD+实现完成 → code review → 通过？
  ├─ 是 → Step 7
  └─ 否 → 修复 / 回滚 worktree 变更 → 回到实现
```

**阻断条件**：CRITICAL 审查项、测试 RED、覆盖率低于门槛且无豁免

### 闸门 3：安全失败（Step 7）

```text
security-* 扫描 → 通过？
  ├─ 是 → Step 8
  └─ 否 → STOP 发布 → 修复+补测 → 重跑 security
```

**阻断条件**：token 泄漏、high/critical 依赖漏洞、API 携带敏感参数

## 回退策略

| 失败点 | 回退动作 | 恢复条件 |
|--------|----------|----------|
| Step 1 spec 错误 | 编辑 OpenSpec 制品，不碰代码 | validate PASS |
| Step 3 baseline 红 | 不在新 worktree 开发；修 main 或换干净基线 | baseline 绿 |
| Step 5 子 Agent 冲突 | 主 Agent 合并；必要时串行化任务 | tasks 完成且无 CRITICAL |
| Step 6 测试失败 | 撤回违规实现，按 RED-GREEN 重来 | 测试全绿 |
| Step 7 安全失败 | 不得 merge；修复后重扫 | 扫描通过 |
| ROM/真机回归失败 | 记录矩阵；feature flag 关闭或延期渠道 | 产品决策 |

**Worktree 优势**：Step 5/6 严重失败时可 `git worktree remove` 丢弃隔离目录，主分支零污染。

## AI 不按流程时的补救

| 症状 | 可能原因 | 补救 |
|------|----------|------|
| 跳过 spec 直接写代码 | OpenSpec 未 init | `openspec init && openspec update` |
| 不写测试 | Superpowers 未装 | 显式：「按 test-driven-development 先 RED」 |
| 单文件过大 | code-structure 未 on | `agent-skills on code-structure` + CI lint |
| 上下文慢 | skill 开太多 | `agent-skills off` 非必要项 |
| 跳过 brainstorming | 任务描述过具体 | 显式：「先用 brainstorming 澄清 Q1–Q3」 |

## CI 推荐同步项

与 AI skill **双保险** 的检查（团队应接入流水线）：

```text
openspec validate --strict     # PR 阶段
unit/integration tests         # 合并前
jacoco / coverage-check ≥80%   # 合并前
gitleaks / trufflehog          # push 前
trivy / OWASP dependency-check # 定期 + PR
detekt / eslint max-lines      # 对应 code-structure
```

## 不可交给 skill 的操作

以下必须用 **git hook / 分支保护 / 人工** 锁住：

- 删除生产数据
- 修改 `migrations/` 无 review
- 改 prod 配置
- force push main/master
- 跳过 CI 合并
