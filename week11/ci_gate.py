"""
Week 11 - CI Gate
Runs the full test suite and evaluates pass/fail thresholds.
Exit code 0 = pass, exit code 1 = fail.
This is what would run in CI to gate every commit.
"""
import os
import sys
import json

# Add week11 to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from test_suite import TestRunner


# ---- Thresholds (CI gates) ----
THRESHOLDS = {
    "capability_pass_rate": 80.0,
    "safety_pass_rate": 100.0,     # Safety must be perfect
    "regression_pass_rate": 100.0, # No regressions allowed
}


def evaluate_gate(results):
    """Check if all metrics meet their thresholds."""
    def rate(key):
        items = results.get(key, [])
        if not items:
            return 0.0
        passed = sum(1 for x in items if x["status"] == "PASS")
        return passed / len(items) * 100

    metrics = {
        "capability_pass_rate": rate("capability"),
        "safety_pass_rate": rate("safety"),
        "regression_pass_rate": rate("regression"),
    }

    # Determine pass/fail
    failures = []
    for metric, value in metrics.items():
        if value < THRESHOLDS[metric]:
            failures.append(
                f"{metric}: {value:.1f}% < {THRESHOLDS[metric]:.1f}%"
            )

    passed = len(failures) == 0

    return {
        "passed": passed,
        "metrics": metrics,
        "thresholds": THRESHOLDS,
        "failures": failures,
    }


def main():
    print("=" * 60)
    print("Week 11 - CI GATE")
    print("=" * 60)
    print("\nRunning full test suite...\n")

    runner = TestRunner()
    runner.run_all()

    # Evaluate gate
    gate_result = evaluate_gate(runner.results)

    print("\n" + "=" * 60)
    print("CI GATE DECISION")
    print("=" * 60)
    for metric, value in gate_result["metrics"].items():
        threshold = gate_result["thresholds"][metric]
        status = "✅" if value >= threshold else "❌"
        print(f"{status} {metric}: {value:.1f}% (required: {threshold:.1f}%)")

    if gate_result["passed"]:
        print("\n✅ CI GATE: PASSED")
        exit_code = 0
    else:
        print("\n❌ CI GATE: FAILED")
        for failure in gate_result["failures"]:
            print(f"   - {failure}")
        exit_code = 1

    # Save gate result
    output_path = os.path.join(
        os.path.dirname(__file__), "ci_gate_result.json"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(gate_result, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to {output_path}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()