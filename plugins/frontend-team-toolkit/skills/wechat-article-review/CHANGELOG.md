# Changelog — wechat-article-review

## [Unreleased]

## [0.1.3] - 2026-05-30

### Changed

- Workflow：稿件类型分流（Blueprint / 领域示例 / 通用干货）
- Workflow：用户要求时持久化 reviews / skill-issues / results.tsv
- Rubric：领域专有示例（OpenSpec 等）仅 P2 建议泛化，不作 P0 否决
- Anti-patterns：补「评审后不写 issues」「误判领域示例为硬伤」

### Notes

- 2 篇 real_usage 后 skill-issues 全部 closed；**小步单假设** 迭代

## [0.1.2] - 2026-05-30

### Added

- 评审 `skill-upgrade-sop-wechat.md` → 9.3 通过
- eval `wechat-article-review-006`

## [0.1.1] - 2026-05-30

### Changed

- 驱动 `skill-engineering-blueprint.md` v2：8.4 → 9.2
- eval `wechat-article-review-005`；skill-issues 首批评审闭环

## [0.1.0] - 2026-05-30

### Added

- 从 `source/agents/article-reviewer.md` 迁移
- 五维评分、evals、output-contract、validate-output.sh
