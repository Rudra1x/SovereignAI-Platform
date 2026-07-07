from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from .types import Language


@dataclass(slots=True)
class Metadata:
    source_name: str

    source_url: Optional[str] = None

    author: Optional[str] = None

    title: Optional[str] = None

    created_at: Optional[str] = None

    updated_at: Optional[str] = None

    language: Language = Language.UNKNOWN

    tags: List[str] = field(default_factory=list)

    checksum: Optional[str] = None

    quality_score: float = 0.0

    custom: Dict[str, str] = field(default_factory=dict)

    ingestion_time: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "source_name": self.source_name,
            "source_url": self.source_url,
            "author": self.author,
            "title": self.title,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "language": self.language.value,
            "tags": self.tags,
            "checksum": self.checksum,
            "quality_score": self.quality_score,
            "custom": self.custom,
            "ingestion_time": self.ingestion_time,
        }