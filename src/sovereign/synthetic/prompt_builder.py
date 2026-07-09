"""
Prompt Builder
"""

from __future__ import annotations

from sovereign.synthetic.prompt_templates import (
    SYSTEM_PROMPT,
    DOCUMENT_PROMPT,
)


class PromptBuilder:

    def build(
        self,
        chunk,
    ) -> str:

        prompt = f"""
Source:{chunk.source}

Title:{chunk.title}

Section:{chunk.section}

Document:{chunk.text}
"""

        return (
            SYSTEM_PROMPT
            + "\n\n"
            + DOCUMENT_PROMPT.format(
                document=prompt.strip()
            )
        )