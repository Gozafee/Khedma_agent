# Week 9 Decision Memo — How Reproducible?

## Decision
Added three human-oversight mechanisms to the Khedma agent:
1. **Approval gate** — blocks final recommendation until human approves.
2. **Audit trail** — logs every action with timestamp, actor, and details.
3. **Reversible action** — allows the user to undo an approved recommendation within the session.

## How Reproducible Is the Audit Trail?

### Yes — Fully Reproducible

Every audit entry contains:
- `timestamp` (ISO 8601 UTC)
- `session_id` (unique per session)
- `actor` (`user` or `agent`)
- `action` (e.g., `prepare_started`, `approval_granted`)
- `details` (JSON-structured payload)

### Audit Log Sample

```json
[
  {
    "timestamp": "2026-10-09T05:40:00Z",
    "session_id": "abc12345",
    "actor": "agent",
    "action": "prepare_started",
    "details": {"query": "ما شروط تجديد جواز السفر؟"}
  },
  {
    "timestamp": "2026-10-09T05:40:05Z",
    "session_id": "abc12345",
    "actor": "user",
    "action": "approval_granted",
    "details": {"by": "user"}
  }
]