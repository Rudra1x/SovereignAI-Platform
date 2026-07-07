from __future__ import annotations

import re

from markdown import markdown

from sovereign.data.core.parsed_content import ParsedContent
from sovereign.data.core.resource import RawResource

from .base import BaseParser


class MarkdownParser(BaseParser):

    def parse(
        self,
        resource: RawResource,
    ) -> ParsedContent:

        md = resource.content.decode(
            "utf-8",
            errors="ignore",
        )

        html = markdown(md)

        text = re.sub(
            "<[^>]+>",
            "",
            html,
        )

        return ParsedContent(
            text=text,
            parser_name="MarkdownParser",
        )