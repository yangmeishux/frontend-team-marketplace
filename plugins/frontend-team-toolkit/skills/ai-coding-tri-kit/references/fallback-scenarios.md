# Fallback Scenarios — 降级方案

当环境受限时，三件套仍可执行降级流程。本文件定义各种受限场景的替代方案。

## 受限场景分类

| 场景 | 受限项 | 影响 | 降级档位 |
|------|--------|------|----------|
| **无网络** | npm registry 不可达 | OpenSpec CLI 不可用 | Standard/Lite + 手写 |
| **无 git** | 仓库未初始化 | worktree 不可用 | Standard/Lite + 目录备份 |
| **无 Node.js** | Node < 20.19 | OpenSpec CLI 不可用 | Lite + 手写验收 |
| **无 Superpowers** | skill 未安装 | brainstorming 等缺失 | Standard + 本 skill 模拟 |
| **无 Agent Skills** | skills 未 enable | 约束缺失 | Standard + 本 skill 内嵌 |
| **CI 不可用** | 无 CI 流水线 | 无法强制门槛 | Standard + 人审加强 |
| **SDK 鉴权缺失** | AppID/API Key 未申请 | 渠道 BLOCKED | Full + 分阶段实现 |

## 场景一：无网络 / npm registry 不可达

### 适用情况

- 中国大陆网络限制
- 公司内网无外网访问
- npm registry 服务不可用

### 降级方案

| Step | 正常流程 | 降级方案 |
|------|----------|----------|
| Step 1 | `npx @fission-ai/openspec validate` | 手写四件套结构（见 environment-check.md） |
| Step 2 | brainstorming skill | 本 skill 内置澄清问题（≤3 轮） |
| Step 3 | git worktree | 视 git 状态 |
| Step 8 | `openspec archive` | 手动移动目录到 archive/ |

### 手写验证替代 CLI validate

```text
人审四件套 → 回复"确认可开发" → Gate 1 PASS
替代命令验证：无 CLI 时，人审确认是唯一 Gate。
```

### 输出调整

```markdown
## Gate Status
Gate 0 Environment: PASS_WITH_FALLBACK（离线模式）
Gate 1 需求确认: PASS（人审替代 CLI validate）
```

## 场景二：无 git / 仓库未初始化

### 适用情况

- 新项目未初始化 git
- SVN/其他 VCS 项目
- 用户拒绝 git init

### 降级方案：隔离替代

| 方案 | 操作 | 适用场景 | 优缺点 |
|------|------|----------|--------|
| **目录备份** | `cp -r project project-backup-<date>` | 小项目、快速隔离 | 简单但无版本控制 |
| **子目录隔离** | 在项目内创建 `dev/<change-id>/` | 临时隔离 | 可回滚但占空间 |
| **容器/虚拟环境** | Docker/venv/conda | Python/容器化项目 | 隔离彻底但配置成本高 |
| **Feature flag** | 配置开关 + 条件编译 | 增量发布项目 | 无物理隔离但有回滚能力 |

### 目录备份隔离流程

```text
Step 3 降级：
1. cp -r . ../project-backup-feat-csv-export
2. 在备份目录开发
3. baseline 验证（测试/构建）
4. 完成后复制回原项目，或直接替换

Exit Criteria 调整：
- 隔离方案就绪（备份目录存在）
- baseline 绿
```

### 输出调整

```markdown
## Step 3 Detail
| 隔离方式 | 目录备份 |
| 备份路径 | ../project-backup-feat-csv-export |
| baseline | ✅ 测试全绿 |
```

## 场景三：无 Superpowers / skill 未安装

### 适用情况

- Claude Code 未安装 Superpowers plugin
- Cursor 未添加 Superpowers
- 其他工具不支持

### 降级方案：本 skill 模拟

本 skill 内置了 Superpowers 的核心行为约束，可模拟执行：

| Superpowers skill | 本 skill 替代 |
|-------------------|---------------|
| brainstorming | Step 2 内置澄清问题 + ≤3 轮约束 |
| writing-plans | Step 4 细化任务模板 |
| test-driven-development | Step 5/6 RED-GREEN-REFACTOR 流程 |
| requesting-code-review | Step 6 审查分级模板 |
| verification-before-completion | Step 6 证据粘贴要求 |
| finishing-a-development-branch | Step 8 收尾选项 |

### 模拟 brainstorming 问题模板

```text
Step 2 澄清（本 skill 模拟）：

Q1. [模糊词]的可验证定义？
Q2. 外部依赖/SDK/降级策略？
Q3. 兜底/占位/权限由谁审？
Q4. （涉及外部时）Q-ext-1~Q-ext-6
Q5. 性能/边界/异常处理？

≤3 轮收敛，超时汇总 Open Questions。
```

### 输出调整

```markdown
## Step 2 Detail
| 主导工具 | 本 skill 模拟（Superpowers 未安装） |
| 澄清轮次 | 2 轮 |
| 模式 | 内置问题模板 |
```

## 场景四：无 Agent Skills / skills 未 enable

### 适用情况

- Agent Skills 未 init
- 核心约束未 enable
- 不想消耗上下文 token

### 降级方案：本 skill 内嵌约束

本 skill 内嵌了 Agent Skills 的核心约束：

| Agent Skills | 本 skill 内嵌 |
|--------------|---------------|
| code-structure | 文件 ≤500 行，函数 ≤50 行（提醒） |
| test-coverage | 分支 ≥80%（建议，无 CI 时人审） |
| test-quality | 覆盖 spec 核心 Scenario |
| security-secrets | 无密钥泄漏（意识检查） |
| production-ready | Step 8 checklist |

### 内嵌约束执行方式

```text
Step 5：AI 主动遵守结构约束，产出时自检行数
Step 6：AI 建议覆盖率目标，无 CI 时人审确认
Step 7：AI 执行 secrets 意识检查（手动 grep 或意识审查）
```

### 注意事项

```markdown
⚠️ 本 skill 内嵌约束是 **AI 行为引导**，无 CI 时无法强制。
关键质量门槛建议：
- secrets：手动 grep -r "token\|key\|secret" 后人审
- 覆盖率：本地跑测试报告，人审确认达标
- 结构：lint 工具或人审行数
```

## 场景五：CI 不可用 / 无流水线

### 适用情况

- 个人项目无 CI
- 团队 CI 未配置质量门槛
- CI 暂时不可用

### 降级方案：人审加强

| 本由 CI 强制的 | 人审替代方式 |
|----------------|--------------|
| `openspec validate --strict` | 人逐条审 spec Scenario |
| 测试覆盖率 ≥80% | 本地跑 coverage 报告，人审确认 |
| gitleaks/trivy 扫描 | 手动 grep + 依赖版本人工检查 |
| lint/max-lines | 手动检查或本地 lint 工具 |

### 人审 checklist 替代 CI

```markdown
## Manual Gate Checklist（替代 CI）

- [ ] spec 所有 Scenario 有对应测试
- [ ] 本地测试全绿：`npm test` / `./gradlew test`
- [ ] 覆盖率报告确认 ≥80%：`npm run coverage`
- [ ] secrets 检查：`grep -r "token\|key\|secret" src/` → 无泄漏
- [ ] 依赖漏洞：查看 npm audit / gradle dependencies
- [ ] 结构检查：关键文件行数 ≤500
```

### 输出调整

```markdown
## Gate 3 Security: PASS（人审替代 CI）
- secrets 手动 grep：✅ 无泄漏
- 依赖版本人工检查：✅ 无已知漏洞
- 建议：后续配置 CI 自动扫描
```

## 场景六：SDK 鉴权缺失 / 外部依赖 BLOCKED

### 适用情况

- AppID/API Key 未申请
- 法务审批未完成
- 测试环境未就绪

### 降级方案：分阶段实现

详见 `external-dependency-check.md`。

核心思路：

```text
Step 2 发现 BLOCKED → 用户选择分阶段 →
  Phase 1：实现可执行部分（UI 骨架 + READY 渠道）
  Phase 2：待 BLOCKED 解除后继续
```

### Phase 分割示例

```markdown
## Implementation Phases

### Phase 1（本次会话）
- [ ] 1. UI 骨架 + 面板 + 蒙层
- [ ] 2. 微信渠道（SDK READY）
- [ ] 3. Payload + 保活
- [ ] 4. 测试 + 审查 + verify

### Phase 2（后续会话，待 QQ AppID）
- [ ] 5. QQ 渠道接入
- [ ] 6. 微博降级方案（待法务）

**Phase 1 时间估算**：25–35 min（不含 Phase 2）
```

## 多重受限组合处理

| 组合场景 | 推档位 | 降级方案组合 |
|----------|--------|--------------|
| 无网络 + 无 git | Lite | 手写验收 + 目录备份 + 直接改 |
| 无网络 + 有 git | Standard | 手写四件套 + feature 分支 |
| 无 Superpowers + 无 Agent Skills | Standard | 本 skill 模拟 + 内嵌约束 |
| CI 不可 + SDK BLOCKED | Standard + Phase | 人审加强 + 分阶段实现 |

## 输出契约调整

当执行降级方案时，Output Contract 增加：

```markdown
## Fallback Mode

| 受限项 | 降级方案 |
|--------|----------|
| [具体受限] | [替代方案] |

**Gate 0 Environment**: PASS_WITH_FALLBACK
**实际档位**: [Standard/Lite]（降级自 Full）
```

## 与 Anti-patterns 对齐

| 跑偏 | 纠正 |
|------|------|
| 无网络时仍尝试 npx | 检测网络失败后直接切换手写方案 |
| 无 git 时强行 worktree | 检测 git 状态后切换目录备份 |
| 无 CI 时宣称"强制" | 明确声明是人审替代，建议后续配置 CI |
| SDK BLOCKED 时强行实现 | Step 2 检查后分阶段，不编造 AppID |