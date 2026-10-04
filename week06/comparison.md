# Week 6: RAG vs. No RAG Comparison

## Test Setup

**Query:** `"شنو المستندات المطلوبة لتجديد جواز السفر؟"`
**Model:** `yousif-khedma` (ALLaM 7B via Ollama)

---

## Results

| **Aspect** | **Without RAG** | **With RAG** |
| :--- | :--- | :--- |
| Sources Cited | ❌ None | ✅ `[doc_001]`, `[doc_004]` |
| Groundedness | ❌ General knowledge only | ✅ Based on knowledge base |
| Tokens | ~80 | **194** |
| Latency | ~5s | **30.39s** |
| Hallucination Risk | High | Low |
| Verifiability | ❌ | ✅ (user can check doc) |

---

## Grounded vs. Ungrounded Examples

### ❌ Ungrounded (No RAG)
**Prompt:** `"شنو المستندات المطلوبة لتجديد جواز السفر؟"`
**Answer:**
> "لتجديد جواز السفر، تحتاج إلى: 1) جواز السفر القديم، 2) الهوية الوطنية، 3) صور شخصية..."
**Problem:** No source. Could be hallucinated.

### ✅ Grounded (With RAG)
**Prompt:** Same query + retrieved `[doc_001]` and `[doc_004]` in context.
**Answer:**
> "استناداً إلى مستند [doc_001]، المستندات المطلوبة هي: 1) جواز السفر القديم، 2) الهوية الوطنية السارية، 3) صورتين شخصيتين، 4) شهادة الميلاد..."
**Improvement:** Specific document cited. User can verify.

---

## Key Findings

1. **RAG dramatically improves trust** — every answer cites a document.
2. **Cost is significant** — 2.4× tokens, 5× latency.
3. **TF-IDF suffices** for this small KB (8 docs).
4. **Character n-grams (2-4)** were critical for Arabic retrieval accuracy.
5. **Keywords in each document** boosted Hit Rate from 60% → 100%.

---

## Recommendation

**Adopt RAG permanently.** The cost is justified by:
- Grounding (essential for government services).
- Citations (user trust).
- Reduced hallucination risk.