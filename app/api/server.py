from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field




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

rag_pipeline = None


def get_rag_pipeline():
    global rag_pipeline

    if rag_pipeline is None:
        print("\nInitializing RAG pipeline...")
        from app.rag_pipeline import RAGPipeline
        rag_pipeline = RAGPipeline()
        print("RAG pipeline initialized successfully!")

    return rag_pipeline


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
    print("\n==============================")
    print("POST /query RECEIVED")
    print(f"Question: {question}")
    print("==============================")
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    print(f"\n========== NEW QUERY ==========")
    print(f"Question: {question}")

    try:
        print("STEP 1: Getting RAG pipeline...")

        pipeline = get_rag_pipeline()

        print("STEP 2: RAG pipeline ready.")
        print("STEP 3: Calling pipeline.ask()...")

        result = pipeline.ask(
            query=question
        )

        print("STEP 4: pipeline.ask() completed.")
        print("STEP 5: Returning response.")

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "confidence": result["confidence"],
        }

    except Exception as error:

        print("\n========== RAG ERROR ==========")
        print(f"ERROR TYPE: {type(error).__name__}")
        print(f"ERROR: {error}")
        print("===============================\n")

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )