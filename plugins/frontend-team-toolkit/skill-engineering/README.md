# Skill Engineering 脚手架

本目录提供 **Frontend Team Toolkit** 内 Agent Skill 的标准化工程能力：创建模板、JSON Schema、结构校验脚本，以及与 Eval 驱动升级流程的衔接。

适用于：在本 Marketplace 插件中 **新建 Skill**、**校验 Skill 目录结构**、**对齐团队 Eval 规范**。

---

## 快速开始

在仓库根目录执行：

```bash
# 创建新 Skill（默认输出到 plugins/frontend-team-toolkit/skills/<name>/）
./plugins/frontend-team-toolkit/skill-engineering/bin/new-skill.sh my-skill-name

# 指定输出目录（例如个人 Cursor skills）
./plugins/frontend-team-toolkit/skill-engineering/bin/new-skill.sh my-skill-name --path ~/.cursor/skills

# 结构校验
python3 plugins/frontend-team-toolkit/skill-engineering/bin/validate-skill.py \
  plugins/frontend-team-toolkit/skills/my-skill-name
```

创建完成后：

1. 编辑 `SKILL.md` 的 `description` 与工作流
2. 填写 `evals/evals.json` 与 `test-prompts.json`
3. 跑 baseline 并写入 `results.tsv`
4. 在 `plugins/frontend-team-toolkit/README.md` 中登记新 Skill（若随插件发布）

---

## 目录说明

```text
skill-engineering/
├── README.md                 # 本文件
├── requirements.txt          # Python 依赖（可选 LLM Judge）
├── bin/
│   ├── new-skill.sh          # 从模板生成 Skill 目录
│   └── validate-skill.py     # frontmatter + 工业级必备文件校验
├── scripts/                  # CI 门禁自动化脚本（新增）
│   ├── run_evals.py          # Eval runner（PR/Release/Scheduled 分层）
│   ├── check_regression.py   # Regression 门禁检查
│   ├── check_new_evals.py    # 新 Eval baseline 检查
│   └── graders/              # Grader 自动化判定脚本
│       ├── rule_grader.py    # 关键词/路径/禁用词检查
│       ├── structure_grader.py # 章节/步骤/frontmatter 检查
│       ├── trajectory_grader.py # Agent 调用顺序检查
│       └── model_grader.py   # LLM Judge 语义判定
├── config/                   # CI 配置（新增）
│   └── risk-layer-config.json # risk 分层 + 门禁红线配置
├── schemas/                  # JSON Schema（evals、test-prompts、meta、issues、workflows）
├── templates/new-skill/      # 新 Skill 模板包（勿直接使用，请用脚本复制）
│   ├── workflows/            # 动态编排脚本模板（新增）
│   │   ├── README.md
│   │   ├── serial-workflow.js
│   │   ├── parallel-workflow.js
│   │   ├── conditional-workflow.js
│   │   ├── loop-workflow.js
│   │   ├── adversarial-workflow.js
│   │   └── weekly-regression.js  # `/loop` 自动化回归（新增）
│   └── evals/
│       ├── evals.json        # 输出Eval模板
│       └── trajectory-evals.json  # 过程Eval模板（新增）
└── docs/
    └── lifecycle-quickref.md # 8 Phase 生命周期速查
```

---

## 生成的 Skill 标准结构

```text
<skill-name>/
├── SKILL.md                    # 静态知识：触发条件、契约、Workflow描述
├── CHANGELOG.md
├── .skill-meta.json
├── evals/
│   ├── evals.json              # 输出 Eval（验证输出内容）
│   └── trajectory-evals.json   # 过程 Eval（验证Workflows执行）
├── test-prompts.json
├── results.tsv
├── skill-issues.jsonl.example
├── references/
│   └── output-contract.md
├── workflows/                  # ← 动态编排脚本（新增）
│   ├── README.md               # Workflows使用说明
│   ├── serial-workflow.js      # 串行编排模板
│   ├── parallel-workflow.js    # 并行编排模板
│   ├── conditional-workflow.js # 条件路由模板
│   ├── loop-workflow.js        # 循环直到完成模板
│   └── adversarial-workflow.js # 对抗验证模板
└── scripts/validate-output.sh
```

与 [agentskills.io 规范](https://agentskills.io/specification) 对齐：`name` / `description` 必填；团队 Skill 默认设置 `disable-model-invocation: true`，需显式 `@` 触发。

---

## 动态编排组件（新增）

Skill 现在支持 **Dynamic Workflows**，提供确定性执行能力：

| Workflow类型 | 适用场景 | 模板文件 |
|-------------|----------|----------|
| **串行编排** | 子Skill有依赖顺序 | `workflows/serial-workflow.js` |
| **并行编排** | 子Skill可独立执行 | `workflows/parallel-workflow.js` |
| **条件路由** | 依输入选择不同子Skill | `workflows/conditional-workflow.js` |
| **循环直到完成** | 不确定工作量的任务 | `workflows/loop-workflow.js` |
| **对抗验证** | 独立agent验证输出 | `workflows/adversarial-workflow.js` |

**SKILL.md 与 Workflows 分工**：

| 组件 | 负责什么 | 不负责什么 |
|------|----------|------------|
| **SKILL.md** | 触发条件、契约、知识 | 具体执行逻辑 |
| **Workflows** | 具体执行逻辑、编排实现 | 触发判断、知识定义 |
| **trajectory Eval** | 验证执行过程 | 验证输出内容（由output Eval负责） |

**新增 Schema**：

| 文件 | 用途 |
|------|------|
| `schemas/workflow.schema.json` | Workflows 脚本元数据结构 |

---

## 与仓库其他模块的关系

| 模块 | 职责 |
|------|------|
| **`skill-engineering/`**（本目录） | 创建骨架、结构校验、Schema、生命周期速查、CI 门禁自动化脚本 |
| **`skills/`** | 实际 Skill 实现（随 Cursor 插件分发） |
| **`skills-quality/`** | 已有 Skill 的质量台账、问题池、baseline / 回归计划、发布门禁 |
| **`.github/workflows/eval-ci.yml`** | GitHub Actions CI 门禁 Workflow（PR/Release/定期回归） |

推荐工作流：

```text
new-skill.sh 创建
  → validate-skill.py 结构校验
  → 填写 evals / test-prompts
  → baseline 写入 results.tsv
  → 真实问题进入 skills-quality/skill-issues.jsonl
  → 按 skills-quality/release-checklist.md 发布
  → CI 门禁自动回归（PR触发 → regression 挂必阻）
```

---

## JSON Schema

| 文件 | 用途 |
|------|------|
| `schemas/evals.schema.json` | `evals/evals.json` 结构（输出Eval） |
| `schemas/trajectory-evals.schema.json` | `evals/trajectory-evals.json` 结构（过程Eval） |
| `schemas/test-prompts.schema.json` | `test-prompts.json` 结构 |
| `schemas/skill-meta.schema.json` | `.skill-meta.json` 结构 |
| `schemas/skill-issue.schema.json` | `skill-issues.jsonl` 单行结构 |
| `schemas/workflow.schema.json` | `workflows/*.js` 元数据结构（新增） |

可在 CI 或本地脚本中用任意 JSON Schema 校验器引用上述文件。

---

## CI 门禁自动化（新增）

CI 门禁实现 Eval 自动回归，改 Skill 后 regression 挂必阻合并。

### 门禁三阶段

| 阶段 | 时机 | 跑什么 | 目的 |
|------|------|--------|------|
| **PR 触发** | 提交 PR | risk=high + medium | 阻止 regression 退化 |
| **发布前** | 合入 main | 全量 Eval | 全能力回归验证 |
| **定期回归** | 每周/月 | spot check + 季度全量 | 发现长期退化 |

### 门禁红线

| 红线 | risk | 类型 | 阻止合并？ |
|------|------|------|:----------:|
| **regression 挂（high）** | high | regression | ✅ BLOCK |
| **regression 挂（medium）** | medium | regression | ⚠️ WARN |
| **新增 Eval 未 baseline** | - | - | ✅ BLOCK |
| **改 Skill 未跑 baseline** | - | - | ✅ BLOCK |

### CI 文件结构

```text
.github/workflows/eval-ci.yml  # GitHub Actions Workflow
skill-engineering/
  scripts/
    run_evals.py               # Eval runner（PR/Release/Scheduled）
    check_regression.py        # Regression 门禁检查
    check_new_evals.py         # 新 Eval baseline 检查
    graders/
      rule_grader.py           # 关键词检查（完全自动）
      structure_grader.py      # 结构检查（完全自动）
      trajectory_grader.py     # 调用顺序检查（完全自动）
      model_grader.py          # LLM Judge（半自动，防漂移）
  config/
    risk-layer-config.json     # risk 分层 + 门禁红线配置
```

### 运行 CI 门禁

```bash
# 手动触发（测试）
gh workflow run eval-ci.yml -f skill=wechat-article-review -f mode=pr

# 本地跑 Eval（模拟 CI）
python3 plugins/frontend-team-toolkit/skill-engineering/scripts/run_evals.py \
  --mode pr --skill wechat-article-review --output results.tsv

# 检查 regression
python3 plugins/frontend-team-toolkit/skill-engineering/scripts/check_regression.py \
  --results results.tsv --risk high --block true

# 检查新 Eval baseline
python3 plugins/frontend-team-toolkit/skill-engineering/scripts/check_new_evals.py \
  --skill wechat-article-review --results results.tsv
```

### `/loop` 自动化回归

Claude Code `/loop` 命令支持定期自动化回归：

```text
/loop weekly 用 workflows/weekly-regression.js 回归 wechat-article-review Skill
```

Workflows 脚本：`templates/new-skill/workflows/weekly-regression.js`

---

## Grader 自动化速查表

| grader | CI 自动化 | 数据来源 | 漂移风险 |
|--------|:--------:|----------|:--------:|
| **rule** | ✅ 完全 | 输出文本 | 无 |
| **structure** | ✅ 完全 | 输出文本 | 无 |
| **trajectory** | ✅ 完全 | Agent trace | 无 |
| **model** | ⚠️ 半自动 | LLM Judge | 有（多次采样防漂移） |
| **human** | ❌ 人工 | 人工审核 | 无 |

---

## 约定

- Skill `name` 使用 **kebab-case**，与目录名一致
- `description` 必须包含 **Use when** 与足够触发词（第三人称）
- 改 Skill 前先改或确认 `evals/evals.json`，再跑 baseline
- 生产问题写入 `skill-issues.jsonl`，再转为 regression case
- 一轮只改一个假设；高风险 regression 失败不发布

---

## 与外部工具配合（可选）

| 步骤 | 工具 |
|------|------|
| 创建骨架 | `new-skill.sh`（本仓库） |
| 结构校验 | `validate-skill.py`（本仓库） |
| Benchmark / A-B | Anthropic [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| 自动棘轮优化 | [darwin-skill](https://github.com/alchaincyf/darwin-skill) |
| 静态 QA | [okjpg/skill-audit](https://github.com/okjpg/skill-audit) |

---

## 升级已有 Skill

仓库内部分 Skill 创建于引入本脚手架之前，可能缺少 `evals/` 或 `references/output-contract.md`。建议：

1. 运行 `validate-skill.py` 查看缺口（warning 可分批补齐）
2. 优先补 `test-prompts.json` + `results.tsv`（见 `skills-quality/eval-plan.md`）
3. 新 Skill 一律通过 `new-skill.sh` 创建，保持结构一致

---

## 本地校验示例

```bash
# 校验插件 manifest（仓库级）
node scripts/validate-template.mjs

# 校验单个 Skill 目录结构
python3 plugins/frontend-team-toolkit/skill-engineering/bin/validate-skill.py \
  plugins/frontend-team-toolkit/skills/code-verify
```

`code-verify` 等历史 Skill 可能仅有部分工业级文件，校验时会出现 warning，属预期行为。
