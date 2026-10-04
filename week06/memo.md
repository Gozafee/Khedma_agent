# Week 6 Decision Memo — At What Cost?

## Decision
Added a **RAG layer** to the Khedma agent using TF-IDF retrieval over an 8-document knowledge base, and generated grounded answers via Ollama (`yousif-khedma`).

## Costs Measured

| **Metric** | **Without RAG** | **With RAG** | **Delta** |
| :--- | :--- | :--- | :--- |
| Avg Tokens/Query | ~80 | **194** | +142% |
| Avg Latency/Query | ~5s | **30.39s** | +507% |
| Answer Grounding | ❌ None | ✅ Cited (`[doc_xxx]`) | Improved |
| Hallucination Risk | High | Low | Improved |

## Evaluation Results (evals/v2)

- **Retrieval Hit Rate:** 100% (5/5 queries)
- **Answer Correctness:** 100% (keyword check)
- **Citation Correctness:** 100% (doc IDs cited)

## Engineering Decisions

1. **Adopt RAG** for all future queries — grounding is critical for government-service answers.
2. **Keep TF-IDF** as the retrieval backbone — sufficient accuracy at zero API cost.
3. **Optimize later:** Consider embeddings/reranking in Week 7 or 8 if latency becomes an issue.

## Lesson Learned

**RAG is expensive but necessary.** The 5× latency and 2.4× token cost are acceptable trade-offs for grounded, verifiable answers in a safety-critical domain like government services.

Without RAG, the agent could hallucinate procedures or fees. With RAG, every claim cites a specific document.