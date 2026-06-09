# 前端开发提示词模板库

> 基于真实工作场景提炼的 8 类提示词模板。  
> 使用时将 `{{占位符}}` 替换为实际值。

---

## PAGE — 页面功能开发

### 模板 P1：新增独立页面

```
当前项目需要新增一个独立页面，具体信息如下：

1. 页面路由：{{route_path}}，页面权限标识：{{permission_code}}
2. 页面结构分为 {{N}} 部分：
   - {{section_1_desc}}
   - {{section_2_desc}}
   - {{section_3_desc}}
3. 筛选区域：{{filter_fields_desc}}
4. 列表数据调用接口：{{list_api_url}}，支持分页
5. 操作按钮：{{action_buttons_desc}}

技术约束：
- 组件库使用 {{component_lib}}（vant / Element UI / 自研）
- 接口可以先使用 mock 数据
- 参考已有页面：{{reference_page_path}}

请根据上述要求进行页面开发。
```

### 模板 P2：现有页面新增功能

```
当前页面新增如下功能：

1. 在 {{location_desc}} 区域中，新增 {{feature_name}}
2. 交互描述：{{interaction_desc}}
3. 点击之后的行为：{{click_behavior}}
4. 数据来源：{{data_source}}

补充说明：
- {{extra_notes}}

请根据上述要求新增功能。
```

### 模板 P3：列表页 + 筛选 + 轮询

```
当前页面是一个列表查询页面，结构如下：

1. 上部分筛选区域：
   - {{filter_field_1}}：{{filter_desc_1}}
   - {{filter_field_2}}：{{filter_desc_2}}
   - 操作按钮：查询、重置、导出

2. 下部分列表展示：
   - 接口地址：{{list_api_url}}
   - 列表字段：{{table_columns_desc}}
   - 支持分页

3. 特殊逻辑：
   - {{special_logic_desc}}（如轮询、状态更新等）

请根据上述要求开发页面。
```

### 模板 P4：多页面批量新增查询条件

```
当前项目中，以下页面路由对应的都是列表查询页面，都有搜索查询区域：

{{route_list}}

需要在所有上述页面的搜索查询区域最后面，新增查询条件：
- 名称：{{field_name}}
- 类型：下拉选择（单选/多选）
- 可选项：{{options}}
- 字段名：{{field_key}}
- 数据枚举：{{enum_mapping}}
- 默认值：{{default_value}}

要求：
- 抽取为独立公共组件，嵌入所有页面，方便后续维护
- 公共组件路径：{{component_path}}
- 如果接口返回的字段不存在或为空，展示为「无」

请根据上述要求新增查询选项。
```

---

## UI — UI 还原

### 模板 U1：从设计稿/描述还原页面

```
这是一个 {{page_type}} 的网页，页面需要 {{layout_constraint}}。

页面布局描述如下：
1. {{layout_section_1}}
2. {{layout_section_2}}
3. {{layout_section_3}}

图片/静态资源：
- {{resource_desc_1}}：{{resource_url_1}}
- {{resource_desc_2}}：{{resource_url_2}}

技术约束：
- 使用 {{component_lib}} 组件库
- {{animation_desc}}（动画效果描述）

请根据上述信息还原页面。
```

### 模板 U2：动画/滚动效果开发

```
需求功能描述如下：

1. {{scroll_area_desc}}，最多 {{max_items}} 条数据
2. 页面可视区域展示 {{visible_count}} 条数据
3. 每间隔 {{interval}} 秒，整体往上移动 1 条数据的高度
4. 滚动动画效果：{{animation_detail}}（如平滑滑动、逐条切换）
5. 移动到末尾时：{{loop_strategy}}（重新请求接口 / 从头循环）
6. 多个滚动区域之间：{{independence}}（独立滚动 / 联动）

请根据上述要求实现滚动效果。
```

### 模板 U3：浮层/弹窗组件

```
当前需求描述如下：

1. 触发条件：{{trigger_desc}}
2. 浮层类型：{{popup_type}}（半屏浮层 / 全屏弹窗 / 侧边抽屉）
3. 浮层组件库：使用 {{component_lib}}
4. 浮层内容：{{content_desc}}
5. 浮层交互：
   - {{interaction_1}}
   - {{interaction_2}}
6. 底部按钮：{{button_desc}}（固定悬浮、数字变动）
7. 确认后的行为：{{confirm_behavior}}

请根据上述要求进行页面设计还原与功能添加。
```

---

## API — 接口对接

### 模板 A1：标准接口对接

```
调用接口：{{api_url}}

接口传参说明：
- {{param_1}}：{{param_desc_1}}
- {{param_2}}：{{param_desc_2}}
- {{param_3}}：不需要传递（由后端自动生成）

接口返回之后的逻辑：
1. {{response_handling_1}}
2. {{response_handling_2}}
3. 将返回数据缓存，缓存 key 为 {{cache_key_desc}}

错误处理：
- {{error_handling_desc}}

请根据上述要求对接接口。
```

### 模板 A2：Yapi MCP 接口对接

```
接口文档地址：{{yapi_url}}，使用 MCP 工具获取接口信息。

接口传参说明：
- {{param_override_desc}}（覆盖 MCP 获取的默认参数）

接口返回数据说明：
- {{response_structure_desc}}

前端处理逻辑：
1. {{processing_step_1}}
2. {{processing_step_2}}

请根据上述要求对接接口。
```

### 模板 A3：多接口联动 + 条件调用

```
接口调用逻辑如下：

1. 先调用接口 A：{{api_a_url}}，获取 {{data_a}}
2. 根据接口 A 的返回，判断：
   - 如果 {{condition_1}}，则调用接口 B：{{api_b_url}}
   - 否则调用接口 C：{{api_c_url}}
3. 最终将数据 {{merge_strategy}}（合并 / 更新 / 替换）

缓存策略：以 {{cache_keys}} 为缓存名称保存数据。

请根据上述要求实现接口联动逻辑。
```

---

## ARCH — 技术方案设计

### 模板 AR1：架构方案设计

```
之前功能描述：
{{current_implementation_desc}}

现在新的需求：
{{new_requirement_desc}}

现在的问题是：
{{problem_desc}}（如：多处调用、维护困难、兼容性问题）

请先帮我提供一份合理的技术方案，要求：
1. 考虑 {{constraint_1}}（如复用性、兼容性）
2. 考虑 {{constraint_2}}（如维护成本、迁移风险）
3. 给出具体的改造步骤
```

### 模板 AR2：第三方集成方案

```
当前项目中 {{feature_name}} 的流程是：
1. {{step_1}}
2. {{step_2}}
3. {{step_3}}

现在需要集成第三方 {{third_party_name}}，变更点：
- {{change_1}}
- {{change_2}}

约束条件：
- {{constraint_desc}}（如：其他项目也需要复用、需要支持回调）

请提供集成方案，包括：流程设计、接口设计、异常处理。
```

---

## REFACTOR — 批量重构

### 模板 R1：域名/配置批量替换

```
需求名称：{{project_name}}

需求简介：
需要对当前项目进行改造，核心要求：
1. 新建分支 {{branch_name}}，新增构建命令 {{build_command}}
2. {{change_type}} 替换规则：
   - {{old_value_1}} → {{new_value_1}}
   - {{old_value_2}} → {{new_value_2}}
3. {{brand_change_desc}}（品牌文案/LOGO 替换）
4. 例外：{{exceptions}}（如 CDN、OSS 不修改）

补充规则：
- {{supplementary_rules}}

建议把项目中的 {{target_pattern}} 抽取成变量，避免散落硬编码。
```

### 模板 R2：多项目批量扫描

```
依次查看项目：{{project_list}}

需求描述：
1. 扫描这些项目中的 {{file_type}} 文件，帮我罗列 {{scan_target}}
2. 以项目为标识，对结果进行去重
3. {{grouping_strategy}}（如：按域名分组、按类型分组）

输出要求：
- 以 {{output_format}} 格式保存
- 以项目名称依次展示结果
```

### 模板 R3：多项目批量变更

```
依次查看项目：{{project_list}}

需求声明：如果当前分支不是 {{branch_name}}，先切换到该分支。

需求描述：
{{change_description}}

请根据上述要求，对项目进行逐一调整与开发。
开发完成之后，将改动提交到远端的 {{branch_name}} 分支。
提交信息前缀：{{commit_prefix}}
```

---

## DEBUG — Bug 调试

### 模板 D1：页面逻辑异常

```
当前问题描述：

预期行为：{{expected_behavior}}
实际行为：{{actual_behavior}}

相关页面/URL：{{page_url}}
相关方法/文件：{{method_or_file}}

日志信息：
{{log_output}}

请定位问题并修复。
```

### 模板 D2：子应用/微前端问题

```
当前遇到的问题：

页面路由：{{route_path}}
子应用名称：{{sub_app_name}}

问题现象：{{symptom_desc}}（如：子应用能看到但反复刷新）
登录体系说明：{{auth_system_desc}}

当前排查进展：{{investigation_status}}

请找下问题并修复。先不考虑 {{deferred_concern}}，先把流程跑通。
```

### 模板 D3：回调/跳转未触发

```
开始页面：{{start_url}}

操作流程：
1. 从开始页面跳转到 {{target_page}}
2. 在 {{target_page}} 完成操作后，回调地址为：{{callback_url}}
3. 回调地址中的关键参数：{{callback_params}}

当前问题：
跳转到 {{return_url}} 之后，{{problem_desc}}（如：未执行 handleXxx 方法）

日志打印：
- nextUrl：{{next_url}}
- returnUrl：{{return_url}}

请定位为何回调未触发并修复。
```

---

## PRD — 需求分析迭代

### 模板 PR1：PRD 转开发文档

```
@{{skill_name}} @{{prd_file_path}}

请读取需求文档，按 {{pipeline_name}} 执行阶段分析：
1. 需求功能拆分与切片
2. 先告知我你理解的需求，在当前项目中具体有哪些改动与新增
3. 生成开发文档

只关注以下板块：{{focus_areas}}
```

### 模板 PR2：需求变更差异分析

```
@{{skill_name}} @{{new_prd_path}}

之前的需求开发文档在 {{existing_doc_path}} 中。
需求文档已更新，请按 {{pipeline_name}} 执行阶段：

1. 对比之前的需求与现在新的需求文档之间的差异
2. 对新增/改动/优化的功能进行拆分与切片
3. 先告知我你理解的需求变更点
4. 在当前项目已有功能基础上进行增量分析

注意：不要全量重新生成，需要在现有功能基础上识别变更。
```

### 模板 PR3：增量迭代开发策略

```
我最近的工作流是：读取 PRD → OpenSpec 生成文档 → 编码开发。

当前问题：PRD 更新了，如果全量重新跑，相同文档生成的代码完全不同。

我的诉求：
1. 需求变更后，代码应在之前基础上迭代，而非全量重写
2. 多次迭代时，保留历史开发的上下文
3. 即使生成全新的开发文档，代码也要基于之前版本二次迭代

请帮我制定增量迭代开发策略，包括：
- 如何保存开发上下文（commit 记录 / 开发文档快照）
- 如何让 AI 在已有代码基础上增量开发
- 需求变更时的最佳操作流程
```

### 模板 PR4：接口文档对接开发文档

```
看下 {{feature_name}} 的需求，以及之前新增的功能与代码。

接口文档：
- {{api_url_1}}
- {{api_url_2}}

使用 MCP 获取接口文档信息，再新增一份接口文档对接的开发文档。

补充说明：
- {{override_1}}（如：某字段前端不传）
- {{override_2}}（如：某接口遗漏，先不对接）

结合上述，更新开发对接文档。
```

---

## MIGRATE — 组件迁移

### 模板 M1：跨项目组件迁移

```
在当前项目新增一个独立的页面，页面结构如下：
- {{page_structure_desc}}

列表展示的功能与另一个项目 {{source_project}} 中的组件 {{component_name}} 一致。

要求：
1. 将该组件完整拷贝到当前项目中
2. 组件涉及的所有资源依赖也需搬过去
3. 将依赖资源与组件放在一个文件夹下，方便后续维护
4. 目标路径：{{target_path}}

请完成组件迁移。
```

### 模板 M2：依赖替换/升级

```
移除 {{old_dependency}} 相关依赖和用法。
用 {{new_dependency}} 替代（功能类似，支持 {{compatibility_note}}）。
重新安装依赖。

涉及的配置文件：{{config_files}}
```

### 模板 M3：批量依赖更新

```
依次查看项目：{{project_list}}

对每个项目：
1. 切换到 {{branch_name}} 分支
2. 查看 package.json，将 {{package_name}} 更新成 {{target_version}}
3. 将改动提交到远端分支

提交信息：{{commit_message}}
```
