#!/usr/bin/env python3
"""
Validate industrial-grade Skill directory structure and SKILL.md frontmatter.

Uses Python stdlib only (no PyYAML). Aligns with agentskills.io frontmatter rules
and frontend-team-toolkit skill-engineering template requirements.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
    "disable-model-invocation",
}

REQUIRED_FILES = [
    "SKILL.md",
    "CHANGELOG.md",
    ".skill-meta.json",
    "evals/evals.json",
    "test-prompts.json",
    "references/output-contract.md",
]

RECOMMENDED_FILES = [
    "results.tsv",
    "skill-issues.jsonl.example",
    "scripts/validate-output.sh",
]


def parse_frontmatter(content: str) -> tuple[dict[str, str], str | None]:
    if not content.startswith("---"):
        return {}, "SKILL.md must start with YAML frontmatter (---)"
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}, "Invalid frontmatter: could not parse --- blocks"
    raw = match.group(1)
    data: dict[str, str] = {}
    metadata: dict[str, str] = {}
    in_metadata = False

    for line in raw.splitlines():
        if in_metadata:
            if re.match(r"^  \w", line) or line.startswith("  "):
                m = re.match(r"^  (\w+):\s*(.*)$", line)
                if m:
                    metadata[m.group(1)] = m.group(2).strip().strip('"').strip("'")
                continue
            in_metadata = False

        m = re.match(r"^(\w+):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if key not in ALLOWED_FRONTMATTER_KEYS:
            return {}, f"Unexpected frontmatter key: {key}"
        if key == "metadata":
            in_metadata = True
            if value in ("", "{}"):
                continue
            if value:
                metadata["_inline"] = value
            continue
        value = value.strip('"').strip("'")
        data[key] = value

    if metadata:
        data["metadata"] = json.dumps(metadata)
    return data, None


def validate_skill(skill_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_path.is_dir():
        return [f"Not a directory: {skill_path}"], []

    skill_name = skill_path.name
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", skill_name):
        errors.append(f"Directory name must be kebab-case: {skill_name}")

    for rel in REQUIRED_FILES:
        if not (skill_path / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    for rel in RECOMMENDED_FILES:
        if not (skill_path / rel).exists():
            warnings.append(f"Missing recommended file: {rel}")

    skill_md = skill_path / "SKILL.md"
    if skill_md.is_file():
        content = skill_md.read_text(encoding="utf-8")
        fm, err = parse_frontmatter(content)
        if err:
            errors.append(err)
        else:
            name = fm.get("name", "")
            desc = fm.get("description", "")
            if not name:
                errors.append("Frontmatter missing 'name'")
            elif name != skill_name:
                errors.append(f"Frontmatter name '{name}' != directory '{skill_name}'")
            elif not re.match(r"^[a-z0-9-]+$", name):
                errors.append(f"Invalid name format: {name}")
            elif len(name) > 64:
                errors.append(f"name too long ({len(name)} > 64)")

            if not desc:
                errors.append("Frontmatter missing 'description'")
            elif len(desc) > 1024:
                errors.append(f"description too long ({len(desc)} > 1024)")
            elif "<" in desc or ">" in desc:
                errors.append("description must not contain angle brackets")
            elif "use when" not in desc.lower():
                warnings.append("description should include 'Use when' trigger phrases")

        body_lower = content.lower()
        for section in ("when not to use", "workflow", "checkpoint"):
            if section not in body_lower:
                warnings.append(f"SKILL.md body missing recommended section: {section}")

    meta_path = skill_path / ".skill-meta.json"
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if meta.get("skill_name") and meta["skill_name"] != skill_name:
                errors.append(".skill-meta.json skill_name mismatch")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid .skill-meta.json: {e}")

    evals_path = skill_path / "evals" / "evals.json"
    if evals_path.is_file():
        try:
            evals_doc = json.loads(evals_path.read_text(encoding="utf-8"))
            cases = evals_doc.get("evals", [])
            if len(cases) < 1:
                warnings.append("evals/evals.json has no eval cases yet")
            for i, case in enumerate(cases):
                if "id" not in case or "prompt" not in case:
                    errors.append(f"evals[{i}] missing id or prompt")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid evals/evals.json: {e}")

    tp_path = skill_path / "test-prompts.json"
    if tp_path.is_file():
        try:
            prompts = json.loads(tp_path.read_text(encoding="utf-8"))
            if not isinstance(prompts, list):
                errors.append("test-prompts.json must be a JSON array")
            elif len(prompts) < 1:
                warnings.append("test-prompts.json is empty")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid test-prompts.json: {e}")

    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate-skill.py <skill-directory>", file=sys.stderr)
        return 1

    skill_path = Path(sys.argv[1]).resolve()
    errors, warnings = validate_skill(skill_path)

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors:
        print(f"\nFAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1

    print(f"PASS: {skill_path.name} ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
