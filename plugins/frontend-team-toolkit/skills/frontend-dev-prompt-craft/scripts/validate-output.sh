#!/usr/bin/env bash
# Optional deterministic checks on skill output (stdin or file path).
# Extend with grep/rg rules as evals mature.
set -euo pipefail

INPUT="${1:-}"
TEXT=""

if [[ -n "${INPUT}" && -f "${INPUT}" ]]; then
  TEXT="$(cat "${INPUT}")"
elif [[ -n "${INPUT}" ]]; then
  TEXT="${INPUT}"
else
  TEXT="$(cat)"
fi

fail=0

check_contains() {
  local label="$1"
  local needle="$2"
  if ! echo "${TEXT}" | grep -qi "${needle}"; then
    echo "FAIL: missing ${label} (expected substring: ${needle})" >&2
    fail=1
  fi
}

# TODO: replace with skill-specific rules from evals/evals.json
check_contains "Summary section" "## Summary"

if [[ ${fail} -eq 0 ]]; then
  echo "PASS: validate-output.sh"
  exit 0
fi
exit 1
