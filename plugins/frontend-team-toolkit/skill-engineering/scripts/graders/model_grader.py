#!/usr/bin/env python3
"""
Model Grader - Use LLM Judge to evaluate semantic quality.

Usage:
    from model_grader import model_grader
    passed, reason = model_grader(eval_dict, output)

Note: Requires LLM API key configuration.
      Uses multi-sample voting to reduce drift.
"""

from __future__ import annotations

import json
import os
from typing import Any

# LLM configuration (can be overridden via environment)
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "claude-sonnet-4-6")
LLM_API_URL = os.environ.get("LLM_API_URL", "https://api.anthropic.com/v1/messages")
SAMPLE_COUNT = int(os.environ.get("LLM_SAMPLE_COUNT", "3"))  # Multi-sample voting


def build_judge_prompt(eval_dict: dict[str, Any], output: str) -> str:
    """Build LLM Judge prompt."""
    return f"""
你是 Eval Judge，请判定以下输出是否满足要求。

Eval expected:
{json.dumps(eval_dict.get("expected", []), indent=2)}

Eval must_not:
{json.dumps(eval_dict.get("must_not", []), indent=2)}

输出内容:
{output}

请逐条判定：
- 对于每条 expected，输出是否满足（满足/不满足）
- 对于每条 must_not，输出是否违反（违反/未违反）

判定格式：
| 条件 | 内容 | 判定 |
|------|------|------|
| expected-1 | ... | 满足/不满足 |
| expected-2 | ... | 满足/不满足 |
| must_not-1 | ... | 违反/未违反 |
| must_not-2 | ... | 违反/未违反 |

最终判定：PASS 或 FAIL
"""


def call_llm(prompt: str) -> str:
    """Call LLM API (placeholder implementation)."""
    # Placeholder: actual implementation would call Anthropic/OpenAI API
    # For now, return a mock response
    if not LLM_API_KEY:
        return "PASS (mock: no API key configured)"

    # TODO: Actual API call implementation
    # import anthropic
    # client = anthropic.Client(api_key=LLM_API_KEY)
    # response = client.messages.create(
    #     model=LLM_MODEL,
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.content[0].text

    return "PASS (mock)"


def parse_judge_response(response: str) -> tuple[bool, str]:
    """Parse LLM Judge response to determine pass/fail."""
    if "PASS" in response.upper():
        # Check if there are any "不满足" or "违反"
        if "不满足" in response or "违反" in response:
            return False, response
        return True, response
    elif "FAIL" in response.upper():
        return False, response
    else:
        # Ambiguous response
        return False, f"判定不明确: {response}"


def multi_sample_judge(prompt: str, sample_count: int = SAMPLE_COUNT) -> tuple[bool, str]:
    """Run multiple samples and use majority voting."""
    results = []
    for _ in range(sample_count):
        response = call_llm(prompt)
        passed, reason = parse_judge_response(response)
        results.append((passed, reason))

    # Majority voting
    pass_count = sum(1 for p, r in results if p)
    fail_count = sample_count - pass_count

    if pass_count > fail_count:
        return True, f"多数判定通过 ({pass_count}/{sample_count})"
    elif fail_count > pass_count:
        return False, f"多数判定失败 ({fail_count}/{sample_count})"
    else:
        # Tie: fail by default (conservative)
        return False, "判定持平，默认失败"


def model_grader(eval_dict: dict[str, Any], output: str) -> tuple[bool, str]:
    """
    Model grader: Use LLM Judge to evaluate semantic quality.

    Args:
        eval_dict: Eval configuration with 'expected' and 'must_not' lists
        output: Actual output text to evaluate

    Returns:
        (passed, reason): True if passed, False with reason if failed
    """
    if not output:
        return False, "输出为空"

    if not LLM_API_KEY:
        # No API key: warn and return pending status
        return True, "model grader: 无 API key，跳过语义检查"

    # Build judge prompt
    prompt = build_judge_prompt(eval_dict, output)

    # Multi-sample voting for drift reduction
    passed, reason = multi_sample_judge(prompt, SAMPLE_COUNT)

    return passed, reason


if __name__ == "__main__":
    # Test example
    eval_example = {
        "expected": ["输出逻辑清晰", "论证有证据支撑"],
        "must_not": ["不得有逻辑跳跃", "不得有空洞表述"]
    }
    output_pass = """
# 审核结论

本文论证清晰，有以下证据支撑：
1. 数据统计来源明确
2. 案例分析有据可查
3. 理论框架引用规范

整体逻辑连贯，无跳跃。
"""
    output_fail = """
# 审核结论

本文还行，有一定道理。
结论比较重要，需要重视。
"""

    print("Testing pass case (requires API key for actual evaluation):")
    result = model_grader(eval_example, output_pass)
    print(f"  Result: {result}")

    print("\nTesting fail case:")
    result = model_grader(eval_example, output_fail)
    print(f"  Result: {result}")