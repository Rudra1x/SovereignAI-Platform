from __future__ import annotations

from sovereign.data.core.parsed_content import ParsedContent
from sovereign.data.core.resource import RawResource

from .base import BaseParser


class TextParser(BaseParser):

    def parse(
        self,
        resource: RawResource,
    ) -> ParsedContent:

        text = resource.content.decode(
            "utf-8",
            errors="ignore",
        )

        return ParsedContent(
            text=text,
            parser_name="TextParser",
        )