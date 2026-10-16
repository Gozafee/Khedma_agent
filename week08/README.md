# Week 08 — Single-Agent vs. Multi-Agent

## Status: ✅ Complete

## Objective
Test whether adding a multi-agent crew improves quality, and at what cost.

## Deliverables
- `single_agent.py` — single tool-using agent (baseline)
- `multi_agent.py` — 4-agent crew (Researcher → Analyst → Writer → Critic)
- `comparison.py` — full comparison runner
- `comparison_results.json` — raw results
- `comparison.md` — detailed comparison
- `memo.md` — Decision memo

## Results

| Metric | Single-Agent | Multi-Agent Crew | Delta |
| :--- | :--- | :--- | :--- |
| Avg Tokens | 200 | **1075** | **+438%** |
| Avg Latency | 40.98s | **182.93s** | **+346%** |
| Retrieval Hit Rate | 100% | 100% | = |
| Answer Correctness | **100%** | **50%** | **−50%** |

## Key Finding
**Multi-agent was WORSE, not just more expensive.**
- 5.4× more tokens
- 4.5× slower
- 50% less accurate

**Root cause:** Context loss across agents. The Analyst dropped a number, the Writer couldn't recover it, and the Critic didn't catch it.

## Decision
**Reject multi-agent** for Khedma's current single-procedure scope.

Revisit when:
- Scope expands to 10+ procedures
- Genuinely different skill sets are needed

## How to Run