"""
Prompt Builder
"""

from __future__ import annotations

import re

from sovereign.synthetic.prompt_templates import (
    SYSTEM_PROMPT,
    DOCUMENT_PROMPT,
)


class PromptBuilder:

    def classify_document(
        self,
        chunk,
    ) -> str:

        title = chunk.title.lower()

        source = chunk.source.lower()

        text = chunk.text[:2500].lower()

        if any(
            word in title
            for word in (
                "api",
                "sdk",
                "reference",
                "library",
            )
        ):
            return "api"

        if any(
            word in title
            for word in (
                "tutorial",
                "guide",
                "getting started",
                "quickstart",
            )
        ):
            return "tutorial"

        if any(
            word in title
            for word in (
                "paper",
                "research",
                "publication",
            )
        ):
            return "research"

        if any(
            word in title
            for word in (
                "conduct",
                "policy",
                "license",
                "security",
            )
        ):
            return "policy"

        if (
            "```" in text
            or "def " in text
            or "class " in text
            or "import " in text
            or "cudaq" in text
        ):
            return "code"

        return "documentation"

    def generation_instruction(
        self,
        doc_type: str,
    ) -> str:

        mapping = {

            "documentation": """
Generate:

- One summary (maximum 40 words)
- Exactly two QA pairs (each answer maximum 25 words)
- Exactly two MCQs
- Keep option text under 8 words.
- Never enumerate long lists.
- Never copy large tables or identifiers.
- Return ONLY valid JSON.

Do not generate coding tasks.
""",

            "tutorial": """
Generate:

- One concise summary
- Exactly two QA pairs
- One coding task

Do not generate MCQs.
""",

            "api": """
Generate:

- One concise summary
- Exactly two QA pairs
- One coding task

Focus on API usage.
""",

            "code": """
Generate:

- One concise summary
- Exactly two QA pairs
- One debugging/coding task

Focus on implementation.
""",

            "research": """
Generate:

- One concise summary
- One explanation
- Exactly two QA pairs

Do not generate coding tasks.
""",

            "policy": """
Generate:

- One concise summary
- Exactly two QA pairs
- Two best practices

Do not generate coding tasks.
""",
        }

        return mapping.get(
            doc_type,
            mapping["documentation"],
        )

    def compress_context(
        self,
        text: str,
    ) -> str:

        words = text.split()

        if len(words) <= 500:
            return text

        if len(words) <= 900:

            head = words[:200]

            tail = words[-75:]

        else:

            head = words[:250]

            tail = words[-100:]

        return (
            " ".join(head)
            + "\n\n"
            + "[...content omitted...]\n\n"
            + " ".join(tail)
        )

    def build(
        self,
        chunk,
    ) -> str:

        doc_type = self.classify_document(
            chunk
        )

        instruction = self.generation_instruction(
            doc_type
        )

        prompt = f"""
Source:{chunk.source}

Title:{chunk.title}

Section:{chunk.section}

Document Type:
{doc_type}

Document:
{self.compress_context(chunk.text)}
"""

        return (
            SYSTEM_PROMPT
            + "\n\n"
            + instruction
            + "\n\n"
            + DOCUMENT_PROMPT.format(
                document=prompt.strip()
            )
        )