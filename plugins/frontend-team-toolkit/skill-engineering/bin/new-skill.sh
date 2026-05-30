#!/usr/bin/env bash
# Generate a new industrial-grade Skill directory from template.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINEERING_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TOOLKIT_ROOT="$(cd "${ENGINEERING_ROOT}/.." && pwd)"
REPO_ROOT="$(cd "${TOOLKIT_ROOT}/../.." && pwd)"
TEMPLATE_DIR="${ENGINEERING_ROOT}/templates/new-skill"
DEFAULT_SKILLS_DIR="${TOOLKIT_ROOT}/skills"

usage() {
  cat <<'EOF'
Usage: new-skill.sh <skill-name> [--path OUTPUT_DIR]

Create a new Skill directory from the skill-engineering template.

Arguments:
  skill-name    kebab-case identifier (e.g. api-contract-review)

Options:
  --path DIR    Output parent directory (default: plugins/frontend-team-toolkit/skills)

Examples:
  ./plugins/frontend-team-toolkit/skill-engineering/bin/new-skill.sh my-skill
  ./plugins/frontend-team-toolkit/skill-engineering/bin/new-skill.sh my-skill --path ~/.cursor/skills
EOF
}

SKILL_NAME=""
OUTPUT_PARENT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path)
      OUTPUT_PARENT="${2:?--path requires a directory}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ -z "${SKILL_NAME}" ]]; then
        SKILL_NAME="$1"
      else
        echo "Unexpected argument: $1" >&2
        usage >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "${SKILL_NAME}" ]]; then
  usage >&2
  exit 1
fi

if [[ ! "${SKILL_NAME}" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Error: skill-name must be kebab-case (lowercase, digits, hyphens): ${SKILL_NAME}" >&2
  exit 1
fi

if [[ -z "${OUTPUT_PARENT}" ]]; then
  OUTPUT_PARENT="${DEFAULT_SKILLS_DIR}"
fi

if [[ ! -d "${TEMPLATE_DIR}" ]]; then
  echo "Error: template not found at ${TEMPLATE_DIR}" >&2
  exit 1
fi

mkdir -p "${OUTPUT_PARENT}"
TARGET_DIR="$(cd "${OUTPUT_PARENT}" && pwd)/${SKILL_NAME}"

if [[ -e "${TARGET_DIR}" ]]; then
  echo "Error: target already exists: ${TARGET_DIR}" >&2
  exit 1
fi

DATE_ISO="$(date -u +"%Y-%m-%d")"
DATE_TIME="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
TITLE="$(echo "${SKILL_NAME}" | sed -E 's/(^|-)([a-z])/\U\2/g' | sed 's/-/ /g')"

copy_template() {
  local src="$1"
  local dest="$2"
  sed \
    -e "s/{{SKILL_NAME}}/${SKILL_NAME}/g" \
    -e "s/{{SKILL_TITLE}}/${TITLE}/g" \
    -e "s/{{DATE_ISO}}/${DATE_ISO}/g" \
    -e "s/{{DATE_TIME}}/${DATE_TIME}/g" \
    "${src}" > "${dest}"
}

mkdir -p "${TARGET_DIR}/evals" "${TARGET_DIR}/references" "${TARGET_DIR}/scripts"

for f in SKILL.md CHANGELOG.md .skill-meta.json test-prompts.json results.tsv skill-issues.jsonl.example; do
  copy_template "${TEMPLATE_DIR}/${f}" "${TARGET_DIR}/${f}"
done

copy_template "${TEMPLATE_DIR}/evals/evals.json" "${TARGET_DIR}/evals/evals.json"
copy_template "${TEMPLATE_DIR}/references/output-contract.md" "${TARGET_DIR}/references/output-contract.md"
copy_template "${TEMPLATE_DIR}/scripts/validate-output.sh" "${TARGET_DIR}/scripts/validate-output.sh"
chmod +x "${TARGET_DIR}/scripts/validate-output.sh" 2>/dev/null || true

echo "Created skill at: ${TARGET_DIR}"
echo ""
echo "Next steps:"
echo "  1. Edit ${TARGET_DIR}/SKILL.md (description + workflow)"
echo "  2. Add eval cases in ${TARGET_DIR}/evals/evals.json"
echo "  3. Run: python3 ${SCRIPT_DIR}/validate-skill.py ${TARGET_DIR}"
echo "  4. Register the skill in plugins/frontend-team-toolkit/README.md if publishing to the team"
