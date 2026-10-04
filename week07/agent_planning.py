"""
Khedma Agent - Week 7
Implements 3 planning strategies:
- direct: retrieve once, then answer
- decomposed: break query into sub-goals, retrieve per sub-goal
- plan_critic: plan, execute, critique, re-plan if needed

Also supports failure injection (simulated retrieval failure).
"""
import os
import time
import sys
import ollama

# Add week06 to path so we can import the retrieval system
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))

from retrieval import RetrievalSystem


class KhedmaAgentPlanning:
    """RAG agent with 3 planning strategies."""

    def __init__(self, retriever, model_name="yousif-khedma"):
        self.retriever = retriever
        self.model_name = model_name
        self.trace = []

    # ---------- Helper: build context string from docs ----------
    def _build_context(self, docs):
        parts = []
        for doc in docs:
            parts.append(f"[{doc['doc_id']}] {doc['title']}\n{doc['content']}")
        return "\n\n".join(parts)

    # ---------- Helper: call the LLM ----------
    def _llm(self, prompt, temperature=0.0):
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": temperature},
        )
        return response["message"]["content"]

    # ---------- Strategy 1: DIRECT ----------
    def _run_direct(self, query, simulate_failure=False):
        """Retrieve once, answer directly."""
        docs = [] if simulate_failure else self.retriever.retrieve(query, top_k=3)

        if not docs:
            # Fallback when retrieval fails
            answer = self._llm(
                f"سؤال المستخدم: {query}\n"
                "لم أتمكن من الوصول إلى قاعدة المعرفة. أجب بتحذير واضح."
            )
            return {"answer": answer, "docs": [], "recovered": False}

        context = self._build_context(docs)
        prompt = (
            "أنت مساعد لتجديد جواز السفر السوداني.\n"
            f"المعلومات:\n{context}\n\n"
            f"السؤال: {query}\n"
            "أجب بالعربية واذكر رقم المستند."
        )
        answer = self._llm(prompt)
        return {"answer": answer, "docs": docs, "recovered": False}

    # ---------- Strategy 2: DECOMPOSED ----------
    def _run_decomposed(self, query, simulate_failure=False):
        """Break query into sub-questions, retrieve per sub-question, then synthesize."""
        # Step 1: Ask the LLM to decompose the query
        decomp_prompt = (
            "قسّم السؤال التالي إلى 2-3 أسئلة فرعية قصيرة، كل سؤال في سطر.\n"
            f"السؤال: {query}"
        )
        decomp_text = self._llm(decomp_prompt)
        sub_questions = [
            q.strip("-•* \t")
            for q in decomp_text.splitlines()
            if q.strip()
        ][:3]

        # Step 2: Retrieve for each sub-question
        all_docs = {}
        for sub_q in sub_questions:
            if simulate_failure:
                continue
            for d in self.retriever.retrieve(sub_q, top_k=2):
                all_docs[d["doc_id"]] = d

        if not all_docs:
            answer = self._llm(
                f"السؤال الأصلي: {query}\n"
                "فشل الاسترجاع لكل الأسئلة الفرعية. أجب بتحذير."
            )
            return {"answer": answer, "docs": [], "recovered": False}

        # Step 3: Synthesize final answer
        docs_list = list(all_docs.values())
        context = self._build_context(docs_list)
        final_prompt = (
            "أنت مساعد لتجديد جواز السفر السوداني.\n"
            f"المعلومات:\n{context}\n\n"
            f"السؤال الأصلي: {query}\n"
            "أجب بالعربية واذكر أرقام المستندات."
        )
        answer = self._llm(final_prompt)
        return {"answer": answer, "docs": docs_list, "recovered": False}

    # ---------- Strategy 3: PLAN + CRITIC ----------
    def _run_plan_critic(self, query, simulate_failure=False):
        """Plan, execute, critique, and re-plan if the critic rejects."""
        # Step 1: Plan
        plan_prompt = (
            "ضع خطة قصيرة (خطوات مرقمة) للإجابة على السؤال التالي.\n"
            f"السؤال: {query}"
        )
        plan = self._llm(plan_prompt)

        # Step 2: Execute the plan (retrieve)
        docs = [] if simulate_failure else self.retriever.retrieve(query, top_k=3)

        if not docs:
            # Fallback: re-plan with broader retrieval
            fallback_docs = self.retriever.retrieve(query[:20], top_k=3)
            if fallback_docs:
                docs = fallback_docs
                recovered = True
            else:
                answer = self._llm(
                    f"السؤال: {query}\n"
                    "فشل الاسترجاع. أجب بتحذير واضح."
                )
                return {"answer": answer, "docs": [], "recovered": False}
        else:
            recovered = False

        # Step 3: Generate initial answer
        context = self._build_context(docs)
        draft_prompt = (
            "أنت مساعد لتجديد جواز السفر السوداني.\n"
            f"المعلومات:\n{context}\n\n"
            f"السؤال: {query}\n"
            "أجب بالعربية واذكر أرقام المستندات."
        )
        draft = self._llm(draft_prompt)

        # Step 4: Critic reviews the draft
        critic_prompt = (
            "راجع الإجابة التالية. هل هي مبنية على المستندات؟ "
            "هل تذكر مصادرها؟ أجب بـ 'موافق' أو 'مرفوض' مع سبب قصير.\n\n"
            f"الإجابة: {draft}"
        )
        critique = self._llm(critic_prompt)

        # Step 5: If critic rejects, re-plan with a broader query
        if "مرفوض" in critique:
            more_docs = self.retriever.retrieve(query[:15], top_k=3)
            all_docs = {d["doc_id"]: d for d in docs}
            for d in more_docs:
                all_docs[d["doc_id"]] = d
            docs = list(all_docs.values())
            context = self._build_context(docs)
            final_prompt = (
                "أعد كتابة الإجابة بناءً على المستندات التالية:\n"
                f"{context}\n\nالسؤال: {query}"
            )
            draft = self._llm(final_prompt)
            recovered = True

        return {"answer": draft, "docs": docs, "recovered": recovered}

    # ---------- Public API ----------
    def ask(self, query, strategy="direct", simulate_failure=False):
        """Run the agent with the chosen strategy."""
        start = time.time()

        if strategy == "direct":
            result = self._run_direct(query, simulate_failure)
        elif strategy == "decomposed":
            result = self._run_decomposed(query, simulate_failure)
        elif strategy == "plan_critic":
            result = self._run_plan_critic(query, simulate_failure)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        latency = time.time() - start
        tokens = len(result["answer"].split())

        # Log to trace
        self.trace.append({
            "strategy": strategy,
            "query": query,
            "simulate_failure": simulate_failure,
            "retrieved": [d["doc_id"] for d in result["docs"]],
            "recovered": result["recovered"],
            "latency": latency,
            "tokens": tokens,
        })

        return {
            "answer": result["answer"],
            "docs": result["docs"],
            "recovered": result["recovered"],
            "latency": latency,
            "tokens": tokens,
        }


# --- Manual test ---
if __name__ == "__main__":
    retriever = RetrievalSystem()
    agent = KhedmaAgentPlanning(retriever)

    query = "شنو المستندات المطلوبة لتجديد جواز السفر؟"
    print(f"📥 Query: {query}\n")

    for strat in ["direct", "decomposed", "plan_critic"]:
        print(f"\n{'=' * 60}")
        print(f"🔧 Strategy: {strat}")
        print("=" * 60)
        r = agent.ask(query, strategy=strat)
        print(f"📄 Docs: {[d['doc_id'] for d in r['docs']]}")
        print(f"⏱️  Latency: {r['latency']:.2f}s")
        print(f"🔢 Tokens: {r['tokens']}")
        print(f"💬 Answer:\n{r['answer'][:300]}...")