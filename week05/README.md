# Week 05 — CrewAI Framework Comparison + ADR

## Status: ✅ Complete

## Objective
Rebuild the Week 4 manual agent in CrewAI and compare.

## Deliverables
- CrewAI agent implementation (`crewai_agent.py`)
- 4-criteria comparison (`comparison.md`)
- Architecture Decision Record (`ADR.md`)
- Decision memo (`memo.md`)

## Comparison Criteria
1. State Visibility
2. Control Flow
3. Trace Quality
4. Token Overhead

## Decision
**Reject CrewAI** for single-procedure scope.
- Cost: 5.4× more tokens
- Latency: 4.5× slower
- State: hidden inside framework

## How to Run