# ADR-001: Adopt or Reject CrewAI for Khedma Project

## Status
**Accepted** (date: 2026-09-29)

## Context

In Week 4, I built a manual ReAct agent (`KhedmaAgent`) using:
- A custom `ModelClient` seam (MockModelClient + OllamaModelClient).
- Explicit `while` loop with a 5-turn cap and 5000-token budget.
- `pytest` tests proving failure conditions (runaway loop, hallucination, budget).
- Structured `trace.log` (JSON) for full auditability.

In Week 5, I rebuilt the same agent using **CrewAI** (v1.15.23) with:
- A single `Agent` with role, goal, and backstory.
- A single `Task` with strict extraction rules.
- The `yousif-khedma` model (ALLaM 7B) via Ollama's OpenAI-compatible endpoint.

Both agents were tested on the same task: extracting `name`, `national_id`, `reason`, and `location` from Arabic user input.

## Decision

**Do NOT adopt CrewAI** for the current single-procedure scope of the Khedma project.

CrewAI will be **re-evaluated in Week 8 (Multi-Agent)** when its orchestration features become essential.

## Evidence

| **Criterion** | **Manual Agent (Week 4)** | **CrewAI + Ollama (Week 5)** |
| :--- | :--- | :--- |
| State visibility | ✅ Full (`self.state`) | ❌ Hidden inside Crew |
| Control flow | ✅ Explicit while loop | ⚠️ Implicit (Process.sequential) |
| Trace quality | ✅ Structured JSON | ⚠️ Verbose console only |
| Turn cap | ✅ Exact (5) | ⚠️ Approximate (`max_iter`) |
| Failure controls | ✅ pytest-proven | ❌ Not built-in |
| Latency (1 run) | ✅ ~2s per turn | ❌ ~57s |
| Token overhead | ✅ Low | ❌ High (framework prompts) |
| Setup complexity | ❌ Manual (~150 lines) | ✅ Fast (~50 lines) |
| Multi-agent ready | ❌ Custom work needed | ✅ Built-in |

**Measured result (CrewAI):**
```json
{
  "name": "يوسف عبدالمنعم",
  "national_id": "123456",
  "reason": "مسافر",
  "location": "not specified"
}