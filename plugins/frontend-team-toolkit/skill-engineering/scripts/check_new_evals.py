#!/usr/bin/env python3
"""
Check New Evals - Verify new Evals have baseline before merge.

Usage:
    python scripts/check_new_evals.py --skill <skill_name> --results results.tsv

Exit codes:
    0: All new Evals have baseline
    1: New Evals without baseline found (BLOCK merge)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def load_evals(skill_path: Path) -> list[dict[str, str]]:
    """Load evals.json for a skill."""
    evals_path = skill_path / "evals" / "evals.json"
    if evals_path.exists():
        doc = json.loads(evals_path.read_text(encoding="utf-8"))
        return doc.get("evals", [])
    return []


def load_results_ids(results_path: Path) -> set[str]:
    """Load existing eval IDs from results.tsv."""
    if not results_path.exists():
        return set()

    ids = set()
    with open(results_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            ids.add(row.get("eval_id", "").strip())

    return ids


def main() -> int:
    parser = argparse.ArgumentParser(description="Check new Evals have baseline")
    parser.add_argument("--skill", required=True, help="Skill name")
    parser.add_argument("--results", required=True, help="Path to results.tsv")
    parser.add_argument("--skill-base-path", default="plugins/frontend-team-toolkit/skills",
                        help="Base path for skills directory")
    parser.add_argument("--block", type=bool, default=True,
                        help="Whether to block on missing baseline (default: true)")

    args = parser.parse_args()

    # Resolve paths
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    skill_base_path = repo_root / args.skill_base_path
    skill_path = skill_base_path / args.skill
    results_path = Path(args.results)

    # Load evals and results
    evals = load_evals(skill_path)
    existing_ids = load_results_ids(results_path)

    # Find new Evals
    new_evals = [e for e in evals if e.get("id") not in existing_ids]

    if new_evals:
        print(f"\n❌ NEW EVALS NOT BASELINED: {len(new_evals)} new Eval(s) without baseline\n")
        for e in new_evals:
            print(f"  - {e.get('id')}: {e.get('name', 'unnamed')}")

        if args.block:
            print("\n**BLOCK**: Merge blocked - new Evals require baseline")
            sys.exit(1)
        else:
            print("\n**WARN**: New Evals without baseline (not blocking)")
            sys.exit(0)

    else:
        print("\n✅ NEW EVALS BASELINED: All Evals have baseline records")
        sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())