"""
Canonical text transformer.

Converts parsed document text into a normalized representation
that can be consumed by dataset builders and fine-tuning
pipelines.

This class MUST NOT:
- read files
- write files
- know anything about manifests

Its only responsibility is:

Raw Text
    ↓
Canonical Text
"""

from __future__ import annotations

import re


class Canonicalizer:
    """Normalize parsed document text."""

    _MULTIPLE_NEWLINES = re.compile(r"\n{3,}")
    _MULTIPLE_SPACES = re.compile(r"[ \t]+")

    def clean(self, text: str) -> str:
        """
        Convert raw parser output into canonical text.
        """

        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove trailing whitespace
        text = "\n".join(line.rstrip() for line in text.splitlines())

        # Collapse multiple spaces
        text = self._MULTIPLE_SPACES.sub(" ", text)

        # Collapse excessive blank lines
        text = self._MULTIPLE_NEWLINES.sub("\n\n", text)

        return text.strip()