# Changelog — ai-coding-tri-kit

## 0.2.0 — 2026-05-31

**改进方案实施**（基于深度调研分析）

### 新增文件
- `references/environment-check.md` — 环境前置检查清单（P0）
- `references/external-dependency-check.md` — SDK/API 可行性检查（P0）
- `references/fallback-scenarios.md` — 离线/非 git/受限环境降级方案（P2）

### 修订文件
- `references/intensity-tiers.md` — 时间估算分层 + 阻塞风险标注（P1）
- `references/workflow-matrix.md` — 工具能力判断 + 子 Agent 并行降级（P1）
- `SKILL.md` — 引用新增文件 + Prerequisites 环境检查 + Step 2 外部依赖检查
- `.cursor/rules/ai-coding-tri-kit.mdc` — 快速路由更新 + 前置检查 + 时间估算

### 核心改进
1. **环境前置检查**：Node/git/OpenSpec/Superpowers/Agent Skills/网络 6 项检查
2. **外部依赖检查**：SDK AppID/维护状态/法务审批/测试环境 4 问 + BLOCKED 处理
3. **时间估算分层**：AI推理时间 vs 人审时间 vs 外部阻塞时间分离
4. **工具能力判断**：子 Agent 并行依赖工具能力，降级为 executing-plans 单线程
5. **降级方案**：无网络手写、无 git 目录备份、无 skill 模拟、无 CI 人审加强

### 文件新增
- `research-analysis-report.md` — 深度调研分析报告（契合度92%、合理性85%）

## 0.1.1 — 2026-05-31

- Capability eval ×3：004 Step1 真落盘、005 Step2 澄清、006 红线拒 skip-spec
- Fixtures：`fixtures/cap-case-{csv-export,step2-clarify,red-line}/`
- Demo：`feat-dashboard-csv-export` validate PASS（4/4 artifacts）
- Baseline：7/7 evals PASS（4 regression + 3 capability）

## 0.1.0 — 2026-05-31

- 初始版本：基于《AI 编程进阶：三件套》文章 8 步主链路
- 编排 OpenSpec（What）+ Superpowers（How）+ Agent Skills（Quality）
- 附带 intensity-tiers（Full/Standard/Lite）、gates-and-rollback、workflow-matrix
- eval 三件套：全流程触发、缺输入 BLOCKED、Lite 小修复
- 安装：复制至 `~/.cursor/skills/` + `.cursor/rules/ai-coding-tri-kit.mdc`
- 示例：`examples/feat-live-share-third-party-walkthrough.md`
- Darwin baseline：4/4 test-prompts PASS；openspec demo validate OK
