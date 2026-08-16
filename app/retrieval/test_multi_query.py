from app.retrieval.multi_query_retriever import (
    MultiQueryRetriever
)


retriever = MultiQueryRetriever(
    num_queries=3,
    dense_top_k=10,
    bm25_top_k=10,
)


query = "What is prompt injection?"


print("\n" + "=" * 80)
print("MULTI-QUERY RETRIEVAL DEBUG")
print("=" * 80)

print("\nORIGINAL QUERY")
print(query)


# ==========================================================
# 1. Generate expanded queries
# ==========================================================

queries = retriever.query_expander.expand(query)

print("\n" + "=" * 80)
print("GENERATED QUERIES")
print("=" * 80)

for index, search_query in enumerate(
    queries,
    start=1,
):
    print(f"{index}. {search_query}")


# ==========================================================
# 2. Run each query independently
# ==========================================================

all_candidates = {}


for query_index, search_query in enumerate(
    queries,
    start=1,
):

    print("\n" + "=" * 80)
    print(
        f"QUERY {query_index}: "
        f"{search_query}"
    )
    print("=" * 80)

    candidates = (
        retriever.hybrid_retriever
        .retrieve_candidates(
            search_query
        )
    )

    for rank, candidate in enumerate(
        candidates[:10],
        start=1,
    ):

        parent_id = candidate[
            "parent_id"
        ]

        page = candidate[
            "metadata"
        ].get(
            "page",
            "N/A",
        )

        rrf_score = candidate.get(
            "rrf_score",
            0,
        )

        print(
            f"\n[{rank}] "
            f"Page: {page} | "
            f"Parent: {parent_id} | "
            f"RRF: {rrf_score:.6f}"
        )

        print(
            candidate["text"][:300]
            .replace("\n", " ")
        )

        # Store candidate across queries
        if parent_id not in all_candidates:

            all_candidates[parent_id] = {
                **candidate,
                "query_matches": [],
            }

        all_candidates[
            parent_id
        ]["query_matches"].append(
            {
                "query": search_query,
                "rrf_score": rrf_score,
            }
        )


# ==========================================================
# 3. Analyze multi-query aggregation
# ==========================================================

print("\n" + "=" * 80)
print("MULTI-QUERY AGGREGATION")
print("=" * 80)


aggregated = []


for parent_id, candidate in (
    all_candidates.items()
):

    matches = candidate[
        "query_matches"
    ]

    scores = [
        match["rrf_score"]
        for match in matches
    ]

    max_score = max(scores)

    aggregated.append(
        {
            **candidate,
            "max_rrf_score": max_score,
            "query_match_count": len(matches),
        }
    )


aggregated.sort(
    key=lambda x: (
        x["max_rrf_score"],
        x["query_match_count"],
    ),
    reverse=True,
)


for rank, candidate in enumerate(
    aggregated[:15],
    start=1,
):

    page = candidate[
        "metadata"
    ].get(
        "page",
        "N/A",
    )

    print(
        f"\n[{rank}] "
        f"Page: {page}"
    )

    print(
        f"Parent ID: "
        f"{candidate['parent_id']}"
    )

    print(
        f"Max RRF: "
        f"{candidate['max_rrf_score']:.6f}"
    )

    print(
        f"Matched Queries: "
        f"{candidate['query_match_count']}"
    )

    for match in candidate[
        "query_matches"
    ]:

        print(
            f"  - "
            f"{match['rrf_score']:.6f} | "
            f"{match['query']}"
        )


# ==========================================================
# 4. Final reranking
# ==========================================================

print("\n" + "=" * 80)
print("FINAL RERANKING")
print("=" * 80)


for candidate in aggregated:

    candidate[
        "multi_query_score"
    ] = candidate[
        "max_rrf_score"
    ]


final_results = (
    retriever.hybrid_retriever.reranker.rerank(
        query=query,
        documents=aggregated,
        top_k=5,
    )
)


for rank, result in enumerate(
    final_results,
    start=1,
):

    page = result[
        "metadata"
    ].get(
        "page",
        "N/A",
    )

    print(
        f"\n[{rank}] "
        f"Page: {page}"
    )

    print(
        f"Parent ID: "
        f"{result['parent_id']}"
    )

    print(
        f"Rerank Score: "
        f"{result.get('rerank_score')}"
    )

    print(
        f"Multi Query Score: "
        f"{result.get('multi_query_score')}"
    )

    print(
        f"Query Matches: "
        f"{len(result.get('query_matches', []))}"
    )

    print(
        "\nText:"
    )

    print(
        result["text"][:700]
    )