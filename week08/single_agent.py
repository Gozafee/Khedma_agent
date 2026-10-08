"""
Week 8 - Single-Agent Baseline
A single tool-using agent that retrieves documents and generates an answer.
This is the baseline against which the multi-agent crew is compared.
"""
import os
import sys
import time
import ollama

# Add week06 to path to reuse the retrieval system
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))

from retrieval import RetrievalSystem


class SingleAgent:
    """Single tool-using agent: retrieve + answer."""

    def __init__(self, retriever, model_name="yousif-khedma"):
        self.retriever = retriever
        self.model_name = model_name
        self.trace = []
        self.total_tokens = 0

    def _call_llm(self, prompt, temperature=0.0):
        """Call the LLM and count approximate tokens."""
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": temperature},
        )
        answer = response["message"]["content"]
        tokens = len(prompt.split()) + len(answer.split())
        self.total_tokens += tokens
        return answer, tokens

    def ask(self, query):
        """Retrieve then answer in one LLM call."""
        start = time.time()

        # Step 1: Retrieve
        docs = self.retriever.retrieve(query, top_k=3)
        retrieved_ids = [d["doc_id"] for d in docs]

        # Step 2: Build context
        context = "\n\n".join(
            [f"[{d['doc_id']}] {d['title']}\n{d['content']}" for d in docs]
        )

        # Step 3: Generate answer
        prompt = (
            "أنت مساعد متخصص في تجديد جواز السفر السوداني.\n"
            f"المعلومات:\n{context}\n\n"
            f"السؤال: {query}\n"
            "أجب بالعربية واذكر أرقام المستندات."
        )

        answer, tokens = self._call_llm(prompt)
        latency = time.time() - start

        # Log to trace
        self.trace.append({
            "agent": "single",
            "query": query,
            "retrieved": retrieved_ids,
            "tokens": tokens,
            "latency": latency,
        })

        return {
            "answer": answer,
            "retrieved": retrieved_ids,
            "tokens": tokens,
            "latency": latency,
        }


# --- Manual test ---
if __name__ == "__main__":
    retriever = RetrievalSystem()
    agent = SingleAgent(retriever)

    query = "ما شروط تجديد جواز السفر؟"
    print(f"Query: {query}\n")

    result = agent.ask(query)

    print(f"Retrieved: {result['retrieved']}")
    print(f"Tokens: {result['tokens']}")
    print(f"Latency: {result['latency']:.2f}s")
    print(f"\nAnswer:\n{result['answer']}")