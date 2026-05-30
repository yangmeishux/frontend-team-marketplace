---
name: {{SKILL_NAME}}
description: "TODO — 描述 {{SKILL_TITLE}} 的能力边界与典型产出。Use when 用户提到 [触发词1]、[触发词2]、[触发词3]；即使用户未明确说 skill 名称，只要任务匹配也应使用本 skill。"
license: MIT
disable-model-invocation: true
metadata:
  version: "0.1.0"
  maturity: draft
---

# {{SKILL_TITLE}}

> 标准 Skill 模板 — 创建日期 {{DATE_ISO}}  
> 输出契约：见 [`references/output-contract.md`](references/output-contract.md)

## When to Activate

- TODO：列出 3–5 个典型触发场景
- TODO：列出输入前提（需要什么上下文/文件）

## When NOT to Use

- TODO：相近但不应触发本 skill 的任务
- TODO：超出职责范围的情况（转交其他 skill 或通用对话）

## Workflow

1. **确认输入** — 检查用户是否提供 TODO；缺失则追问，不得编造
2. **读取契约** — Read `references/output-contract.md`
3. **执行核心步骤** — TODO：可执行步骤，每步说明输入/输出
4. **自检** — 对照 output-contract 与 evals 中的 must / must_not
5. **交付** — 按契约格式输出；高风险项需用户确认

## Checkpoints

在以下情况 **必须暂停并请求用户确认**，不得自主继续：

- TODO：例如对外发布、删除数据、覆盖已有文件
- TODO：例如 eval 标记为 high risk 的分支

## Output Contract

完整格式见 [`references/output-contract.md`](references/output-contract.md)。

## Anti-patterns

| 跑偏 | 纠正 |
|------|------|
| TODO | TODO |
| 跳过输入检查直接执行 | 先补全输入契约 |
| 一次改动多个假设 | 单轮只改触发/步骤/模板之一 |

## Eval & Upgrade

- 结构化 eval：`evals/evals.json`
- 快速实测：`test-prompts.json`
- 结果记录：`results.tsv`
- 问题池：复制 `skill-issues.jsonl.example` → `skill-issues.jsonl`
- 团队升级流程：见 [`../skills-quality/`](../skills-quality/) 与 [`../skill-engineering/docs/lifecycle-quickref.md`](../skill-engineering/docs/lifecycle-quickref.md)

## Bundled Resources

| 路径 | 何时读取 |
|------|----------|
| `references/output-contract.md` | 每次执行前 |
| `scripts/validate-output.sh` | 输出完成后（可选） |
