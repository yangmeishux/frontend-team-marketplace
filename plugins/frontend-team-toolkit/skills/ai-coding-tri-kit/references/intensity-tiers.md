# Intensity Tiers — 三件套强度分级

会话开始时必须先判定变更强度，再决定跑 Full / Standard / Lite。

**前置**：先 Read `environment-check.md`，确认环境可用后再判档位。

## 判定决策树

```text
变更涉及多少文件 / 风险？
│
├─ 大型功能（多模块、多文件、外部 SDK、安全敏感）
│   └─ Full — 8 步完整流程 + worktree + 子 Agent 并行
│
├─ 中等功能（1–3 文件、单一模块、有明确验收）
│   └─ Standard — OpenSpec 简化 + 单线程实现 + 核心测试
│
└─ 小修复（<20 行、单点 bug、文案/配置微调）
    └─ Lite — 保留 TDD + secrets 底线，跳过 propose/worktree
```

## 时间估算分层（修订）

**口径说明**：以下"AI 推理"指模型在会话内生成 + 调用 CLI 的累计耗时。**不含**外部阻塞时间。

| 时间类型 | Full | Standard | Lite |
|----------|------|----------|------|
| **AI 推理 + 命令** | 30–40 min | 15–25 min | 5–10 min |
| **人审阅决策** | 10–15 min | 5–8 min | 1–2 min |
| **测试执行（本地）** | 5–10 min | 3–5 min | 1–2 min |
| **不含项** | SDK 联调、真机回归、CI 排队、跨团队审批 | 同上 | 无 |

### 阻塞风险标注

| 档位 | 典型阻塞风险 | 阻塞时处理 |
|------|--------------|------------|
| **Full** | SDK 鉴权申请、ROM 兼容回归、法务审批 | Step 2 外部依赖检查，分阶段实现 |
| **Standard** | 编码/Worker 技术难点、第三方 API 限制 | Step 2 澄清，design.md 记录 |
| **Lite** | 无显著阻塞 | 直接执行 |

### 外部阻塞时间（不计入估算）

| 阻塞类型 | 典型耗时 | 责任方 |
|----------|----------|--------|
| SDK AppID 申请 | 3–5 工作日 | 产品运营 |
| 法务/隐私审批 | 1–3 工作日 | 法务团队 |
| 真机回归（多 ROM） | 1–2 天 | QA 团队 |
| CI 排队/失败排查 | 0.5–2 小时 | DevOps |

**技能声明**：时间估算仅覆盖会话内可控部分。外部阻塞需单独评估。

## 三档对照表

| 维度 | Full | Standard | Lite |
|------|------|----------|------|
| **典型场景** | 新功能多文件、SDK 接入、重构 | CSV 导出、单页组件 | typo、一行 null check |
| **OpenSpec** | 完整 4 件套 + validate | propose + spec（可合并 design） | Issue/口头描述即可 |
| **澄清轮次** | brainstorming ≤3 轮 | 1–2 个关键问题 | 跳过 |
| **Worktree** | 必须 | 可选 | 跳过 |
| **实现方式** | subagent 并行 | executing-plans 单线程 | 直接改 |
| **测试** | 全 Scenario + ≥80% 分支 | 核心路径 + 关键边界 | 至少 1 个回归测试 |
| **安全** | security-* 三项 | security-secrets | security-secrets |
| **Archive** | 必须 | verify 后建议 archive | 可选 |
| **预估人时** | 10–15 min 审阅 | 5–8 min | 1–2 min |

## 各档必保底线（不可跳过）

无论哪一档，以下 **至少保留一层程序性强制 + 一层 AI 约束**：

1. **有书面验收口径** — 哪怕 Lite 也写清「改什么、怎样算对」
2. **测试证据** — Lite 至少 1 条；Standard/Full 按 spec Scenario
3. **secrets** — 不得提交密钥；Lite 也跑 secrets 意识检查
4. **人审合并** — 不得自动 push/merge 除非用户明确要求

## 用户说「快点」时的处理

1. 说明 Lite 与 Full 的质量差异（可追溯性、回归风险）
2. 若用户坚持 Lite → 记录 **Assumptions** 中「用户选择 Lite，跳过 OpenSpec 归档」
3. 若变更规模实际超过 Lite 阈值 → **建议升级 Standard**，给出 1 句理由

## 示例

| 用户原话 | 建议档位 |
|----------|----------|
| 「直播间分享到微信/QQ/微博，含保活」 | Full |
| 「Dashboard 加 CSV 导出」 | Standard → 可升 Full |
| 「fix: escapeCSV 处理 null」 | Lite |
| 「重构整个 auth 模块」 | Full + 强调 TDD |
