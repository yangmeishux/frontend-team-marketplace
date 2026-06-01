# 模糊需求样例：直播分享保活

| 字段 | 内容 |
|------|------|
| 原文 | 「分享评论的过程保持 app 后台运行，直播状态」 |
| 问题 | 「后台运行」可指进程不被杀，也可指不向直播域发停止指令 |
| 关联 spec | `source/live-app-openspec-demo/.../spec.md` Requirement: 授权与分享期间直播保活 |

**Eval 用途**：capability-005 Step 2 — Agent 应 Socratic 追问 ≤3 轮，并将未决项写入 `design.md` Open Questions，不得直接进入 Step 5 写代码。

## 期望澄清问题（至少命中 2 条）

1. 「后台运行」的可验证定义？
2. 微信 vs 朋友圈是否同一 SDK scene？
3. 微博 SDK vs 系统分享降级？

## Pass 判据

- 输出含 Open Questions 或等价澄清清单
- 澄清轮次 ≤3（req-clarify 约束）
- Gate 1 仍为 PENDING 或 PASS（若 spec 已存在则更新 design）
