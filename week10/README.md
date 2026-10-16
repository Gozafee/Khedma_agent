# Week 10 — Security & Red-Team

## Status: ✅ Complete

## Objective
Threat-model the Khedma agent against the OWASP Agentic Top 10 and defend against indirect prompt injection.

## Deliverables
- `vulnerable_agent.py` — agent that blindly trusts retrieved docs
- `patched_agent.py` — agent with 3-layer defense
- `red_team.py` — attack runner
- `red_team_results.json` — raw results
- `security_report.md` — full threat model + Red-Green matrix
- `memo.md` — Decision memo

## Threat Model
Focused on **ASI01 (Agent Goal Hijacking)** via **Indirect Prompt Injection**.

The attacker poisons a retrieved document with a hidden instruction: