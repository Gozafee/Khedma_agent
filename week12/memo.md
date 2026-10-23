
```markdown
# Week 12 Decision Memo — At What Cost?

## Decision
Exposed the Khedma agent via FastAPI with a strict token budget (1,000) and timeout (120s).

## Measured Cost
- Tokens per request: ~174
- Latency per request: ~29.86s
- Cost (Local Ollama): $0.00

## Production Cost (Hypothetical)
If using OpenAI `gpt-4o-mini`:
- Input: ~150 tokens @ $0.15/1M
- Output: ~24 tokens @ $0.60/1M
- **Total:** ~$0.000037 per request
- At 10,000 requests/day: ~$0.37/day

## Lesson Learned
An API endpoint turns a script into a product. The addition of a token budget and timeout ensures that a runaway agent cannot exhaust resources.