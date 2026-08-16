from app.retrieval.retriever import Retriever


retriever = Retriever(
    top_k=10
)


queries = [
    "What is prompt injection?",
]


for query in queries:

    print("\n" + "=" * 80)
    print("QUERY:")
    print(query)
    print("=" * 80)

    results = retriever.search_parents(
        query
    )

    print(
        f"\nRetrieved {len(results)} unique parents"
    )

    for index, result in enumerate(
        results,
        start=1,
    ):

        metadata = result.get(
            "metadata",
            {}
        )

        print(
            f"\n--- Result {index} ---"
        )

        print(
            "Dense Score:",
            result.get(
                "best_child_score",
                0.0
            )
        )

        print(
            "Parent ID:",
            result.get(
                "parent_id"
            )
        )

        print(
            "Source:",
            metadata.get(
                "source",
                "Unknown"
            )
        )

        print(
            "Page:",
            metadata.get(
                "page",
                "N/A"
            )
        )

        print(
            "\nText:"
        )

        print(
            result.get(
                "text",
                ""
            )
        )