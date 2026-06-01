# Skill Eval Plan

## 目标

把三个核心 Skill 升级为可测试、可回归、可发布的工程资产。

## 评估粒度

| 层级 | 内容 | 何时跑 |
|------|------|--------|
| Baseline | 不改 Skill，跑当前版本全部 eval | 第一次落地、每个大版本前 |
| Spot Check | 只跑本轮改动最相关的 2-4 条 | 每次小改后 |
| Targeted Eval | 跑同一风险类别的所有 case | Spot 通过后 |
| Regression Eval | 跑该 Skill 全部旧 case | 发布前 |

## 推荐 baseline 顺序

1. `change-spec-workflow/test-prompts.json` id 1-6
2. `pm-md-to-openspec-pipeline/test-prompts.json` `pipeline-001` 到 `pipeline-010`
3. `openspec-contract-authoring/test-prompts.json` `openspec-001` 到 `openspec-010`
4. `incremental-implementation/test-prompts.json` `incremental-001` 到 `incremental-010`

## 结果记录格式

各 Skill 的 `results.tsv` 使用同一含义：

```tsv
eval_id	pass	date	version	eval_mode	severity	reviewer	notes
```

字段说明：

| 字段 | 说明 |
|------|------|
| `eval_id` | `test-prompts.json` 中的 id |
| `pass` | `1` 通过，`0` 失败 |
| `date` | 评估日期，格式 `YYYY-MM-DD` |
| `version` | Skill 版本或 git 短 SHA；首次可写 `baseline` |
| `eval_mode` | `full_test`、`dry_run`、`human_review` |
| `severity` | `high`、`medium`、`low` |
| `reviewer` | 模型名、人名或 `manual` |
| `notes` | 失败原因、证据、后续处理 |

> `change-spec-workflow/results.tsv` 目前沿用旧表头。若要统一格式，先迁移历史记录或确认无历史数据后再改表头。

## 通过线

- 高风险 regression：发布前必须 100% 通过。
- 中风险 regression：允许有明确 TBD，但不得静默失败。
- Capability eval：不能低于上一版；若下降，必须写明取舍理由。
- 修改触发词时，必须额外做误触发检查。

## 改动假设模板

每轮修改前先写：

```markdown
### Hypothesis

- Skill:
- Target eval:
- Problem:
- Proposed change:
- Expected improvement:
- Rollback condition:
```

## Baseline 执行方式

如果暂时没有自动 runner，可以先用人工 dry run：

1. 新开独立会话或子 Agent。
2. 只提供目标 `SKILL.md` 与单条 `prompt`。
3. 对照 `expected` 判断 `pass` / `fail`。
4. 将结果写入该 Skill 的 `results.tsv`，`eval_mode` 标 `dry_run` 或 `human_review`。

后续可升级为脚本化 runner，但不要因为没有 runner 就跳过 baseline。
