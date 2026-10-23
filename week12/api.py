"""
Week 12 - Deployment (AgentOps)
Exposes the Khedma RAG agent via a FastAPI endpoint with:
- Token budget enforcement
- Request timeout
- Health check
- Cost & latency tracking
"""
import os
import sys
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add week06 to path for the RAG agent
WEEK06_DIR = os.path.join(os.path.dirname(__file__), "..", "week06")
sys.path.insert(0, os.path.abspath(WEEK06_DIR))

from retrieval import RetrievalSystem
from agent_rag import KhedmaAgentRAG

# Initialize FastAPI app
app = FastAPI(title="Khedma Agent API", version="1.0")

# Initialize the agent once at startup
retriever = RetrievalSystem()
agent = KhedmaAgentRAG(retriever)


# --- Configuration ---
MAX_TOKENS_PER_REQUEST = 1000
TIMEOUT_SECONDS = 120
COST_PER_1K_TOKENS = 0.0  # Local Ollama is free

# Track metrics
metrics = {
    "total_requests": 0,
    "total_tokens": 0,
    "total_latency": 0.0,
    "failed_requests": 0,
}


# --- Request/Response Models ---
class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    tokens: int
    latency: float
    retrieved_docs: list


# --- Endpoints ---

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": "yousif-khedma",
        "documents_indexed": len(retriever.documents),
    }


@app.post("/ask", response_model=QueryResponse)
def ask_agent(request: QueryRequest):
    """Main endpoint: receive a query, return a grounded answer."""
    global metrics

    start_time = time.time()

    try:
        # Run the RAG agent
        result = agent.ask(request.query)
        latency = time.time() - start_time

        # Enforce token budget
        if result["tokens"] > MAX_TOKENS_PER_REQUEST:
            metrics["failed_requests"] += 1
            raise HTTPException(
                status_code=429,
                detail=f"Token budget exceeded: {result['tokens']} > {MAX_TOKENS_PER_REQUEST}",
            )

        # Enforce timeout
        if latency > TIMEOUT_SECONDS:
            metrics["failed_requests"] += 1
            raise HTTPException(
                status_code=504,
                detail=f"Request timeout: {latency:.1f}s > {TIMEOUT_SECONDS}s",
            )

        # Update metrics
        metrics["total_requests"] += 1
        metrics["total_tokens"] += result["tokens"]
        metrics["total_latency"] += latency

        return QueryResponse(
            answer=result["answer"],
            tokens=result["tokens"],
            latency=round(latency, 2),
            retrieved_docs=[d["doc_id"] for d in result["retrieved_docs"]],
        )

    except HTTPException:
        raise
    except Exception as e:
        metrics["failed_requests"] += 1
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def get_metrics():
    """Return aggregated metrics."""
    avg_latency = (
        metrics["total_latency"] / metrics["total_requests"]
        if metrics["total_requests"] > 0
        else 0
    )
    return {
        **metrics,
        "avg_latency": round(avg_latency, 2),
        "estimated_cost_usd": round(
            (metrics["total_tokens"] / 1000) * COST_PER_1K_TOKENS, 4
        ),
    }