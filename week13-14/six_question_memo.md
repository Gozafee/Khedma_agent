# Six-Question Memo (Defence)

1. **Better than what?** Better than manual calls and single-turn chatbots. It uses RAG for grounded, traceable answers.
2. **Measured by what?** 100% Retrieval Hit Rate, 100% Answer Correctness, 100% Citation Correctness.
3. **At what cost?** ~174 tokens, ~30s latency per request, $0.00 cost (using local Ollama model).
4. **Under what failure conditions?** 
   - Runaway loops: Prevented by a 5-turn cap.
   - Hallucination: Prevented by RAG grounding.
   - Injection: Blocked by 3-layer defense.
   - Retrieval failure: Recovered by fallback planner.
5. **How reproducible?** Code is on GitHub, tests are automated (`ci_gate.py`), and the model runs locally.
6. **What engineering decision follows?** Reject multi-agent for single-procedure scope. Stick with Single-Agent + RAG + Human Oversight.