from app.retrieval.query_expander import QueryExpander


expander = QueryExpander(
    num_queries=3
)


queries = [
    "What is prompt injection?",
    "How do Lusha and ZoomInfo work in an automated lead workflow?",
]


for query in queries:

    print("\n" + "=" * 80)
    print("ORIGINAL QUERY")
    print("=" * 80)

    print(query)

    expanded_queries = expander.expand(
        query
    )

    print("\nEXPANDED QUERIES")
    print("-" * 80)

    for index, expanded_query in enumerate(
        expanded_queries,
        start=1,
    ):

        print(
            f"{index}. {expanded_query}"
        )