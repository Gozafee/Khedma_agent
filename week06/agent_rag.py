"""
Khedma Agent with RAG - Week 6
Combines the retrieval system with Ollama to generate grounded answers.
"""
import os
import time
import ollama
from retrieval import RetrievalSystem


class KhedmaAgentRAG:
    """Agent that retrieves relevant documents before generating answers."""

    def __init__(self, retriever: RetrievalSystem, model_name: str = "yousif-khedma"):
        self.retriever = retriever
        self.model_name = model_name
        self.trace = []

    def _build_context(self, docs: list) -> str:
        """Build a context string from retrieved documents."""
        parts = []
        for doc in docs:
            parts.append(f"[{doc['doc_id']}] {doc['title']}\n{doc['content']}")
        return "\n\n".join(parts)

    def ask(self, query: str) -> dict:
        """Retrieve relevant docs then generate a grounded answer."""
        # Step 1: Retrieve
        t0 = time.time()
        docs = self.retriever.retrieve(query, top_k=3)
        retrieval_latency = time.time() - t0

        # Step 2: Build prompt with context
        context = self._build_context(docs)
        prompt = f"""أنت مساعد متخصص في تجديد جواز السفر السوداني.
استخدم المعلومات التالية للإجابة على سؤال المستخدم:

{context}

سؤال المستخدم: {query}

أجب بالعربية، واذكر رقم المستند الذي استندت إليه (مثلاً [doc_001])."""

        # Step 3: Generate answer via Ollama
        t1 = time.time()
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.0},
        )
        generation_latency = time.time() - t1

        answer = response["message"]["content"]
        tokens = len(prompt.split()) + len(answer.split())

        # Step 4: Log the trace
        self.trace.append({
            "query": query,
            "retrieved": [d["doc_id"] for d in docs],
            "retrieval_latency": retrieval_latency,
            "generation_latency": generation_latency,
            "total_latency": retrieval_latency + generation_latency,
            "tokens": tokens,
        })

        return {
            "answer": answer,
            "retrieved_docs": docs,
            "retrieval_latency": retrieval_latency,
            "generation_latency": generation_latency,
            "latency": retrieval_latency + generation_latency,
            "tokens": tokens,
        }


# --- Manual test ---
if __name__ == "__main__":
    print("=" * 60)
    print("Khedma RAG Agent - Week 6")
    print("=" * 60)

    retriever = RetrievalSystem()
    agent = KhedmaAgentRAG(retriever)

    test_query = "شنو المستندات المطلوبة لتجديد جواز السفر؟"
    print(f"\n📥 Query: {test_query}\n")

    result = agent.ask(test_query)

    print(f"📄 Retrieved: {[d['doc_id'] for d in result['retrieved_docs']]}")
    print(f"⏱️  Retrieval: {result['retrieval_latency']:.2f}s")
    print(f"⏱️  Generation: {result['generation_latency']:.2f}s")
    print(f"⏱️  Total: {result['latency']:.2f}s")
    print(f"🔢 Tokens: {result['tokens']}")
    print(f"\n💬 Answer:\n{result['answer']}")
    print("=" * 60)