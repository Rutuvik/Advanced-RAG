from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.rag_pipeline import RAGPipeline


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Advanced RAG API",
    description="Production-style Retrieval Augmented Generation API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Schema
# ============================================================

class QueryRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask the RAG system",
    )


# ============================================================
# Response Schema
# ============================================================

class QueryResponse(BaseModel):

    answer: str
    sources: list
    confidence: dict


# ============================================================
# Initialize RAG Pipeline
# ============================================================

print("\nStarting Advanced RAG API...")

rag_pipeline = RAGPipeline()

print("Advanced RAG API ready!")


# ============================================================
# Health Check
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Advanced RAG API is running",
        "status": "ok",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
    }


# ============================================================
# Query Endpoint
# ============================================================

@app.post(
    "/query",
    response_model=QueryResponse,
)
def query(request: QueryRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:

        result = rag_pipeline.ask(
            query=question
        )

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "confidence": result["confidence"],
        }

    except Exception as error:

        print(
            f"Error while processing query: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the query.",
        )