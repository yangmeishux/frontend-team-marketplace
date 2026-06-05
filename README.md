# Frontend Team Marketplace

面向前端团队的 **Cursor Team Marketplace** 仓库：管理员在 Dashboard 导入本 Git 仓库后，团队成员即可安装其中的插件并获得统一的 MCP 与 Skills 配置入口。

当前仓库只发布 **一个插件**：**Frontend Team Toolkit**（见 `plugins/frontend-team-toolkit`）。

---

## Cursor 插件里常见能力对照（本仓库现状）

Cursor 插件可以把多种能力打包分发，常见类型如下：

| 能力 | 说明 | 本 Marketplace 是否包含 |
|------|------|-------------------------|
| **MCP**（Model Context Protocol） | 连接外部工具/API（YApi、Figma、蓝湖等），Agent 通过 MCP 提供的 **Tools** 拉数据、执行操作 | **已包含**：`mcp.json` 中声明 3 个 MCP Server |
| **Skills** | 带 YAML 头信息的 `SKILL.md`，教 Agent **何时、如何用**某套流程（可与 MCP 配合） | **已包含**：5 个技能目录 |
| **Rules**（`.mdc`） | 持久规则：编码规范、项目约定等 | **未包含**（可按需在插件下增加 `rules/`） |
| **Agents** | 自定义代理人设与任务拆分 | **未包含**（可按需增加 `agents/`） |
| **Commands** | 可在对话中触发的命令文档 | **未包含** |
| **Hooks** | 基于事件的自动化脚本 | **未包含** |

也就是说：**当前聚焦「设计/接口协作 MCP」+「规格与交付类 Skills（迁移 / YApi / OpenSpec 契约）」**；若团队还需要统一代码规范，可在同一插件目录下补充 `rules/` 等，并在仓库内跑校验脚本确认格式无误。

---

## MCP 集成说明（`plugins/frontend-team-toolkit/mcp.json`）

插件通过 **`mcp.json`** 声明 Cursor 应加载的 MCP 服务。声明成功后，成员可在 **Settings → Features → Model Context Protocol** 中开关各服务。以下为当前三个服务的用途与典型用法。

### 1. `yapi-devloper-mcp`（YApi）

- **作用**：让 Agent 读取你们 YApi 上的接口列表与接口详情，用于联调、生成请求封装、对齐字段说明。
- **运行方式**：`npx` 拉起 `yapi-devloper-mcp`，stdio 传输。
- **环境变量（需在仓库占位符基础上改成真实值或使用本机覆盖配置）**：
  - `YAPI_BASE_URL`：YApi 站点根地址。
  - `YAPI_USERNAME` / `YAPI_PASSWORD`：用于登录 YApi 的账号凭证（具体权限以你们实例为准）。
- **常见 Tools（以当前 npm 包为准，名称可能随版本微调）**：
  - **`get_api_list`**：按分类等维度列出接口，便于从「分类链接」或项目维度批量浏览。
  - **`get_api_desc`**：按接口 ID 拉取 method、path、请求/响应结构等详情。
  - **`create_api` / `update_api`**：在具备权限时创建或更新接口定义（需谨慎使用，避免误改线上文档）。

配套 **Skill**「yapi-frontend-integration」会引导 Agent 优先用上述工具查文档再写前端代码。

### 2. `figma-developer-mcp`（Figma / Framelink 生态）

- **作用**：根据 Figma 文件链接拉取节点结构、布局与样式相关信息，便于对照设计稿实现 UI，减少「仅凭截图猜样式」的误差。
- **运行方式**：`npx` 拉起 `figma-developer-mcp`，stdio 传输。
- **鉴权**：需在配置中提供 **Figma Personal Access Token**（本仓库使用占位符 `YOUR_FIGMA_PERSONAL_ACCESS_TOKEN`，切勿提交真实 Token）。
- **常见 Tools**：
  - **`get_figma_data`**：输入 `fileKey`（及可选 `nodeId`）获取结构化设计数据。
  - **`download_figma_images`**：按需导出图像资源到允许的路径（具体参数以工具描述为准）。

使用前可在对话里粘贴 **Figma 文件/Frame 链接**，Agent 解析 `fileKey` / `node-id` 后调用 MCP。

### 3. `lanhu`（蓝湖）

- **作用**：通过 **HTTP MCP URL** 连接蓝湖侧提供的 MCP 端点，便于获取设计稿、标注或与蓝湖工作流相关的上下文（具体能力与蓝湖 MCP 服务版本一致）。
- **运行方式**：本仓库使用 **`url`** 字段指向 MCP 地址（示例为本地 `127.0.0.1:8000`，查询参数中的 `role`、`name` 需按你们环境修改）。
- **注意**：此类 URL 通常依赖 **本机或内网已启动的蓝湖 MCP 网关**；若链接不可用，请在 Cursor MCP 面板查看连接错误并按蓝湖文档排查。

---

## Skills（技能）说明

Skills 位于 `plugins/frontend-team-toolkit/skills/<skill-name>/SKILL.md`。Cursor 会根据描述的触发场景，在 **Agent Decides** 等模式下选用对应技能；也可在对话中使用 **`/` + 技能名** 手动唤起（以客户端实际展示为准）。

当前仓库包含 **10 个技能**（按功能分组）：

### 核心编排类

- **`ai-coding-tri-kit`** — OpenSpec + Superpowers + Agent Skills 三件套 8 步工程化工作流
- **`pm-md-to-openspec-pipeline`** — PM 需求 MD → Change Spec → OpenSpec 四文件编排
- **`change-spec-workflow`** — 切片 → 勘探 → Change Spec 三阶段

### 契约与验证类

- **`openspec-contract-authoring`** — OpenSpec 四文件契约化（field-matrix / design / spec / tasks）
- **`incremental-implementation`** — 锚定现有代码，增量迭代（禁止 greenfield 重建）
- **`code-verify`** — AI 辅助第三方开发五阶段防偏方法论

### 迁移与集成类

- **`vue2-to-vue3-migration`** — Vue 2 → Vue 3 两阶段迁移（登记 + 扫雷 + 就地升级）
- **`yapi-frontend-integration`** — YApi 接口对接与请求封装

### 内容质量类

- **`wechat-article-review`** — 微信公众号文章 0–10 分结构化评分与审稿
- **`skills-quality`** — 质量台账、eval 计划、发布门禁（内部治理）

详细说明见下文各技能章节。

### `ai-coding-tri-kit`

- **用途**：编排 **OpenSpec + Superpowers + Agent Skills 三件套** 8 步工程化工作流——需求不漂移、流程可控、质量可验。从 `/opsx:propose` 到 archive 全链路，强制「OpenSpec 先说清楚 → Superpowers 走对流程 → Agent Skills 守质量」顺序，不可跳跃（Lite 模式除外）。
- **核心护栏**：强度分层（Full/Standard/Lite）、前置环境检查、外部依赖可行性、闸门与回退、禁止 greenfield 重建、关键门槛落两层（AI skill + CI/pre-commit）。
- **附带文档**：`references/`（环境检查、外部依赖、workflow-matrix、intensity-tiers、gates-and-rollback、output-contract、fallback-scenarios）、`examples/`（Full/Standard 档位完整 walkthrough）。
- **典型触发**：「按三件套走一遍」「先对齐 spec 再开发」「AI 编程从碰运气变可复制」「`/opsx:propose` 到 archive」「防跳过 spec 直接写代码」「防不写测试」「防质量波动」。

### `openspec-contract-authoring`

- **用途（甲）**：把 **OpenSpec 四文件**（`field-matrix`、`spec`、`design`、`tasks`）写成**可验收契约**——字段矩阵、实现约束、Open Questions 闸门、Evidence；禁止「按图一致」代替矩阵。  
- **可选（乙）**：仅当用户明确要 **「按 OpenSpec / 按契约 / 按 field-matrix 落地代码」** 时，**改业务代码前**先核对 `tasks` 中 Gate（矩阵与设计定稿、OQ 关闭）。  
- **附带文档**：`reference.md`（目录树、四文件骨架、填空摘要、自检）。  
- **典型触发**：`openspec/changes`、`field-matrix`、`openspec validate`、契约化需求、防 AI 需求跑偏。

### `pm-md-to-openspec-pipeline`

- **用途**：**薄封装编排**——固定「PM/规格 MD → change-spec-workflow（阶段 A 1→2→3）→ 闸门 → openspec-contract-authoring（阶段 B 四文件）」顺序，缺输入只出待补充清单。支持 **Reconcile 编排**（源文档版本演进 R0~R7）与 **局部刷新护栏**（单文件刷新必输出未同步清单 + 风险）。
- **核心护栏**：禁止跳切片直接写 field-matrix；双根目录（specs/ ↔ openspec/changes/）版本号必须一致；步骤 2 强制输出易混淆模块对照表；Reconcile 闸门 R7 未闭合禁止宣称「已按 vN 定稿」。
- **附带文档**：`reference.md`（落盘路径、阶段 A/B 映射、子阶段模式、口令示例）、`BACKLOG.md`（迭代反馈）。
- **典型触发**：`pm-md-to-openspec-pipeline`、PM 需求转 OpenSpec、需求切片转契约、源文档 vN 重审 / reconcile、仅刷新某契约文件。

### `vue2-to-vue3-migration`

- **用途**：默认 **两阶段**——先 **一页纸登记**（`reference.md` §8）+ **易漏扫雷**（§10），再改业务源码；迁移前做 **`package.json`/构建/TS** 等工程就绪（§9）；用 **双重闸门** 与 **因果链** 保证行为可追溯。随后在 **行为等价** 前提下迁入 Vue 3（`<script setup>`、组合式 API、`v-model`/emit 等）；支持 **就地升级** 与 **隔离可拷贝包**。
- **附带文档**：`reference.md`（§1–§7 示例与 API 表，§8 模板，**§9 工程就绪展开 §10–§12 扫雷/校验/坑点完整版**）、`MIGRATION_BASELINE.md`（可选：增量 Git 基线）。
- **典型触发**：「Vue2 迁 Vue3」「先出迁移表再写代码」「防漏依赖」「对齐宿主构建与依赖版本」等。

### `incremental-implementation`

- **用途**：**「锚定现有代码，再做增量迭代」**——源文档 / 开发文档变更后，禁止 greenfield 全量重跑，只在已提交的旧代码上生成最小 diff（新增/修改/删除），未变项显式跳过并断言。通过 `实现映射.md` 把任务锚定到文件/函数；支持 **Reconcile 代码编排**（IC-R0~IC-R7，多产物共享版本号）与 **局部代码更新护栏**（未同步产物清单 + 风险）。
- **核心护栏**：禁止重建已有实现；git 基线先行；多产物版本对齐；缺对齐分析时停下或用户书面接受 tasks-diff 风险。
- **附带文档**：`reference.md`（实现映射模板、变更分类表、影响定位表、Reconcile 口令、局部更新模板）、`BACKLOG.md`、`test-prompts.json`、`results.tsv`。
- **典型触发**：源文档 vN 升版后改代码、需求二次/多次迭代、按 reconcile 结果落地代码（接力 pipeline R6）、按 vN 全链同步代码、仅改部分模块/文件、增量实现、锚定式代码迭代。

### `yapi-frontend-integration`

- **用途**：默认 **两阶段**——先输出 **接口摘要 + 拟生成路径/类型依据**（经确认再落盘）；通过 **`yapi-devloper-mcp`** 拉取 YApi 文档后，按项目请求基座实现封装与页面调用。  
- **附带文档**：`reference.md`（MCP 与字段说明、axios 映射、**TS/Schema**、排障、快速表、安全；**写回 YApi** 为非默认）。  
- **典型触发**：「对接接口」「联调」「请求封装」、粘贴 YApi 链接 / `apiId` / 接口名；**未说 YApi** 但需按契约对接后端同样适用。

### `wechat-article-review`

- **用途**：微信公众号文章 **0–10 分结构化评分**与改稿审稿。五维加权打分，每分附依据，禁止印象分；承诺一致性检查（未兑现承诺必进主要问题）。≥9.0 通过，<9.0 不通过且必须输出按 P0/P1/P2 排序的可执行修改清单与复评目标。
- **核心护栏**：合规/敏感风险直接不通过；总分 8.5–8.9 标「接近达标」但仍为 ❌；用户要求「只给总分」仍须输出维度表。
- **附带文档**：`references/scoring-rubric.md`（评分细则、稿件类型分流）、`references/output-contract.md`（输出契约）、`scripts/validate-output.sh`（结构校验）、`reviews/`（持久化目录）。
- **典型触发**：「打分」「评分」「评审」「审稿」「改稿反馈」「是否通过」「重写」「复评」「文章质量把关」「看看这篇能不能发」「帮我审一下稿子」。

### `change-spec-workflow`

- **用途**：默认 **三阶段**（切片 → 勘探 → Change Spec），产出 **实操记录** 与 **变更规格八块**；按仓库 `openspec` 布局落盘（`specs/<change-id>/`）。  
- **附带文档**：`reference.md`（三阶段详细、勘探 checklist、Change Spec 八块对照表、落盘路径）。  
- **典型触发**：「切片」「勘探」「Change Spec」「先切片再写契约」「易漏点」「易混淆模块」「步骤 1→2→3」。

### `code-verify`

- **哲学**：**先锚定，再迭代** — AI 辅助第三方开发的全链路防偏方法论（文章/案例仅为举例，非技能边界）。
- **五阶段**：① 方案锚定 → ② 双锚验证（官方文档 + 参考实现 + 七维引擎）→ ③ 小步 MVU → ④ 止损换策 → ⑤ 检查清单沉淀。
- **附带文档**：`templates/report-template.md`、`templates/checklist-template.md`、`validate.sh`。
- **典型触发**：不熟悉 SDK/API、AI 方案/代码可能从第一步就错、防盲目迭代、code-verify。

---

## 仓库结构

```text
frontend-team-marketplace/
├── .cursor-plugin/
│   └── marketplace.json          # Team Marketplace 总清单（插件注册表）
├── plugins/
│   └── frontend-team-toolkit/
│       ├── .cursor-plugin/
│       │   └── plugin.json       # 单个插件元数据
│       ├── mcp.json              # 三个 MCP 的定义（占位符需替换）
│       ├── skills/
│       │   ├── ai-coding-tri-kit/          # 三件套 8 步工程化工作流
│       │   ├── pm-md-to-openspec-pipeline/ # PM MD → OpenSpec 编排
│       │   ├── change-spec-workflow/       # 切片 → 勘探 → Change Spec
│       │   ├── openspec-contract-authoring/ # 四文件契约化
│       │   ├── incremental-implementation/ # 增量实现（禁止重建）
│       │   ├── vue2-to-vue3-migration/     # Vue 2 → Vue 3 迁移
│       │   ├── yapi-frontend-integration/  # YApi 接口对接
│       │   ├── wechat-article-review/      # 公众号文章评分审稿
│       │   ├── code-verify/                # 第三方开发防偏方法论
│       │   └── skills-quality/             # 质量台账、eval 计划、发布门禁
│       ├── skill-engineering/    # Skill 创建模板、Schema、结构校验
│       └── README.md             # 插件级说明（密钥与 MCP 细节）
├── scripts/
│   └── validate-template.mjs     # manifest / frontmatter 校验
└── README.md                     # 本文件
```

---

## 团队管理员：导入 Marketplace

1. 将本仓库推送到组织 GitHub（默认分支一般为 `main`）。
2. Cursor Dashboard → **Settings → Plugins → Team Marketplaces** → **Import**。
3. 粘贴仓库 URL，按组分配 **Required**（全员强制安装）或 **Optional**（自选安装）。

## 团队成员：安装后与密钥

1. 在 Cursor **Marketplace / Plugins** 面板中安装 **Frontend Team Toolkit**（若管理员设为 Required 则可能自动生效）。
2. 打开 **Settings → MCP**，确认三个服务已列出；将 **YApi / Figma / 蓝湖 URL** 等替换为真实配置。
3. **切勿**将 Token、密码写入 Git；可选做法包括：每人本机 MCP 覆盖、组织密钥管理方案、或 CI 仅校验结构不提交机密。

---

## 本地校验

```bash
cd frontend-team-marketplace && node scripts/validate-template.mjs
```

## 新建与校验 Skill

团队 Skill 工程化脚手架位于 `plugins/frontend-team-toolkit/skill-engineering/`：

```bash
# 创建新 Skill
./plugins/frontend-team-toolkit/skill-engineering/bin/new-skill.sh my-skill-name

# 校验 Skill 目录结构
python3 plugins/frontend-team-toolkit/skill-engineering/bin/validate-skill.py \
  plugins/frontend-team-toolkit/skills/my-skill-name
```

升级与回归流程见 `plugins/frontend-team-toolkit/skills/skills-quality/`。

---

## 参考

- [Cursor Plugins 文档](https://cursor.com/docs/plugins)
- [Cursor Plugins 参考（manifest、组件格式）](https://cursor.com/docs/reference/plugins)
- 工作区内另有 **`cursor-team-marketplace-template-main`** 可作多插件、hooks、rules 等扩展参考。
