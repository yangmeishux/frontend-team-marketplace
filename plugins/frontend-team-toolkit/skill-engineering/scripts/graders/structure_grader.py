#!/usr/bin/env python3
"""
Structure Grader - Check sections, steps, frontmatter structure.

Usage:
    from structure_grader import structure_grader
    passed, reason = structure_grader(eval_dict, output)
"""

from __future__ import annotations

import re
from typing import Any


def extract_sections(text_list: list[str]) -> list[str]:
    """Extract section names from text patterns."""
    sections = []
    for text in text_list:
        # Pattern: 必须有「xxx」章节
        match = re.search(r"必须[有包含][「【\[]?([^」】\]]+)[」】\]]?章节", text)
        if match:
            sections.append(match.group(1).strip())

        # Pattern: 缺少章节: xxx
        match = re.search(r"缺少章节[:：]\s*(.+)", text)
        if match:
            sections.append(match.group(1).strip())

    return sections


def extract_forbidden_sections(text_list: list[str]) -> list[str]:
    """Extract forbidden section names from text patterns."""
    sections = []
    for text in text_list:
        # Pattern: 不得出现「xxx」章节
        match = re.search(r"不得出现[「【\[]?([^」】\]]+)[」】\]]?章节", text)
        if match:
            sections.append(match.group(1).strip())

        # Pattern: 禁止章节: xxx
        match = re.search(r"禁止章节[:：]\s*(.+)", text)
        if match:
            sections.append(match.group(1).strip())

    return sections


def check_steps(output: str, expected_steps: list[str]) -> tuple[bool, str]:
    """Check if expected steps are present in output."""
    missing_steps = []
    for step in expected_steps:
        # Pattern: Step N: xxx or 步骤N: xxx
        if f"Step {step}" not in output and f"步骤{step}" not in output:
            missing_steps.append(step)

    if missing_steps:
        return False, f"缺少步骤: {', '.join(missing_steps)}"
    return True, "步骤检查通过"


def structure_grader(eval_dict: dict[str, Any], output: str) -> tuple[bool, str]:
    """
    Structure grader: Check sections, steps, frontmatter.

    Args:
        eval_dict: Eval configuration with 'expected' and 'must_not' lists
        output: Actual output text to check

    Returns:
        (passed, reason): True if passed, False with reason if failed
    """
    # Check required sections
    required_sections = extract_sections(eval_dict.get("expected", []))
    for section in required_sections:
        # Check various section formats
        if not any([
            f"## {section}" in output,
            f"## {section.lower()}" in output.lower(),
            f"# {section}" in output,
            f"# {section.lower()}" in output.lower()
        ]):
            return False, f"缺少章节: {section}"

    # Check forbidden sections
    forbidden_sections = extract_forbidden_sections(eval_dict.get("must_not", []))
    for section in forbidden_sections:
        if f"## {section}" in output or f"# {section}" in output:
            return False, f"出现禁止章节: {section}"

    # Check frontmatter (if expected)
    for expected in eval_dict.get("expected", []):
        # Must have frontmatter
        if "frontmatter" in expected.lower() or "元数据" in expected.lower():
            if not output.startswith("---"):
                return False, "缺少 YAML frontmatter"

            # Check frontmatter structure
            match = re.match(r"^---\n(.*?)\n---", output, re.DOTALL)
            if not match:
                return False, "frontmatter 格式错误"

            # Check required frontmatter fields
            fm_content = match.group(1)
            if "name:" not in fm_content:
                return False, "frontmatter 缺少 name"
            if "description:" not in fm_content:
                return False, "frontmatter 缺少 description"

    # Check steps (if expected)
    for expected in eval_dict.get("expected", []):
        # Must have steps
        if "步骤" in expected or "step" in expected.lower():
            match = re.search(r"步骤[:：]\s*(.+)", expected)
            if match:
                steps = match.group(1).split(",")
                passed, reason = check_steps(output, steps)
                if not passed:
                    return passed, reason

    return True, "structure grader 通过"


if __name__ == "__main__":
    # Test example
    eval_example = {
        "expected": ["必须有「When to Activate」章节", "必须有「Workflow」章节", "必须有 frontmatter"],
        "must_not": ["不得出现「参考资料」章节"]
    }
    output_pass = """---
name: test-skill
description: Test skill
---
# Test Skill

## When to Activate
- Trigger 1
- Trigger 2

## Workflow
1. Step 1
2. Step 2
"""
    output_fail = """# Test Skill
没有 frontmatter
没有 When to Activate 章节"""

    print("Testing pass case:")
    result = structure_grader(eval_example, output_pass)
    print(f"  Result: {result}")

    print("\nTesting fail case:")
    result = structure_grader(eval_example, output_fail)
    print(f"  Result: {result}")