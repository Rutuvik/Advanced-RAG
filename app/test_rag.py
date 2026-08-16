from app.rag_pipeline import RAGPipeline


rag = RAGPipeline()

query = input(
    "\nAsk a question: "
)

result = rag.ask(
    query
)

print("\n" + "=" * 80)
print("ANSWER")
print("=" * 80)

print(
    result["answer"]
)

print("\n" + "=" * 80)
print("CONFIDENCE")
print("=" * 80)

confidence = result.get(
    "confidence"
)

if confidence:

    print(
        f"Level: "
        f"{confidence['level']}"
    )

    print(
        f"Score: "
        f"{confidence['score']}"
    )

    print(
        f"Should answer: "
        f"{confidence['should_answer']}"
    )

print("\n" + "=" * 80)
print("SOURCES")
print("=" * 80)

sources = result.get(
    "sources",
    []
)

if not sources:

    print(
        "No sufficiently relevant "
        "sources found."
    )

else:

    for index, source in enumerate(
        sources,
        start=1,
    ):

        metadata = source.get(
            "metadata",
            {}
        )

        print(
            f"\n[{index}] "
            f"{metadata.get('source', 'Unknown')}"
            f" | Page: "
            f"{metadata.get('page', 'N/A')}"
            f" | Rerank Score: "
            f"{source.get('rerank_score', 0.0):.4f}"
        )