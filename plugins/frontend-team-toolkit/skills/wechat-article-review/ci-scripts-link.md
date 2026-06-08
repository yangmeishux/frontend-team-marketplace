# CI Scripts Reference

本 Skill 使用仓库级别的 CI 门禁脚本，位于 `skill-engineering/scripts/`。

## 脚本位置

| 脚本 | 路径 | 用途 |
|------|------|------|
| **run_evals.py** | `plugins/frontend-team-toolkit/skill-engineering/scripts/run_evals.py` | Eval runner（PR/Release/Scheduled 分层） |
| **check_regression.py** | `plugins/frontend-team-toolkit/skill-engineering/scripts/check_regression.py` | Regression 门禁检查 |
| **check_new_evals.py** | `plugins/frontend-team-toolkit/skill-engineering/scripts/check_new_evals.py` | 新 Eval baseline 检查 |
| **graders/** | `plugins/frontend-team-toolkit/skill-engineering/scripts/graders/` | Grader 自动化判定脚本 |

## Workflow 配置

| 文件 | 路径 |
|------|------|
| **eval-ci.yml** | `.github/workflows/eval-ci.yml` |
| **risk-layer-config.json** | `plugins/frontend-team-toolkit/skill-engineering/config/risk-layer-config.json` |

## 如何运行

### 本地跑 Eval

```bash
# 从仓库根目录执行
python3 plugins/frontend-team-toolkit/skill-engineering/scripts/run_evals.py \
  --mode pr \
  --skill wechat-article-review \
  --output results.tsv
```

### 检查 Regression

```bash
python3 plugins/frontend-team-toolkit/skill-engineering/scripts/check_regression.py \
  --results results.tsv \
  --risk high \
  --block true
```

### 检查新 Eval Baseline

```bash
python3 plugins/frontend-team-toolkit/skill-engineering/scripts/check_new_evals.py \
  --skill wechat-article-review \
  --results results.tsv \
  --block true
```

## CI 自动触发

当 PR 修改 `skills/wechat-article-review/` 目录时：

1. GitHub Actions 自动运行 `eval-ci.yml`
2. 执行 `run_evals.py --mode pr`
3. 执行 `check_regression.py --risk high`
4. Regression 挂 → PR Comment 报警 → BLOCK 合并

## 相关文章

- [[AI Agent Skill 工程化 06：CI 里的 Skill——Eval 门禁与自动化回归]]
- [[AI Agent Skill 工程化 06（实战篇）：Eval 门禁从 0 到 1——以 wechat-article-review 为例]]