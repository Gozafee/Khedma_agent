# Khedma Project — Final Report

## Overview
Khedma is an AI agentic assistant for Sudanese passport renewal. It retrieves verified procedures, drafts a checklist, and requires human approval before final submission.

## Architecture
- **Agent Loop:** ReAct (Reasoning and Acting)
- **Knowledge:** TF-IDF Retrieval (8 documents)
- **Model:** ALLaM 7B (via Ollama)
- **Security:** 3-layer defense (Sanitize, Delimit, System Rules)
- **Oversight:** Approval gate + Audit trail
- **Deployment:** FastAPI with token budget

## Key Results
- Retrieval Hit Rate: 100%
- Answer Correctness: 100%
- Safety Tests: 100%
- CI Gate: PASSED
- Cost: $0.00 (local model)

## Limitations
- Single procedure only (passport renewal).
- Synthetic data only (no real government APIs).
- Arabic text only.