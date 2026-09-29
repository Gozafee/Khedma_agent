# Week 5: Manual Agent vs. CrewAI

## Overview

This document compares two implementations of the same Khedma agent:

- **Manual Agent** (Week 4): Hand-built ReAct loop with `MockModelClient` and `OllamaModelClient`.
- **CrewAI Agent** (Week 5): Same agent rebuilt using the CrewAI framework with Ollama (`yousif-khedma` model).

Both agents perform the same task: extracting `name`, `national_id`, `reason`, and `location` from Arabic user input for Sudanese passport renewal.

---

## Comparison Table

| **Criterion** | **Manual Agent (Week 4)** | **CrewAI + Ollama (Week 5)** |
| :--- | :--- | :--- |
| **State Visibility** | ✅ Full control (`self.state` dict directly accessible) | ❌ Hidden inside `Crew` and `Task` objects |
| **Control Flow** | ✅ Explicit `while` loop with clear stop conditions | ⚠️ Implicit — managed by `Process.sequential` |
| **Trace Quality** | ✅ Structured `trace.log` with per-turn entries (turn, input, extracted, result, tokens) | ⚠️ Verbose console output (rich panels), not structured data |
| **Token Overhead** | ✅ Low — only 1 LLM call per turn | ❌ Higher — framework adds prompt templates and system messages |
| **Turn Cap** | ✅ Exact (`self.max_turns = 5`) | ⚠️ Approximate (`max_iter=5` — not strictly enforced) |
| **Failure Detection** | ✅ Explicit keywords ("هالوسة") and budget checks | ❌ No built-in failure controls |
| **Arabic Quality** | ✅ Controlled (MockModel) / Good (Ollama) | ✅ Excellent (via `yousif-khedma` = ALLaM 7B) |
| **Setup Complexity** | ❌ Manual — needs more code to maintain | ✅ Fast to write using framework abstractions |
| **Multi-Agent Ready** | ❌ Would need custom orchestration | ✅ Built-in support (roles, tasks, handoffs) |
| **Latency (measured)** | ~2 seconds per turn | ~57 seconds for one full run |
| **Cost** | Free (Mock) / Free (Local Ollama) | Free (Local Ollama) |

---

## Measured Evidence

### Manual Agent (Week 4)

**Input:** `"اسمي يوسف، رقم هويتي 123456، أريد تجديد الجواز للسفر، أنا في الخرطوم"`

**Output:**