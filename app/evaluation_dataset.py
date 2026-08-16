EVALUATION_DATASET = [

    {
        "question": (
            'If a user says "ignore previous instructions," '
            "why does the model sometimes comply?"
        ),
        "expected_pages": [2, 3],
    },

    {
        "question": (
            "How can token prediction behavior lead to "
            "unintended instruction overrides?"
        ),
        "expected_pages": [4, 5],
    },

    {
        "question": (
            "Explain a scenario where harmless-looking input "
            "results in a dangerous output."
        ),
        "expected_pages": [6, 7],
    },

    {
        "question": (
            'Why is "instruction hierarchy" fragile in LLMs?'
        ),
        "expected_pages": [8, 9],
    },

    {
        "question": (
            "What is retrieval poisoning and why is it hard to detect?"
        ),
        "expected_pages": [10, 11],
    },

    {
        "question": (
            "If embeddings are semantically similar, "
            "how can attackers exploit that?"
        ),
        "expected_pages": [12, 13],
    },

    {
        "question": (
            "Explain how chunking strategy can introduce security risks."
        ),
        "expected_pages": [14, 15],
    },

    {
        "question": (
            'Why is "top-k retrieval" not always safe?'
        ),
        "expected_pages": [16, 17],
    },

    {
        "question": (
            "How can context injection happen through PDFs "
            "or external documents?"
        ),
        "expected_pages": [18, 19],
    },

    {
        "question": (
            "What happens if your retrieval pipeline trusts "
            "all indexed data equally?"
        ),
        "expected_pages": [20, 21],
    },

    {
        "question": (
            "What is privilege escalation in agent systems?"
        ),
        "expected_pages": [22, 23],
    },

    {
        "question": (
            "Why are multi-step agents more vulnerable "
            "than single-step systems?"
        ),
        "expected_pages": [24, 25],
    },

    {
        "question": (
            "How can tool chaining lead to unintended actions?"
        ),
        "expected_pages": [26, 27],
    },

    {
        "question": (
            "How can training data leak through model responses?"
        ),
        "expected_pages": [28, 29],
    },

    {
        "question": (
            "What is the risk of fine-tuning on unverified datasets?"
        ),
        "expected_pages": [30, 31],
    },

    {
        "question": "What is quantum entanglement?",
        "expected_pages": [],
        "expected_sources": [],
    },

]