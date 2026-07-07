from __future__ import annotations

import json

from sovereign.data.core.parsed_content import ParsedContent
from sovereign.data.core.resource import RawResource

from .base import BaseParser


class JsonParser(BaseParser):

    def parse(
        self,
        resource: RawResource,
    ) -> ParsedContent:

        obj = json.loads(
            resource.content.decode("utf-8")
        )

        pretty = json.dumps(
            obj,
            indent=2,
            ensure_ascii=False,
        )

        return ParsedContent(
            text=pretty,
            parser_name="JsonParser",
        )