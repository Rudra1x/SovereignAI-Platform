"""
Canonical parser output.

Every parser returns ParsedContent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ParsedContent:

    text: str

    parser_name: str

    title: str | None = None

    headings: list[str] = field(default_factory=list)

    tables: list[list[list[str]]] = field(default_factory=list)

    images: list[str] = field(default_factory=list)

    links: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @property
    def character_count(self) -> int:
        return len(self.text)

    def to_dict(self) -> dict:

        return {
            "title": self.title,
            "parser_name": self.parser_name,
            "text": self.text,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "headings": self.headings,
            "tables": self.tables,
            "images": self.images,
            "links": self.links,
            "metadata": self.metadata,
        }