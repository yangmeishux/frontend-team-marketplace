# 从零到跑通 Cursor Team Marketplace 插件（公众号稿）

> 本文改编自仓库内 [`CURSOR_TEAM_MARKETPLACE_PLUGIN_HANDBOOK.md`](./CURSOR_TEAM_MARKETPLACE_PLUGIN_HANDBOOK.md)，话术与段落节奏参考微信公众号写作习惯：**开篇抓痛点 → 可执行方法论 → 分层结构 → 清单收尾**。技术约定以 [Cursor Plugins 官方文档](https://cursor.com/docs/plugins)与 [Plugins reference](https://cursor.com/docs/reference/plugins) 为准。

---

## 备选标题（可三选一）

1. **从零到跑通：团队用 Cursor Team Marketplace 做插件分发，这一篇就够**
2. **一人配环境、全员可复制：Cursor Team Marketplace 插件开发与维护指南**
3. **不写代码也能统一管理 MCP？Team Marketplace 多插件仓库入门**

---

## 正文

你还在让每个同事各自拷贝一份 `.cursor`、`mcp.json` 和自建 Skills 吗？装一次忘一次、改了规则又不同步。**Cursor Team Marketplace** 把「规则、Skills、MCP、Hooks」打成可安装的插件包，团队在 Dashboard 绑定 **一个 Git 仓库**，成员点开安装就能对齐能力。

这篇文章只做一件事：**帮你在脑中搭好骨架，并按步骤从 0 到 1 做出第一个可上线的团队插件**。文中概念与 Cursor 官方文档一致；实操细节可随时对照 [Plugins 概览](https://cursor.com/docs/plugins) 与 [Plugins reference（manifest、组件发现、多插件仓库）](https://cursor.com/docs/reference/plugins)。

### 一、先想清楚：你到底在分发什么？

**Team Marketplace** 本质是：**用 Git 仓库维护「可被 Cursor 识别的插件清单 + 插件内容」**。和「单机单仓库只放一个插件」不同，团队常用形态是：

| 形态 | 根清单 | 典型用途 |
|------|--------|----------|
| **单插件仓库** | 主要为某个 `plugins/<name>/.cursor-plugin/plugin.json` | 开源提交、单包分发 |
| **Team Marketplace 多插件仓库** | 根目录 **`.cursor-plugin/marketplace.json`** + 每个插件目录内 **`plugin.json`** | 组织内 Import、多插件并行演化 |

第二点是你做「前端团队套件」「设计协作包」「后端规范包」时能并行演化的形态。**`marketplace.json` 里每个插件条的 `name`，必须和它目录里的 `plugin.json` 里的 `name` 完全一致**，否则校验和导入都会对不上——这是新手最容易翻车的地方。

### 二、插件能打包哪些能力（别漏项）

装上插件后，Cursor 会把下面几类资源统一暴露给成员（与官方组件发现规则一致）：

- **Rules**（`.mdc`）：持久项目约定。
- **Skills**：`skills/<某目录>/SKILL.md`，写清「何时、怎么做」。
- **Agents / Commands**：自定义说明或可执行命令文档。
- **Hooks**：`hooks/hooks.json` + 脚本，做自动化钩子。
- **MCP**：`mcp.json` 里的 `mcpServers`。

**关键规则记在脑子里**：若在 `plugin.json` 里 **显式写死了某类资源的目录**，一般会 **只按你写的路径来**，不再叠加扫描默认目录。要么全交给默认约定，要么就写全、写对并在仓库里校验。（默认发现路径详见官方 [Component discovery](https://cursor.com/docs/reference/plugins)。）

### 三、从零搭目录：建议你照抄这套结构再改

多插件仓库可以按下面这样长（与本仓库 [`README.md`](./README.md) 实践一致）：

```text
<仓库根>/
├── .cursor-plugin/
│   └── marketplace.json       # Marketplace 总清单（多插件必填）
├── plugins/
│   └── <plugin-id>/           # 单个插件的根
│       ├── .cursor-plugin/
│       │   └── plugin.json    # 单插件 manifest（必填）
│       ├── mcp.json           # 可选
│       ├── skills/            # 可选，每 skill 目录内 SKILL.md
│       ├── rules/
│       ├── agents/
│       ├── commands/
│       ├── hooks/
│       ├── assets/            # 如 logo
│       └── README.md          # 强烈建议：装完后成员要配的步骤写这里
├── scripts/
│   └── validate-template.mjs  # 本仓库：manifest / 路径 / frontmatter 校验
└── README.md
```

**`marketplace.json` 里常要注意的字段**：Marketplace `name`、`owner`、`plugins[]`（每项要有 `name` + `source`）；若使用了 **`metadata.pluginRoot`**（例如 `plugins`），`source` 往往会和这个前缀拼接再解析——改路径时别把拼接规则忘了。

**`plugin.json`**：`name` 必填且符合命名规范；可选 `displayName`、`version`、`description`、`logo`、以及指向 rules/skills/mcp 的路径类字段。**所有路径都必须相对插件根、合法且无 `..`。** 成员能在面板搜到、能看懂，很大程度靠 `displayName`、`description`、`keywords`。

### 四、各组件怎么写，才「能被用上」？

**Rules（`rules/*.mdc`）**  
YAML frontmatter 里 **`description` 必填**；常用 `alwaysApply`、`globs`。正文就是给 Agent 的长期约束。

**Skills（`skills/xxx/SKILL.md`）**  
Frontmatter：**`name`、`description` 必填**。`description` 要写清楚 **在什么口语场景下该被选用**，否则很容易出现「写好却从不触发」。正文推荐：何时用 → 分步流程 → 项目内约定 → 坑点。

**Agents / Commands**  
对应 markdown 文件 frontmatter：**`name`、`description` 必填**。（Commands 另支持部分扩展名，以官方文档为准。）

**Hooks**  
有自动化需求再上；没有可以放掉——本仓库校验脚本对缺失 `hooks.json` 常为 **warning**。

**MCP（`mcp.json`）**  

- **stdio**：`command` + `args`，可选 `env`。  
- **远程**：`url` 字段。

示例（占位符示意）：

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

**安全红线**：仓库里只放 **占位符** 与变量名说明，**永远不要提交真实 Token**。真密钥由成员在本机 **Settings → MCP** 等处补全，或通过组织侧密钥方案注入。

### 五、「主编 + 写手」六步法：从需求到可安装包（可当团队 Wiki）

把内容生产里的「选题—结构—成稿—发布」映射到插件交付，会减少扯皮。思路与手册第 6 节一致。

**主编视角（定方向 + 验收）**

| 步骤 | 插件交付里做什么 | 产出 |
|------|------------------|------|
| 1 选题 | 要解决 MCP 统一、编码规范还是 onboarding？ | 需求一页纸：用户、非目标、成功标准 |
| 2 角度 | 一个插件还是多个？是否共用 MCP？ | Marketplace 条目草稿（`name` / `source` / 简述） |
| 3 结构 | 定目录与各 manifest 字段 | 目录树 + `marketplace.json` + 各 `plugin.json` 清单 |
| 4 撰写 | 先 MVP：最小 Rules + README +（可选）Skill | 可安装的最小可用包 |
| 5 打磨 | 跑校验、走查路径与 frontmatter、评审 | PR：校验绿、无明文密钥 |
| 6 发布复盘 | Dashboard Import/更新；抽人干净环境验收 | 记录路径易错点、Skill 触发问题 |

**主编改编铁律**：价值优先（成员能感知省了什么）、合规底线（无侵权与违规内容、无硬编码密钥）、用反馈迭代 `description` 与 README。

**写手视角（把 Skill / README 写好）**

1. 理解选题并对照官方 Plugins 文档。  
2. 素材：MCP 包名、环境变量名、内部 Wiki / YApi / Figma 等链接。  
3. **README 第一段就写**：装完能少做哪几件重复劳动。  
4. 初稿顺序：先有 `mcp.json`（占位）+ README，再写 Skill 正文。  
5. 打磨：朗读步骤是否可独立执行；`description` 是否覆盖口语触发说法。  
6. 上架前检查 `displayName` / `description` / `keywords`，合并前再过校验。

### 六、本地怎么验、上线怎么分发？

**运行校验（建议接入 CI）**

```bash
cd <repo根目录> && node scripts/validate-template.mjs
```

脚本会覆盖（以 `scripts/validate-template.mjs` 实现为准）：`marketplace.json` / `plugin.json` JSON 合法性、命名规则、`source` 存在性、**Marketplace 与 plugin 的 `name` 一致**、manifest 解析出的路径真实存在且无 `..`、已有 Rules/Skills/Agents/Commands 的 frontmatter、`mcp.json` 按需 warning 等。团队约定：**合入主干前本条命令与 CI（如 `.github/workflows/validate-template.yml`）通过。**

**团队侧操作流程**

1. 将仓库推到组织可访问的 Git 远程（常见 GitHub）。  
2. Cursor **Dashboard → Settings → Plugins → Team Marketplaces → Import**，粘贴仓库 URL。  
3. 插件设为 **Required**（强制）或 **Optional**（自选）。  
4. 成员在 Cursor **Marketplace / Plugins** 安装，并按各插件 **README** 补全 MCP 与环境。

若要提交到 Cursor **公开** Marketplace，流程与 Team Import 不同，详见官方 [Submitting a plugin](https://cursor.com/docs/reference/plugins)。

### 七、迭代与维护：别做完就扔

**版本与沟通**  

- 有行为变更就更新 **`plugin.json` 的 `version`、`description`**。  
- 大改时在仓库 README 或团队频道说明：成员是否需要重装、或仅靠同步仓库即可——以控制台行为为准，关键是 **沟通习惯**。

**三类高频迭代**  

1. **MCP**：换包名、加 server、统一 env 说明模板。  
2. **Skills**：触发率低多半是 `description` 不像人话；补步骤与链接。  
3. **Rules**：新项目类型或栈升级时调整 `globs`，避免全局误伤。

**文档与对齐**  

- 根 README：Marketplace 下有哪些插件、各负责什么。  
- 每插件 README：安装后「必做三件事」。  
- 能力对照表一有增减就更新。

**发布后小复盘（约 5 分钟）**：路径报错 → manifest；Skill 唤不出 → 触发描述；密钥误提交 → PR review。

### 八、合并前自检清单（团队模板）

改编自手册第 7 节与内容发布类清单思路（如团队本地 wechat-agents 中的 `publish-checklist` 模板）；以下与仓库内手册一致：

- [ ] **`marketplace.json`**：`name`、`owner`、`plugins` 正确；`source` 与 `pluginRoot` 解析无误。  
- [ ] **每个 `plugin.json`**：`name` 与 marketplace 条目一致；有变更则 `version` / `description` 已更新。  
- [ ] **路径**：引用文件均在仓库内，无 `..`，无非法绝对路径。  
- [ ] **Frontmatter**：Rule / Skill / Agent / Command 必需字段齐全。  
- [ ] **密钥**：无真实 Token / 密码；仅占位符或文档说明。  
- [ ] **校验**：`node scripts/validate-template.mjs` 通过；CI 通过。  
- [ ] **成员文档**：插件根 `README.md` 写明安装后的 MCP / 环境步骤。  
- [ ] **抽样验收**：干净环境安装，确认 MCP 列表与 Skill 可见。

**必须修复（阻塞发布）**：校验失败、名称不一致、路径缺失、机密泄露。  

**可选优化**：`logo`、`keywords`、Skill 附带 `reference.md` 等。

### 延伸阅读（官方）

- [Cursor Plugins（概览）](https://cursor.com/docs/plugins)  
- [Cursor Plugins reference](https://cursor.com/docs/reference/plugins)  
- [Cursor Rules](https://cursor.com/docs/rules)  
- [Cursor Skills](https://cursor.com/docs/skills)  
- [Cursor Hooks](https://cursor.com/docs/hooks)  
- [Cursor MCP](https://cursor.com/docs/mcp)  
- 模板仓库：[cursor/plugin-template](https://github.com/cursor/plugin-template)

---

## 结语

Team Marketplace 的价值不在「多了一个配置文件」，而在于 **把组织能力产品化**：一次定义，全员复用；一次修正，整条链路对齐。你从 **一个最小插件 + 一段写清触发场景的 Skill + 能通过校验的 manifest** 开始，就已经完成了最有价值的从 0 到 1。

---

*文稿版本：与 `frontend-team-marketplace` 当前结构对齐；Cursor 行为以 cursor.com 文档为准。*
