# Week 5 Decision Memo — What Decision Follows?

## Decision

**Do NOT adopt CrewAI** for the current single-procedure scope of the Khedma project.

Continue with the **manual ReAct agent** from Week 4.

## Evidence

The comparison between the two implementations showed:

| **Aspect** | **Manual Agent** | **CrewAI** |
| :--- | :--- | :--- |
| Latency (1 run) | ~2s per turn | 57.46s |
| State visibility | ✅ Full (`self.state`) | ❌ Hidden |
| Trace format | ✅ Structured JSON | ⚠️ Verbose console |
| Turn cap | ✅ Exact (5) | ⚠️ Approximate |
| Failure tests | ✅ 4 pytest tests | ❌ None |
| Setup lines | ~150 | ~50 |

**The manual agent is faster, more observable, and more controllable.**

## Engineering Decision That Follows

1. **For Week 6 (RAG):** Continue with the manual agent, adding a retrieval layer (TF-IDF or embeddings).
2. **For Week 7 (Planning):** Test 3 planning strategies within the manual agent.
3. **For Week 8 (Multi-Agent):** Re-evaluate CrewAI, since its orchestration strengths (roles, handoffs, critic) become essential at that scope.
4. **Keep `crewai_agent.py` in the repo** as documented evidence of this comparison.

## Lesson Learned

**Frameworks are not shortcuts.** They trade control and observability for setup speed. For a safety-critical, single-procedure project like Khedma, **direct control of the agent loop is more valuable than framework convenience.**

A framework earns its abstraction only when its features (multi-agent orchestration, built-in tools, persistence) are actually needed — not by default.