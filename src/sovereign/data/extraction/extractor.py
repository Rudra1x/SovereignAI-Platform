from sovereign.data.extraction.strategies.base import (
    ExtractionStrategy,
)


class KnowledgeExtractor:

    def __init__(
        self,
        strategy: ExtractionStrategy,
    ):

        self.strategy = strategy

    def extract(
        self,
        parsed_document,
    ):

        return self.strategy.extract(
            parsed_document
        )