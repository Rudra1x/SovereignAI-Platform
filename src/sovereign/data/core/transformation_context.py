from __future__ import annotations

from dataclasses import dataclass, field

from sovereign.data.core.parsed_content import ParsedContent


@dataclass(slots=True)
class TransformationContext:

    parsed_content: ParsedContent

    language: str | None = None

    quality_score: float = 0.0

    duplicate_score: float = 0.0

    pii_detected: bool = False

    warnings: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    processing_history: list[str] = field(default_factory=list)

    statistics: dict = field(default_factory=dict)

    def add_step(self, step: str):

        self.processing_history.append(step)