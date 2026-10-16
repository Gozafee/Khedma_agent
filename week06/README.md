# Week 06 — RAG (Retrieval-Augmented Generation)

## Status: ✅ Complete

## Objective
Add a retrieval layer to the Khedma agent so every answer is grounded in a source document.

## Deliverables
- `knowledge_base.json` — 8 synthetic passport documents
- `retrieval.py` — TF-IDF retrieval system
- `agent_rag.py` — RAG agent using Ollama
- `evaluation.py` — 3-metric evaluation
- `comparison.md` — RAG vs No RAG
- `memo.md` — Decision memo
- `../evals/v2.jsonl` — 5 eval cases

## Metrics Measured
1. **Retrieval Hit Rate:** 100%
2. **Answer Correctness:** 100%
3. **Citation Correctness:** 100%

## Key Innovation
- Character n-grams (2-4) for Arabic retrieval
- Keywords added to each document boosted Hit Rate from 60% to 100%

## Cost
- Tokens: +142% (with RAG)
- Latency: +507% (with RAG)
- Trade-off accepted: grounding is critical for government services

## How to Run