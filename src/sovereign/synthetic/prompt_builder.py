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
        document: str,
    ) -> str:

        return (
            SYSTEM_PROMPT
            + "\n\n"
            + DOCUMENT_PROMPT.format(
                document=document
            )
        )