"""
Week 9 - Human Oversight
An agent with:
1. Approval Gate: blocks final recommendation until human approves.
2. Audit Trail: logs every action with timestamp and rationale.
3. Reversible Action: allows the user to undo a submitted recommendation.
"""
import os
import sys
import json
import time
import uuid
from datetime import datetime

import ollama

# Add week06 path for retrieval
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))

from retrieval import RetrievalSystem


class AgentWithGates:
    """RAG agent with approval gate, audit trail, and reversible actions."""

    def __init__(self, retriever, model_name="yousif-khedma"):
        self.retriever = retriever
        self.model_name = model_name
        self.session_id = str(uuid.uuid4())[:8]
        self.audit_log = []
        self.last_recommendation = None  # For reversal

    # ---------- Audit log ----------
    def _log(self, action, details, actor="agent"):
        """Append an entry to the audit trail."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "session_id": self.session_id,
            "actor": actor,
            "action": action,
            "details": details,
        }
        self.audit_log.append(entry)
        print(f"  [AUDIT] {actor} -> {action}")

    # ---------- LLM call ----------
    def _call_llm(self, prompt):
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.0},
        )
        return response["message"]["content"]

    # ---------- Step 1: Prepare recommendation (no submission yet) ----------
    def prepare_recommendation(self, query):
        """Retrieve + generate a DRAFT recommendation. Does NOT submit."""
        self._log("prepare_started", {"query": query})

        # Retrieve
        docs = self.retriever.retrieve(query, top_k=3)
        retrieved_ids = [d["doc_id"] for d in docs]
        self._log("retrieved_documents", {"docs": retrieved_ids})

        # Build context
        context = "\n\n".join(
            [f"[{d['doc_id']}] {d['title']}\n{d['content']}" for d in docs]
        )

        # Generate draft
        prompt = (
            "أنت مساعد متخصص في تجديد جواز السفر السوداني.\n"
            f"المعلومات:\n{context}\n\n"
            f"السؤال: {query}\n"
            "أجب بالعربية واذكر أرقام المستندات."
        )
        draft = self._call_llm(prompt)
        self._log("draft_generated", {"draft_length": len(draft)})

        # Store as pending (NOT submitted)
        self.last_recommendation = {
            "query": query,
            "draft": draft,
            "docs": retrieved_ids,
            "status": "pending_approval",
        }

        return self.last_recommendation

    # ---------- Step 2: Approval gate ----------
    def request_approval(self, user_input):
        """
        Present the draft and wait for user decision.
        user_input: "approve" or "reject"
        """
        if self.last_recommendation is None:
            raise ValueError("No recommendation pending approval.")

        self._log(
            "approval_requested",
            {"draft_preview": self.last_recommendation["draft"][:100]},
        )

        if user_input.lower() == "approve":
            self.last_recommendation["status"] = "approved"
            self._log(
                "approval_granted",
                {"by": "user"},
                actor="user",
            )
            return {"status": "approved", "recommendation": self.last_recommendation}

        elif user_input.lower() == "reject":
            self.last_recommendation["status"] = "rejected"
            self._log(
                "approval_rejected",
                {"by": "user"},
                actor="user",
            )
            return {"status": "rejected", "recommendation": None}

        else:
            raise ValueError("Invalid input. Use 'approve' or 'reject'.")

    # ---------- Step 3: Reversible action ----------
    def undo_recommendation(self):
        """
        Revert an approved recommendation within the session.
        This is the reversible action.
        """
        if self.last_recommendation is None:
            raise ValueError("Nothing to undo.")

        if self.last_recommendation["status"] != "approved":
            raise ValueError("Only approved recommendations can be undone.")

        self.last_recommendation["status"] = "reverted"
        self._log(
            "recommendation_reverted",
            {"by": "user", "previous_status": "approved"},
            actor="user",
        )
        return {"status": "reverted", "recommendation": self.last_recommendation}

    # ---------- Audit export ----------
    def export_audit(self, path="audit_log.json"):
        """Save the audit trail to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.audit_log, f, indent=2, ensure_ascii=False)
        print(f"\n  [AUDIT] Saved to {path}")


# --- Manual test ---
if __name__ == "__main__":
    print("=" * 60)
    print("Week 9 - Agent with Human Oversight")
    print("=" * 60)

    retriever = RetrievalSystem()
    agent = AgentWithGates(retriever)

    query = "ما شروط تجديد جواز السفر؟"
    print(f"\nQuery: {query}\n")

    # Step 1: Prepare (no submission)
    print("--- Step 1: Prepare Recommendation ---")
    rec = agent.prepare_recommendation(query)
    print(f"  Draft preview: {rec['draft'][:150]}...")
    print(f"  Status: {rec['status']}\n")

    # Step 2: Approval gate
    print("--- Step 2: Approval Gate ---")
    print("  (In real use, the user would read the draft and approve/reject)")
    result = agent.request_approval("approve")
    print(f"  Result: {result['status']}\n")

    # Step 3: Reversible action
    print("--- Step 3: Reversible Action ---")
    undo_result = agent.undo_recommendation()
    print(f"  Undo result: {undo_result['status']}\n")

    # Export audit
    print("--- Step 4: Export Audit Trail ---")
    agent.export_audit(os.path.join(os.path.dirname(__file__), "audit_log.json"))

    print("\n" + "=" * 60)
    print("Demo complete. Check audit_log.json for full trail.")
    print("=" * 60)