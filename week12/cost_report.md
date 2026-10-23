```markdown
# Week 12 — Cost & Latency Report

## Test Run (via Swagger UI)
**Query:** "كم رسوم تجديد جواز السفر؟"

| **Metric** | **Value** |
| :--- | :--- |
| HTTP Status | 200 (OK) |
| Tokens Consumed | 174 |
| Latency | 29.86s |
| Estimated Cost | $0.00 (Local Ollama) |

## Token Budget Enforcement
- **Max Tokens:** 1,000 per request.
- **Timeout:** 120 seconds.
- If exceeded: HTTP 429 or 504.

## Conclusion
Running on local Ollama, the cost is $0.00. The latency is acceptable for a government service where accuracy matters more than speed.