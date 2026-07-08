from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class KnowledgeUnit:
    """
    Smallest semantic unit extracted
    from a document.
    """

    id: str

    text: str

    source_document: str

    section: str | None = None

    page: int | None = None

    metadata: dict = field(default_factory=dict)