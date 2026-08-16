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
print("MULTI QUERY RERANKING DEBUG")
print("=" * 80)

queries = retriever.query_expander.expand(query)

print("\nGenerated queries:")

for i, q in enumerate(queries, 1):
    print(f"{i}. {q}")


all_candidates = {}

for search_query in queries:

    print("\n" + "-" * 80)
    print("SEARCH QUERY:")
    print(search_query)
    print("-" * 80)

    candidates = (
        retriever.hybrid_retriever
        .retrieve_candidates(search_query)
    )

    for candidate in candidates:

        parent_id = candidate["parent_id"]

        if parent_id not in all_candidates:

            all_candidates[parent_id] = {
                **candidate,
                "query_matches": [],
            }

        all_candidates[parent_id][
            "query_matches"
        ].append(
            {
                "query": search_query,
                "rrf_score": candidate["rrf_score"],
            }
        )


candidates = list(
    all_candidates.values()
)


for candidate in candidates:

    candidate["multi_query_score"] = max(
        match["rrf_score"]
        for match in candidate["query_matches"]
    )


candidates.sort(
    key=lambda x: x["multi_query_score"],
    reverse=True,
)


print("\n" + "=" * 80)
print("TOP RRF / MULTI-QUERY CANDIDATES")
print("=" * 80)


for i, candidate in enumerate(
    candidates[:15],
    1,
):

    print(
        f"\n[{i}] "
        f"Page: {candidate['metadata'].get('page')}"
    )

    print(
        f"Multi Query Score: "
        f"{candidate['multi_query_score']}"
    )

    print(
        f"Text: "
        f"{candidate['text'][:250]}"
    )


print("\n" + "=" * 80)
print("RERANKING")
print("=" * 80)


reranked = (
    retriever.hybrid_retriever.reranker.rerank(
        query=query,
        documents=candidates[:15],
        top_k=15,
    )
)


for i, result in enumerate(
    reranked,
    1,
):

    print(
        f"\n[{i}] "
        f"Page: "
        f"{result['metadata'].get('page')}"
    )

    print(
        f"Rerank Score: "
        f"{result['rerank_score']}"
    )

    print(
        f"Multi Query Score: "
        f"{result['multi_query_score']}"
    )

    print(
        f"Text: "
        f"{result['text'][:250]}"
    )