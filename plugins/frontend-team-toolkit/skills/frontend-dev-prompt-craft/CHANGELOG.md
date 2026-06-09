# Changelog — frontend-dev-prompt-craft

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [Unreleased]

### Baseline
- 2026-06-09 跑 baseline，14/14 PASS（8 test-prompts + 6 evals）
- regression: 3/3 (100%), capability: 3/3 (100%)
- 详见 results.tsv

## [0.1.0] - 2026-06-09

### Added
- SKILL.md：8 类前端任务类型识别 + Workflow + Input Contract
- references/prompt-templates.md：17 条结构化提示词模板（PAGE/UI/API/ARCH/REFACTOR/DEBUG/PRD/MIGRATE）
- references/output-contract.md：输出格式契约 + 质量红线
- evals/evals.json：6 条结构化 Eval（4 regression + 2 capability）
- test-prompts.json：8 条快速实测用例
- 所有提示词模板均来自真实工作场景提炼

### Notes
- maturity: draft — 尚未跑 baseline eval
- validate-skill.py 校验通过，0 warnings
