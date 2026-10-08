"""
Week 8 - Multi-Agent Crew
A 4-agent crew: Researcher -> Analyst -> Writer -> Critic.
Each agent has a specific role. The Critic can reject and trigger a rewrite.
"""
import os
import sys
import time
import ollama

# Add week06 to path to reuse the retrieval system
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))

from retrieval import RetrievalSystem


class MultiAgentCrew:
    """4-agent crew: Researcher, Analyst, Writer, Critic."""

    def __init__(self, retriever, model_name="yousif-khedma", max_rewrites=1):
        self.retriever = retriever
        self.model_name = model_name
        self.max_rewrites = max_rewrites
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

    # ---------- Agent 1: Researcher ----------
    def _researcher(self, query):
        """Retrieve relevant documents from the knowledge base."""
        docs = self.retriever.retrieve(query, top_k=3)
        retrieved_ids = [d["doc_id"] for d in docs]

        # Researcher summarizes the retrieved content
        context = "\n\n".join(
            [f"[{d['doc_id']}] {d['title']}\n{d['content']}" for d in docs]
        )
        prompt = (
            "أنت باحث. لخّص المعلومات التالية في 3-5 نقاط أساسية:\n\n"
            f"{context}"
        )
        summary, tokens = self._call_llm(prompt)

        return {
            "retrieved_ids": retrieved_ids,
            "context": context,
            "summary": summary,
            "tokens": tokens,
        }

    # ---------- Agent 2: Analyst ----------
    def _analyst(self, query, research):
        """Analyze the researcher's summary and extract key facts."""
        prompt = (
            "أنت محلل. اقرأ الملخص التالي واستخرج الحقائق الأساسية "
            "المرتبطة بسؤال المستخدم.\n\n"
            f"السؤال: {query}\n"
            f"الملخص:\n{research['summary']}\n\n"
            "أجب بقائمة قصيرة من الحقائق، مع ذكر أرقام المستندات."
        )
        analysis, tokens = self._call_llm(prompt)
        return {"analysis": analysis, "tokens": tokens}

    # ---------- Agent 3: Writer ----------
    def _writer(self, query, analysis):
        """Write the final answer based on the analysis."""
        prompt = (
            "أنت كاتب. اكتب إجابة واضحة ومباشرة للمستخدم بناءً على التحليل التالي.\n\n"
            f"السؤال: {query}\n"
            f"التحليل:\n{analysis['analysis']}\n\n"
            "أجب بالعربية الفصحى، واذكر أرقام المستندات (مثلاً [doc_001])."
        )
        draft, tokens = self._call_llm(prompt)
        return {"draft": draft, "tokens": tokens}

    # ---------- Agent 4: Critic ----------
    def _critic(self, query, draft):
        """Review the draft; accept or reject."""
        prompt = (
            "أنت ناقد صارم. راجع الإجابة التالية.\n\n"
            f"السؤال: {query}\n"
            f"الإجابة:\n{draft['draft']}\n\n"
            "هل الإجابة: 1) مبنية على المستندات؟ 2) تذكر المصادر؟ 3) دقيقة؟\n"
            "أجب بـ 'موافق' أو 'مرفوض' فقط."
        )
        verdict, tokens = self._call_llm(prompt)
        is_approved = "موافق" in verdict and "مرفوض" not in verdict
        return {"verdict": verdict, "approved": is_approved, "tokens": tokens}

    # ---------- Main flow ----------
    def ask(self, query):
        """Run the full crew flow: Researcher -> Analyst -> Writer -> Critic."""
        start = time.time()
        total_tokens = 0

        # 1. Researcher
        research = self._researcher(query)
        total_tokens += research["tokens"]

        # 2. Analyst
        analysis = self._analyst(query, research)
        total_tokens += analysis["tokens"]

        # 3. Writer
        draft = self._writer(query, analysis)
        total_tokens += draft["tokens"]

        # 4. Critic
        critique = self._critic(query, draft)
        total_tokens += critique["tokens"]

        rewrites = 0
        final_answer = draft["draft"]

        # 5. If rejected, rewrite (bounded by max_rewrites)
        while not critique["approved"] and rewrites < self.max_rewrites:
            rewrite_prompt = (
                "أعد كتابة الإجابة التالية مع تحسين الدقة والمصادر:\n\n"
                f"{draft['draft']}"
            )
            rewritten, tokens = self._call_llm(rewrite_prompt)
            total_tokens += tokens
            final_answer = rewritten
            rewrites += 1
            # Re-check
            critique = self._critic(query, {"draft": final_answer})
            total_tokens += critique["tokens"]

        latency = time.time() - start

        # Log to trace
        self.trace.append({
            "agent": "crew",
            "query": query,
            "retrieved": research["retrieved_ids"],
            "rewrites": rewrites,
            "approved": critique["approved"],
            "tokens": total_tokens,
            "latency": latency,
        })

        return {
            "answer": final_answer,
            "retrieved": research["retrieved_ids"],
            "rewrites": rewrites,
            "approved": critique["approved"],
            "tokens": total_tokens,
            "latency": latency,
        }


# --- Manual test ---
if __name__ == "__main__":
    retriever = RetrievalSystem()
    crew = MultiAgentCrew(retriever)

    query = "ما شروط تجديد جواز السفر؟"
    print(f"Query: {query}\n")

    result = crew.ask(query)

    print(f"Retrieved: {result['retrieved']}")
    print(f"Rewrites: {result['rewrites']}")
    print(f"Approved: {result['approved']}")
    print(f"Tokens: {result['tokens']}")
    print(f"Latency: {result['latency']:.2f}s")
    print(f"\nAnswer:\n{result['answer']}")