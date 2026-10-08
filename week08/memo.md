# Week 8 Decision Memo — At What Cost?

## Decision
**Do NOT adopt multi-agent architecture** for the Khedma project at its current single-procedure scope.

Keep the **single-agent** implementation from Week 6/7.

## Evidence

**Setup:** 2 queries × 2 architectures (single vs. 4-agent crew).

| **Metric** | **Single-Agent** | **Multi-Agent Crew** | **Delta** |
| :--- | :--- | :--- | :--- |
| Avg Tokens | 200 | **1075** | **+438%** |
| Avg Latency (s) | 40.98 | **182.93** | **+346%** |
| Retrieval Hit Rate | 100% | 100% | = |
| **Answer Correctness** | **100%** | **50%** | **−50%** |

## What Happened?

The multi-agent crew **failed on one query** ("كم رسوم تجديد جواز السفر؟"):

- **Researcher** retrieved `doc_002` correctly.
- **Analyst** extracted the fee from the summary.
- **Writer** rephrased the answer but **lost the exact number (5000)**.
- **Critic** approved it anyway (didn't catch the missing number).

**Result:** The crew's answer was **wrong**, despite 5.4× more tokens and 4.5× more latency.

## Why Multi-Agent Failed Here

1. **Context loss across agents** — each agent rewrites the previous agent's output, and details fade.
2. **Error propagation** — if the Analyst misses a number, the Writer can't recover it.
3. **The Critic isn't a fact-checker** — it checks style/citations, not numerical accuracy.
4. **Single-procedure scope** — no genuine need for role specialization.

## At What Cost?

| **Cost Type** | **Multi-Agent Penalty** |
| :--- | :--- |
| Token cost | **+438%** (5.4× more expensive) |
| Latency | **+346%** (4.5× slower) |
| Accuracy | **−50%** (worse!) |
| Complexity | 4 agents, more failure points |

## Engineering Decision

**Reject multi-agent for Khedma's current scope.**

Reasons:
1. **No specialization benefit** — single procedure doesn't need roles.
2. **High token cost** — 5.4× more expensive for worse results.
3. **High latency** — 4.5× slower.
4. **Accuracy regression** — from 100% to 50%.
5. **Failure propagation** — errors compound across agents.

**When to revisit multi-agent:**
- When Khedma expands to **multiple procedures** (10+).
- When queries require **genuinely different skill sets** (research, legal analysis, translation).
- When the critic can be made **domain-aware** (fact-checking, not style-checking).

## Lesson Learned

**More agents ≠ better answers.**

The multi-agent crew added cost, latency, and error surface — **without improving quality**. In fact, it **degraded** quality.

The single-agent approach, with `plan_critic` from Week 7, remains the right choice for Khedma:
- Lower cost.
- Lower latency.
- Higher accuracy.
- Simpler to debug and audit.