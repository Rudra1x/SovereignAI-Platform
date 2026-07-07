"""
HTTP/HTTPS Loader.
"""

from __future__ import annotations

import requests

from sovereign.data.core.resource import RawResource

from .base import BaseLoader


class HTTPLoader(BaseLoader):

    def __init__(
        self,
        timeout: int = 60,
        headers: dict | None = None,
    ):

        self.timeout = timeout

        self.headers = headers or {
            "User-Agent": "SovereignAI-Platform/1.0"
        }

    def load(self, source: str) -> RawResource:

        response = requests.get(
            source,
            headers=self.headers,
            timeout=self.timeout,
        )

        response.raise_for_status()

        filename = source.rstrip("/").split("/")[-1]

        resource = RawResource.from_bytes(
            uri=source,
            filename=filename,
            content=response.content,
        )

        resource.metadata["status_code"] = response.status_code

        resource.metadata["headers"] = dict(response.headers)

        return resource