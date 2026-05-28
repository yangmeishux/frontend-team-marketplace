# Skill Release Checklist

每次修改 `SKILL.md`、`reference.md`、测试集或发布给团队使用前，按此清单核对。

## 1. 改动前

- [ ] 已确认本轮只改一个 Skill 或一个明确假设。
- [ ] 已在 `skill-issues.jsonl` 找到对应问题，或新增了一条问题记录。
- [ ] 已确认对应问题有 eval case；没有则先补 `test-prompts.json`。
- [ ] 已跑当前版本 baseline，或明确记录无法运行的原因。

## 2. 改动中

- [ ] 没有把所有失败案例都塞进 `SKILL.md`。
- [ ] 高频硬规则放 `SKILL.md`；长解释、模板、路径变体放 `reference.md`。
- [ ] 新增规则有对应自检项或输出契约。
- [ ] 没有引入与子技能职责冲突的重复流程。

## 3. 改动后

- [ ] 已跑本轮相关 Spot Check。
- [ ] Spot Check 通过后，已跑同类 Targeted Eval。
- [ ] 发布前已跑 Regression Eval。
- [ ] 高风险 regression 没有失败。
- [ ] 若出现失败，已记录到 `results.tsv`，并决定回滚、继续修或不发布。

## 4. 发布记录

每次可发布改动建议写入对应 Skill 的 `CHANGELOG.md`：

```markdown
## v0.x.x

### Changed
- ...

### Fixed
- ...

### Verification
- Baseline:
- Spot:
- Targeted:
- Regression:
- Known risks:
```

## 5. 不允许发布的情况

- 高风险 regression 失败。
- 没有 baseline，却宣称新版更好。
- 只改了措辞，没有任何 eval 改善证据。
- 局部刷新、Reconcile、Open Questions、四文件版本一致性任一场景存在静默失败。
- 修改触发词后未检查误触发。
