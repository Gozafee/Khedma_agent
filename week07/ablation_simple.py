"""
Week 7 - Simplified Ablation (Fast Version)
Runs 1 query x 3 strategies x 2 conditions = 6 calls (~3 min).
"""
import os
import sys
import json

# Add week06 to path
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from retrieval import RetrievalSystem
from agent_planning import KhedmaAgentPlanning


def run_one(agent, strategy, simulate_failure):
    """Run one query with one strategy."""
    query = "كم رسوم تجديد جواز السفر؟"

    print(f"\n>> Running: strategy={strategy}, failure={simulate_failure}")
    result = agent.ask(query, strategy=strategy, simulate_failure=simulate_failure)

    print(f"   Docs: {[d['doc_id'] for d in result['docs']]}")
    print(f"   Latency: {result['latency']:.2f}s")
    print(f"   Tokens: {result['tokens']}")
    print(f"   Recovered: {result['recovered']}")

    return {
        "strategy": strategy,
        "simulate_failure": simulate_failure,
        "docs": [d["doc_id"] for d in result["docs"]],
        "latency": result["latency"],
        "tokens": result["tokens"],
        "recovered": result["recovered"],
    }


if __name__ == "__main__":
    retriever = RetrievalSystem()
    agent = KhedmaAgentPlanning(retriever)

    results = []

    # Without failure
    for strat in ["direct", "decomposed", "plan_critic"]:
        results.append(run_one(agent, strat, simulate_failure=False))

    # With failure
    for strat in ["direct", "decomposed", "plan_critic"]:
        results.append(run_one(agent, strat, simulate_failure=True))

    # Print summary table
    print("\n" + "=" * 80)
    print("ABLATION SUMMARY")
    print("=" * 80)
    print(f"{'Strategy':<15} {'Fail?':<6} {'Tokens':<10} {'Latency(s)':<12} {'Recovered'}")
    print("-" * 80)
    for r in results:
        print(
            f"{r['strategy']:<15} "
            f"{str(r['simulate_failure']):<6} "
            f"{r['tokens']:<10} "
            f"{r['latency']:<12.2f} "
            f"{r['recovered']}"
        )
    print("=" * 80)

    # Save results
    output_path = os.path.join(os.path.dirname(__file__), "ablation_simple_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to {output_path}")