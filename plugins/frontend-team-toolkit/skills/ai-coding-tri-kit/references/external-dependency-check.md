# External Dependency Check — 外部依赖可行性检查

涉及第三方 SDK/API/外部服务时，必须在 Step 2 澄清阶段增加可行性检查，提前发现非技术阻塞。

## 适用场景

当变更涉及以下内容时，**必须执行外部依赖检查**：

- 第三方 SDK（微信、QQ、微博、支付、地图等）
- 外部 API（云服务、OAuth、推送服务等）
- 需审批的合规项（法务、隐私、安全审核）
- 需申请的凭证（AppID、API Key、证书）
- 特殊环境（沙箱、测试账号、VPN）

## Step 2 增加问题清单

| # | 问题 | 阻塞级别 | 缺失时的处理 |
|---|------|----------|--------------|
| Q-ext-1 | SDK/AppID/API Key 是否已申请且可用？ | **BLOCKED** | 分阶段实现或等待申请完成 |
| Q-ext-2 | SDK 官方维护状态（活跃/停更/弃用）？ | WARN | 记录，准备降级方案 |
| Q-ext-3 | 法务/隐私/安全合规是否需审批？ | **BLOCKED** | Open Questions，等审批 |
| Q-ext-4 | 测试账号/沙箱环境是否就绪？ | WARN | 影响时间估算，记录 |
| Q-ext-5 | SDK 版本兼容性（最低版本、依赖冲突）？ | WARN | design.md Decisions |
| Q-ext-6 | 降级/备用方案是否可行？ | INFO | 记录备选方案 |

## 阻塞级别定义

| 级别 | 含义 | 处理方式 |
|------|------|----------|
| **BLOCKED** | 无法继续实现该渠道/功能 | 分阶段实现、标记 Open Questions、等待 |
| **WARN** | 可实现但有风险/延迟 | 记录 design.md，时间估算 +buffer |
| **INFO** | 信息收集，不影响主流程 | 记录备选方案 |

## BLOCKED 渠道处理流程

### 判断逻辑

```text
Step 2 澄清 → 发现有 BLOCKED 项 → 
  ├─ 用户选择「分阶段实现」→ 继续，仅实现可执行部分
  ├─ 用户选择「等待」→ STOP，记录待办，会话暂停
  └─ BLOCKED 影响核心 Scenario → STOP，需求阶段无法推进
```

### 分阶段实现示例

```markdown
## design.md 更新

### BLOCKED Channels
| 渠道 | 阻塞原因 | 状态 |
|------|----------|------|
| QQ 分享 | AppID 未申请 | BLOCKED — Phase 2 |
| 微博分享 | SDK 已停更 | WARN — 降级 ACTION_SEND |

### Implementation Phases
- **Phase 1（本次）**：UI 骨架 + 微信渠道 + Payload + 保活
- **Phase 2（后续）**：QQ 渠道（待 AppID）
- **Phase 3（后续）**：微博降级方案（待法务确认）
```

### 时间估算调整

当存在 BLOCKED 项时：

```text
原估算：40-65 min（Full）
调整后：25-40 min（不含 BLOCKED 渠道）
备注：Phase 2/3 需额外等待申请/审批时间（不计入本次）
```

## 输出到 design.md 的格式

```markdown
## External Dependencies

### Ready
| 依赖 | 状态 | 凭证/环境 |
|------|------|-----------|
| 微信 SDK | ✅ READY | AppID: wx123xxx，沙箱已配置 |

### BLOCKED
| 依赖 | 阻塞原因 | 需谁处理 | 预计时间 |
|------|----------|----------|----------|
| QQ SDK | AppID 未申请 | 产品运营 | 3-5 工作日 |

### WARN
| 依赖 | 风险 | 降级方案 |
|------|------|----------|
| 微博 SDK | 官方停更 | ACTION_SEND |

## Open Questions（外部依赖相关）
- QQ AppID 申请进度？—— 需产品运营跟进
- 微博 ACTION_SEND 降级是否需法务确认？—— 需法务审批
```

## 输出到 Output Contract 的格式

在 **Assumptions & Open Questions** 节增加：

```markdown
## External Dependency Status

| 类型 | 数量 | 影响 |
|------|------|------|
| READY | 1（微信） | 可实现 |
| BLOCKED | 1（QQ） | Phase 2 |
| WARN | 1（微博） | 降级方案 |

**Phase 1 Scope**：微信 + UI + Payload + 保活
**Phase 2 Scope**：QQ（待 AppID）
```

## 实际案例：直播间分享第三方

### 原需求

"分享到微信/朋友圈/QQ/QQ空间/微博"

### 外部依赖检查结果

| 渠道 | SDK 状态 | AppID/凭证 | 阻塞级别 |
|------|----------|------------|----------|
| 微信/朋友圈 | 官方维护活跃 | 已申请 | ✅ READY |
| QQ/QQ空间 | 官方维护 | **未申请** | **BLOCKED** |
| 微博 | 官方 SDK 停更 | N/A | WARN（降级） |

### 分阶段实现决策

```text
用户选择：Phase 1 先实现微信 + UI + 保活
Phase 2 待 QQ AppID 申请完成
微博降级方案待 Step 4 design 确认

Gate 1：PASS（Phase 1 scope 确认）
```

## 与 gates-and-rollback.md 对齐

外部依赖 BLOCKED 应触发 **Gate 0 External** 检查：

```text
Gate 0 External Dependencies:
  ├─ 无 BLOCKED → PASS → 继续 Step 3
  ├─ 有 BLOCKED 但用户选分阶段 → PASS_WITH_PHASE_SPLIT → 调整 scope
  └─ 有 BLOCKED 影响核心 → BLOCKED → STOP，等待或取消
```

## Anti-patterns

| 跑偏 | 纠正 |
|------|------|
| 未检查 SDK 状态直接实现 | Step 2 必问 Q-ext-1~Q-ext-6 |
| 发现 BLOCKED 后仍宣称"全渠道完成" | design.md 明确 Phase 分割 |
| 时间估算未扣除 BLOCKED 渠道 | 调整估算，标注"不含 Phase 2" |
| 降级方案未记录 | design.md WARN 节记录备选方案 |