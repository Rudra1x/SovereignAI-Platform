from abc import ABC, abstractmethod

from sovereign.data.core.parsed_content import ParsedContent

from sovereign.data.extraction.unit import KnowledgeUnit


class ExtractionStrategy(ABC):

    @abstractmethod
    def extract(
        self,
        document: ParsedContent,
    ) -> list[KnowledgeUnit]:
        pass