
from app.retrieval.multi_query_retriever import (MultiQueryRetriever)
from app.retrieval.confidence import (RetrievalConfidence)  
from app.context_builder import build_context
from app.generation.groq_generator import GroqGenerator
import time

class RAGPipeline:

    def __init__(self):

        print("\nInitializing RAG pipeline...")

        self.retriever = MultiQueryRetriever(
            num_queries=3,
            dense_top_k=10,
            bm25_top_k=10,
        )

        self.confidence = RetrievalConfidence()
        self.generator = GroqGenerator()

        print(
            "RAG pipeline initialized successfully!"
        )

    def ask(self, query: str):

        pipeline_start = time.perf_counter()

        print("\n==============================")
        print("RAG QUERY STARTED")
        print(f"Query: {query}")
        print("==============================")

        # 1. Retrieval
        retrieval_start = time.perf_counter()

        print("\n[1] Starting retrieval...")

        retrieval_result = self.retriever.retrieve(
            query=query,
            top_k=5,
        )

        results = retrieval_result["results"]
        queries = retrieval_result["queries"]
        candidate_count = retrieval_result["candidate_count"]

        retrieval_time = time.perf_counter() - retrieval_start

        print(
            f"[1] Retrieval completed. "
            f"Results: {len(results)} "
            f"Time: {retrieval_time:.3f}s"
        )

        # 2. Confidence
        confidence_start = time.perf_counter()

        print("\n[2] Evaluating confidence...")

        confidence = self.confidence.evaluate(results)

        confidence_time = (
            time.perf_counter() - confidence_start
        )

        print(f"[2] Confidence: {confidence}")

        if not confidence["should_answer"]:

            total_time = (
                time.perf_counter() - pipeline_start
            )

            return {
                "answer": (
                    "The provided documents do not contain "
                    "sufficient information to answer the query."
                ),
                "sources": results,
                "confidence": confidence,
                "retrieval": {
                    "queries": queries,
                    "query_count": len(queries),
                    "candidate_count": candidate_count,
                    "reranked_count": len(results),
                    "sources_used": len(results),
    },
                "metrics": {
                    "retrieval_time": retrieval_time,
                    "confidence_time": confidence_time,
                    "generation_time": 0,
                    "total_time": total_time,
                },
            }

        # 3. Context
        context_start = time.perf_counter()

        print("\n[3] Building context...")

        context, used_results = build_context(results)

        context_time = (
            time.perf_counter() - context_start
        )

        print(
            f"[3] Context built. "
            f"Length: {len(context)}"
        )

        # 4. Generation
        generation_start = time.perf_counter()

        print("\n[4] Starting LLM generation...")

        answer = self.generator.generate(
            query=query,
            context=context,
        )

        generation_time = (
            time.perf_counter() - generation_start
        )

        total_time = (
            time.perf_counter() - pipeline_start
        )

        print(
            f"\n[4] LLM generation completed "
            f"in {generation_time:.3f}s"
        )

        print(
            f"Total pipeline time: "
            f"{total_time:.3f}s"
        )

        return {
    "answer": answer,

    "sources": used_results,

    "confidence": confidence,

    "retrieval": {
        "queries": queries,
        "query_count": len(queries),
        "candidate_count": candidate_count,
        "reranked_count": len(results),
        "sources_used": len(used_results),
    },

    "metrics": {
        "retrieval_time": retrieval_time,
        "confidence_time": confidence_time,
        "context_time": context_time,
        "generation_time": generation_time,
        "total_time": total_time,
    },
}
        