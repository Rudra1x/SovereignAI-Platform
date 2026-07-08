from dataclasses import dataclass, field


@dataclass(slots=True)
class DatasetMetadata:

    source_document: str

    source_uri: str | None = None

    language: str = "unknown"

    quality_score: float = 0.0

    tags: list[str] = field(default_factory=list)

    version: str = "1.0"