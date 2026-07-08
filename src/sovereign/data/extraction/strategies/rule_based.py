import uuid

from sovereign.data.core.parsed_content import ParsedContent

from sovereign.data.extraction.unit import (
    KnowledgeUnit,
)

from .base import ExtractionStrategy


class RuleBasedExtractionStrategy(
    ExtractionStrategy
):

    def extract(
        self,
        document: ParsedContent,
    ):

        paragraphs = [
            p.strip()
            for p in document.text.split("\n\n")
            if p.strip()
        ]

        units = []

        for paragraph in paragraphs:

            units.append(
                KnowledgeUnit(
                    id=str(uuid.uuid4()),
                    text=paragraph,
                    source_document=document.title
                    or "unknown",
                )
            )

        return units