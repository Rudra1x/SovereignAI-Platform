from __future__ import annotations

import fitz

from sovereign.data.core.parsed_content import ParsedContent
from sovereign.data.core.resource import RawResource

from .base import BaseParser


class PDFParser(BaseParser):

    def parse(
        self,
        resource: RawResource,
    ) -> ParsedContent:

        pdf = fitz.open(
            stream=resource.content,
            filetype="pdf",
        )

        pages = []

        metadata = pdf.metadata

        for page in pdf:

            pages.append(
                page.get_text("text")
            )

        pdf.close()

        return ParsedContent(
            text="\n".join(pages),
            title=metadata.get("title"),
            parser_name="PDFParser",
            metadata=metadata,
        )