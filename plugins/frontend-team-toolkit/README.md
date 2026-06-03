# Frontend Team Toolkit

团队前端插件：**YApi**（`yapi-devloper-mcp`）、**Figma**（`figma-developer-mcp`）、**蓝湖**（`lanhu`，HTTP MCP URL）。

## 技能（Skills）

| 目录 | 说明 |
|------|------|
| `skills/openspec-contract-authoring` | OpenSpec 四文件契约化（甲）；可选「按契约落地」前 Gate（乙） |
| `skills/vue2-to-vue3-migration` | 两阶段协议 + 工程就绪；`reference` §1–§12（模板、扫雷、完整校验、坑点）、可选 `MIGRATION_BASELINE` |
| `skills/yapi-frontend-integration` | 两阶段摘要 + YApi MCP；`reference`（字段映射、TS、排障、安全） |
| `skills/code-verify` | **先锚定再迭代**：五阶段闸门 + 七维双锚验证；`report-template`、`checklist-template`、`validate.sh` |
| `skills/incremental-implementation` | **锚定现有代码做增量迭代**：源文档 vN 变更后不 greenfield 重跑；Reconcile 代码编排 IC-R0~IC-R7、多产物版本对齐、局部更新护栏；`实现映射` 锚点 + 五阶段流水线；接力 `pm-md-to-openspec-pipeline` R6 |
| `skills/ai-coding-tri-kit` | **三件套工程化工作流**：OpenSpec（What）→ Superpowers（How）→ Agent Skills（Quality）8 步流水线；强度分级 Full/Standard/Lite；闸门强制、回退机制、输出契约；适合新功能/中等以上改动、可预测交付场景 |
| `skills/wechat-article-review` | **微信公众号文章评分审稿**：0–10 分结构化评分与改稿反馈；五维加权评分（主题、结构、清晰度、实用性、合规）；≥9.0 通过，<9.0 必须输出 P0/P1/P2 修改清单；含评分细则、输出契约、持久化记录 |

技能随本插件版本在本仓库内维护与迭代。

## Skill 工程化（`skill-engineering/`）

| 能力 | 说明 |
|------|------|
| `skill-engineering/bin/new-skill.sh` | 从标准模板创建新 Skill 目录 |
| `skill-engineering/bin/validate-skill.py` | 校验 Skill 结构与 frontmatter |
| `skills/skills-quality/` | 问题池、baseline 计划、发布门禁 |

详见 [`skill-engineering/README.md`](skill-engineering/README.md)。

## MCP 配置（`mcp.json`）

提交到仓库的是**占位配置**，避免泄露密钥。安装插件后请在本机完成：

### yapi-devloper-mcp

- 设置 `YAPI_BASE_URL`、`YAPI_USERNAME`、`YAPI_PASSWORD` 为真实值（或在 Cursor MCP 设置里覆盖整条 server 配置）。
- 若团队统一使用自定义 `npx` 包装脚本，可将 `command` 改为该脚本路径。

### figma-developer-mcp

- 将 `--figma-api-key=` 后的占位符替换为你的 [Figma Personal Access Token](https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens)，或使用 CLI 支持的 `--env` 指向本地 `.env`（勿提交 `.env`）。

### lanhu

- `url` 需指向你们环境中运行的蓝湖 MCP 服务地址（示例为本地 `127.0.0.1:8000`）。
- 按蓝湖侧要求调整查询参数（如 `role`、`name`/`邮箱`）。

## 与上游模板对齐

新增规则（`rules/`）、代理（`agents/`）等可参考 [Cursor plugin 结构说明](https://cursor.com/docs/plugins)；注册新插件时需同步修改根目录 `.cursor-plugin/marketplace.json`。
