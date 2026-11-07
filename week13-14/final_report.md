
Project: Khedma - FINAL REPORT- Intelligent Agentic Assistant for Sudanese Government Services
1. EXECUTIVE SUMMARY
Khedma is an intelligent, agentic AI assistant designed to simplify Sudanese civil procedures, specifically focusing on passport renewal. The system utilizes a Retrieval-Augmented Generation (RAG) architecture to ground its answers in verified documentation, a ReAct loop for iterative reasoning, and human-in-the-loop oversight to ensure safety and accountability. The project evolved from a manual ReAct loop into a robust API-deployed system with enterprise-grade security and CI-gated evaluation.

2. PROBLEM STATEMENT
In Sudan, citizens face a maze of inconsistent information and bureaucratic delays when renewing passports. Word-of-mouth is unreliable, and official resources are often inaccessible. Khedma solves this by providing a conversational agent that retrieves exact requirements, checks prerequisites, and builds a verified checklist.

3. SYSTEM ARCHITECTURE
1. Agent Loop: Custom ReAct implementation with strict turn caps (max 5) and token budgets (max 1000) to prevent runaway execution.
2. Knowledge Layer (RAG): TF-IDF retrieval system indexing 8 synthetic passport documents. Character n-grams (2-4) were specifically tuned for Arabic accuracy.
3. Language Model: ALLaM 7B (via Ollama), selected for its superior Arabic capabilities and local execution (zero API cost).
4. Human Oversight: A mandatory approval gate that pauses the agent before final submission, accompanied by a full audit trail.
5. Security: A 3-layer defense mechanism (Sanitization, Delimitation, System Rules) designed to block Indirect Prompt Injection attacks (OWASP ASI01).
6. Deployment: FastAPI service with health checks, timeout enforcement, and real-time token/cost metrics.

4. EVALUATION AND RESULTS
Evaluation was consolidated into a CI-gated suite (Capability, Safety, Regression):
- Retrieval Hit Rate: 100% (Target: >= 90%)
- Answer Correctness: 100% (Target: 100%)
- Citation Correctness: 100% (Target: 100%)
- Safety Tests (Injection): 100% (Target: 100%)
- CI Gate Status: PASSED

5. KEY ENGINEERING DECISIONS
5.1 Single-Agent vs. Multi-Agent
A 4-agent crew (Researcher, Analyst, Writer, Critic) was built and tested. The crew consumed 438% more tokens and was 50% less accurate due to context loss across agents. Therefore, multi-agent architecture was rejected for this single-procedure scope.

5.2 Planning Strategy
Ablation testing showed that a plan_critic approach was the only strategy that successfully recovered from a simulated retrieval failure, at a cost of +21% latency.

5.3 Security
Testing proved that while the vulnerable agent survived injection attacks by luck (model resistance), the patched agent survived by design (architectural defense).

6. LIMITATIONS
1. Single Procedure: Currently scoped only to passport renewal.
2. Synthetic Data: The knowledge base is simulated; the system is advisory and not connected to real government APIs.
3. Language: Arabic text-only (no voice or multilingual support).

7. CONCLUSION
Khedma demonstrates that combining RAG, robust security, and human oversight creates a reliable and safe AI agent for public services. The system successfully degrades gracefully under failure and strictly adheres to safety guardrails.
