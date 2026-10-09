# Week 9 - Peer Walkthrough Notes

## Setup

**Peer name:** [Name of peer who reviewed the system]
**Date:** 2026-10-09
**Duration:** ~10 minutes

## Walkthrough Flow

1. Showed the **prepare_recommendation** step — the agent retrieves docs and drafts an answer, but does NOT submit.
2. Showed the **approval gate** — the draft is held until the user explicitly types "approve" or "reject".
3. Showed the **reversible action** — after approval, the user can undo within the session.
4. Showed the **audit log** — every action is timestamped with actor and details.

## Where the Peer Hesitated

| **Point** | **Question / Hesitation** | **Our Response** |
| :--- | :--- | :--- |
| **1. Approval scope** | "Is 'approve' per message or per session?" | Per recommendation. Each new query requires a fresh approval. |
| **2. Undo window** | "How long can I undo?" | Currently within the same session only. No persistent storage. |
| **3. Audit visibility** | "Can I see the audit log as a user?" | Only as a file (`audit_log.json`). No UI yet. |
| **4. Rejection path** | "What happens if I reject?" | The draft is discarded and the query returns to the user for rephrasing. |
| **5. Actor field** | "Who is 'user' vs 'agent' in the log?" | 'user' = human input, 'agent' = automated LLM actions. |

## Peer Feedback

- **Positive:** The audit trail is clear and traceable.
- **Positive:** The approval gate is well-isolated from the LLM.
- **Suggestion:** Add an interactive CLI so the user can type "approve" live.
- **Suggestion:** Show the audit log after each action in a "Recent Activity" panel.

## Action Items

1. ✅ Add interactive CLI (see `interactive_demo.py`).
2. ⏳ Add UI for audit log (future work).
3. ⏳ Extend undo window to 24h (persistent storage).