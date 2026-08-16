from app.retrieval.multi_query_retriever import (
    MultiQueryRetriever
)

from app.context_builder import build_context


retriever = MultiQueryRetriever(
    num_queries=3,
    dense_top_k=10,
    bm25_top_k=10,
)


query = (
    "Explain a scenario where harmless-looking "
    "input results in a dangerous output?"
)


results = retriever.retrieve(
    query=query,
    top_k=5,
)


print("\n" + "=" * 80)
print("RETRIEVED RESULTS")
print("=" * 80)

for index, result in enumerate(
    results,
    start=1,
):

    print(
        f"\nResult {index}"
    )

    print(
        "Rerank score:",
        result.get(
            "rerank_score"
        ),
    )

    print(
        "Source:",
        result["metadata"].get(
            "source"
        ),
    )

    print(
        "Page:",
        result["metadata"].get(
            "page",
            "N/A"
        ),
    )


context = build_context(
    results
)


print("\n" + "=" * 80)
print("FINAL CONTEXT")
print("=" * 80)

print(context)

print("\n" + "=" * 80)
print("CONTEXT CHARACTERS")
print("=" * 80)

print(len(context))