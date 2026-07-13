"""
Latency benchmark prompt template.

Ensures every model generates responses
under identical conditions.
"""


def build_prompt(question: str) -> str:

    return f"""
You are an expert in Quantum Computing.

Answer the following question using these rules:

1. Provide ONE concise paragraph.
2. Target approximately 100 words.
3. Do NOT exceed 120 words.
4. Include only the essential technical explanation.
5. Do not add introductions.
6. Do not add conclusions.
7. Do not use bullet points.
8. Do not repeat the question.

Question:

{question}
""".strip()