#!/usr/bin/env python3
"""
Trajectory Grader - Check agent/skill call sequence.

Usage:
    from trajectory_grader import trajectory_grader
    passed, reason = trajectory_grader(eval_dict, agent_trace)
"""

from __future__ import annotations

from typing import Any


def extract_read_sequence(agent_trace: list[dict[str, Any]]) -> list[str]:
    """Extract sequence of Read tool calls from agent trace."""
    sequence = []
    for step in agent_trace:
        if step.get("tool") == "Read":
            path = step.get("path", "")
            # Extract skill name from path
            if "/skills/" in path:
                parts = path.split("/skills/")
                if len(parts) > 1:
                    skill_name = parts[1].split("/")[0]
                    sequence.append(skill_name)
    return sequence


def extract_agent_sequence(agent_trace: list[dict[str, Any]]) -> list[str]:
    """Extract sequence of agent spawn calls from agent trace."""
    sequence = []
    for step in agent_trace:
        if step.get("tool") == "Agent":
            agent_name = step.get("agent", "")
            if agent_name:
                sequence.append(agent_name)
    return sequence


def check_order(sequence: list[str], expected_order: str) -> bool:
    """Check if sequence matches expected order."""
    # Parse expected order: "先A再B最后C"
    import re
    match = re.findall(r"[先再最后]+(\w+)", expected_order)
    if not match:
        return True  # Can't parse, assume pass

    # Check order
    for i, name in enumerate(match):
        if i >= len(sequence):
            return False
        if name.lower() not in sequence[i].lower():
            return False

    return True


def trajectory_grader(eval_dict: dict[str, Any], agent_trace: list[dict[str, Any]]) -> tuple[bool, str]:
    """
    Trajectory grader: Check agent/skill call sequence.

    Args:
        eval_dict: Eval configuration with 'expected' and 'must_not' lists
        agent_trace: List of agent execution steps with tool calls

    Returns:
        (passed, reason): True if passed, False with reason if failed
    """
    if not agent_trace:
        return False, "agent_trace 为空"

    read_sequence = extract_read_sequence(agent_trace)
    agent_sequence = extract_agent_sequence(agent_trace)

    # Check expected calls
    for expected in eval_dict.get("expected", []):
        expected_lower = expected.lower()

        # Must Read sub-skill
        if "必须 read" in expected_lower or "必须调用" in expected_lower:
            import re
            match = re.search(r"[子]?[skill|skill][:：]?[「【\[]?([^」】\]]+)[」】\]]?", expected)
            if match:
                sub_skill = match.group(1).strip()
                if sub_skill.lower() not in [s.lower() for s in read_sequence]:
                    return False, f"未调用子 Skill: {sub_skill}"

        # Must spawn agent
        if "必须 spawn" in expected_lower or "必须运行" in expected_lower:
            import re
            match = re.search(r"[agent][:：]?[「【\[]?([^」】\]]+)[」】\]]?", expected)
            if match:
                agent_name = match.group(1).strip()
                if agent_name.lower() not in [a.lower() for a in agent_sequence]:
                    return False, f"未运行 Agent: {agent_name}"

        # Check order
        if "按顺序" in expected_lower or "依次" in expected_lower:
            if not check_order(agent_sequence, expected):
                return False, "调用顺序错误"

        # Must be serial (await)
        if "串行" in expected_lower or "serial" in expected_lower:
            # Check if there's parallel execution
            parallel_count = sum(1 for s in agent_trace if "Promise.all" in str(s))
            if parallel_count > 0:
                return False, "串行编排中使用了并行执行"

        # Must be parallel (Promise.all)
        if "并行" in expected_lower or "parallel" in expected_lower:
            parallel_count = sum(1 for s in agent_trace if "Promise.all" in str(s))
            if parallel_count == 0:
                return False, "并行编排中未使用 Promise.all"

    # Check forbidden calls
    for must_not in eval_dict.get("must_not", []):
        must_not_lower = must_not.lower()

        # Must not skip sub-skill
        if "不得跳过" in must_not_lower:
            import re
            match = re.search(r"[子]?[skill|skill][:：]?[「【\[]?([^」】\]]+)[」】\]]?", must_not)
            if match:
                sub_skill = match.group(1).strip()
                if sub_skill.lower() in [s.lower() for s in read_sequence]:
                    # Check if it was skipped (not in expected position)
                    return False, f"跳过了子 Skill: {sub_skill}"

        # Must not call wrong agent
        if "不得调用" in must_not_lower:
            import re
            match = re.search(r"[agent][:：]?[「【\[]?([^」】\]]+)[」】\]]?", must_not)
            if match:
                agent_name = match.group(1).strip()
                if agent_name.lower() in [a.lower() for a in agent_sequence]:
                    return False, f"调用了错误的 Agent: {agent_name}"

    return True, "trajectory grader 通过"


if __name__ == "__main__":
    # Test example
    eval_example = {
        "expected": ["必须 Read 子 Skill: change-spec-workflow", "必须 spawn Agent: argument-builder", "按顺序先lint再review"],
        "must_not": ["不得跳过 lint 直接 review"]
    }
    trace_pass = [
        {"tool": "Read", "path": "/skills/change-spec-workflow/SKILL.md"},
        {"tool": "Agent", "agent": "lint-checker"},
        {"tool": "Agent", "agent": "code-reviewer"},
    ]
    trace_fail = [
        {"tool": "Agent", "agent": "code-reviewer"},  # Skipped lint
    ]

    print("Testing pass case:")
    result = trajectory_grader(eval_example, trace_pass)
    print(f"  Result: {result}")

    print("\nTesting fail case:")
    result = trajectory_grader(eval_example, trace_fail)
    print(f"  Result: {result}")