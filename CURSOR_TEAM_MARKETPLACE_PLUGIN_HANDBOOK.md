# Cursor Team Marketplace 插件开发规范教程手册

本手册面向在 **Git 仓库中维护 Cursor Team Marketplace** 的团队：管理员在 Dashboard 导入仓库后，成员可安装插件并获得统一的 MCP、Skills、Rules 等能力。内容综合了 [Cursor Plugins 官方参考](https://cursor.com/docs/reference/plugins)、[Cursor Plugins 概览](https://cursor.com/docs/plugins)，以及本仓库 `frontend-team-marketplace` 的实践与校验脚本。

**方法论说明**：下文「内容生产工作流」借鉴自本地 **wechat-agents** 项目（例如 `dist/openclaw/souls/chief-editor/SOUL.md`、`dist/openclaw/souls/content-writer/SOUL.md` 与 `learning/templates/publish-checklist.md`）中的 **主编（Chief Editor）六步法** 与 **写作者（Content Writer）六步法**——将「选题—角度—结构—撰写—打磨—发布复盘」映射为插件场景下的「需求与边界—插件拆分—清单与 manifest—实现资源—本地校验与评审—导入 Marketplace 与成员侧验收」。

---

## 1. 核心概念

### 1.1 Team Marketplace 与单插件仓库的区别

| 形态 | 根清单 | 典型用途 |
|------|--------|----------|
| **单插件仓库** | 仅 `plugins/<name>/.cursor-plugin/plugin.json`（或模板根结构） | 开源提交、单包分发 |
| **Team Marketplace 多插件仓库** | 根目录 **`.cursor-plugin/marketplace.json`** + 每个插件目录内 **`plugin.json`** | 组织内统一导入、多插件并行演化 |

本仓库属于第二种：`metadata.pluginRoot` 为 `plugins`，`marketplace.json` 的 `plugins[].source` 指向各插件子目录。

### 1.2 插件能打包的能力（与官方一致）

插件可将以下能力打成可分发包（成员安装后 Cursor 侧统一暴露）：

- **Rules**（`.mdc`）：持久规则与项目约定  
- **Skills**：`skills/<skill>/SKILL.md`，定义「何时、如何做」  
- **Agents**：自定义 Agent 说明  
- **Commands**：可执行命令文档  
- **Hooks**：`hooks/hooks.json` 与脚本  
- **MCP**：`mcp.json` 中的 `mcpServers`  

官方约定默认发现路径见 [Plugins reference - Component discovery](https://cursor.com/docs/reference/plugins)；若在 `plugin.json` 中显式指定某类路径，则**仅使用显式路径**，不再叠加扫描默认目录。

---

## 2. 仓库与目录规范（本仓库实践）

推荐结构（与根 `README.md` 一致）：

```text
<repo-root>/
├── .cursor-plugin/
│   └── marketplace.json       # Team Marketplace 总清单（必填于多插件仓库）
├── plugins/
│   └── <plugin-id>/
│       ├── .cursor-plugin/
│       │   └── plugin.json   # 单插件 manifest（必填）
│       ├── mcp.json          # 可选：MCP 定义
│       ├── skills/           # 可选：每个子目录含 SKILL.md
│       ├── rules/            # 可选：.mdc 等
│       ├── agents/
│       ├── commands/
│       ├── hooks/
│       ├── assets/           # 可选：logo 等
│       └── README.md         # 建议：成员安装后的配置说明
├── scripts/
│   └── validate-template.mjs # 本仓库：manifest / 路径 / frontmatter 校验
└── README.md
```

### 2.1 `marketplace.json` 要点

- **`name`**：Marketplace 标识，小写 kebab-case，首尾为字母或数字（本仓库校验与 `plugin.json` 的 `name` 规则分列，见脚本内 `marketplaceNamePattern` / `pluginNamePattern`）。  
- **`owner`**：至少 `owner.name`（本仓库校验强制）。  
- **`plugins`**：非空数组；每项含 **`name`**、**`source`**（相对路径，安全、无 `..`）。  
- **`metadata.pluginRoot`**：可选；若设置（如 `plugins`），则 entry 的 `source` 会与此前缀拼接解析（见 `scripts/validate-template.mjs` 中 `resolveMarketplaceSource`）。  
- **一致性**：每个 `plugins[].name` 必须与其目录内 `plugin.json` 的 **`name` 完全一致**（校验会报错）。

### 2.2 `plugin.json` 要点

**必填**：`name`（小写，仅字母数字、连字符、点号，首尾为字母数字）。

**常用可选字段**：`displayName`、`version`、`description`、`author`、`license`、`keywords`、`logo`、`rules`、`skills`、`agents`、`commands`、`hooks`、`mcpServers` 等。字段含义以 [官方 Plugin manifest](https://cursor.com/docs/reference/plugins) 为准。

**路径类字段**：引用仓库内资源须为**相对插件根目录**的路径，且**合法**（无 `..`、无端盘绝对路径）。本仓库 `validate-template.mjs` 会检查这些路径是否存在。

---

## 3. 各组件编写规范摘要

### 3.1 Rules（`rules/*.mdc`）

- 顶部 **YAML frontmatter** 必填 **`description`**。  
- 常用字段：`alwaysApply`、`globs`。  
- 正文为面向 Agent 的持久约束说明。  

### 3.2 Skills（`skills/<dir>/SKILL.md`）

- Frontmatter 必填：**`name`**、**`description`**（`description` 应写清触发场景，便于 Agent Decides 选用）。  
- 正文建议包含：适用场景、步骤化工作流、项目内约定、注意事项。  

本仓库示例：`plugins/frontend-team-toolkit/skills/yapi-frontend-integration/SKILL.md`；OpenSpec 四文件契约见 `skills/openspec-contract-authoring/SKILL.md`。

### 3.3 Agents / Commands

- 对应目录下 `.md`/`.mdc`/`.markdown`（Commands 另支持 `.txt`）。  
- Frontmatter 必填 **`name`**、**`description`**。  

### 3.4 Hooks

- 配置文件默认期望：`hooks/hooks.json`（事件列表与命令见官方 Hooks 文档）。  
- 本仓库校验：无 `hooks.json` 时仅 **warning**，因非每个插件都需要 Hooks。  

### 3.5 MCP（`mcp.json`）

```json
{
  "mcpServers": {
    "server-id": {
      "command": "npx",
      "args": ["-y", "some-mcp-package", "--stdio"],
      "env": { "API_KEY": "placeholder" }
    },
    "http-server": {
      "url": "https://example.com/mcp"
    }
  }
}
```

- **stdio 型**：`command` + `args`（+ 可选 `env`）。  
- **URL 型**：`url` 字段。  
- **安全**：仓库内仅保留占位符；真实 Token/密码由成员在本机 MCP 设置中覆盖或使用组织密钥方案，**禁止提交机密**。  

---

## 4. 本地校验与 CI

### 4.1 运行校验

```bash
cd <repo-root> && node scripts/validate-template.mjs
```

### 4.2 校验覆盖范围（实现以脚本为准）

- `marketplace.json` / `plugin.json` JSON 合法性及命名规则。  
- `plugins[]` 中 `source` 目录存在性；**marketplace 与 plugin 的 `name` 一致**。  
- `plugin.json` 中 `logo`、`rules`、`skills`、`agents`、`commands`、`hooks`、`mcpServers` 等解析出的路径存在且安全。  
- 已存在的 `rules/`、`skills/**/SKILL.md`、`agents/`、`commands/` 的 frontmatter 关键字段。  
- `mcp.json` 缺失时 warning（按需）。  

团队新增插件或组件后，应保证 **`node scripts/validate-template.mjs` 在 CI 与本机均通过**（本仓库含 `.github/workflows/validate-template.yml`）。

---

## 5. 团队运营：导入与安装

1. 将仓库推送到组织可访问的 Git 远程（常见为 GitHub）。  
2. **Cursor Dashboard → Settings → Plugins → Team Marketplaces → Import**，粘贴仓库 URL。  
3. 设置插件为 **Required**（强制）或 **Optional**（自选）。  
4. 成员在 Cursor **Marketplace / Plugins** 安装对应插件，并在 **Settings → MCP** 等处补全环境相关配置。  

公开 Marketplace 提交流程见 [Submitting a plugin](https://cursor.com/docs/reference/plugins)（与 Team 内部导入流程不同，本手册侧重 Team Marketplace 仓库维护）。

---

## 6. 开发工作流（映射 wechat-agents 主编 / 写作者流程）

以下将 `wechat-agents` 中 **主编六步法** 与 **写作者六步法** 压缩为可执行的插件交付流程。可直接作为团队 Wiki 或 PR 描述模板。

### 6.1 主编视角（Chief Editor）— 从战略到验收

| 主编步骤 | 插件开发中的对应动作 | 产出 |
|----------|----------------------|------|
| **Step 1 选题策划** | 明确团队痛点：要统一的是 MCP、规范、流程技能还是自动化 Hooks？ | 需求一页纸：目标用户（前端/全栈）、非目标、成功标准 |
| **Step 2 角度确定** | 拆成「一个插件 vs 多个插件」、是否共用一个 MCP 配置文件 | Marketplace 插件列表草稿（`name` / `source` / 简短 `description`） |
| **Step 3 结构搭建** | 定目录：`rules` / `skills` / `mcp.json` 等是否 needed | 目录树 + `marketplace.json` + 各 `plugin.json` 字段清单 |
| **Step 4 内容撰写** | 编写 SKILL、规则、MCP 占位 config、README | 可安装的最小可用包 |
| **Step 5 优化打磨** | 跑 `validate-template.mjs`、走查路径与 frontmatter、同事评审 | PR：校验绿、文档无密钥 |
| **Step 6 发布与复盘** | Dashboard 导入或更新仓库；抽样一名成员全新安装验收 | 复盘：哪些路径易错、是否需再加 Skill 触发说明 |

**主编铁律（改编）**：

- **价值优先**：每个插件对成员有明确可感知的收益（少配一次 MCP、少翻一次内部文档）。  
- **合规底线**：无政治/侵权内容；无硬编码真实密钥。  
- **数据/反馈**：收集「装不上 / MCP 连不上 / Skill 没被触发」反馈，迭代 `description` 与 README。  

### 6.2 写作者视角（Content Writer）— 从材料到成稿

| 写作者步骤 | 插件开发中的对应动作 |
|------------|----------------------|
| **Step 1 理解选题** | 阅读需求一页纸与官方 Plugins 参考，确认与 Cursor 当前行为一致 |
| **Step 2 素材准备** | 收集：MCP 包名、环境变量名、内部 Wiki 链接、示例链接（YApi/Figma 等） |
| **Step 3 结构搭建** | 为大篇 `SKILL.md` 写大纲：何时用 → 步骤 → 表格速查 → 注意事项 |
| **Step 4 初稿撰写** | 先写 MCP `mcp.json` 占位与插件 README，再写 SKILL 正文 |
| **Step 5 优化打磨** | 朗读 SKILL 的步骤是否可单独执行；`description` 是否覆盖口语触发说法 |
| **Step 6 标题与发布** | `displayName` / `description` / `keywords` 便于面板搜索；合并前再跑校验 |

**写作者铁律（改编）**：

- **开头交代价值**：`README.md` 首段说明「安装后你能多省什么事」。  
- **干货占比**：Skill 正文以可操作步骤为主，少空话。  
- **结构清晰**：多级标题 + 步骤编号 + 必要时表格。  

---

## 7. 发布前检查清单（改编自 wechat-agents `publish-checklist`）

在合并入主分支或通知管理员重新导入前，逐项确认：

- [ ] **`marketplace.json`**：`name`、`owner`、`plugins` 正确；`source` 与 `pluginRoot` 解析无误。  
- [ ] **每个 `plugin.json`**：`name` 与 marketplace 条目一致；`version` / `description` 已更新（若有变更）。  
- [ ] **路径**：manifest 中引用的文件均在仓库内，无 `..`，无绝对路径。  
- [ ] **Frontmatter**：所有 Rule / Skill / Agent / Command 已含必需字段。  
- [ ] **密钥**：无真实 Token、密码、内网秘文；仅有占位符或文档说明。  
- [ ] **校验**：`node scripts/validate-template.mjs` 通过；CI 通过。  
- [ ] **成员文档**：插件根 `README.md` 说明安装后必做的 MCP / 环境步骤。  
- [ ] **抽样验收**：任选一台干净环境按 README 安装，确认 MCP 列表与 Skill 可见。  

**必须修复（阻塞发布）**：校验失败、名称不一致、路径缺失、机密泄露。  

**可选优化**：补充 `logo`、丰富 `keywords`、为 Skill 增加 `reference.md` 附件。  

---

## 8. 参考链接

- [Cursor Plugins（概览）](https://cursor.com/docs/plugins)  
- [Cursor Plugins reference（manifest、目录、组件格式、多插件仓库）](https://cursor.com/docs/reference/plugins)  
- [Cursor Rules](https://cursor.com/docs/rules)  
- [Cursor Skills](https://cursor.com/docs/skills)  
- [Cursor Hooks](https://cursor.com/docs/hooks)  
- [Cursor MCP](https://cursor.com/docs/mcp)  
- 官方插件模板仓库：[cursor/plugin-template](https://github.com/cursor/plugin-template)  

---

## 9. 附录：本仓库当前插件速览

| 项目 | 说明 |
|------|------|
| Marketplace `name` | `frontend-team-marketplace` |
| 插件目录 | `plugins/frontend-team-toolkit` |
| MCP | `yapi-devloper-mcp`、`figma-developer-mcp`、蓝湖 HTTP MCP（`url`） |
| Skills | `openspec-contract-authoring`、`vue2-to-vue3-migration`、`yapi-frontend-integration` |

若团队扩展 **Rules / Agents / Commands / Hooks**，请同步更新根 `README.md` 中的「能力对照表」，并保证校验脚本仍然通过。

---

*文档版本：与仓库 `frontend-team-marketplace` 当前结构同步撰写；官方 Cursor 行为以 cursor.com 文档为准。*
