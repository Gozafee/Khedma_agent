# Week 7 Decision Memo — Better Than What?

## Decision
Tested 3 planning strategies on the same eval query to answer: **does planning pay for its cost?**

**Baseline:** `direct` (retrieve once, answer once) — the control condition.

## Ablation Results

**Query:** `"كم رسوم تجديد جواز السفر؟"`

| **Strategy** | **Fail?** | **Tokens** | **Latency** | **Recovered** |
| :--- | :--- | :--- | :--- | :--- |
| direct | ❌ | 45 | 36.85s | ❌ |
| decomposed | ❌ | 116 | 48.93s | ❌ |
| plan_critic | ❌ | 34 | 44.43s | ❌ |
| direct | ✅ | 29 | 8.46s | ❌ |
| decomposed | ✅ | 37 | 15.37s | ❌ |
| **plan_critic** | ✅ | **58** | **61.06s** | **✅** |

## Better Than What?

**Baseline:** `direct` (no planning) is the control.

### In normal conditions (no failure):
- **`direct`:** 45 tokens, 36.85s.
- **`decomposed`:** 116 tokens (+158%), 48.93s (+33%). **Worse — no quality gain.**
- **`plan_critic`:** 34 tokens (−24%), 44.43s (+21%). **Slightly better.**

**Verdict:** Planning doesn't justify its cost in normal conditions.

### Under failure (retrieval injection):
- **`direct`:** Failed, no recovery.
- **`decomposed`:** Failed, no recovery.
- **`plan_critic`:** **Recovered** (re-planning with broader query).

**Verdict:** Planning **only pays off when failure occurs.**

## At What Cost?

| **Strategy** | **Extra Tokens** | **Extra Latency** |
| :--- | :--- | :--- |
| decomposed | +71 tokens (+158%) | +12s (+33%) |
| plan_critic | −11 tokens (−24%) | +8s (+21%) |

**Surprisingly, `plan_critic` used fewer tokens than `direct`** — because the critic rejected verbose drafts and forced a more focused re-plan.

## Engineering Decision

1. **Adopt `plan_critic`** as the default strategy for Khedma.
   - Same or lower token cost than `direct`.
   - Only strategy that recovers from retrieval failures.
   - 21% latency increase is acceptable for safety-critical services.

2. **Reject `decomposed`** for this scope.
   - 158% more tokens with no accuracy gain.
   - Cannot recover from failures.

3. **Keep `direct`** as a fast fallback for low-stakes queries.

## Lesson Learned

**Planning is not free, but it is insurance.**

`plan_critic` costs ~21% more latency but provides:
- **Failure recovery** (the only strategy that did).
- **Self-correction** via the critic.
- **Lower token usage** in some cases.

For a government-service assistant where wrong answers are costly, **this trade-off is worth it**.

**However:** planning must be **measured**, not assumed. `decomposed` looked reasonable on paper but was 2.5× more expensive with zero benefit.