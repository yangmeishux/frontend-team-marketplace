# Output Contract — {{SKILL_NAME}}

本文件定义本 Skill 的 **交付物格式**。Agent 在 Workflow 步骤 2 必须 Read 本文件。

## 必交付节（Must Have）

1. **Summary** — 1–3 句说明完成了什么
2. **Main Output** — TODO：主交付内容结构（章节/字段）
3. **Assumptions & Gaps** — 做了哪些假设；仍有哪些 TBD
4. **Next Steps** — 用户可选的后续动作（如有）

## 禁止（Must NOT）

- 不得编造未提供的文件路径、API、数据
- 不得在未过 Checkpoint 时宣称「已完成/可发布」
- TODO：本 skill 特有的禁止项

## 格式示例

```markdown
## Summary
...

## Main Output
...

## Assumptions & Gaps
- Assumption: ...
- TBD: ...

## Next Steps
- ...
```

## 与 Eval 对齐

| eval id | 本契约中对应的检查点 |
|---------|---------------------|
| {{SKILL_NAME}}-001 | happy path 输出结构 |
| {{SKILL_NAME}}-002 | 缺输入时必须出现在 Assumptions / 追问 |
| {{SKILL_NAME}}-003 | 边界场景的处理说明 |
