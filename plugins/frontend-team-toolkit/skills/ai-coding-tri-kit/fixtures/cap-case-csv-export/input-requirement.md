# 产品需求：Dashboard CSV 导出

| 字段 | 内容 |
|------|------|
| 模块 | React Dashboard 数据表格 |
| 功能 | 将用户选中的行导出为 CSV 文件并触发浏览器下载 |
| 优先级 | 中 |
| 前置条件 | 用户在 Dashboard 页面，表格支持行选择（checkbox） |
| 需求 1 | 用户选中若干行后点击「导出 CSV」，浏览器下载 CSV，仅含选中行 |
| 需求 2 | 未选中任何行时点击导出，显示 Toast「请先选择要导出的数据」，不触发下载 |
| 需求 3 | 导出超过 10000 条时显示进度条，避免 UI 冻结 |
| 约束 | 技术栈 React + TypeScript；不引入服务端导出（首版纯前端） |
| 未说明 | CSV 编码（Excel 兼容？）、字段是否可配置、特殊字符转义规则 |

**Eval 用途**：capability-004 Step 1 真落盘 — Agent 应生成 `feat-dashboard-csv-export` 四件套并通过 `openspec validate`。
