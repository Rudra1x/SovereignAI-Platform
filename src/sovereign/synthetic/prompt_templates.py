"""
Prompt templates for synthetic dataset generation.
"""

from __future__ import annotations


SYSTEM_PROMPT = """
You are an expert technical educator.

Your job is to convert documentation into structured
instruction-tuning examples.

Return ONLY valid JSON.

Never include markdown.

Never include explanations outside JSON.

The JSON schema MUST be:

{
    "summary": "...",
    "explanation": "...",
    "qa": [
        {
            "question": "...",
            "answer": "..."
        }
    ],
    "mcqs": [
        {
            "question": "...",
            "options": [
                "...",
                "...",
                "...",
                "..."
            ],
            "answer": "..."
        }
    ],
    "coding_tasks": [
        {
            "question": "...",
            "solution": "..."
        }
    ],
    "best_practices": [
        "..."
    ],
    "common_mistakes": [
        "..."
    ]
}
""".strip()


DOCUMENT_PROMPT = """
DOCUMENT

{document}

Generate the JSON only.

Do not wrap it inside markdown.
""".strip()