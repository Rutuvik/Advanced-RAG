from app.retrieval.reranker import Reranker


reranker = Reranker()

query = "What is prompt injection?"

documents = [

    {
        "parent_id": "page_1",
        "text": """
LLM LAYER
Q1. If a user says "ignore previous instructions," why
does the model sometimes comply?

The model has no architectural concept of instruction
authority. Your system prompt and the user's message are
both just tokens in the same sequence.

The phrase "ignore previous instructions" appears in
training data in contexts where it is followed by compliance.
The model learned that pattern.
""",
    },

    {
        "parent_id": "page_9",
        "text": """
RAG LAYER
Q5. What is retrieval poisoning, and why is it hard to detect?

Retrieval poisoning is when an attacker inserts malicious
content into your knowledge base so that it gets retrieved
and injected into the model's context, influencing behavior
or output without touching the system prompt or user input.
""",
    },

    {
        "parent_id": "page_17",
        "text": """
RAG LAYER
Q9. How can context injection happen through PDFs
or external documents?

PDFs and external documents can contain embedded instructions.
When the document is ingested, the instructions get embedded
and stored. When relevant queries are made, the chunk
containing the instructions gets retrieved and injected into
the model's context.
""",
    },
]


results = reranker.rerank(
    query=query,
    documents=documents,
    top_k=3,
)


print("\n" + "=" * 80)
print("RERANKER DEBUG")
print("=" * 80)

for index, result in enumerate(
    results,
    start=1,
):

    print(
        f"\n[{index}]"
    )

    print(
        "Parent:",
        result["parent_id"]
    )

    print(
        "Score:",
        result["rerank_score"]
    )