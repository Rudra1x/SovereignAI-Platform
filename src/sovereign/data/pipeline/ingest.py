from sovereign.data.pipeline.router import Router
from sovereign.data.pipeline.factory import (
    LoaderFactory,
    ParserFactory,
)

from sovereign.data.core.parsed_content import ParsedContent


class DataPipeline:

    """
    End-to-end ingestion pipeline.

    Source
      ↓
    Loader
      ↓
    RawResource
      ↓
    Parser
      ↓
    ParsedContent
    """

    def ingest(self, source: str) -> ParsedContent:

        loader = LoaderFactory.create(source)

        resource = loader.load(source)

        document_format = Router.detect_format(source)

        parser = ParserFactory.create(document_format)

        parsed = parser.parse(resource)

        return parsed