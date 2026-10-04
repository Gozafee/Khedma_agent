"""
Week 6 - Evaluation
Measures 3 metrics for the RAG agent:
1. Retrieval Hit Rate
2. Answer Correctness
3. Citation Correctness
Also saves eval cases to evals/v2.jsonl.
"""
import json
import os
from retrieval import RetrievalSystem
from agent_rag import KhedmaAgentRAG


# Evaluation test cases
EVAL_CASES = [
    {
        "query": "شنو المستندات المطلوبة لتجديد الجواز؟",
        "expected_doc": "doc_001",
        "expected_keywords": ["جواز", "هوية", "صور"],
    },
    {
        "query": "كم رسوم تجديد جواز السفر؟",
        "expected_doc": "doc_002",
        "expected_keywords": ["5000", "جنيه", "رسوم"],
    },
    {
        "query": "كم تستغرق مدة تجديد الجواز؟",
        "expected_doc": "doc_003",
        "expected_keywords": ["أسبوع", "مدة"],
    },
    {
        "query": "ما شروط تجديد جواز السفر؟",
        "expected_doc": "doc_004",
        "expected_keywords": ["شروط", "هوية", "ساري"],
    },
    {
        "query": "كيف أجدد الجواز وأنا خارج السودان؟",
        "expected_doc": "doc_006",
        "expected_keywords": ["سفارة", "قنصلية", "خارج"],
    },
]


def save_eval_set():
    """Save eval cases to evals/v2.jsonl."""
    evals_dir = os.path.join(os.path.dirname(__file__), "..", "evals")
    os.makedirs(evals_dir, exist_ok=True)

    v2_path = os.path.join(evals_dir, "v2.jsonl")
    with open(v2_path, "w", encoding="utf-8") as f:
        for case in EVAL_CASES:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")

    print(f"[Eval] Saved {len(EVAL_CASES)} cases to evals/v2.jsonl")


def run_evaluation():
    """Run all eval cases and compute metrics."""
    retriever = RetrievalSystem()
    agent = KhedmaAgentRAG(retriever)

    results = []
    for case in EVAL_CASES:
        r = agent.ask(case["query"])

        retrieved_ids = [d["doc_id"] for d in r["retrieved_docs"]]

        # Metric 1: Retrieval Hit Rate
        hit = case["expected_doc"] in retrieved_ids

        # Metric 2: Answer Correctness (keywords present)
        answer_correct = any(
            kw in r["answer"] for kw in case["expected_keywords"]
        )

        # Metric 3: Citation Correctness (any retrieved doc cited)
        cited = any(did in r["answer"] for did in retrieved_ids)

        results.append({
            "query": case["query"],
            "expected": case["expected_doc"],
            "retrieved": retrieved_ids,
            "hit": hit,
            "answer_correct": answer_correct,
            "citation_correct": cited,
            "tokens": r["tokens"],
            "latency": r["latency"],
        })

        # Print per-case summary
        status = "✅" if hit else "❌"
        print(f"{status} Query: {case['query'][:40]}... "
              f"| Retrieved: {retrieved_ids} "
              f"| Expected: {case['expected_doc']}")

    # Aggregate metrics
    n = len(results)
    hit_rate = sum(r["hit"] for r in results) / n * 100
    answer_acc = sum(r["answer_correct"] for r in results) / n * 100
    citation_acc = sum(r["citation_correct"] for r in results) / n * 100
    avg_tokens = sum(r["tokens"] for r in results) / n
    avg_latency = sum(r["latency"] for r in results) / n

    print("\n" + "=" * 60)
    print("📊 WEEK 6 EVALUATION RESULTS")
    print("=" * 60)
    print(f"🎯 Retrieval Hit Rate:    {hit_rate:.1f}%")
    print(f"✅ Answer Correctness:    {answer_acc:.1f}%")
    print(f"📖 Citation Correctness:  {citation_acc:.1f}%")
    print(f"🔢 Avg Tokens/Query:      {avg_tokens:.0f}")
    print(f"⏱️  Avg Latency/Query:     {avg_latency:.2f}s")
    print("=" * 60)

    return results


if __name__ == "__main__":
    save_eval_set()
    print("\nRunning evaluation...\n")
    run_evaluation()