from app.generation.groq_generator import GroqGenerator


class QueryExpander:

    def __init__(
        self,
        num_queries: int = 3,
    ):

        self.num_queries = num_queries
        self.generator = GroqGenerator()

    def expand(
        self,
        query: str,
    ) -> list[str]:
        prompt = f"""
You are a query expansion component for a RAG retrieval system.

Your job is NOT to answer the question.

Your job is to generate {self.num_queries} search queries that can
retrieve the answer from a technical knowledge base.

IMPORTANT:

The knowledge base may NOT use the exact terminology used by the
user.

Therefore, at least TWO of the generated queries MUST describe the
underlying mechanism or behavior instead of repeating the original
term.

For example:

User question:
What is prompt injection?

Bad expansion:
prompt injection definition
prompt injection attack
prompt injection in LLMs

Good expansion:
how can user instructions override system instructions in an LLM
why does an LLM sometimes follow a command to ignore previous instructions
how does instruction hierarchy failure cause unintended model behavior

Generate exactly {self.num_queries} queries using these categories:

Query 1:
A definition-oriented technical query.

Query 2:
A mechanism-oriented query describing how the phenomenon works.

Query 3:
A behavior/failure-oriented query using terminology that could
actually appear in a technical document.

Rules:

- Preserve the meaning of the original question.
- Do NOT answer the question.
- Do NOT explain anything.
- Do NOT repeat the original terminology in every query.
- At least TWO queries must use related concepts rather than simply
  repeating the main keyword.
- Prefer concrete technical phrases that may literally appear in
  documents.
- Return ONLY the queries.
- One query per line.
- Do not number them.
- Do not use bullets.

Original question:

{query}
"""
        

        response = self.generator.generate_text(
            prompt
        )

        queries = []

        for line in response.splitlines():

            line = line.strip()

            if not line:
                continue

            # Remove accidental numbering
            if (
                len(line) >= 2
                and line[0].isdigit()
                and line[1] in [".", ")"]
            ):
                line = line[2:].strip()

            # Remove accidental bullets
            if line.startswith("- "):
                line = line[2:].strip()

            if line:
                queries.append(line)

        # Always preserve original query
        queries.insert(
            0,
            query
        )

        # Remove duplicates
        unique_queries = []

        seen = set()

        for q in queries:

            normalized = q.lower().strip()

            if normalized not in seen:

                seen.add(normalized)

                unique_queries.append(q)

        return unique_queries[
            : self.num_queries + 1
        ]