"""
Canonical raw resource object.

A Loader returns a RawResource.
A Parser consumes a RawResource.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mimetypes


@dataclass(slots=True)
class RawResource:
    uri: str
    content: bytes

    filename: str | None = None
    mime_type: str | None = None
    extension: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_bytes(
        cls,
        uri: str,
        content: bytes,
        filename: str | None = None,
    ) -> "RawResource":

        if filename is None:
            filename = Path(uri).name

        mime_type, _ = mimetypes.guess_type(filename)

        extension = Path(filename).suffix.lower()

        return cls(
            uri=uri,
            filename=filename,
            content=content,
            mime_type=mime_type or "application/octet-stream",
            extension=extension,
        )

    @property
    def size_bytes(self) -> int:
        return len(self.content)

    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / (1024 * 1024), 4)