from app.retrieval.multi_query_retriever import (
    MultiQueryRetriever
)

from app.retrieval.confidence import (
    RetrievalConfidence
)


retriever = MultiQueryRetriever(
    num_queries=3,
    dense_top_k=10,
    bm25_top_k=10,
)

confidence = RetrievalConfidence()


queries = [
    "Explain a scenario where harmless-looking input results in a dangerous output?",
    "What is quantum entanglement?",
]


for query in queries:

    print("\n" + "=" * 80)
    print("QUERY")
    print("=" * 80)

    print(query)

    results = retriever.retrieve(
        query=query,
        top_k=5,
    )

    evaluation = confidence.evaluate(
        results
    )

    print("\nCONFIDENCE")
    print("-" * 80)

    print(
        "Level:",
        evaluation["level"]
    )

    print(
        "Score:",
        evaluation["score"]
    )

    print(
        "Should answer:",
        evaluation["should_answer"]
    )