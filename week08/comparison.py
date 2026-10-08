"""
Week 8 - Single-Agent vs. Multi-Agent Comparison
Runs both systems on the same queries and compares:
- Quality (answer correctness)
- Cost (tokens)
- Latency (seconds)
- Failure propagation
"""
import os
import sys
import json
import time

# Add paths
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from retrieval import RetrievalSystem
from single_agent import SingleAgent
from multi_agent import MultiAgentCrew


# Same eval cases (2 queries for speed)
EVAL_CASES = [
    {
        "query": "ما شروط تجديد جواز السفر؟",
        "expected_doc": "doc_004",
        "expected_keywords": ["هوية", "ساري", "شروط"],
    },
    {
        "query": "كم رسوم تجديد جواز السفر؟",
        "expected_doc": "doc_002",
        "expected_keywords": ["5000", "جنيه"],
    },
]


def evaluate(agent_type, agent, query, expected_doc, expected_keywords):
    """Run one query and evaluate the answer."""
    result = agent.ask(query)

    retrieved = result["retrieved"]
    hit = expected_doc in retrieved
    answer_ok = any(kw in result["answer"] for kw in expected_keywords)

    return {
        "agent_type": agent_type,
        "query": query,
        "hit": hit,
        "answer_ok": answer_ok,
        "tokens": result["tokens"],
        "latency": result["latency"],
    }


def print_table(rows):
    """Print a comparison table."""
    print("\n" + "=" * 90)
    print("SINGLE-AGENT vs MULTI-AGENT")
    print("=" * 90)
    print(f"{'Agent':<15} {'Query':<40} {'Hit?':<6} {'Answer?':<8} "
          f"{'Tokens':<10} {'Latency(s)':<12}")
    print("-" * 90)
    for r in rows:
        q_short = r["query"][:37] + "..." if len(r["query"]) > 37 else r["query"]
        print(
            f"{r['agent_type']:<15} "
            f"{q_short:<40} "
            f"{str(r['hit']):<6} "
            f"{str(r['answer_ok']):<8} "
            f"{r['tokens']:<10} "
            f"{r['latency']:<12.2f}"
        )
    print("=" * 90)


def aggregate(rows, agent_type):
    """Aggregate metrics per agent type."""
    subset = [r for r in rows if r["agent_type"] == agent_type]
    n = len(subset)
    return {
        "agent_type": agent_type,
        "avg_tokens": sum(r["tokens"] for r in subset) / n,
        "avg_latency": sum(r["latency"] for r in subset) / n,
        "hit_rate": sum(r["hit"] for r in subset) / n * 100,
        "answer_rate": sum(r["answer_ok"] for r in subset) / n * 100,
    }


if __name__ == "__main__":
    retriever = RetrievalSystem()

    print("=" * 90)
    print("Week 8 - Single-Agent vs. Multi-Agent Comparison")
    print("=" * 90)

    single = SingleAgent(retriever)
    crew = MultiAgentCrew(retriever)

    all_rows = []

    # Run single agent
    print("\n[Phase 1] Running Single-Agent baseline...")
    for case in EVAL_CASES:
        print(f"   Query: {case['query'][:50]}...")
        row = evaluate(
            "single", single,
            case["query"], case["expected_doc"], case["expected_keywords"],
        )
        all_rows.append(row)

    # Run multi-agent crew
    print("\n[Phase 2] Running Multi-Agent crew...")
    for case in EVAL_CASES:
        print(f"   Query: {case['query'][:50]}...")
        row = evaluate(
            "crew", crew,
            case["query"], case["expected_doc"], case["expected_keywords"],
        )
        all_rows.append(row)

    # Print table
    print_table(all_rows)

    # Aggregated metrics
    single_agg = aggregate(all_rows, "single")
    crew_agg = aggregate(all_rows, "crew")

    print("\n" + "=" * 90)
    print("AGGREGATED METRICS")
    print("=" * 90)
    print(f"{'Metric':<25} {'Single':<15} {'Crew':<15} {'Delta'}")
    print("-" * 90)

    # Tokens
    tok_delta = (crew_agg["avg_tokens"] - single_agg["avg_tokens"]) / single_agg["avg_tokens"] * 100
    print(f"{'Avg Tokens':<25} {single_agg['avg_tokens']:<15.0f} "
          f"{crew_agg['avg_tokens']:<15.0f} {tok_delta:+.0f}%")

    # Latency
    lat_delta = (crew_agg["avg_latency"] - single_agg["avg_latency"]) / single_agg["avg_latency"] * 100
    print(f"{'Avg Latency (s)':<25} {single_agg['avg_latency']:<15.2f} "
          f"{crew_agg['avg_latency']:<15.2f} {lat_delta:+.0f}%")

    # Hit rate
    print(f"{'Retrieval Hit Rate (%)':<25} {single_agg['hit_rate']:<15.0f} "
          f"{crew_agg['hit_rate']:<15.0f}")

    # Answer correctness
    print(f"{'Answer Correctness (%)':<25} {single_agg['answer_rate']:<15.0f} "
          f"{crew_agg['answer_rate']:<15.0f}")

    print("=" * 90)

    # Save results
    output = {
        "rows": all_rows,
        "single_agg": single_agg,
        "crew_agg": crew_agg,
    }
    output_path = os.path.join(os.path.dirname(__file__), "comparison_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to {output_path}")