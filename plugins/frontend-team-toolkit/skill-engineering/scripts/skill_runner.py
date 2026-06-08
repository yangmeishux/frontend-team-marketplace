#!/usr/bin/env python3
"""
Skill Runner - Execute Skill and capture output + agent_trace.

Usage:
    from skill_runner import run_skill
    output, agent_trace = run_skill(skill_name, skill_path, prompt)

Supports:
    - Local execution (simulate skill behavior)
    - Claude Code integration (via subprocess)
    - Anthropic API integration (direct API call)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Execution mode configuration
EXECUTION_MODE = os.environ.get("SKILL_EXECUTION_MODE", "local")  # local | claude_code | api
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_CODE_PATH = os.environ.get("CLAUDE_CODE_PATH", "claude")


def load_skill_md(skill_path: Path) -> dict[str, Any]:
    """Load SKILL.md and parse frontmatter."""
    skill_md_path = skill_path / "SKILL.md"
    if not skill_md_path.exists():
        return {}

    content = skill_md_path.read_text(encoding="utf-8")

    # Parse YAML frontmatter
    if not content.startswith("---"):
        return {}

    import re
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    frontmatter_raw = match.group(1)
    frontmatter = {}

    for line in frontmatter_raw.splitlines():
        line_match = re.match(r"^(\w+):\s*(.*)$", line)
        if line_match:
            key, value = line_match.group(1), line_match.group(2).strip()
            # Remove quotes
            value = value.strip('"').strip("'")
            frontmatter[key] = value

    return frontmatter


def build_skill_context(skill_path: Path) -> str:
    """Build context from skill files."""
    context_parts = []

    # Load SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        context_parts.append(f"## SKILL.md\n{skill_md.read_text(encoding='utf-8')}")

    # Load output-contract
    output_contract = skill_path / "references" / "output-contract.md"
    if output_contract.exists():
        context_parts.append(f"## Output Contract\n{output_contract.read_text(encoding='utf-8')}")

    # Load scoring-rubric
    scoring_rubric = skill_path / "references" / "scoring-rubric.md"
    if scoring_rubric.exists():
        context_parts.append(f"## Scoring Rubric\n{scoring_rubric.read_text(encoding='utf-8')}")

    return "\n\n---\n\n".join(context_parts)


def run_skill_local(skill_name: str, skill_path: Path, prompt: str) -> tuple[str, list[dict[str, Any]]]:
    """
    Local execution mode: Simulate skill behavior for testing.

    Returns simulated output and empty agent_trace.
    """
    frontmatter = load_skill_md(skill_path)
    description = frontmatter.get("description", "")

    # Simulate output based on skill type
    if skill_name == "wechat-article-review":
        # Simulate article review output
        output = simulate_article_review(prompt, skill_path)
    else:
        # Generic simulation
        output = f"[Simulated {skill_name} output for prompt: {prompt[:100]}...]"

    # Empty agent_trace for local mode
    agent_trace = []

    return output, agent_trace


def simulate_article_review(prompt: str, skill_path: Path) -> str:
    """Simulate wechat-article-review skill output."""

    # Check if prompt contains article content
    if len(prompt) < 50 or "评审" not in prompt:
        # Missing article - return BLOCKED
        return """
# 评审报告

**状态**: BLOCKED

缺正文或路径，请提供以下最少信息：
- 文章内容或 articles/ 路径

不得编造文章内容或虚构分数。
"""

    # Simulate a basic review based on prompt quality
    # This is a placeholder - actual implementation would use LLM

    # Check for common issues in the prompt
    issues = []

    # Check for hollow opening
    if prompt.startswith("# ") and len(prompt.split("\n\n")[0]) < 100:
        issues.append({
            "location": "第 1 段",
            "issue": "开头空洞，无痛点/数据/故事",
            "suggestion": "补痛点场景或数据开头",
            "severity": "P0"
        })

    # Check for missing substance
    if len(prompt) < 300:
        issues.append({
            "location": "全文",
            "issue": "干货不足，无具体技巧/案例/数据",
            "suggestion": "补充可抄走的内容",
            "severity": "P0"
        })

    # Check for unfulfilled promises
    if "下文将" in prompt or "本文提供" in prompt:
        if "清单" not in prompt or "步骤" not in prompt:
            issues.append({
                "location": "开头",
                "issue": "承诺未兑现",
                "suggestion": "补小节/清单",
                "severity": "P0"
            })

    # Generate output
    if issues:
        score = max(6.0, 9.0 - len(issues) * 1.5)
        status = "❌ 不通过"
    else:
        score = 9.2
        status = "✅ 通过"

    output = f"""
# 文章评审报告

**状态**: {status}
**综合评分**: {score:.1f}/10

## 各维度得分

| 维度 | 得分 | 说明 |
|------|------|------|
| 主题与价值 | 2.0/2.5 | {issues[0]['issue'] if issues else '主题明确'} |
| 结构与逻辑 | 1.8/2.0 | {'结构需优化' if issues else '结构清晰'} |
| 干货密度 | 2.0/2.5 | {'干货不足' if issues else '干货充足'} |
| 可读性与表达 | 1.8/2.0 | {'表达需加强' if issues else '表达清晰'} |
| 标题与 CTA | 0.6/1.0 | {'缺 CTA' if any('CTA' not in prompt for _ in [1]) else '有 CTA'} |

"""

    if issues:
        output += "\n## 主要问题\n\n"
        for issue in issues:
            output += f"- **{issue['severity']}** {issue['location']}: {issue['issue']}\n"
            output += f"  - 建议: {issue['suggestion']}\n"

        output += "\n## 修改清单\n\n"
        output += "- [ ] 补开头痛点\n"
        output += "- [ ] 补干货案例\n"
        output += "- [ ] 补 CTA\n"
        output += "\n**复评目标**: 9.0-9.2 分"

    return output


def run_skill_api(skill_name: str, skill_path: Path, prompt: str) -> tuple[str, list[dict[str, Any]]]:
    """
    API execution mode: Call Anthropic API directly.

    Requires ANTHROPIC_API_KEY.
    """
    if not ANTHROPIC_API_KEY:
        print("WARNING: No ANTHROPIC_API_KEY, falling back to local mode", file=sys.stderr)
        return run_skill_local(skill_name, skill_path, prompt)

    try:
        import anthropic

        # Build context
        skill_context = build_skill_context(skill_path)

        # Build full prompt
        full_prompt = f"""
You are executing the skill: {skill_name}

Skill Context:
{skill_context}

User Prompt:
{prompt}

Please follow the skill's workflow and output contract.
"""

        client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": full_prompt}]
        )

        output = response.content[0].text

        # Build agent_trace from API response
        agent_trace = [
            {
                "tool": "API",
                "action": "messages.create",
                "timestamp": datetime.now().isoformat(),
                "model": "claude-sonnet-4-6",
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        ]

        return output, agent_trace

    except ImportError:
        print("WARNING: anthropic package not installed, falling back to local mode", file=sys.stderr)
        return run_skill_local(skill_name, skill_path, prompt)
    except Exception as e:
        print(f"ERROR: API call failed: {e}", file=sys.stderr)
        return f"[API Error: {e}]", []


def run_skill_claude_code(skill_name: str, skill_path: Path, prompt: str) -> tuple[str, list[dict[str, Any]]]:
    """
    Claude Code execution mode: Invoke Claude Code CLI.

    Requires Claude Code installed and configured.
    """
    try:
        # Build skill invocation command
        skill_context = build_skill_context(skill_path)

        # Create temp file with prompt
        temp_prompt_file = Path("/tmp/skill_prompt.txt")
        temp_prompt_file.write_text(f"{skill_context}\n\n---\n\n{prompt}", encoding="utf-8")

        # Execute Claude Code
        result = subprocess.run(
            [CLAUDE_CODE_PATH, "--skill", skill_name, "--input", str(temp_prompt_file)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        output = result.stdout

        # Parse agent_trace from output (if available)
        agent_trace = []
        # Try to parse trace markers in output
        import re
        trace_matches = re.findall(r"\[TRACE\] (\w+): (.+)", output)
        for tool, action in trace_matches:
            agent_trace.append({
                "tool": tool,
                "action": action,
                "timestamp": datetime.now().isoformat()
            })

        return output, agent_trace

    except subprocess.TimeoutExpired:
        return "[Timeout: Claude Code execution exceeded 5 minutes]", []
    except FileNotFoundError:
        print(f"WARNING: Claude Code not found at {CLAUDE_CODE_PATH}, falling back to local mode", file=sys.stderr)
        return run_skill_local(skill_name, skill_path, prompt)
    except Exception as e:
        print(f"ERROR: Claude Code execution failed: {e}", file=sys.stderr)
        return f"[Claude Code Error: {e}]", []


def run_skill(skill_name: str, skill_path: Path, prompt: str) -> tuple[str, list[dict[str, Any]]]:
    """
    Execute a skill and return output + agent_trace.

    Args:
        skill_name: Name of the skill
        skill_path: Path to skill directory
        prompt: User prompt/input

    Returns:
        (output, agent_trace): Output text and list of tool calls
    """
    if EXECUTION_MODE == "api":
        return run_skill_api(skill_name, skill_path, prompt)
    elif EXECUTION_MODE == "claude_code":
        return run_skill_claude_code(skill_name, skill_path, prompt)
    else:
        return run_skill_local(skill_name, skill_path, prompt)


def run_skill_from_eval(eval_dict: dict[str, Any], skill_path: Path) -> tuple[str, list[dict[str, Any]]]:
    """
    Execute skill using eval prompt.

    Args:
        eval_dict: Eval configuration with 'prompt' field
        skill_path: Path to skill directory

    Returns:
        (output, agent_trace): Output and trace
    """
    prompt = eval_dict.get("prompt", "")
    skill_name = eval_dict.get("skill_name", skill_path.name)

    # Check if prompt references a file path
    import re
    path_match = re.search(r"(articles/[\w\-]+\.md|plugins/[\w\-/]+\.md)", prompt)

    if path_match:
        # Read the referenced file
        file_path = Path(path_match.group(1))
        if file_path.exists():
            file_content = file_path.read_text(encoding="utf-8")
            prompt = f"{prompt}\n\n---\n\n文章内容:\n{file_content}"
        else:
            # File not found - return BLOCKED-like response
            return f"[BLOCKED] 文件不存在: {file_path}", []

    return run_skill(skill_name, skill_path, prompt)


if __name__ == "__main__":
    # Test example
    import argparse

    parser = argparse.ArgumentParser(description="Run a skill")
    parser.add_argument("--skill", required=True, help="Skill name")
    parser.add_argument("--prompt", required=True, help="Prompt to execute")
    parser.add_argument("--skill-path", default="plugins/frontend-team-toolkit/skills", help="Skills directory")

    args = parser.parse_args()

    skill_path = Path(args.skill_path) / args.skill
    output, trace = run_skill(args.skill, skill_path, args.prompt)

    print("=== Output ===")
    print(output[:500])

    print("\n=== Agent Trace ===")
    for step in trace:
        print(f"  {step}")