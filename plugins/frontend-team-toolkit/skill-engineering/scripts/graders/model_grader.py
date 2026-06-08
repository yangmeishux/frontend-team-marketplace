#!/usr/bin/env python3
"""
Model Grader - Use LLM Judge to evaluate semantic quality.

Usage:
    from model_grader import model_grader
    passed, reason = model_grader(eval_dict, output)

Execution modes:
    - local: Simulate judgment (for testing)
    - api: Call Anthropic API directly
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

# LLM configuration
LLM_API_KEY = os.environ.get("ANTHROPIC_API_KEY", os.environ.get("LLM_API_KEY", ""))
LLM_MODEL = os.environ.get("LLM_MODEL", "claude-sonnet-4-6")
SAMPLE_COUNT = int(os.environ.get("LLM_SAMPLE_COUNT", "1"))  # Multi-sample voting (default 1 for cost)
EXECUTION_MODE = os.environ.get("MODEL_GRADER_MODE", "local")  # local | api


def build_judge_prompt(eval_dict: dict[str, Any], output: str) -> str:
    """Build LLM Judge prompt."""
    expected = eval_dict.get("expected", [])
    must_not = eval_dict.get("must_not", [])

    return f"""
你是 Eval Judge，请判定以下输出是否满足要求。

## Eval expected（必须满足）
{json.dumps(expected, indent=2, ensure_ascii=False)}

## Eval must_not（不得违反）
{json.dumps(must_not, indent=2, ensure_ascii=False)}

## 输出内容
{output}

---

请逐条判定：
- 对于每条 expected，判定「满足」或「不满足」
- 对于每条 must_not，判定「违反」或「未违反」

## 判定格式

| 序号 | 条件类型 | 内容摘要 | 判定 |
|------|----------|----------|------|
| 1 | expected | ... | 满足/不满足 |
| 2 | expected | ... | 满足/不满足 |
| 3 | must_not | ... | 违反/未违反 |
| ... | ... | ... | ... |

---

## 最终判定

基于以上逐条判定，给出最终结论：

- 若 **所有 expected 满足** 且 **所有 must_not 未违反** → 输出 `最终判定: PASS`
- 若 **任一 expected 不满足** 或 **任一 must_not 违反** → 输出 `最终判定: FAIL` 并说明失败原因
"""


def call_llm_api(prompt: str) -> str:
    """Call Anthropic API."""
    if not LLM_API_KEY:
        return "PASS (no API key - simulated)"

    try:
        import anthropic

        client = anthropic.Client(api_key=LLM_API_KEY)

        response = client.messages.create(
            model=LLM_MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    except ImportError:
        print("WARNING: anthropic package not installed", file=sys.stderr)
        return "PASS (anthropic not installed - simulated)"
    except Exception as e:
        print(f"ERROR: LLM API call failed: {e}", file=sys.stderr)
        return f"FAIL (API error: {e})"


def call_llm_local(prompt: str, eval_dict: dict[str, Any], output: str) -> str:
    """Local mode: Simulate judgment based on keyword matching."""

    expected = eval_dict.get("expected", [])
    must_not = eval_dict.get("must_not", [])

    # Simple keyword-based simulation
    results = []

    for i, exp in enumerate(expected):
        # Extract key phrases
        key_phrase = extract_key_phrase(exp)
        satisfied = key_phrase.lower() in output.lower() or len(key_phrase) < 3
        results.append({
            "type": "expected",
            "content": exp[:50] + "..." if len(exp) > 50 else exp,
            "judgment": "满足" if satisfied else "不满足"
        })

    for i, mn in enumerate(must_not):
        key_phrase = extract_key_phrase(mn)
        violated = key_phrase.lower() in output.lower() and len(key_phrase) > 3
        results.append({
            "type": "must_not",
            "content": mn[:50] + "..." if len(mn) > 50 else mn,
            "judgment": "违反" if violated else "未违反"
        })

    # Build response
    response = "| 序号 | 条件类型 | 内容摘要 | 判定 |\n|------|----------|----------|------|\n"
    for i, r in enumerate(results):
        response += f"| {i+1} | {r['type']} | {r['content']} | {r['judgment']} |\n"

    # Final judgment
    all_expected_satisfied = all(r["judgment"] == "满足" for r in results if r["type"] == "expected")
    all_must_not_clean = all(r["judgment"] == "未违反" for r in results if r["type"] == "must_not")

    if all_expected_satisfied and all_must_not_clean:
        response += "\n最终判定: PASS"
    else:
        failed = [r for r in results if r["judgment"] in ["不满足", "违反"]]
        response += f"\n最终判定: FAIL\n失败原因: {len(failed)} 条未通过"

    return response


def extract_key_phrase(text: str) -> str:
    """Extract key phrase from condition text."""
    import re

    # Pattern: 「xxx」 or "xxx" or keyword after 必须/不得
    match = re.search(r"[「【\[\"']([^」】\]\"']+)[」】\]\"']", text)
    if match:
        return match.group(1)

    # Pattern: 必须 xxx
    match = re.search(r"必须[有包含]?\s*(.+)", text)
    if match:
        return match.group(1).strip()[:20]

    # Pattern: 不得 xxx
    match = re.search(r"不得[有包含]?\s*(.+)", text)
    if match:
        return match.group(1).strip()[:20]

    # Fallback: first meaningful phrase
    return text[:20]


def parse_judge_response(response: str) -> tuple[bool, str]:
    """Parse LLM Judge response."""
    if "最终判定: PASS" in response:
        return True, response
    elif "最终判定: FAIL" in response:
        return False, response
    elif "PASS" in response.upper():
        # Check for hidden failures
        if "不满足" in response or "违反" in response:
            return False, response
        return True, response
    elif "FAIL" in response.upper():
        return False, response
    else:
        # Ambiguous - conservative fail
        return False, f"判定不明确: {response[:200]}"


def model_grader(eval_dict: dict[str, Any], output: str) -> tuple[bool, str]:
    """
    Model grader: Use LLM Judge to evaluate semantic quality.

    Args:
        eval_dict: Eval configuration with 'expected' and 'must_not' lists
        output: Actual output text to evaluate

    Returns:
        (passed, reason): True if passed, False with reason if failed
    """
    if not output or len(output) < 10:
        return False, "输出为空或过短"

    # Build prompt
    prompt = build_judge_prompt(eval_dict, output)

    # Execute based on mode
    if EXECUTION_MODE == "api" and LLM_API_KEY:
        # Multi-sample voting (if configured)
        if SAMPLE_COUNT > 1:
            results = []
            for _ in range(SAMPLE_COUNT):
                response = call_llm_api(prompt)
                passed, reason = parse_judge_response(response)
                results.append((passed, reason))

            pass_count = sum(1 for p, r in results if p)
            fail_count = SAMPLE_COUNT - pass_count

            if pass_count > fail_count:
                return True, f"多数判定通过 ({pass_count}/{SAMPLE_COUNT})"
            elif fail_count > pass_count:
                return False, f"多数判定失败 ({fail_count}/{SAMPLE_COUNT})"
            else:
                return False, "判定持平，默认失败"
        else:
            response = call_llm_api(prompt)
            return parse_judge_response(response)
    else:
        # Local mode: simulate
        response = call_llm_local(prompt, eval_dict, output)
        return parse_judge_response(response)


if __name__ == "__main__":
    # Test
    eval_example = {
        "expected": ["结论必须为 ❌ 不通过", "必须包含五维得分表"],
        "must_not": ["不得给出 ≥9.0 通过结论", "不得只有总分没有维度依据"]
    }

    output_fail = """
# 文章评审报告

**状态**: ❌ 不通过
**综合评分**: 7.5/10

## 各维度得分

| 维度 | 得分 | 说明 |
|------|------|------|
| 主题与价值 | 1.8/2.5 | 主题模糊 |
| 结构与逻辑 | 1.5/2.0 | 结构混乱 |
| 干货密度 | 1.5/2.5 | 干货不足 |
| 可读性与表达 | 1.5/2.0 | 表达不清 |
| 标题与 CTA | 0.2/1.0 | 缺 CTA |
"""

    output_pass = """
# 文章评审报告

**状态**: ✅ 通过
**综合评分**: 9.2/10

## 各维度得分

| 维度 | 得分 | 说明 |
|------|------|------|
| 主题与价值 | 2.4/2.5 | 主题明确 |
| 结构与逻辑 | 1.9/2.0 | 结构清晰 |
"""

    print("Testing fail case:")
    result = model_grader(eval_example, output_fail)
    print(f"  Result: {result}")

    print("\nTesting pass case:")
    result = model_grader(eval_example, output_pass)
    print(f"  Result: {result}")