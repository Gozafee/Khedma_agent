# Week 8: Single-Agent vs. Multi-Agent Comparison

## Setup

**Queries tested:** 2 (conditions + fees)
**Single-Agent:** Week 6 RAG agent (retrieve + answer in 1 LLM call)
**Multi-Agent Crew:** 4 agents (Researcher → Analyst → Writer → Critic)
**Model:** `yousif-khedma` (ALLaM 7B via Ollama)

---

## Per-Query Results

| **Agent** | **Query** | **Hit?** | **Answer OK?** | **Tokens** | **Latency (s)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| single | ما شروط تجديد جواز السفر؟ | ✅ | ✅ | 242 | 58.34 |
| single | كم رسوم تجديد جواز السفر؟ | ✅ | ✅ | 158 | 23.62 |
| crew | ما شروط تجديد جواز السفر؟ | ✅ | ✅ | 1380 | 236.86 |
| crew | كم رسوم تجديد جواز السفر؟ | ✅ | ❌ | 770 | 128.99 |

---

## Aggregated Metrics

| **Metric** | **Single-Agent** | **Multi-Agent Crew** | **Delta** |
| :--- | :--- | :--- | :--- |
| Avg Tokens | 200 | 1075 | **+438%** |
| Avg Latency (s) | 40.98 | 182.93 | **+346%** |
| Retrieval Hit Rate | 100% | 100% | = |
| Answer Correctness | **100%** | **50%** | **−50%** |

---

## Why the Crew Failed

### Query: "كم رسوم تجديد جواز السفر؟" (How much is the renewal fee?)

**Expected:** 5000 جنيه

**Crew's flow:**
1. **Researcher** retrieved `doc_002` ✅ (contains "5000 جنيه")
2. **Analyst** summarized the doc but **dropped the number**
3. **Writer** wrote a generic answer without the fee
4. **Critic** approved (checked sources, not numbers)

**Result:** User gets no specific fee. **Answer = wrong.**

---

## Failure Propagation
