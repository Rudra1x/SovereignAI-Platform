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

        match = re.search(r"\n\s*\{", text)

        if match:
            start = match.start() + match.group().find("{")
        else:
            start = text.find("{")

        if start == -1:

            raise ValueError(
                "No JSON object found."
            )

        decoder = json.JSONDecoder()

        try:

            obj, _ = decoder.raw_decode(text[start:])

            print("\n" + "="*80)
            print("INSIDE JSON PARSER")
            print(type(obj))
            print(obj)
            print("="*80)

            return obj

        except json.JSONDecodeError as exc:

            raise ValueError(
                f"Invalid JSON: {exc}"
            ) from exc