from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List
from uuid import uuid4

from .metadata import Metadata
from .types import (
    DocumentCategory,
    DocumentFormat,
    LicenseType,
    SourceType,
)


class DocumentStatus(str, Enum):
    RAW = "raw"
    PARSED = "parsed"
    TRANSFORMED = "transformed"
    ENRICHED = "enriched"
    VALIDATED = "validated"
    FAILED = "failed"


@dataclass(slots=True)
class Document:

    content: str

    metadata: Metadata

    source_type: SourceType

    document_format: DocumentFormat

    category: DocumentCategory

    license_type: LicenseType

    id: str = field(default_factory=lambda: str(uuid4()))

    version: int = 1

    status: DocumentStatus = DocumentStatus.RAW

    chunks: List[str] = field(default_factory=list)

    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def word_count(self) -> int:
        return len(self.content.split())

    @property
    def character_count(self) -> int:
        return len(self.content)

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "version": self.version,
            "status": self.status.value,
            "content": self.content,
            "metadata": self.metadata.to_dict(),
            "source_type": self.source_type.value,
            "document_format": self.document_format.value,
            "category": self.category.value,
            "license_type": self.license_type.value,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "chunks": self.chunks,
            "extra": self.extra,
        }