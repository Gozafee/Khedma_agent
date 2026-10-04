# Week 7: Planning Strategies Comparison

## Test Setup

**Query:** `"كم رسوم تجديد جواز السفر؟"`
**Model:** `yousif-khedma` (ALLaM 7B via Ollama)
**Retriever:** TF-IDF over 8 documents (Week 6 knowledge base)

**Strategies compared:**
1. **direct** — retrieve once, answer once (baseline)
2. **decomposed** — break query into sub-questions, retrieve per sub-question
3. **plan_critic** — plan, execute, critique, re-plan if the critic rejects

---

## Results Table

| **Strategy** | **Fail?** | **Tokens** | **Latency (s)** | **Recovered** |
| :--- | :--- | :--- | :--- | :--- |
| direct | ❌ | 45 | 36.85 | ❌ |
| decomposed | ❌ | 116 | 48.93 | ❌ |
| plan_critic | ❌ | 34 | 44.43 | ❌ |
| direct | ✅ | 29 | 8.46 | ❌ |
| decomposed | ✅ | 37 | 15.37 | ❌ |
| **plan_critic** | ✅ | **58** | **61.06** | **✅** |

---

## Analysis

### 1. Normal Conditions (No Failure)

| **Strategy** | **Δ Tokens vs Direct** | **Δ Latency vs Direct** |
| :--- | :--- | :--- |
| direct | Baseline | Baseline |
| decomposed | **+158%** | +33% |
| plan_critic | −24% | +21% |

**Finding:** `decomposed` is significantly more expensive with no quality gain.
`plan_critic` is slightly cheaper in tokens, but slower.

### 2. Under Failure (Retrieval Injected Failure)

| **Strategy** | **Recovered?** | **Why?** |
| :--- | :--- | :--- |
| direct | ❌ | No fallback mechanism |
| decomposed | ❌ | Sub-queries also fail |
| plan_critic | ✅ | Critic rejects → re-plan → broader retrieval |

**Finding:** `plan_critic` is the **only strategy that recovers** from retrieval failure.

---

## Key Insights

### Insight 1: Planning Is Not Free
- `decomposed` adds **+158% tokens** and **+33% latency**.
- Cost is not justified by quality (same answers as `direct`).

### Insight 2: Critic-Review Pays Off Under Failure
- Only `plan_critic` recovered when retrieval failed.
- It automatically re-planned with a broader query.

### Insight 3: Cost Is Non-Monotonic
- `plan_critic` used **fewer tokens** than `direct` in normal conditions (−24%).
- Reason: the critic rejected verbose drafts and forced conciseness.

### Insight 4: The Trade-Off Is Context-Dependent
- **Fast services** → use `direct`.
- **Safety-critical services** → use `plan_critic`.

---

## Verdict

| **Use Case** | **Recommended Strategy** |
| :--- | :--- |
| Low-stakes queries (FAQ) | `direct` |
| High-stakes queries (government services) | `plan_critic` |
| Complex multi-step queries (future) | `decomposed` (if query is truly multi-part) |

**For Khedma:** Adopt `plan_critic` as default. Keep `direct` as fallback.

---

## Reproduction

**To reproduce these results:**
```bash
cd week07
python ablation_simple.py