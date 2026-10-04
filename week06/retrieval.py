"""
Retrieval system for Khedma project.
Uses TF-IDF to retrieve relevant documents from the knowledge base.
"""
import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RetrievalSystem:
    """TF-IDF based retrieval system for the Khedma knowledge base."""

    def __init__(self, kb_path: str = "knowledge_base.json"):
        """Load knowledge base and build TF-IDF index."""
        # Locate knowledge base file relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, kb_path)

        # Load documents from JSON
        with open(full_path, "r", encoding="utf-8") as f:
            self.kb = json.load(f)

        self.documents = self.kb["documents"]

        # Combine title and content for indexing
                # Combine keywords + title + content for better retrieval
        self.doc_texts = [
            f"{doc.get('keywords', '')} {doc['title']} {doc['content']}"
            for doc in self.documents
        ]

        # Build TF-IDF index
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 4),
            min_df=1,
        )
        self.doc_vectors = self.vectorizer.fit_transform(self.doc_texts)

        print(f"[RetrievalSystem] Indexed {len(self.documents)} documents")

    def retrieve(self, query: str, top_k: int = 2) -> list:
        """Return top_k most relevant documents for a query."""
        # Convert query to TF-IDF vector
        query_vector = self.vectorizer.transform([query])

        # Compute cosine similarity against all documents
        similarities = cosine_similarity(query_vector, self.doc_vectors)[0]

        # Get indices of top_k scores (descending)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        # Build results list (only include matches with score > 0)
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                results.append({
                    "doc_id": self.documents[idx]["id"],
                    "title": self.documents[idx]["title"],
                    "content": self.documents[idx]["content"],
                    "score": float(similarities[idx]),
                })

        return results


# --- Manual test (run this file directly to verify) ---
if __name__ == "__main__":
    retriever = RetrievalSystem()

    test_queries = [
        "شنو المستندات المطلوبة لتجديد الجواز؟",
        "كم رسوم تجديد الجواز؟",
        "كم مدة تجديد الجواز؟",
    ]

    for q in test_queries:
        print(f"\n📥 Query: {q}")
        results = retriever.retrieve(q)
        for r in results:
            print(f"   → [{r['doc_id']}] {r['title']} (score: {r['score']:.3f})")