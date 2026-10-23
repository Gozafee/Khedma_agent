# Week 12 — Deployment (AgentOps)

## Status: ✅ Complete

## Objective
Expose the Khedma agent as a live HTTP service using FastAPI.

## Deliverables
- `api.py` — FastAPI application
- `cost_report.md` — Token cost & latency report
- `runbook.md` — How to run the service
- `memo.md` — Decision memo

## How to Run
```bash
cd week12
uvicorn api:app --reload