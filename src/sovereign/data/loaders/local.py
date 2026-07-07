"""
Load files from local disk.
"""

from __future__ import annotations

from pathlib import Path

from sovereign.data.core.resource import RawResource

from .base import BaseLoader


class LocalLoader(BaseLoader):

    def load(self, source: str) -> RawResource:

        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(source)

        with open(path, "rb") as f:
            data = f.read()

        return RawResource.from_bytes(
            uri=str(path.resolve()),
            filename=path.name,
            content=data,
        )