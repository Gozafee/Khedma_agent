# Week 4 Decision Memo

## 1. Runaway Loop
- Condition: Incomplete data repeatedly.
- Handling: Stops at turn 5.
- Evidence: test_stops_after_5_turns passes.

## 2. Hallucinated Tool
- Condition: Non-existent tool call.
- Handling: Detects keyword "هالوسة".
- Evidence: test_hallucination_detection passes.

## 3. Budget Exhaustion
- Condition: Token usage > 5000.
- Handling: Stops and shows budget message.
- Evidence: test_token_budget passes.

## Conclusion
All failure conditions proven with pytest.
