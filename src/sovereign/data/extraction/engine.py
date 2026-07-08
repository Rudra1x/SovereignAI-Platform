from sovereign.data.extraction.extractor import (
    KnowledgeExtractor,
)


class ExtractionEngine:

    def __init__(
        self,
        extractor: KnowledgeExtractor,
    ):

        self.extractor = extractor

    def run(
        self,
        parsed_document,
    ):

        return self.extractor.extract(
            parsed_document
        )