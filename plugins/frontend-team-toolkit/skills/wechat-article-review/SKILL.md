---
name: wechat-article-review
description: "微信公众号文章 0–10 分结构化评分与改稿审稿。Use when 用户要求打分、评分、评审、审稿、改稿反馈、是否通过、重写、复评、文章质量把关；即使用户只说「看看这篇能不能发」或「帮我审一下稿子」也应使用本 skill。9 分及以上通过，低于 9 分必须输出按 P0/P1/P2 排序的可执行修改清单与复评目标。"
license: MIT
metadata:
  version: "0.1.4"
  author: wechat-agents
  maturity: beta
  source_agent: article-reviewer
---

# 微信公众号文章评分（Wechat Article Review）

> 对齐 `source/agents/article-reviewer.md`  
> 输出契约：[`references/output-contract.md`](references/output-contract.md)  
> 评分细则：[`references/scoring-rubric.md`](references/scoring-rubric.md)

## When to Activate

- 用户提交公众号文章初稿，需要 **0–10 分评分** 与通过/不通过结论
- 用户要求 **修改清单、复评目标、提分路径**
- 多 Agent 流水线中：文案产出 → **本 skill 把关** → 设计/主编

## When NOT to Use

- 仅要 **选题策划、大纲、素材收集** → 用 content-planner，不要评分
- 仅要 **从零写文/扩写** → 用 content-writer
- 仅要 **封面/配图/排版** → 用 visual-designer
- 用户未提供 **正文或可读路径** 且拒绝补充 → 输出 BLOCKED，不要编造文章打分

## Input Contract

| 字段 | 必填 | 默认 |
|------|:----:|------|
| 文章内容或 `articles/` 路径 | 是 | — |
| 文章类型（干货/故事/观点） | 否 | 干货 |
| 目标受众 | 否 | 技术从业者/内容创作者 |
| 发布渠道 | 否 | 微信公众号 |
| 约束（字数/口吻/合规） | 否 | — |

缺正文时：**列出最少必填项并 STOP**（状态 `BLOCKED`）。

## Workflow

1. **确认输入** — 有正文或路径；缺则 BLOCKED
2. **Read 细则** — Read `references/scoring-rubric.md` 与 `references/output-contract.md`
3. **通读全文** — 把握主题、结构、承诺句（「下文将…」「本文提供…」）
4. **开头 3 秒检查** — 若第 1 段无痛点/数据/故事/问题，写入主要问题（见 rubric「空洞开头识别」）
5. **逐维打分** — 五维加权（见 rubric）；每分附依据，禁止印象分
6. **承诺一致性检查** — 未兑现承诺必须进「主要问题」并给最小修复动作
7. **汇总结论** — ≥9.0 通过；<9.0 不通过
8. **按契约输出** — 完整评分报告；不通过必含 P0/P1/P2 修改清单与复评目标
9. **（条件）30 分钟提分** — 若用户限时可改，附 30 分钟执行脚本（见 rubric）
10. **（条件）持久化** — 用户要求「记录到 skill」时：报告 → `reviews/YYYY-MM-DD-<slug>.md`；问题 → `skill-issues.jsonl`；本次结果 → `results.tsv`；可转化问题 → 提议新增 `evals.json` case

### 稿件类型分流（Read rubric 对应节）

| 特征 | 适用 rubric |
|------|-------------|
| 含大量仓库路径、命令块、架构图 | `scoring-rubric.md` → **技术 Blueprint 公众号改编** |
| 含 OpenSpec / 流水线专有示例 | 同上 + **领域示例**（见 rubric，不作为 P0 否决） |
| 普通公众号干货 | 通用五维表 |

## Checkpoints

- **合规/敏感风险**：疑似违规 → 直接不通过，不给出「擦边通过」
- **总分 8.5–8.9**：可标注「接近达标」，但仍为 ❌ 不通过，直到 ≥9.0
- **用户要求「只给总分」**：仍须输出维度表；可压缩问题描述但不可省略结论格式

## Scoring Threshold

```text
≥ 9.0  →  ✅ 通过 → 设计 / 主编终审
< 9.0  →  ❌ 不通过 → 修改清单 → 文案改稿 → 复评
```

## Output Contract

必须遵循 [`references/output-contract.md`](references/output-contract.md)。  
校验（可选）：`scripts/validate-output.sh` 对报告 Markdown 做结构检查。

## Anti-patterns

| 跑偏 | 纠正 |
|------|------|
| 只给总分无维度 | 必须五维得分表 + 加权说明 |
| 「整体不错但…」无位置 | 问题须「第 N 段 / 小标题「XXX」」 |
| <9 分无修改清单 | 必须 P0/P1/P2 TODO |
| 放松 9 分线（8.7 也通过） | 严格执行 ≥9.0 |
| 未读正文就评 | BLOCKED |
| 评审后不写 issues（用户已要求记录） | 必须更新 skill-issues.jsonl + results.tsv |
| 把领域示例当 P0 否决 | 仅 P2 建议泛化，见 rubric「领域专有示例」 |
| 未识别空洞开头 | 必须检查第 1 段，见 rubric「空洞开头识别」 |

## Downstream

- **通过** → visual-designer（封面）→ chief-editor（终审）
- **不通过** → content-writer（按修改清单改稿）→ 再次调用本 skill 复评

## Eval & Upgrade

- `evals/evals.json` — 回归与能力用例
- `test-prompts.json` — Darwin / 人工 spot check
- 问题池：`skill-issues.jsonl`（从 `.example` 复制）
