# Week 4 Decision Memo — Under What Failure Conditions?

## 1. Runaway Loop
- **Condition:** Incomplete data sent repeatedly.
- **Handling:** Agent stops at turn 5 (turn cap).
- **Evidence:** `test_stops_after_5_turns` passes.

## 2. Hallucinated Tool
- **Condition:** Non-existent tool call or adversarial input.
- **Handling:** Agent detects keyword "هالوسة" and flags state.
- **Evidence:** `test_hallucination_detection` passes.

## 3. Budget Exhaustion
- **Condition:** Token usage exceeds 5000.
- **Handling:** Agent stops and shows budget message.
- **Evidence:** `test_token_budget` passes.

## Conclusion
All failure conditions are proven with pytest tests, not just narrated.