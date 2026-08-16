from app.retrieval.bm25_retriever import BM25Retriever


retriever = BM25Retriever()


queries = [
    "What is prompt injection?",
    "How can token prediction behavior lead to unintended instruction overrides?",
    "How do Lusha and ZoomInfo work in an automated lead workflow?",
]


for query in queries:

    print("\n" + "=" * 80)
    print("QUERY:")
    print(query)
    print("=" * 80)

    results = retriever.retrieve(
        query,
        top_k=5,
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):

        parent = result["parent"]

        print(
            f"\n--- Result {rank} ---"
        )

        print(
            f"BM25 Score: "
            f"{result['score']:.4f}"
        )

        print(
            f"Source: "
            f"{parent['metadata'].get('source')}"
        )

        print(
            f"Page: "
            f"{parent['metadata'].get('page', 'N/A')}"
        )

        print(
            f"Parent ID: "
            f"{parent['metadata'].get('parent_id')}"
        )

        print("\nText:")

        print(
            parent["text"][:500]
        )