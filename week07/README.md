# Week 07 — Planning Ablation

## Status: ✅ Complete

## Objective
Test whether adding a planning layer improves the agent — and at what cost.

## Deliverables
- `agent_planning.py` — 3 planning strategies
- `ablation_simple.py` — fast ablation runner
- `ablation.py` — full ablation (documented but not run end-to-end)
- `ablation_simple_results.json` — raw results
- `comparison.md` — strategy comparison
- `memo.md` — Decision memo

## Strategies Compared
1. **direct** — retrieve once, answer once (baseline)
2. **decomposed** — break query into sub-questions
3. **plan_critic** — plan → execute → critique → re-plan

## Results

| Strategy | Tokens | Latency | Recovered (on failure) |
| :--- | :--- | :--- | :--- |
| direct | 45 | 36.85s | ❌ |
| decomposed | 116 | 48.93s | ❌ |
| **plan_critic** | **58** | 61.06s | ✅ |

## Key Finding
**`plan_critic` is the only strategy that recovers from retrieval failure.**
- Cost: +21% latency
- Benefit: self-correction + recovery

## Decision
Adopt `plan_critic` as default. Keep `direct` as a fast fallback.

## How to Run