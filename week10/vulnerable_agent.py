"""
Week 10 - Vulnerable Agent (Before Patching)
This agent is intentionally vulnerable to indirect prompt injection.
It treats retrieved document content as trusted instructions.
"""
import os
import sys
import ollama

# Add week06 for retrieval
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))

from retrieval import RetrievalSystem


class VulnerableAgent:
    """Agent that blindly trusts retrieved documents (VULNERABLE)."""

    def __init__(self, retriever, model_name="yousif-khedma"):
        self.retriever = retriever
        self.model_name = model_name

    def _call_llm(self, prompt):
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.0},
        )
        return response["message"]["content"]

    def ask(self, query):
        """Retrieve + answer, WITHOUT separating instructions from data."""
        docs = self.retriever.retrieve(query, top_k=3)

        # VULNERABILITY: document content is concatenated directly
        # into the prompt WITHOUT being marked as untrusted data.
        context = "\n\n".join(
            [f"[{d['doc_id']}] {d['title']}\n{d['content']}" for d in docs]
        )

        prompt = (
            "أنت مساعد لتجديد جواز السفر.\n"
            f"المعلومات:\n{context}\n\n"
            f"السؤال: {query}\n"
            "أجب بالعربية."
        )

        return self._call_llm(prompt)


# --- Manual test ---
if __name__ == "__main__":
    retriever = RetrievalSystem()
    agent = VulnerableAgent(retriever)

    query = "ما شروط تجديد جواز السفر؟"
    print(f"Query: {query}\n")
    print(agent.ask(query))