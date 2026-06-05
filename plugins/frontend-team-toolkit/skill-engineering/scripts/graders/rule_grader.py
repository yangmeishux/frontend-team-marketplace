#!/usr/bin/env python3
"""
Rule Grader - Check keywords, paths, forbidden words.

Usage:
    from rule_grader import rule_grader
    passed, reason = rule_grader(eval_dict, output)
"""

from __future__ import annotations

import re
from typing import Any


def extract_keyword(text: str) -> str:
    """Extract keyword from '必须包含xxx' or '不得包含xxx' patterns."""
    # Pattern: 必须包含[关键词]
    match = re.search(r"必须包含[「【\[]?([^」】\]]+)[」】\]]?", text)
    if match:
        return match.group(1).strip()

    # Pattern: 不得包含[关键词]
    match = re.search(r"不得包含[「【\[]?([^」】\]]+)[」】\]]?", text)
    if match:
        return match.group(1).strip()

    # Pattern: 缺少关键词: xxx
    match = re.search(r"缺少关键词[:：]\s*(.+)", text)
    if match:
        return match.group(1).strip()

    # Fallback: extract quoted content
    match = re.search(r"[「【\["']([^」】\]"']+)[」】\]"']", text)
    if match:
        return match.group(1).strip()

    return ""


def rule_grader(eval_dict: dict[str, Any], output: str) -> tuple[bool, str]:
    """
    Rule grader: Check keywords, paths, forbidden words.

    Args:
        eval_dict: Eval configuration with 'expected' and 'must_not' lists
        output: Actual output text to check

    Returns:
        (passed, reason): True if passed, False with reason if failed
    """
    output_lower = output.lower()

    # Check expected keywords
    for expected in eval_dict.get("expected", []):
        expected_lower = expected.lower()

        # Must include keyword
        if "必须" in expected_lower or "must" in expected_lower:
            keyword = extract_keyword(expected)
            if keyword and keyword.lower() not in output_lower:
                return False, f"缺少关键词: {keyword}"

        # Must include path
        if "路径" in expected_lower or "path" in expected_lower:
            keyword = extract_keyword(expected)
            if keyword and keyword not in output:
                return False, f"缺少路径: {keyword}"

        # Must include section
        if "章节" in expected_lower or "section" in expected_lower:
            keyword = extract_keyword(expected)
            if keyword and f"## {keyword}" not in output:
                return False, f"缺少章节: {keyword}"

    # Check forbidden keywords
    for must_not in eval_dict.get("must_not", []):
        must_not_lower = must_not.lower()

        # Must not include forbidden word
        if "不得" in must_not_lower or "禁止" in must_not_lower or "must not" in must_not_lower:
            forbidden = extract_keyword(must_not)
            if forbidden and forbidden.lower() in output_lower:
                return False, f"出现禁用词: {forbidden}"

        # Must not include forbidden section
        if "不得出现" in must_not_lower or "禁止章节" in must_not_lower:
            forbidden = extract_keyword(must_not)
            if forbidden and f"## {forbidden}" in output:
                return False, f"出现禁止章节: {forbidden}"

    return True, "rule grader 通过"


if __name__ == "__main__":
    # Test example
    eval_example = {
        "expected": ["必须包含「BLOCKED」", "必须包含路径 references/output-contract.md"],
        "must_not": ["不得包含「TODO」", "不得出现「参考资料」章节"]
    }
    output_pass = "状态: BLOCKED\n已读取 references/output-contract.md\n完成审核"
    output_fail = "状态: TODO\n缺少明确结论"

    print("Testing pass case:")
    result = rule_grader(eval_example, output_pass)
    print(f"  Result: {result}")

    print("\nTesting fail case:")
    result = rule_grader(eval_example, output_fail)
    print(f"  Result: {result}")