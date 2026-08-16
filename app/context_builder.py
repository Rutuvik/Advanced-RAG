def build_context(
    results: list[dict],
    max_chars: int = 12000,
    min_score: float = 0.01,
) -> str:

    contexts = []
    used_results = []

    seen_texts = set()

    total_chars = 0

    source_index = 1

    for result in results:

        # ==================================================
        # 1. Score filtering
        # ==================================================

        rerank_score = result.get(
            "rerank_score",
            0.0,
        )

        if rerank_score < min_score:
            continue

        # ==================================================
        # 2. Duplicate filtering
        # ==================================================

        text = result.get(
            "text",
            "",
        ).strip()

        if not text:
            continue

        normalized_text = " ".join(
            text.lower().split()
        )

        if normalized_text in seen_texts:
            continue

        seen_texts.add(
            normalized_text
        )

        # ==================================================
        # 3. Metadata
        # ==================================================

        metadata = result.get(
            "metadata",
            {},
        )

        source = metadata.get(
            "source",
            "Unknown",
        )

        page = metadata.get(
            "page",
            "N/A",
        )

        parent_id = result.get(
            "parent_id",
            "Unknown",
        )

        # ==================================================
        # 4. Build context block
        # ==================================================

        context = f"""
SOURCE {source_index}

Source: {source}
Page: {page}
Parent ID: {parent_id}

Content:
{text}
""".strip()

        # ==================================================
        # 5. Character budget
        # ==================================================

        additional_chars = len(context)

        if (
            total_chars + additional_chars
            > max_chars
        ):

            remaining_chars = (
                max_chars - total_chars
            )

            if remaining_chars <= 0:
                break

            context = context[
                :remaining_chars
            ]

        contexts.append(
            context
        )

        total_chars += len(
            context
        )

        used_results.append(result)
        source_index += 1

        if total_chars >= max_chars:
            break

    # ==================================================
    # 6. Final context
    # ==================================================

    if not contexts:
        return (
            "No sufficiently relevant "
            "information was retrieved."
        )

    return "\n\n".join(
        contexts
    ), used_results