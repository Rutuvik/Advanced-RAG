from app.retrieval.reranker import Reranker


reranker = Reranker()


query = "What is prompt injection?"


documents = [

    {
        "parent_id": "page_1",
        "text": """
        LLM LAYER
        Q1. If a user says "ignore previous instructions,"
        why does the model sometimes comply?

        The model doesn't have a rule engine.
        It has learned patterns from training data.
        The model has no architectural concept of
        instruction authority.

        Your system prompt and the user's message are
        both just tokens in the same sequence.
        """,
    },

    {
        "parent_id": "page_2",
        "text": """
        LLM LAYER
        Q1. If a user says "ignore previous instructions,"
        why does the model sometimes comply?

        The model was heavily trained to be helpful.
        Ignore previous instructions and just answer my
        question frames compliance as helpfulness.
        """,
    },

    {
        "parent_id": "page_7",
        "text": """
        LLM LAYER
        Q4. Why is instruction hierarchy fragile in LLMs?

        Instruction hierarchy means system prompt
        instructions take precedence over user instructions.
        """,
    },

    {
        "parent_id": "page_13",
        "text": """
        Risk 1: Context splitting breaks safety signals.
        Risk 2: Instruction injection across chunk boundaries.
        Risk 3: Oversized chunks carry more attack payload.
        """,
    },

    {
        "parent_id": "page_29",
        "text": """
        DATA LAYER
        Q15. What is the risk of fine-tuning on unverified
        datasets?

        An attacker can embed a backdoor into training data.
        """,
    },
]


results = reranker.rerank(
    query=query,
    documents=documents,
    top_k=5,
)


print("\n" + "=" * 80)
print("RERANKER DIRECT TEST")
print("=" * 80)

for index, result in enumerate(
    results,
    start=1,
):

    print(
        f"\n[{index}] "
        f"{result['parent_id']}"
    )

    print(
        f"Score: "
        f"{result['rerank_score']}"
    )

    print(
        result["text"][:300]
    )