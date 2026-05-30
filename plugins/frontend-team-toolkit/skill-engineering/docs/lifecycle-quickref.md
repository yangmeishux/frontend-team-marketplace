# Skill 生命周期速查（8 Phase）

完整质量流程见 [`../skills-quality/`](../skills-quality/)（问题池、评估计划、发布门禁）。

| Phase | 动作 | 产出 |
|-------|------|------|
| 0 创建 | `new-skill.sh` | 标准目录 |
| 1 边界 | 访谈 + output-contract | `references/output-contract.md` |
| 2 写 Eval | ≥3 case，先 eval 后改 skill | `evals/evals.json` |
| 3 Baseline | with skill dry run / benchmark | `results.tsv` 首行 |
| 4 单假设 | 只改触发/步骤/模板之一 | git commit |
| 5 验证 | Spot → Targeted → Regression | `results.tsv` 追加 |
| 6 棘轮 | pass 则 keep，否则 revert | version bump 或 revert |
| 7 发布 | CHANGELOG + meta | `CHANGELOG.md` |
| 8 监控 | 真实任务问题 | `skill-issues.jsonl` |

## 发布门禁（最小）

- [ ] `validate-skill.py` 通过
- [ ] Regression eval 无退步
- [ ] CHANGELOG 已写动机与风险
- [ ] `.skill-meta.json` 的 `baseline` 已更新

## 与现有 Skill 的关系

本仓库中已有 Skill 可能尚未包含 `evals/evals.json` 等工业级文件。升级路径：

1. 用 `validate-skill.py` 检查缺口
2. 补 `test-prompts.json` / `results.tsv`（可参考 `skills-quality/eval-plan.md`）
3. 逐步补齐 `evals/evals.json` 与 `references/output-contract.md`
4. 新 Skill 一律从 `new-skill.sh` 创建，避免结构漂移
