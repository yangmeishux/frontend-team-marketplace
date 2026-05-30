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
├── bin/
│   ├── new-skill.sh          # 从模板生成 Skill 目录
│   └── validate-skill.py     # frontmatter + 工业级必备文件校验
├── schemas/                  # JSON Schema（evals、test-prompts、meta、issues）
├── templates/new-skill/      # 新 Skill 模板包（勿直接使用，请用脚本复制）
└── docs/
    └── lifecycle-quickref.md # 8 Phase 生命周期速查
```

---

## 生成的 Skill 标准结构

```text
<skill-name>/
├── SKILL.md
├── CHANGELOG.md
├── .skill-meta.json
├── evals/evals.json
├── test-prompts.json
├── results.tsv
├── skill-issues.jsonl.example
├── references/output-contract.md
└── scripts/validate-output.sh
```

与 [agentskills.io 规范](https://agentskills.io/specification) 对齐：`name` / `description` 必填；团队 Skill 默认设置 `disable-model-invocation: true`，需显式 `@` 触发。

---

## 与仓库其他模块的关系

| 模块 | 职责 |
|------|------|
| **`skill-engineering/`**（本目录） | 创建骨架、结构校验、Schema、生命周期速查 |
| **`skills/`** | 实际 Skill 实现（随 Cursor 插件分发） |
| **`skills-quality/`** | 已有 Skill 的质量台账、问题池、baseline / 回归计划、发布门禁 |

推荐工作流：

```text
new-skill.sh 创建
  → validate-skill.py 结构校验
  → 填写 evals / test-prompts
  → baseline 写入 results.tsv
  → 真实问题进入 skills-quality/skill-issues.jsonl
  → 按 skills-quality/release-checklist.md 发布
```

---

## JSON Schema

| 文件 | 用途 |
|------|------|
| `schemas/evals.schema.json` | `evals/evals.json` 结构 |
| `schemas/test-prompts.schema.json` | `test-prompts.json` 结构 |
| `schemas/skill-meta.schema.json` | `.skill-meta.json` 结构 |
| `schemas/skill-issue.schema.json` | `skill-issues.jsonl` 单行结构 |

可在 CI 或本地脚本中用任意 JSON Schema 校验器引用上述文件。

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
