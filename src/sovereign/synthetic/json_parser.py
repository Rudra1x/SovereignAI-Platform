"""
Safe JSON parser.
"""

from __future__ import annotations

import json
import re


class JSONParser:

    def parse(
        self,
        text: str,
    ) -> dict:

        text = text.strip()

        if text.startswith("```"):

            text = re.sub(
                r"^```(?:json)?",
                "",
                text,
                flags=re.MULTILINE,
            )

            text = text.replace(
                "```",
                "",
            ).strip()

        start = text.find("{")

        end = text.rfind("}")

        if start == -1 or end == -1:

            raise ValueError(
                "No JSON object found."
            )

        text = text[start:end + 1]

        return json.loads(text)