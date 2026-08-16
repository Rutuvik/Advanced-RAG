from app.retrieval.hybrid_retriever import HybridRetriever


print("\nInitializing Hybrid Retriever...")

retriever = HybridRetriever(
    dense_top_k=10,
    bm25_top_k=10,
    rrf_k=60,
    rerank_top_k=5,
)

print("\nHybrid Retriever initialized!")


queries = [
    "What is prompt injection?",
    "How do Lusha and ZoomInfo work in an automated lead workflow?",
]


for query in queries:

    print("\n" + "=" * 80)
    print("QUERY:")
    print(query)
    print("=" * 80)

    results = retriever.retrieve(
        query=query,
        top_k=5,
    )

    print(
        f"\nRetrieved {len(results)} results"
    )

    for index, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n--- Result {index} ---"
        )

        print(
            f"Parent ID: "
            f"{result.get('parent_id')}"
        )

        print(
            f"Rerank Score: "
            f"{result.get('rerank_score')}"
        )

        print(
            f"RRF Score: "
            f"{result.get('rrf_score')}"
        )

        print(
            f"Source: "
            f"{result['metadata'].get('source')}"
        )

        print(
            f"Page: "
            f"{result['metadata'].get('page', 'N/A')}"
        )

        print("\nText:")
        print(result["text"][:1000])