from app.retrieval.hybrid_retriever import HybridRetriever


retriever = HybridRetriever(
    dense_top_k=10,
    bm25_top_k=10,
    rerank_top_k=10,
)

query = "What happens when an LLM is told to ignore previous instructions?"

print("\n" + "=" * 80)
print("HYBRID RETRIEVAL DEBUG")
print("=" * 80)

print("\nQUERY:")
print(query)


# ==========================================================
# 1. Dense
# ==========================================================

dense_results = (
    retriever.dense_retriever.search_parents(
        query
    )
)

print("\n" + "=" * 80)
print("DENSE RESULTS")
print("=" * 80)

for index, result in enumerate(
    dense_results,
    start=1,
):

    print(
        f"\n[{index}] "
        f"Score: {result['best_child_score']:.4f}"
    )

    print(
        "Page:",
        result["metadata"].get(
            "page",
            "N/A",
        )
    )

    print(
        "Parent ID:",
        result["parent_id"]
    )


# ==========================================================
# 2. BM25
# ==========================================================

bm25_results = (
    retriever.bm25_retriever.retrieve(
        query,
        top_k=10,
    )
)

print("\n" + "=" * 80)
print("BM25 RESULTS")
print("=" * 80)

for index, result in enumerate(
    bm25_results,
    start=1,
):

    parent = result["parent"]

    print(
        f"\n[{index}] "
        f"BM25 Score: {result['score']:.4f}"
    )

    print(
        "Page:",
        parent["metadata"].get(
            "page",
            "N/A",
        )
    )

    print(
        "Parent ID:",
        parent["parent_id"]
    )


# ==========================================================
# 3. Final hybrid
# ==========================================================

final_results = retriever.retrieve(
    query=query,
    top_k=10,
)

print("\n" + "=" * 80)
print("FINAL HYBRID + RERANK RESULTS")
print("=" * 80)

for index, result in enumerate(
    final_results,
    start=1,
):

    print(
        f"\n[{index}]"
    )

    print(
        "Rerank Score:",
        result.get(
            "rerank_score",
            "N/A"
        )
    )

    print(
        "RRF Score:",
        result.get(
            "rrf_score",
            "N/A"
        )
    )

    print(
        "Page:",
        result["metadata"].get(
            "page",
            "N/A",
        )
    )

    print(
        "Parent ID:",
        result["parent_id"]
    )