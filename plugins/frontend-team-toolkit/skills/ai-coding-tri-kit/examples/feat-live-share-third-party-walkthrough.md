# Walkthrough：feat-live-share-third-party

> 本示例演示 **Full 档位** 下，三件套 8 步如何串联处理「直播间分享到第三方」需求。  
> 制品路径：`source/live-app-openspec-demo/openspec/changes/feat-live-share-third-party/`  
> 编排 Skill：`ai-coding-tri-kit`

---

## 输入：产品需求表（节选）

| 字段 | 内容 |
|------|------|
| 功能 | 分享直播地址到微信、朋友圈、QQ、QQ 空间、微博 |
| 交互 | 底部纵向面板 + 透明蒙层，点空白关闭 |
| 保活 | 第三方授权期间 app 后台运行，直播不中断 |
| 素材 | 主播头像缩略图 + 直播标题（或固定模板） |

需求表典型问题：**口径模糊**（「后台运行」）、**隐含前提多**（SDK、降级、法务）。

---

## Step 1：需求对齐 — OpenSpec

**命令**：

```bash
/opsx:propose "新增直播间分享到第三方渠道：微信/朋友圈/QQ/QQ 空间/微博，含底部面板、第三方授权期间直播保活、主播头像 + 标题/兜底模板"
```

**产出**（本仓库已有）：

```text
openspec/changes/feat-live-share-third-party/
├── proposal.md
├── design.md
├── tasks.md
└── specs/third-party-live-share/spec.md
```

**proposal.md 关键句**：

- Why：解决渠道未安装、授权后直播误停、素材不一致
- What：五渠道面板、环境检测、保活、头像+标题兜底

**spec.md 关键转化**（模糊 → 可验证）：

```markdown
### Requirement: 授权与分享期间直播保活
宿主 App MUST NOT 主动向音视频模块发送「停止直播/停止推流」指令
```

**验证**：

```bash
npx @fission-ai/openspec validate feat-live-share-third-party
# → Change 'feat-live-share-third-party' is valid
```

**Exit**：人审 spec 后回复「确认可开发」  
**Gate 1**：PENDING → PASS

---

## Step 2：需求澄清 — Superpowers + req-clarify

**brainstorming 典型追问**（≤3 轮）：

| # | 问题 | 影响 |
|---|------|------|
| Q1 | 「后台运行」= 进程不被杀，还是禁止向直播域发停止指令？ | 保活策略 |
| Q2 | 微信与朋友圈是否同一 SDK scene？ | tasks 2.2/2.3 |
| Q3 | 微博走官方 SDK 还是 ACTION_SEND 降级？ | design Open Questions |
| Q4 | 标题为空时固定模板文案谁审？ | SharePayloadFactory |
| Q5 | 头像失败占位图规格？ | UI 规范 |

**沉淀到 design.md**：

```markdown
## Open Questions
- 微博最终走「官方 SDK」还是「系统分享面板降级」——需产品 + 法务确认
```

**Exit**：Decisions + Open Questions 齐全，用户确认

---

## Step 3：分支隔离 — using-git-worktrees

```bash
git worktree add -b feat/live-share-third-party ../app-live-share
cd ../app-live-share
./gradlew :app:assembleDebug && ./gradlew test   # baseline 必须绿
```

**价值**：微信/QQ/微博 SDK 并行接入；ROM 回归失败可删 worktree，主分支零污染。

---

## Step 4：计划制定 — writing-plans + req-breakdown

**输入**：OpenSpec `tasks.md`（5 大块）

**细化示例**（1.2 任务）：

```markdown
Task 1.2: 底部渠道面板 + 蒙层 dismiss
  文件: ui/share/ShareBottomSheet.kt
  验收: spec Scenario「打开与关闭面板」
  预估: 4 min
  可独立回滚: 是（feature flag share_panel.enabled）
```

**Exit**：tasks.md 每条任务均有文件路径 + 验收口径

---

## Step 5：子 Agent 并行 — subagent-driven-dev

**design.md Decisions 约束**：

- `ShareCoordinator` + `RoomContext`
- `ShareChannel` 接口 + `ShareChannelRegistry`
- 直播启停 ONLY 由直播域 API 控制

**子 Agent 切分**：

| Agent | 任务 | 并行 |
|-------|------|:----:|
| Agent-UI | 1.2, 1.3 面板+入口 | ✅ |
| Agent-WeChat | 2.2, 2.3 | ✅ |
| Agent-QQ | 2.4 | ✅ |
| Agent-Weibo | 2.5（待 Open Q 结论） | 视情况 |
| Agent-Payload | 3.1, 3.2 | ✅ |
| Agent-Lifecycle | 4.1, 4.2 | ❌ 依赖 1.x |

**纪律约束**（Agent Skills）：

- code-structure：ShareCoordinator 不得单文件 >500 行
- TDD：每个 `canShare()` 先 RED
- code-documentation：`ShareChannel` 公开 API 有文档

**两阶段审查**：规格一致性（对照 MUST）+ 代码质量

---

## Step 6：测试 + 审查

**关键 RED 测试**（保活 spec）：

```kotlin
@Test
fun `分享流程期间不得向直播域发送停止指令`() {
    val streamSpy = StreamControlSpy()
    val coordinator = ShareCoordinator(streamControl = streamSpy)
    coordinator.present(roomContext)
    coordinator.onChannelSelected(ChannelId.WECHAT)
    coordinator.onReturnFromThirdParty()
    assertThat(streamSpy.stopInvocations).isEqualTo(0)  // RED → GREEN
}
```

**审查分级示例**：

```text
🔴 CRITICAL：无
🟡 WARNING：onChannelSelected 未对 RoomContext 做空检查
🟢 INFO：微博 SDK/降级抽 BuildConfig
📊 分支覆盖 86%（≥80% ✅）
```

**Exit**：测试全绿 + 无 CRITICAL + 覆盖 spec 核心 Scenario

---

## Step 7：安全检查 — security-*

对照 spec「隐私与日志」：

```bash
security-secrets       → 0 token 泄漏 ✅
security-dependencies  → SDK 0 high/critical ✅
security-api           → 分享 URL 无敏感参数 ✅
```

**失败 → STOP**，修复后重跑；CI 同步 gitleaks/trivy 才算不可绕过。

---

## Step 8：验证 + 收尾

**8a OpenSpec**：

```bash
openspec validate feat-live-share-third-party --strict
/opsx:verify   # 逐条对照 6 个 Scenario
```

**8b production-ready**：单测绿、覆盖≥80%、ROM 矩阵记录、feature flag 回滚

**8c finishing-a-development-branch**：用户选 Create PR

**8d 归档**：

```bash
/opsx:archive
# → openspec/changes/archive/2026-04-27-feat-live-share-third-party/
```

---

## 8 步耗时参考（Full）

| Step | 人 | AI+命令 |
|:----:|:--:|:-------:|
| 1 | 5 min 审 spec | 30 s |
| 2 | 5–10 min 答题 | 1–2 min |
| 3 | — | 30 s + baseline 构建 |
| 4 | — | 1–2 min |
| 5 | 卡点介入 | 15–30 min |
| 6 | 3 min 审关键点 | 5–10 min |
| 7 | — | 1–2 min |
| 8 | 1 min 决策 | 2 min |
| **人合计** | **~10–15 min** | |

---

## 与本 Skill 的交叉引用

| 需要 | 读 |
|------|-----|
| 步骤 → 工具映射 | `references/workflow-matrix.md` |
| 为何用 Full 档 | `references/intensity-tiers.md` |
| 闸门失败怎么办 | `references/gates-and-rollback.md` |
| 会话输出格式 | `references/output-contract.md` |

---

## 本地复刻

```bash
cd source/live-app-openspec-demo
npx @fission-ai/openspec validate feat-live-share-third-party
cat openspec/changes/feat-live-share-third-party/specs/third-party-live-share/spec.md
```

对话触发：

```text
按三件套 Full 流程，参照 examples/feat-live-share-third-party-walkthrough.md，
对 feat-live-share-third-party 从 Step 1 走到 Step 8。
```
