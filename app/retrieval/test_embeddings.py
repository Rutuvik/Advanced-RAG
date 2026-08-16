from app.retrieval.embeddings import EmbeddingModel


embedding_model = EmbeddingModel()


query = "What is prompt injection?"

documents = [
    "Prompt injection is an attack where malicious instructions are provided to an AI system.",
    "The weather is sunny today.",
    "An attacker can manipulate an LLM by injecting instructions into its input.",
]


query_embedding = embedding_model.embed_query(query)

document_embeddings = embedding_model.embed_documents(
    documents
)


def cosine_similarity(a, b):

    return sum(
        x * y
        for x, y in zip(a, b)
    )


scores = []

for document, embedding in zip(
    documents,
    document_embeddings,
):

    score = cosine_similarity(
        query_embedding,
        embedding,
    )

    scores.append(
        (score, document)
    )


scores.sort(
    key=lambda x: x[0],
    reverse=True,
)


print("\nQuery:")
print(query)

print("\nRanking:")
print("--------")

for rank, (score, document) in enumerate(
    scores,
    start=1,
):

    print(f"\n{rank}. Score: {score:.4f}")
    print(document)