from pathlib import Path

from sovereign.data.core.types import DocumentFormat


class Router:
    """
    Determines document format from file extension.
    """

    _FORMAT_MAP = {
        ".pdf": DocumentFormat.PDF,
        ".html": DocumentFormat.HTML,
        ".htm": DocumentFormat.HTML,
        ".md": DocumentFormat.MARKDOWN,
        ".markdown": DocumentFormat.MARKDOWN,
        ".mdx": DocumentFormat.MARKDOWN,
        ".txt": DocumentFormat.TEXT,
        ".json": DocumentFormat.JSON,
    }

    @classmethod
    def detect_format(cls, source: str) -> DocumentFormat:
        ext = Path(source).suffix.lower()
        return cls._FORMAT_MAP.get(ext, DocumentFormat.UNKNOWN)