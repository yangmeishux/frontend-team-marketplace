#!/bin/bash
# Code Verify Skill v2.0 — 全链路锚定验证骨架生成
# 用法: bash validate.sh --tool "工具名" [--code "代码"] [--code-file path] [--lang 语言] [--doc-url URL] [--ref-url URL] [--output path]

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

TOOL_NAME=""
CODE_CONTENT=""
LANG=""
DOC_URL=""
REF_URL=""
OUTPUT=""
PHASE="双锚验证"

while [[ $# -gt 0 ]]; do
  case $1 in
    --tool)
      TOOL_NAME="$2"
      shift 2
      ;;
    --code)
      CODE_CONTENT="$2"
      shift 2
      ;;
    --code-file)
      if [[ -f "$2" ]]; then
        CODE_CONTENT=$(cat "$2")
      else
        echo "❌ 文件不存在: $2"
        exit 1
      fi
      shift 2
      ;;
    --lang)
      LANG="$2"
      shift 2
      ;;
    --doc-url)
      DOC_URL="$2"
      shift 2
      ;;
    --ref-url)
      REF_URL="$2"
      shift 2
      ;;
    --phase)
      PHASE="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --help)
      echo "Code Verify Skill v2.0 — 先锚定，再迭代"
      echo ""
      echo "用法:"
      echo "  bash validate.sh --tool \"工具名\" [选项]"
      echo ""
      echo "必填:"
      echo "  --tool       工具名称"
      echo ""
      echo "可选:"
      echo "  --code         待验证代码/方案（直接传入）"
      echo "  --code-file    待验证文件路径"
      echo "  --lang         编程语言（语法检查用）"
      echo "  --doc-url      官方文档 URL"
      echo "  --ref-url      参考实现 URL"
      echo "  --phase        当前阶段：方案锚定|双锚验证|小步验证|联调受阻"
      echo "  --output       输出路径（默认 stdout）"
      echo ""
      echo "哲学: 五阶段（方案→双锚→小步→止损→清单）+ 七维引擎"
      exit 0
      ;;
    *)
      echo "❌ 未知参数: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$TOOL_NAME" ]]; then
  echo "❌ 缺少 --tool"
  exit 1
fi

if [[ -z "$OUTPUT" ]]; then
  OUTPUT="/dev/stdout"
fi

CODE_BLOCK=""
if [[ -n "$CODE_CONTENT" ]]; then
  CODE_BLOCK="## 待验证内容

\`\`\`${LANG:-text}
${CODE_CONTENT}
\`\`\`"
else
  CODE_BLOCK="## 待验证内容

（未提供 --code / --code-file；若处于阶段 1，请粘贴 AI 方案）"
fi

REPORT_FILE=$(mktemp)

cat > "$REPORT_FILE" << EOF
# 📋 锚定验证报告：${TOOL_NAME}

**工具**: ${TOOL_NAME}
**验证时间**: $(date '+%Y-%m-%d %H:%M')
**当前阶段**: ${PHASE}
**编程语言**: ${LANG:-未指定}
**官方文档**: ${DOC_URL:-待搜索}
**参考实现**: ${REF_URL:-待搜索}

---

${CODE_BLOCK}

---

## Agent 执行清单（见 SKILL.md）

### 阶段 1 方案锚定
- [ ] 方案含官方文档链接
- [ ] AI 已标注不确定部分
- [ ] 调用顺序与文档章节可对应

### 阶段 2 双锚验证（七维 + 参考实现）
- [ ] 文档锚：维度 1–6 逐项验证
- [ ] 维度 7 语法检查${LANG:+（语言: ${LANG}）}
- [ ] 实现锚：至少 1 份参考实现对比

### 阶段 3 小步验证
- [ ] MVU 按文档章节顺序拆分
- [ ] 进度表已填写

### 阶段 4 止损
- [ ] 时间盒与置信度闸门已评估
- [ ] ≤4/7 或超时 → 建议换策略

### 阶段 5 经验沉淀
- [ ] 提示更新 templates/checklist-template.md

---

## 七维结果（待 Agent 填写）

| 维度 | 结果 | 详情 |
|------|------|------|
| 📄 文档存在性 | ⏳ | |
| 🔑 API 签名 | ⏳ | |
| 🔐 认证方式 | ⏳ | |
| 📦 依赖包 | ⏳ | |
| 🏗️ 初始化顺序 | ⏳ | |
| 🔄 版本兼容 | ⏳ | |
| ⚡ 语法检查 | ⏳ | |

**置信度**: 0/7 (0%)

---

*骨架由 Code Verify Skill v2.0.0 生成 — 完整模板见 templates/report-template.md*
EOF

if [[ "$OUTPUT" == "/dev/stdout" ]]; then
  cat "$REPORT_FILE"
else
  cp "$REPORT_FILE" "$OUTPUT"
  echo "✅ 报告骨架已生成: $OUTPUT"
fi

rm -f "$REPORT_FILE"
