# Skill Quality Hub

本目录用于把 `frontend-team-toolkit` 的 Skill 升级从「使用中体感改写」升级为 **Eval 驱动的 SkillOps 流程**。

新建 Skill 请使用 [`../skill-engineering/`](../skill-engineering/) 脚手架（`new-skill.sh` + `validate-skill.py`）；本目录负责 **已有 Skill 的质量运营**。

## 当前采用的方案

```text
真实使用问题
  -> 记录到 skill-issues.jsonl
  -> 转成各 skill 的 test-prompts.json
  -> 先跑当前版本 baseline
  -> 一轮只改一个 skill / 一个假设
  -> 重跑 spot / targeted / regression eval
  -> 通过则保留，不通过则回滚或继续修
  -> 记录 results.tsv 与 CHANGELOG
```

## 文件分工

| 文件 | 用途 |
|------|------|
| `skill-inventory.md` | 三个核心 Skill 的定位、上下游、当前质量状态 |
| `skill-issues.jsonl` | 真实使用中发现的问题池，后续转为 regression case |
| `eval-plan.md` | 如何跑 baseline、spot、targeted、regression eval |
| `release-checklist.md` | 每次修改 Skill 前后的发布门禁 |

## 结果记录位置

每个重点 Skill 独立维护自己的测试集和结果：

```text
pm-md-to-openspec-pipeline/
  test-prompts.json
  results.tsv

change-spec-workflow/
  test-prompts.json
  results.tsv

openspec-contract-authoring/
  test-prompts.json
  results.tsv

incremental-implementation/
  test-prompts.json
  results.tsv
```

## 升级原则

- 先新增或确认 eval，再改 `SKILL.md`。
- 一轮只改一个最高风险问题。
- 高风险 regression 失败时，不发布。
- 只要修复来自真实使用的问题，就必须把它沉淀为 regression case。
- `SKILL.md` 不应无限膨胀；长模板、示例和路径变体放进 `reference.md` 或 `examples.md`。
