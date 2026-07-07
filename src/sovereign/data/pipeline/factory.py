from sovereign.data.core.types import DocumentFormat

from sovereign.data.loaders import LocalLoader, HTTPLoader

from sovereign.data.parsers import (
    HTMLParser,
    MarkdownParser,
    PDFParser,
    JsonParser,
    TextParser,
)


class LoaderFactory:

    @staticmethod
    def create(source: str):

        if source.startswith("http://") or source.startswith("https://"):
            return HTTPLoader()

        return LocalLoader()


class ParserFactory:

    _PARSERS = {
        DocumentFormat.HTML: HTMLParser,
        DocumentFormat.PDF: PDFParser,
        DocumentFormat.MARKDOWN: MarkdownParser,
        DocumentFormat.TEXT: TextParser,
        DocumentFormat.JSON: JsonParser,
    }

    @classmethod
    def create(cls, document_format):

        parser = cls._PARSERS.get(document_format)

        if parser is None:
            raise ValueError(
                f"No parser registered for {document_format}"
            )

        return parser()