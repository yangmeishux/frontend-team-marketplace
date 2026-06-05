#!/usr/bin/env python3
"""
Check Regression - Verify regression Evals passed before merge.

Usage:
    python scripts/check_regression.py --results results.tsv
    python scripts/check_regression.py --results results.tsv --risk high --block true

Exit codes:
    0: All regression Evals passed
    1: Regression Evals failed (BLOCK merge)
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def load_results_tsv(results_path: Path) -> list[dict[str, str]]:
    """Load results.tsv file."""
    if not results_path.exists():
        print(f"ERROR: Results file not found: {results_path}", file=sys.stderr)
        sys.exit(1)

    results = []
    with open(results_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            results.append(row)

    return results


def check_regression(results: list[dict[str, str]], risk_filter: list[str] | None = None) -> list[dict[str, str]]:
    """Find failed regression Evals."""
    failed = []
    for r in results:
        # Check if it's a regression type
        eval_type = r.get("type", "")
        if "regression" not in eval_type.lower():
            continue

        # Check risk filter
        if risk_filter and r.get("severity", "medium") not in risk_filter:
            continue

        # Check if failed
        if r.get("pass", "").strip() in ["❌", "0", "FAIL", "false"]:
            failed.append(r)

    return failed


def main() -> int:
    parser = argparse.ArgumentParser(description="Check regression Evals")
    parser.add_argument("--results", required=True, help="Path to results.tsv")
    parser.add_argument("--risk", choices=["high", "medium", "low", "all"], default="all",
                        help="Risk level to check (default: all)")
    parser.add_argument("--block", type=bool, default=True,
                        help="Whether to block on failure (default: true)")

    args = parser.parse_args()

    results_path = Path(args.results)
    results = load_results_tsv(results_path)

    # Determine risk filter
    if args.risk == "all":
        risk_filter = None
    elif args.risk == "high":
        risk_filter = ["high"]
    elif args.risk == "medium":
        risk_filter = ["medium", "high"]  # medium includes high check
    else:
        risk_filter = ["low", "medium", "high"]

    failed = check_regression(results, risk_filter)

    if failed:
        print(f"\n❌ REGRESSION FAILED: {len(failed)} regression Eval(s) failed\n")
        for r in failed:
            print(f"  - {r.get('eval_id', 'unknown')}: {r.get('notes', 'no reason')}")

        if args.block:
            print("\n**BLOCK**: Merge blocked due to regression failure")
            sys.exit(1)
        else:
            print("\n**WARN**: Regression failure (not blocking)")
            sys.exit(0)

    else:
        print("\n✅ REGRESSION PASSED: All regression Evals passed")
        sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())