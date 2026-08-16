from app.api.server import query
from app.retrieval.multi_query_retriever import (MultiQueryRetriever)
from app.retrieval.confidence import (RetrievalConfidence)  
from app.context_builder import build_context
from app.generation.groq_generator import GroqGenerator


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

    def ask(
    self,
    query: str,
):

        print("\n==============================")
        print("RAG QUERY STARTED")
        print(f"Query: {query}")
        print("==============================")

    # 1. Retrieve relevant documents
        print("\n[1] Starting retrieval...")

        results = self.retriever.retrieve(
            query=query,
            top_k=5,
        )

        print(f"[1] Retrieval completed. Results: {len(results)}")

        # 2. Confidence
        print("\n[2] Evaluating confidence...")

        confidence = self.confidence.evaluate(
            results
        )

        print(f"[2] Confidence: {confidence}")

        if not confidence["should_answer"]:

            print("[2] Confidence too low. Returning fallback.")

            return {
                "answer": (
                    "The provided documents do not contain "
                    "sufficient information to answer the query."
                ),
                "sources": results,
                "confidence": confidence,
            }

        # 3. Build context
        print("\n[3] Building context...")

        context, used_results = build_context(
            results
        )

        print(
            f"[3] Context built. Length: {len(context)}"
        )

        # 4. Generation
        print("\n[4] Starting LLM generation...")

        answer = self.generator.generate(
            query=query,
            context=context,
        )

        print("\n[4] LLM generation completed.")

        print("\n==============================")
        print("RAG QUERY COMPLETED")
        print("==============================")

        return {
            "answer": answer,
            "sources": used_results,
            "confidence": confidence,
        }