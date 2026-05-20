#!/bin/bash
# Code Verify Skill - 主入口脚本
# 用法: bash validate.sh --tool "工具名" --code "代码内容" [--lang 语言] [--doc-url URL]

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
REPORT_TEMPLATE="$SKILL_DIR/templates/report-template.md"

# 解析参数
TOOL_NAME=""
CODE_CONTENT=""
LANG=""
DOC_URL=""
OUTPUT=""

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
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --help)
      echo "Code Verify Skill - 第三方工具代码验证器"
      echo ""
      echo "用法:"
      echo "  bash validate.sh --tool \"工具名\" --code \"代码内容\" [--lang 语言] [--doc-url URL] [--output 输出路径]"
      echo ""
      echo "参数:"
      echo "  --tool       工具名称（必填）"
      echo "  --code       代码内容（直接传入）"
      echo "  --code-file  代码文件路径（与 --code 二选一）"
      echo "  --lang       编程语言（可选，用于语法检查）"
      echo "  --doc-url    官方文档 URL（可选，已知时提供可加速）"
      echo "  --output     输出路径（可选，默认输出到终端）"
      echo ""
      echo "示例:"
      echo '  bash validate.sh --tool "企业微信 JS-SDK" --code "wx.config({...})" --lang javascript'
      echo '  bash validate.sh --tool "Stripe API" --code-file code.js --lang javascript --output report.md'
      exit 0
      ;;
    *)
      echo "❌ 未知参数: $1"
      echo "运行 'bash validate.sh --help' 查看帮助"
      exit 1
      ;;
  esac
done

# 检查必填参数
if [[ -z "$TOOL_NAME" ]]; then
  echo "❌ 缺少必填参数: --tool"
  echo "运行 'bash validate.sh --help' 查看帮助"
  exit 1
fi

if [[ -z "$CODE_CONTENT" ]]; then
  echo "❌ 缺少必填参数: --code 或 --code-file"
  echo "运行 'bash validate.sh --help' 查看帮助"
  exit 1
fi

# 输出配置
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="/dev/stdout"
fi

# 生成报告
REPORT_FILE=$(mktemp)

cat > "$REPORT_FILE" << EOF
# 📋 验证报告：${TOOL_NAME}

**工具**: ${TOOL_NAME}
**验证时间**: $(date '+%Y-%m-%d %H:%M')
**编程语言**: ${LANG:-未指定}

---

## 📋 待验证代码

\`\`\`${LANG:-text}
${CODE_CONTENT}
\`\`\`

---

## 📋 验证步骤

请按照以下流程执行验证（由 AI Agent 完成）：

### 步骤 1: 搜索官方文档
- 搜索关键词: \`${TOOL_NAME} official documentation API reference\`
- 如果提供了 --doc-url: 直接使用 ${DOC_URL}

### 步骤 2: 提取文档关键信息
- API 参考页 URL
- 快速开始页 URL
- 认证说明页 URL
- 安装/依赖说明 URL

### 步骤 3: 逐项验证（7 个维度）

#### 维度 1: 📄 文档存在性
- [ ] AI 引用的文档链接是否可访问
- [ ] 页面标题是否匹配工具名称
- [ ] 是否为官方文档

#### 维度 2: 🔑 API 签名对比
- [ ] API 方法名称是否一致
- [ ] 参数数量和名称是否匹配
- [ ] 参数类型是否匹配
- [ ] 返回值处理是否正确

#### 维度 3: 🔐 认证方式
- [ ] 认证类型是否一致
- [ ] 参数名称是否正确
- [ ] 流程步骤是否完整

#### 维度 4: 📦 依赖包检查
- [ ] 包是否存在
- [ ] 版本号是否正确
- [ ] 安装命令是否正确

#### 维度 5: 🏗️ 初始化顺序
- [ ] 初始化是否在调用之前
- [ ] 配置项是否完整
- [ ] 调用顺序是否正确

#### 维度 6: 🔄 版本兼容性
- [ ] 使用的 API 在当前版本是否可用
- [ ] 是否使用了已废弃的 API
- [ ] SDK 版本是否匹配

#### 维度 7: ⚡ 语法检查
$(if [[ -n "$LANG" ]]; then
  case "$LANG" in
    javascript|js)
      echo "- [ ] 运行: node --check <code>"
      ;;
    typescript|ts)
      echo "- [ ] 运行: npx tsc --noEmit <code>"
      ;;
    python|py)
      echo "- [ ] 运行: python3 -m py_compile <code>"
      ;;
    go)
      echo "- [ ] 运行: go vet <code>"
      ;;
    java)
      echo "- [ ] 运行: javac -d /tmp <code>"
      ;;
    *)
      echo "- [ ] 运行: 对应语言的语法检查器"
      ;;
  esac
else
  echo "- [ ] 未指定语言，跳过语法检查"
fi)

---

## 📊 验证结果

| 维度 | 结果 | 详情 |
|------|------|------|
| 📄 文档存在性 | ⏳ 待验证 | - |
| 🔑 API 签名对比 | ⏳ 待验证 | - |
| 🔐 认证方式 | ⏳ 待验证 | - |
| 📦 依赖包检查 | ⏳ 待验证 | - |
| 🏗️ 初始化顺序 | ⏳ 待验证 | - |
| 🔄 版本兼容性 | ⏳ 待验证 | - |
| ⚡ 语法检查 | ⏳ 待验证 | - |

---

## 📌 结论

**置信度**: 0/7 (0%)  
**状态**: ⏳ 待验证

---

*验证由 Code Verify Skill v1.0.0 生成*
EOF

# 输出报告
if [[ "$OUTPUT" == "/dev/stdout" ]]; then
  cat "$REPORT_FILE"
else
  cp "$REPORT_FILE" "$OUTPUT"
  echo "✅ 验证报告已生成: $OUTPUT"
fi

# 清理
rm -f "$REPORT_FILE"
