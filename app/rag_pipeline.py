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

        # 1. Retrieve relevant documents
        results = self.retriever.retrieve(
            query=query,
            top_k=5,
        )
        
        confidence = self.confidence.evaluate(
            results
        )
        if not confidence["should_answer"]:
            return{
                "answer":("The provided documents do not contain sufficient information to answer the query."),
                "sources": results,
                "confidence":confidence,
            }

        # 2. Build context
        context, used_results = build_context(
            results
        )

        # 3. Generate answer
        answer = self.generator.generate(
            query=query,
            context=context,
        )

        return {
            "answer": answer,
            "sources": used_results,
            "confidence":confidence,
        }