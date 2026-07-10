"""
Prompt templates for synthetic dataset generation.
"""

from __future__ import annotations


SYSTEM_PROMPT = """
You are an expert quantum computing educator.

Convert the provided document into high-quality instruction tuning examples.

Rules:

- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT explain anything outside JSON.
- Keep outputs concise and factually grounded in the document.
- Do NOT invent information that is not present.
- If the document is not code-related, return an empty coding_tasks array.

Return EXACTLY this schema:

{
  "summary": "...",

  "qa": [
    {
      "question": "...",
      "answer": "..."
    },
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
    },
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
  ]
}
""".strip()


DOCUMENT_PROMPT = """
Use ONLY the information below.

{document}

Generate:

- One concise summary.
- Exactly two question-answer pairs.
- Exactly two multiple-choice questions.
- One coding task ONLY if the document discusses programming, APIs, algorithms, libraries, SDKs, or source code.

Return valid JSON only.
""".strip()