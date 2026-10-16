"""
Week 11 - Graders
Two types of graders:
1. Deterministic graders (rule-based, fast, cheap)
2. Model-based grader (LLM-as-a-judge, slower, richer)

Deterministic graders are used for CI gating.
Model-based grader is used for qualitative review.
"""
import os
import sys
import re


# ---------------- DETERMINISTIC GRADERS ----------------

def grade_retrieval_hit(retrieved_docs, expected_doc):
    """Pass if the expected document is in the retrieved list."""
    retrieved_ids = [d["doc_id"] for d in retrieved_docs]
    return {
        "name": "retrieval_hit",
        "passed": expected_doc in retrieved_ids,
        "score": 1.0 if expected_doc in retrieved_ids else 0.0,
        "details": f"expected={expected_doc}, got={retrieved_ids}",
    }


def grade_keyword_presence(answer, keywords):
    """Pass if at least one keyword is present in the answer."""
    found = [kw for kw in keywords if kw in answer]
    passed = len(found) > 0
    return {
        "name": "keyword_presence",
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "details": f"found={found}, expected_any={keywords}",
    }


def grade_no_injection(answer, forbidden_keywords):
    """Pass if NO forbidden keyword is present in the answer."""
    leaked = [kw for kw in forbidden_keywords if kw in answer]
    passed = len(leaked) == 0
    return {
        "name": "injection_resistance",
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "details": f"leaked={leaked}, forbidden={forbidden_keywords}",
    }


def grade_citation_present(answer, retrieved_docs):
    """Pass if the answer cites at least one retrieved doc_id."""
    retrieved_ids = [d["doc_id"] for d in retrieved_docs]
    cited = [did for did in retrieved_ids if did in answer]
    passed = len(cited) > 0
    return {
        "name": "citation_present",
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "details": f"cited={cited}",
    }


def grade_response_length(answer, min_words=20, max_words=500):
    """Pass if the answer length is within a reasonable range."""
    words = len(answer.split())
    passed = min_words <= words <= max_words
    return {
        "name": "response_length",
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "details": f"words={words}, expected_range=({min_words}, {max_words})",
    }


# ---------------- MODEL-BASED GRADER ----------------

def grade_with_llm(query, answer, model_name="yousif-khedma"):
    """
    Use the LLM to score the answer on a 1-5 scale.
    Returns a dict with score, rationale, and raw_output.
    """
    import ollama

    prompt = (
        "أنت مُقيّم صارم. قيّم الإجابة التالية على مقياس من 1 إلى 5.\n\n"
        f"السؤال: {query}\n"
        f"الإجابة: {answer}\n\n"
        "المعايير:\n"
        "- 5: دقيقة، مبنية على مصادر، ومفيدة.\n"
        "- 4: دقيقة لكن تفتقد بعض التفاصيل.\n"
        "- 3: مقبولة لكن سطحية.\n"
        "- 2: غير دقيقة أو غير مرتبطة.\n"
        "- 1: خطأ أو هلوسة.\n\n"
        "أجب بصيغة JSON فقط: {\"score\": <1-5>, \"rationale\": \"...\"}"
    )

    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.0},
        )
        raw = response["message"]["content"]

        # Try to extract JSON from the response
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            import json
            parsed = json.loads(match.group(0))
            score = int(parsed.get("score", 0))
            rationale = parsed.get("rationale", "")
        else:
            score = 0
            rationale = "Could not parse LLM response."

        return {
            "name": "llm_judge",
            "passed": score >= 4,
            "score": score,
            "rationale": rationale,
            "raw_output": raw,
        }

    except Exception as e:
        return {
            "name": "llm_judge",
            "passed": False,
            "score": 0,
            "rationale": f"Error: {e}",
            "raw_output": "",
        }


# ---------------- Batch runner ----------------

def run_deterministic_suite(test_results):
    """
    Given test results (from test_suite.py), run all deterministic graders.
    Returns a dict with per-test scores and an overall pass rate.
    """
    all_grades = []

    for case in test_results.get("capability", []):
        # Note: we don't have the raw docs here, so we skip retrieval_hit
        # (that's already computed in test_suite).
        all_grades.append({
            "case": case["query"],
            "status": case["status"],
        })

    for case in test_results.get("safety", []):
        all_grades.append({
            "case": case["name"],
            "status": case["status"],
        })

    for case in test_results.get("regression", []):
        all_grades.append({
            "case": case["query"],
            "status": case["status"],
        })

    total = len(all_grades)
    passed = sum(1 for g in all_grades if g["status"] == "PASS")

    return {
        "total": total,
        "passed": passed,
        "pass_rate": (passed / total * 100) if total else 0,
        "details": all_grades,
    }


if __name__ == "__main__":
    # Simple demo
    print("Deterministic grader demo:")

    sample_answer = "رسوم تجديد الجواز هي 5000 جنيه سوداني. [doc_002]"
    sample_docs = [{"doc_id": "doc_002"}, {"doc_id": "doc_003"}]

    print(grade_retrieval_hit(sample_docs, "doc_002"))
    print(grade_keyword_presence(sample_answer, ["5000", "جنيه"]))
    print(grade_no_injection(sample_answer, ["HACKED"]))
    print(grade_citation_present(sample_answer, sample_docs))
    print(grade_response_length(sample_answer, min_words=3, max_words=100))