#!/usr/bin/env python3
"""
Eval Runner - Run Evals based on CI mode (PR/Release/Scheduled).

Usage:
    python scripts/run_evals.py --mode pr --skill <skill_name>
    python scripts/run_evals.py --mode release --skill <skill_name>
    python scripts/run_evals.py --mode scheduled --skill <skill_name> --frequency weekly

Modes:
    pr:        Run risk=high + medium Evals (PR trigger)
    release:   Run all Evals (release trigger)
    scheduled: Run based on frequency (weekly/monthly/quarterly)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add graders directory to path
sys.path.insert(0, str(Path(__file__).parent / "graders"))

from rule_grader import rule_grader
from structure_grader import structure_grader
from trajectory_grader import trajectory_grader
from model_grader import model_grader


def load_config(config_path: Path) -> dict[str, Any]:
    """Load risk layer configuration."""
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    # Default config
    return {
        "pr_mode": {
            "risk_filter": ["high", "medium"],
            "block_on_regression_high": True,
            "block_on_regression_medium": False
        },
        "release_mode": {
            "risk_filter": ["high", "medium", "low"],
            "block_on_any_regression": True,
            "require_human_review": []
        },
        "scheduled_mode": {
            "weekly": {"risk_filter": ["high"], "spot_check_count": 3},
            "monthly": {"risk_filter": ["high", "medium"]},
            "quarterly": {"risk_filter": ["high", "medium", "low"]}
        }
    }


def load_evals(skill_path: Path) -> list[dict[str, Any]]:
    """Load evals.json for a skill."""
    evals_path = skill_path / "evals" / "evals.json"
    if evals_path.exists():
        doc = json.loads(evals_path.read_text(encoding="utf-8"))
        return doc.get("evals", [])
    return []


def filter_evals_by_risk(evals: list[dict[str, Any]], risk_filter: list[str]) -> list[dict[str, Any]]:
    """Filter evals by risk level."""
    return [e for e in evals if e.get("risk", "medium") in risk_filter]


def add_spot_check(evals: list[dict[str, Any]], count: int) -> list[dict[str, Any]]:
    """Add random spot check evals."""
    import random
    all_evals = [e for e in evals if e.get("risk") not in ["high", "medium"]]
    spot = random.sample(all_evals, min(count, len(all_evals)))
    return evals + spot


def run_single_eval(eval_dict: dict[str, Any], output: str, agent_trace: list | None = None) -> dict[str, Any]:
    """Run a single eval using appropriate grader."""
    grader_type = eval_dict.get("grader", "rule")

    if grader_type == "rule":
        passed, reason = rule_grader(eval_dict, output)
    elif grader_type == "structure":
        passed, reason = structure_grader(eval_dict, output)
    elif grader_type == "trajectory":
        passed, reason = trajectory_grader(eval_dict, agent_trace or [])
    elif grader_type == "model":
        passed, reason = model_grader(eval_dict, output)
    elif grader_type == "human":
        # Human grader requires manual review
        passed, reason = None, "requires_human_review"
    else:
        # Composite grader (rule+human, structure+human, etc.)
        graders = grader_type.split("+")
        results = []
        for g in graders:
            if g == "rule":
                results.append(rule_grader(eval_dict, output))
            elif g == "structure":
                results.append(structure_grader(eval_dict, output))
            elif g == "trajectory":
                results.append(trajectory_grader(eval_dict, agent_trace or []))
            elif g == "human":
                results.append((None, "requires_human_review"))

        # Composite: all non-human must pass
        non_human = [r for r in results if r[0] is not None]
        if all(r[0] for r in non_human):
            if "human" in graders:
                passed, reason = None, "requires_human_review"
            else:
                passed, reason = True, "all graders passed"
        else:
            passed, reason = False, "; ".join(r[1] for r in non_human if not r[0])

    return {
        "eval_id": eval_dict.get("id"),
        "name": eval_dict.get("name"),
        "type": eval_dict.get("type"),
        "risk": eval_dict.get("risk"),
        "grader": grader_type,
        "pass": "✅" if passed else ("⚠️" if passed is None else "❌"),
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }


def run_evals(mode: str, skill: str, skill_base_path: Path, frequency: str | None = None) -> list[dict[str, Any]]:
    """Run evals based on mode."""

    config_path = skill_base_path.parent / "skill-engineering" / "config" / "risk-layer-config.json"
    config = load_config(config_path)

    skill_path = skill_base_path / skill
    evals = load_evals(skill_path)

    if mode == "pr":
        risk_filter = config["pr_mode"]["risk_filter"]
        filtered = filter_evals_by_risk(evals, risk_filter)

    elif mode == "release":
        risk_filter = config["release_mode"]["risk_filter"]
        filtered = filter_evals_by_risk(evals, risk_filter)

    elif mode == "scheduled":
        if frequency is None:
            frequency = "weekly"
        freq_config = config["scheduled_mode"].get(frequency, config["scheduled_mode"]["weekly"])
        risk_filter = freq_config["risk_filter"]
        filtered = filter_evals_by_risk(evals, risk_filter)
        if "spot_check_count" in freq_config:
            filtered = add_spot_check(filtered, freq_config["spot_check_count"])

    else:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)

    # Run each eval (placeholder - actual implementation needs LLM runner)
    results = []
    for eval_dict in filtered:
        # Placeholder: would call actual skill runner here
        output = ""  # TODO: actual output from skill execution
        agent_trace = []  # TODO: actual agent trace

        result = run_single_eval(eval_dict, output, agent_trace)
        results.append(result)

    return results


def write_results_tsv(results: list[dict[str, Any]], output_path: Path) -> None:
    """Write results to TSV file."""
    header = "eval_id\tpass\tdate\tversion\teval_mode\tseverity\treviewer\tnotes\n"
    lines = [header]

    for r in results:
        line = f"{r['eval_id']}\t{r['pass']}\t{r['timestamp'][:10]}\tci-run\t{r['grader']}\t{r['risk']}\tauto\t{r['reason']}\n"
        lines.append(line)

    output_path.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Evals based on CI mode")
    parser.add_argument("--mode", required=True, choices=["pr", "release", "scheduled"],
                        help="CI mode (pr/release/scheduled)")
    parser.add_argument("--skill", required=True, help="Skill name to evaluate")
    parser.add_argument("--frequency", choices=["weekly", "monthly", "quarterly"],
                        help="Frequency for scheduled mode")
    parser.add_argument("--skill-base-path", default="plugins/frontend-team-toolkit/skills",
                        help="Base path for skills directory")
    parser.add_argument("--output", default="results.tsv", help="Output results file")

    args = parser.parse_args()

    # Resolve skill base path
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    skill_base_path = repo_root / args.skill_base_path

    results = run_evals(args.mode, args.skill, skill_base_path, args.frequency)
    write_results_tsv(results, Path(args.output))

    # Print summary
    print(f"\n## Eval CI Results ({args.mode} mode)\n")
    print("| Eval ID | Type | Risk | Grader | Pass |")
    print("|---------|------|------|--------|:----:|")
    for r in results:
        print(f"| {r['eval_id']} | {r['type']} | {r['risk']} | {r['grader']} | {r['pass']} |")

    # Summary stats
    passed = len([r for r in results if r["pass"] == "✅"])
    failed = len([r for r in results if r["pass"] == "❌"])
    pending = len([r for r in results if r["pass"] == "⚠️"])

    print(f"\n**Summary**: {passed} PASS, {failed} FAIL, {pending} PENDING")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())