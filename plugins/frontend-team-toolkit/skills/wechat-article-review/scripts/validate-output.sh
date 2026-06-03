#!/usr/bin/env bash
# Structural checks for wechat-article-review report (stdin or file).
set -euo pipefail

INPUT="${1:-}"
if [[ -n "${INPUT}" && -f "${INPUT}" ]]; then
  TEXT="$(cat "${INPUT}")"
else
  TEXT="$(cat)"
fi

fail=0
check() {
  local label="$1"
  local pattern="$2"
  if ! echo "${TEXT}" | grep -Eq "${pattern}"; then
    echo "FAIL: ${label}" >&2
    fail=1
  fi
}

# Conclusion line
if echo "${TEXT}" | grep -q "BLOCKED"; then
  check "blocked asks for input" "(正文|路径|提供|粘贴)"
  [[ ${fail} -eq 0 ]] && echo "PASS: validate-output.sh (BLOCKED)"
  exit "${fail}"
fi

check "has score conclusion" "(通过|不通过|✅|❌).*[0-9]+(\.[0-9]+)?.*(/10|分)"
check "has dimension table or 维度" "(维度|主题与价值|干货密度)"
check "has weighted or 综合评分" "(综合评分|加权|总分)"

if echo "${TEXT}" | grep -qE "不通过|❌"; then
  check "fail report has issues or 问题" "(主要问题|修改清单|P0|修改建议)"
  check "fail report has checklist" "(\- \[ \]|修改清单|TODO)"
fi

if [[ ${fail} -eq 0 ]]; then
  echo "PASS: validate-output.sh"
  exit 0
fi
exit 1
