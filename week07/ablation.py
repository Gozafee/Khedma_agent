"""
Week 7 - Ablation Study
Runs the same eval set under 3 planning strategies:
- direct (baseline)
- decomposed
- plan_critic

Also injects one retrieval failure to test recovery.
Produces a comparison table (success, tokens, latency).
"""
import json
import os
import sys

# Add week06 and week07 to path
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from retrieval import RetrievalSystem
from agent_planning import KhedmaAgentPlanning


# Reuse the same eval set from Week 6
EVAL_CASES = [
    {"query": "شنو المستندات المطلوبة لتجديد الجواز؟",
     "expected_doc": "doc_001",
     "expected_keywords": ["جواز", "هوية", "صور"]},
    {"query": "كم رسوم تجديد جواز السفر؟",
     "expected_doc": "doc_002",
     "expected_keywords": ["5000", "جنيه", "رسوم"]},
    {"query": "كم تستغرق مدة تجديد الجواز؟",
     "expected_doc": "doc_003",
     "expected_keywords": ["أسبوع", "مدة"]},
    {"query": "ما شروط تجديد جواز السفر؟",
     "expected_doc": "doc_004",
     "expected_keywords": ["شروط", "هوية", "ساري"]},
    {"query": "كيف أجدد الجواز وأنا خارج السودان؟",
     "expected_doc": "doc_006",
     "expected_keywords": ["سفارة", "قنصلية", "خارج"]},
]


def evaluate_strategy(agent, strategy, simulate_failure=False):
    """Run all eval cases for one strategy and return aggregate metrics."""
    results = []
    for case in EVAL_CASES:
        r = agent.ask(
            case["query"],
            strategy=strategy,
            simulate_failure=simulate_failure,
        )

        retrieved_ids = [d["doc_id"] for d in r["docs"]]
        hit = case["expected_doc"] in retrieved_ids
        answer_ok = any(kw in r["answer"] for kw in case["expected_keywords"])

        results.append({
            "hit": hit,
            "answer_ok": answer_ok,
            "tokens": r["tokens"],
            "latency": r["latency"],
            "recovered": r["recovered"],
        })

    n = len(results)
    return {
        "strategy": strategy,
        "simulate_failure": simulate_failure,
        "hit_rate": sum(r["hit"] for r in results) / n * 100,
        "answer_correctness": sum(r["answer_ok"] for r in results) / n * 100,
        "avg_tokens": sum(r["tokens"] for r in results) / n,
        "avg_latency": sum(r["latency"] for r in results) / n,
        "recovery_rate": sum(r["recovered"] for r in results) / n * 100,
    }


def print_table(rows):
    """Print a clean comparison table."""
    print("\n" + "=" * 90)
    print("📊 ABLATION RESULTS")
    print("=" * 90)
    print(f"{'Strategy':<15} {'Fail?':<6} {'Hit%':<8} {'Answer%':<10} "
          f"{'Tokens':<10} {'Latency(s)':<12} {'Recovered%':<12}")
    print("-" * 90)
    for r in rows:
        print(
            f"{r['strategy']:<15} "
            f"{str(r['simulate_failure']):<6} "
            f"{r['hit_rate']:<8.0f} "
            f"{r['answer_correctness']:<10.0f} "
            f"{r['avg_tokens']:<10.0f} "
            f"{r['avg_latency']:<12.2f} "
            f"{r['recovery_rate']:<12.0f}"
        )
    print("=" * 90)


if __name__ == "__main__":
    retriever = RetrievalSystem()
    agent = KhedmaAgentPlanning(retriever)

    all_rows = []

    # Run each strategy with normal conditions
    for strat in ["direct", "decomposed", "plan_critic"]:
        print(f"\n🔧 Running strategy: {strat} (no failure)")
        row = evaluate_strategy(agent, strat, simulate_failure=False)
        all_rows.append(row)

    # Inject retrieval failure for each strategy
    for strat in ["direct", "decomposed", "plan_critic"]:
        print(f"\n💥 Running strategy: {strat} (WITH injected retrieval failure)")
        row = evaluate_strategy(agent, strat, simulate_failure=True)
        all_rows.append(row)

    print_table(all_rows)

    # Save results to JSON
    output_path = os.path.join(os.path.dirname(__file__), "ablation_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_rows, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Results saved to {output_path}")

    # Save trace
    trace_path = os.path.join(os.path.dirname(__file__), "recovery_trace.json")
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump(agent.trace, f, indent=2, ensure_ascii=False)
    print(f"✅ Trace saved to {trace_path}")